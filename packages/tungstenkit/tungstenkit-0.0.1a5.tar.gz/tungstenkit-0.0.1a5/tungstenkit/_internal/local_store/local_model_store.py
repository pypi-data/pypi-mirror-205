import hashlib
import json
import os
import tempfile
import typing as t
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

import attrs
from filelock import FileLock
from typing_extensions import Literal

from tungstenkit import exceptions
from tungstenkit._internal.constants import LOCK_DIR, PKG_DIR
from tungstenkit._internal.utils.docker import get_docker_client
from tungstenkit._internal.utils.json import apply_to_jsonable
from tungstenkit._internal.utils.serialize import load_attrs_from_json, save_attrs_to_json
from tungstenkit._internal.utils.uri import get_path_from_file_uri

from .local_blob_store import LocalBlobStore
from .local_model import ExampleData, LocalModel, ModelData

MODELS_DIR = PKG_DIR / "models"
MODELS_LOCK_PATH = LOCK_DIR / "model_collection.json.lock"


@attrs.frozen
class ModelCollection:
    repositories: t.Dict[str, t.Dict[str, str]] = attrs.field(factory=dict)
    models: t.Dict[str, ModelData] = attrs.field(factory=dict)

    def add(self, model_id: str, repo_name: str, tags: t.Iterable[str], data: ModelData):
        self.models[model_id] = data
        if repo_name not in self.repositories.keys():
            self.repositories[repo_name] = dict()
        for tag in tags:
            self.repositories[repo_name][tag] = model_id

    def prune(
        self, candidate_ids: t.Optional[t.Iterable[str]] = None
    ) -> t.List[t.Tuple[str, ModelData]]:

        if candidate_ids is None:
            candidate_ids = [id for id in self.models.keys()]
        else:
            candidate_ids = [id for id in candidate_ids if id in self.models.keys()]

        deleted: t.List[t.Tuple[str, ModelData]] = list()
        for id in set(candidate_ids):
            is_model_removed = not self.check_if_model_id_used(id)
            if is_model_removed:
                deleted.append((id, self.models[id]))
                del self.models[id]

        return deleted

    def check_if_model_id_used(self, id: str) -> bool:
        for repo_name in self.repositories.keys():
            if id in self.repositories[repo_name].values():
                return True
        return False

    def check_if_docker_image_used(self, docker_image_id: str) -> bool:
        for repo_name in self.repositories.keys():
            for model_id in self.repositories[repo_name].values():
                model_data = self.models[model_id]
                if model_data.docker_image_id == docker_image_id:
                    return True
        return False


class LocalModelStore:
    def __init__(self, base_dir: Path, lock_path: Path):
        self.base_dir = base_dir
        self.lock_path = lock_path

        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.filelock = FileLock(self.lock_path, timeout=180.0)

    @property
    def model_collection_path(self) -> Path:
        return self.base_dir / "collection.json"

    @staticmethod
    def generate_id():
        return uuid4().hex

    def add_model(
        self,
        docker_image_name: str,
        blob_store: LocalBlobStore,
        input_schema: t.Dict,
        output_schema: t.Dict,
        readme_content: t.Optional[str] = None,
        readme_image_base_dir: t.Optional[Path] = None,
        avatar_data_and_ext: t.Optional[t.Tuple[bytes, str]] = None,
        use_tag_as_id: bool = False,
        blob_create_policy: t.Union[Literal["copy"], Literal["rename"]] = "copy",
    ) -> LocalModel:
        repo, tag = parse_model_name(docker_image_name)
        if tag is None:
            raise ValueError(f"No tag in docker image name: {docker_image_name}")

        if use_tag_as_id:
            id = tag
        else:
            id = self.generate_id()

        tags = set([tag, "latest"])
        with blob_store.prevent_deletion():
            model_data = ModelData.build(
                docker_image_name=f"{repo}:{tag}",
                blob_store=blob_store,
                input_schema=input_schema,
                output_schema=output_schema,
                readme_content=readme_content,
                readme_image_base_dir=readme_image_base_dir,
                avatar_data_and_ext=avatar_data_and_ext,
                blob_create_policy=blob_create_policy,
            )

            # Add to the model colleciton and prune dangling models
            with self.filelock:
                col = self._load_model_collection()
                to_be_pruned: t.List[str] = list()
                if repo in col.repositories.keys():
                    for tag in tags:
                        if tag in col.repositories[repo].keys():
                            to_be_pruned.append(col.repositories[repo][tag])
                col.add(model_id=id, repo_name=repo, tags=tags, data=model_data)
                removed_models = col.prune(to_be_pruned)
                self._save_model_collection(col)

        self._collect_removed_model_garbages(col, removed_models)

        return LocalModel(
            id=id,
            repo_name=repo,
            tag=tag,
            **attrs.asdict(model_data, recurse=False),
        )

    def add_model_example(
        self,
        model_name: str,
        blob_store: LocalBlobStore,
        input_json: t.Dict,
        output_json: t.Dict,
        demo_output_json: t.Dict,
        blob_create_policy: t.Union[Literal["copy"], Literal["rename"]] = "copy",
        logs: t.Optional[str] = None,
    ):
        input_file_uris = []
        output_file_uris = []

        def append_input_file(file_uri: str) -> str:
            input_file_uris.append(file_uri)
            return file_uri

        def append_output_file(file_uri: str) -> str:
            output_file_uris.append(file_uri)
            return file_uri

        input_json = apply_to_jsonable(
            input_json,
            cond=lambda value: isinstance(value, str) and value.startswith("file:///"),
            fn=append_input_file,
        )
        output_json = apply_to_jsonable(
            output_json,
            cond=lambda value: isinstance(value, str) and value.startswith("file:///"),
            fn=append_output_file,
        )
        demo_output_json = apply_to_jsonable(
            demo_output_json,
            cond=lambda value: isinstance(value, str) and value.startswith("file:///"),
            fn=append_output_file,
        )

        input_file_uri_mapping: t.Dict[str, str] = dict()
        output_file_uri_mapping: t.Dict[str, str] = dict()
        with blob_store.prevent_deletion():
            input_file_paths = [get_path_from_file_uri(file_uri) for file_uri in input_file_uris]
            if blob_create_policy == "copy":
                input_file_blobs = blob_store.add_multiple_by_writing(*input_file_paths)
            else:
                input_file_blobs = [blob_store.add_by_renaming(p) for p in input_file_paths]
            for file_uri, blob in zip(input_file_uris, input_file_blobs):
                input_file_uri_mapping[file_uri] = blob.file_path.as_uri()

            output_file_paths = [get_path_from_file_uri(file_uri) for file_uri in output_file_uris]
            if blob_create_policy == "copy":
                output_file_blobs = blob_store.add_multiple_by_writing(*output_file_paths)
            else:
                output_file_blobs = [blob_store.add_by_renaming(p) for p in output_file_paths]
            for file_uri, blob in zip(output_file_uris, output_file_blobs):
                output_file_uri_mapping[file_uri] = blob.file_path.as_uri()

            input_json = apply_to_jsonable(
                input_json,
                cond=lambda value: value in input_file_uri_mapping,
                fn=lambda value: input_file_uri_mapping[value],
            )
            output_json = apply_to_jsonable(
                output_json,
                cond=lambda value: value in output_file_uri_mapping,
                fn=lambda value: output_file_uri_mapping[value],
            )
            demo_output_json = apply_to_jsonable(
                demo_output_json,
                cond=lambda value: value in output_file_uri_mapping,
                fn=lambda value: output_file_uri_mapping[value],
            )

            input_data = json.dumps(input_json).encode("utf-8")
            output_data = json.dumps(output_json).encode("utf-8")
            demo_data = json.dumps(demo_output_json).encode("utf-8")
            input_blob, output_blob, demo_blob = blob_store.add_multiple_by_writing(
                (input_data, "input.json"),
                (output_data, "output.json"),
                (demo_data, "output.json"),
            )

            hash_ = hashlib.sha1()
            hash_.update(input_data)
            hash_.update(output_data)
            hash_.update(demo_data)
            example_id = hash_.hexdigest()

            with self.filelock:
                model = self.get_model(model_name)
                model.examples[example_id] = ExampleData(
                    input_json=input_blob,
                    output_json=output_blob,
                    demo_output_json=demo_blob,
                    input_files=input_file_blobs,
                    output_files=output_file_blobs,
                    logs=logs,
                )
                self._update_model(model_name, model.data)

        return example_id

    def get_model(self, name: str) -> LocalModel:
        repo, tag = parse_model_name(name)
        tag = "latest" if tag is None else tag
        col = self._load_model_collection()
        try:
            id = col.repositories[repo][tag]
        except KeyError:
            raise exceptions.ModelNotFound(f"'{repo}:{tag}'")
        model_data = col.models[id]
        data_dict = attrs.asdict(model_data, recurse=False)
        return LocalModel(id=id, repo_name=repo, tag=tag, **data_dict)

    def list_models(self) -> t.List[LocalModel]:
        ret: t.List[LocalModel] = []
        col = self._load_model_collection()
        for repo_name in col.repositories.keys():
            for tag, id in col.repositories[repo_name].items():
                model_data = col.models[id]
                data_dict = attrs.asdict(model_data, recurse=False)
                ret.append(LocalModel(id=id, repo_name=repo_name, tag=tag, **data_dict))
        return ret

    def delete_model(self, name: str):
        repo, tag = parse_model_name(name)
        tag = "latest" if tag is None else tag

        with self.filelock:
            col = self._load_model_collection()
            try:
                id_to_be_removed = col.repositories[repo][tag]
            except KeyError:
                raise exceptions.ModelNotFound(name)

            del col.repositories[repo][tag]
            if len(col.repositories[repo]) == 0:
                del col.repositories[repo]

            removed_models = col.prune(candidate_ids=[id_to_be_removed])
            self._save_model_collection(col)

        self._collect_removed_model_garbages(col, removed_models)

    def delete_model_example(self, model_name: str, example_id: str):
        with self.filelock:
            model = self.get_model(model_name)
            del model.examples[example_id]
            self._update_model(model_name, model.data)

    def _load_model_collection(self) -> ModelCollection:
        if not self.model_collection_path.exists():
            col_dir = self.model_collection_path.parent
            tmp_col_paths = [
                col_dir / name for name in col_dir.glob("*" + self.model_collection_path.name)
            ]
            if len(tmp_col_paths) == 0:
                return ModelCollection()

            tmp_col_paths = sorted(
                tmp_col_paths, key=lambda path: path.stat().st_mtime, reverse=True
            )
            latest_tmp_col = tmp_col_paths[0]
            col = load_attrs_from_json(ModelCollection, latest_tmp_col)
            os.replace(latest_tmp_col, self.model_collection_path)

            # Clean up
            for tmp_col_path in tmp_col_paths[1:]:
                os.remove(tmp_col_path)
            return col
        return load_attrs_from_json(ModelCollection, self.model_collection_path)

    def _save_model_collection(self, model_collection: ModelCollection):
        col_dir = self.model_collection_path.parent
        tmp_col_fd, tmp_col_path_str = tempfile.mkstemp(
            suffix=self.model_collection_path.name, dir=col_dir
        )
        try:
            tmp_col_path = Path(tmp_col_path_str)
            save_attrs_to_json(model_collection, tmp_col_path)
            os.replace(tmp_col_path, self.model_collection_path)
        finally:
            os.close(tmp_col_fd)

        # Clean up
        tmp_col_paths = [
            col_dir / p
            for p in col_dir.glob("*" + self.model_collection_path.name)
            if p.name != self.model_collection_path.name
        ]
        for tmp_col_path in tmp_col_paths:
            os.remove(tmp_col_path)

    def _collect_removed_model_garbages(
        self,
        col: ModelCollection,
        removed_model_id_and_data: t.Optional[t.List[t.Tuple[str, ModelData]]] = None,
    ):
        removed_model_id_and_data = (
            col.prune() if removed_model_id_and_data is None else removed_model_id_and_data
        )

        def remove_docker_image(removed_model: ModelData):
            docker_client = get_docker_client(timeout=None)
            if not col.check_if_docker_image_used(removed_model.docker_image_id):
                docker_client.images.remove(image=removed_model.docker_image_id, force=True)

        with ThreadPoolExecutor(max_workers=8) as executor:
            for _, model in removed_model_id_and_data:
                executor.submit(remove_docker_image, model)

    def _update_model(self, name: str, data: ModelData) -> None:
        repo, tag = parse_model_name(name)
        tag = "latest" if tag is None else tag
        col = self._load_model_collection()
        try:
            id = col.repositories[repo][tag]
        except KeyError:
            raise exceptions.ModelNotFound(f"'{repo}:{tag}'")
        col.models[id] = data
        self._save_model_collection(col)


def parse_model_name(name: str) -> t.Tuple[str, t.Optional[str]]:
    path_components = name.split("/")
    last_component_splitted = path_components[-1].split(":")
    if len(last_component_splitted) > 2:
        raise exceptions.InvalidName(f"'{name}' (format: '<repo_name>[:<tag>]')")
    elif len(last_component_splitted) > 1:
        repo = "/".join(path_components[:-1] + [last_component_splitted[0]])
        tag: t.Optional[str] = last_component_splitted[1]
    else:
        repo = "/".join(path_components[:-1] + [last_component_splitted[0]])
        tag = None
    if not repo:
        raise exceptions.InvalidName("'' (format: '<repo_name>[:<tag>]')")
    return repo, tag
