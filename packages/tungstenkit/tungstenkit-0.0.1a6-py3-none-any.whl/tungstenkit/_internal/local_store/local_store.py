import typing as t
from pathlib import Path

from typing_extensions import Literal

from tungstenkit._internal.constants import LOCK_DIR, PKG_DIR

from .local_blob_store import Blob, LocalBlobStore
from .local_model_store import LocalModel, LocalModelStore


class LocalStore:
    def __init__(self, base_dir: Path = PKG_DIR, lock_dir: Path = LOCK_DIR) -> None:
        self._blob_store = LocalBlobStore(
            base_dir=base_dir / "blobs", lock_path=lock_dir / "blobs.lock"
        )
        self._model_store = LocalModelStore(
            base_dir=base_dir / "models",
            lock_path=lock_dir / "models.lock",
        )

    def generate_model_id(self):
        return self._model_store.generate_id()

    def add_model(
        self,
        docker_image_name: str,
        *,
        input_schema: t.Dict,
        output_schema: t.Dict,
        readme_content: t.Optional[str] = None,
        readme_image_base_dir: t.Optional[Path] = None,
        avatar_data_and_ext: t.Optional[t.Tuple[bytes, str]] = None,
        use_tag_as_id: bool = False,
        blob_create_policy: t.Union[Literal["copy"], Literal["rename"]] = "copy",
    ) -> LocalModel:
        kwargs = {kwd: arg for kwd, arg in locals().items() if kwd != "self"}
        model = self._model_store.add_model(blob_store=self._blob_store, **kwargs)
        return model

    def add_model_example(
        self,
        model_name: str,
        input_json: t.Dict,
        output_json: t.Dict,
        demo_output_json: t.Dict,
        blob_create_policy: t.Union[Literal["copy"], Literal["rename"]] = "copy",
        logs: t.Optional[str] = None,
    ) -> str:
        kwargs = {kwd: arg for kwd, arg in locals().items() if kwd != "self"}
        return self._model_store.add_model_example(blob_store=self._blob_store, **kwargs)

    def get_model(self, name: str) -> LocalModel:
        return self._model_store.get_model(name=name)

    def list_models(self) -> t.List[LocalModel]:
        return self._model_store.list_models()

    def delete_model(self, name: str):
        self._model_store.delete_model(name=name)
        self._delete_unused_blobs()

    def delete_model_example(self, model_name: str, example_id: str):
        self._model_store.delete_model_example(model_name=model_name, example_id=example_id)
        self._delete_unused_blobs()

    def clear_model_repo(self, repo: t.Optional[str]) -> t.List[str]:
        removed = []
        for m in self._model_store.list_models():
            if repo is None or m.repo_name == repo:
                self._model_store.delete_model(name=m.name)
                removed.append(m.name)
        if len(removed) > 0:
            self._delete_unused_blobs()
        return removed

    def _delete_unused_blobs(self):
        self._blob_store.delete_unused(self._collect_blobs())

    def _collect_blobs(self) -> t.Set[Blob]:
        blobs: t.Set[Blob] = set()
        for m in self._model_store.list_models():
            blobs = blobs.union(m.blobs)
        return blobs
