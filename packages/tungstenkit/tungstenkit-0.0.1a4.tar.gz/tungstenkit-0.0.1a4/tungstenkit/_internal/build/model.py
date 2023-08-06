import inspect
import typing as t
from pathlib import Path

from tungstenkit._internal.constants import default_model_repo
from tungstenkit._internal.local_store import LocalStore, LocalModel
from tungstenkit._internal.local_store.local_model_store import parse_model_name
from tungstenkit._internal.model import TungstenModel

from .build_context import setup_build_ctx
from .dockerfile import ModelDockerfile

if t.TYPE_CHECKING:
    from _typeshed import StrPath


def build_model(
    tungsten_model: TungstenModel,
    *,
    copy_files: t.Optional[t.List[t.Tuple[str, str]]] = None,
    name: t.Optional[str] = None,
    build_dir: "StrPath" = ".",
) -> LocalModel:
    _build_dir = Path(build_dir).resolve()

    io_schema = tungsten_model._get_io_classes()
    # TODO type checking for include_files
    model_config = tungsten_model._get_model_config()
    if copy_files is not None:
        model_config.copy_files.extend(copy_files)
    model_module_path = Path(inspect.getfile(tungsten_model.__class__)).resolve()

    dockerfile_generator = ModelDockerfile(config=model_config)
    with setup_build_ctx(
        build_config=model_config,
        build_dir=_build_dir,
        module_path=model_module_path,
        dockerfile_generator=dockerfile_generator,
    ) as build_ctx:
        store = LocalStore()
        model_name = default_model_repo() if name is None else name
        repo_name, tag = parse_model_name(model_name)
        use_tag_as_id = False
        if tag is None:
            tag = store.generate_model_id()
            use_tag_as_id = True
        model_name = f"{repo_name}:{tag}"

        build_ctx.build(
            tags=[model_name] if tag == "latest" else [model_name, f"{repo_name}:latest"]
        )
        added = store.add_model(
            model_name,
            input_schema=io_schema.input.schema(),
            output_schema=io_schema.output.schema(),
            use_tag_as_id=use_tag_as_id,
            readme_content=None
            if model_config.readme_md is None
            else model_config.readme_md.read_text(),
            readme_image_base_dir=_build_dir,
        )
        return added
