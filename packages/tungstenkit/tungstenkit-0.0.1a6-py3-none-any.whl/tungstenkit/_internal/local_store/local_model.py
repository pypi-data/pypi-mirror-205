import json
import tempfile
import typing as t
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import attrs
from typing_extensions import Literal

from tungstenkit import exceptions
from tungstenkit._internal.utils.avatar import get_default_avatar_png
from tungstenkit._internal.utils.docker import get_docker_client
from tungstenkit._internal.utils.markdown import (
    apply_to_image_src_in_markdown,
    change_img_links_in_markdown,
    get_image_links,
)
from tungstenkit._internal.utils.requests import download_files_in_threadpool

from .local_blob_store import Blob, LocalBlobStore


@attrs.frozen(kw_only=True)
class SchemaData:
    input: Blob
    output: Blob


@attrs.frozen(kw_only=True)
class ReadmeData:
    markdown: Blob
    images: t.List[Blob] = attrs.field(factory=list)


@attrs.frozen(kw_only=True)
class ExampleData:
    input_json: Blob
    output_json: Blob
    demo_output_json: Blob
    input_files: t.List[Blob] = attrs.field(factory=list)
    output_files: t.List[Blob] = attrs.field(factory=list)
    logs: t.Optional[str] = None

    @property
    def files(self):
        return self.input_files + self.output_files


@attrs.frozen(kw_only=True)
class ModelDataInImage:
    module_name: str
    class_name: str
    docker_image_id: str
    description: str
    batch_size: int
    device: str
    gpu_mem_gb: t.Optional[int]

    @property
    def gpu(self) -> bool:
        return self.device == "gpu"

    @staticmethod
    def from_image(docker_image_name: str):
        docker_client = get_docker_client()
        docker_image = docker_client.images.get(docker_image_name)
        docker_image_id = docker_image.id

        env_vars: t.Optional[t.List[str]] = docker_image.attrs["Config"]["Env"]
        labels: t.Optional[t.Dict[str, str]] = docker_image.attrs["Config"]["Labels"]
        module_name = "tungsten_model"
        class_name = "Model"
        description = "Model"
        batch_size = 1
        device = "cpu"
        gpu_mem_gb = None
        if env_vars:
            for e in env_vars:
                try:
                    key, val = e.split("=", maxsplit=1)
                except ValueError:
                    continue
                if key == "TUNGSTEN_MODEL_MODULE":
                    module_name = val
                elif key == "TUNGSTEN_MODEL_CLASS":
                    class_name = val
                elif key == "TUNGSTEN_MAX_BATCH_SIZE":
                    batch_size = int(val)
        if labels:
            for label_name, label_value in labels.items():
                if label_name == "description":
                    description = label_value
                elif label_name == "device":
                    device = label_value
                elif label_name == "gpu_mem_gb":
                    gpu_mem_gb = int(label_value)

        return ModelDataInImage(
            module_name=module_name,
            class_name=class_name,
            docker_image_id=docker_image_id,
            description=description,
            batch_size=batch_size,
            device=device,
            gpu_mem_gb=gpu_mem_gb,
        )


@attrs.define(kw_only=True)
class ModelData(ModelDataInImage):
    schema: SchemaData
    readme: t.Optional[ReadmeData] = None
    examples: t.Dict[str, ExampleData] = attrs.field(factory=dict)
    avatar: Blob

    created_at: datetime = attrs.field(factory=datetime.utcnow)

    @property
    def blobs(self) -> t.Set[Blob]:
        blob_set: t.Set[Blob] = set()
        blob_set.add(self.schema.input)
        blob_set.add(self.schema.output)
        blob_set.add(self.avatar)
        if self.readme is not None:
            blob_set.add(self.readme.markdown)
            for b in self.readme.images:
                blob_set.add(b)
        if self.examples is not None:
            for example in self.examples.values():
                blob_set.add(example.input_json)
                blob_set.add(example.output_json)
                blob_set.add(example.demo_output_json)
                for b in example.files:
                    blob_set.add(b)

        return blob_set

    @staticmethod
    def build(
        docker_image_name: str,
        blob_store: LocalBlobStore,
        input_schema: t.Dict,
        output_schema: t.Dict,
        readme_content: t.Optional[str] = None,
        readme_image_base_dir: t.Optional[Path] = None,
        avatar_data_and_ext: t.Optional[t.Tuple[bytes, str]] = None,
        blob_create_policy: t.Union[Literal["copy"], Literal["rename"]] = "copy",
    ):
        with tempfile.TemporaryDirectory() as download_dir_str:
            # Save remote files and data uris
            download_dir = Path(download_dir_str)
            readme_image_download_dir = download_dir / "readme"
            readme_image_download_dir.mkdir()

            if readme_content:
                readme_content = _download_remote_files_in_readme(
                    save_dir=readme_image_download_dir, markdown_content=readme_content
                )

            # Add blobs to the blob store
            readme_file_set: t.Set[Path] = set()

            def add_readme_image(path: str):
                parsed = urlparse(path)
                if parsed.scheme == "file":
                    if parsed.netloc:
                        raise exceptions.UnsupportedURL(
                            f"'{path}' in README: file-uri for a remote file is not supported"
                        )
                    path = parsed.path

                pathlib_path = Path(path)

                if not pathlib_path.is_absolute() and readme_image_base_dir is not None:
                    pathlib_path = readme_image_base_dir / pathlib_path

                if pathlib_path.exists():
                    resolved = pathlib_path.resolve()
                    readme_file_set.add(resolved)
                    path = str(resolved)
                return path

            if readme_content:
                readme_content = apply_to_image_src_in_markdown(
                    md=readme_content, fn=add_readme_image
                )

            readme_file_list = list(readme_file_set)

            if blob_create_policy == "copy":
                readme_image_blobs = blob_store.add_multiple_by_writing(*readme_file_list)
            else:
                readme_image_blobs = [blob_store.add_by_renaming(f) for f in readme_file_list]
            input_schema_blob = blob_store.add_by_writing(
                (json.dumps(input_schema).encode("utf-8"), "input_schema.json")
            )
            output_schema_blob = blob_store.add_by_writing(
                (json.dumps(output_schema).encode("utf-8"), "output_schema.json")
            )

        # Update readme

        def update_readme_image(path: str):
            pathlib_path = Path(path)
            try:
                idx = readme_file_list.index(pathlib_path)
                path = str(readme_image_blobs[idx].file_path.resolve())
            except ValueError:
                pass

            return path

        if readme_content:
            readme_content = apply_to_image_src_in_markdown(
                md=readme_content, fn=update_readme_image, ret_updated=True
            )
            readme_md_blob = blob_store.add_multiple_by_writing(
                (readme_content.encode("utf-8"), "README.md")
            )[0]
            readme_data = ReadmeData(markdown=readme_md_blob, images=readme_image_blobs)
        else:
            readme_data = None

        # Schema blobs
        schema_data = SchemaData(input=input_schema_blob, output=output_schema_blob)

        # Avatar blob
        avatar_data_and_ext = (
            avatar_data_and_ext
            if avatar_data_and_ext
            else (get_default_avatar_png(name=docker_image_name), ".png")
        )
        avatar_blob = blob_store.add_by_writing(
            (avatar_data_and_ext[0], "avatar" + avatar_data_and_ext[1])
        )

        return ModelData(
            readme=readme_data,
            schema=schema_data,
            avatar=avatar_blob,
            **attrs.asdict(ModelDataInImage.from_image(docker_image_name), recurse=False),
        )


@attrs.define(kw_only=True)
class LocalModel(ModelData):
    id: str
    repo_name: str
    tag: str

    @property
    def name(self) -> str:
        return f"{self.repo_name}:{self.tag}"

    @property
    def data(self) -> ModelData:
        kwargs = dict()
        for field_name, _ in attrs.fields_dict(ModelData).items():
            kwargs[field_name] = getattr(self, field_name)

        return ModelData(**kwargs)


def _download_remote_files_in_readme(save_dir: Path, markdown_content: str) -> str:
    to_be_downloaded = get_image_links(md=markdown_content, schemes=["http", "https"])
    downloaded = download_files_in_threadpool(*to_be_downloaded, download_dir=save_dir)
    return change_img_links_in_markdown(
        md=markdown_content, images=to_be_downloaded, updates=[str(p) for p in downloaded]
    )
