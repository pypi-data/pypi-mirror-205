import os
import subprocess
import sys
import tempfile
import typing as t
from datetime import timezone
from pathlib import Path

import click
import uvicorn
from tabulate import tabulate

from tungstenkit._internal.build import build_model
from tungstenkit._internal.clients.tungsten import TungstenClient
from tungstenkit._internal.constants import TUNGSTEN_LOGO
from tungstenkit._internal.containerized_services import start_model_service
from tungstenkit._internal.local_store import LocalStore
from tungstenkit._internal.model import TungstenModel
from tungstenkit._internal.servers.demo_server import create_demo_app
from tungstenkit._internal.utils.console import print_pretty, print_success, yes_or_no_prompt
from tungstenkit._internal.utils.context import chdir
from tungstenkit._internal.utils.string import removeprefix

from .callbacks import (
    existing_local_model_name_callback,
    project_full_slug_callback,
    remote_model_name_callback,
)
from .options import common_options


@click.group(hidden=True)
@common_options
def model(**kwargs):
    """
    Run model commands
    """
    pass


@model.command()
@click.argument("model_class", default="tungsten_model:Model")
@click.option(
    "--name",
    "-n",
    help="Name of the model in '<repo name>[:<tag>]' format",
)
@click.option(
    "--copy-files",
    "-f",
    help="Copy files to the container (format: <src in host>:<dest in container>)",
    multiple=True,
)
@click.option(
    "--build-dir",
    "-d",
    help="Build root directory",
    default=".",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    show_default=True,
)
@common_options
def build(
    model_class: str, name: t.Optional[str], copy_files: t.Iterable[str], build_dir: str, **kwargs
):
    """
    Build a docker image of a tungsten model

    'MODEL_CLASS' should be in the '<module>:<class>' format
    (default: tungsten_model:Model)
    """

    model_name_parts = model_class.split(":")
    if len(model_name_parts) != 2:
        raise click.BadArgumentUsage(
            message=f"The model class '{model_class}' is not in '<module>:<class>' format "
            "(e.g. tungsten_models.mymodel:MyModel)"
        )

    model_module, model_class_name = model_name_parts

    _copy_files: t.List[t.Tuple[str, str]] = []
    for f in copy_files:
        if ":" in f:
            splitted = f.split(":", maxsplit=1)
            _copy_files.append((splitted[0], splitted[1]))
        else:
            raise click.BadOptionUsage(
                "--copy_files",
                message=f"'{f}' is not in the format of '<src_in_host>:<dest_in_container>'",
            )

    # Set path to import the module
    cwd = os.getcwd()
    if cwd != build_dir:
        idx = 0
        while cwd in sys.path:
            idx = sys.path.index(cwd)
            sys.path.remove(cwd)
        sys.path.insert(idx, build_dir)

    # Do lazy import of the module
    with chdir(build_dir):
        tungsten_model = TungstenModel._from_module(
            model_module, model_class_name, lazy_import=True
        )

    print(TUNGSTEN_LOGO)
    model = build_model(tungsten_model, copy_files=_copy_files, name=name, build_dir=build_dir)
    print()
    success_msg = f"Successfully built tungsten model: '{model.repo_name}:{model.tag}' "
    if model.tag != "latest":
        success_msg += f"(also tagged as '{model.repo_name}:latest')"
    print_success(success_msg)
    print("\n- Run demo service:")
    print_pretty(f"  $ tungsten demo [green]{model.repo_name}:latest[/green]")
    print("\n- Run prediction service:")
    print_pretty(f"  $ tungsten serve [green]{model.repo_name}:latest[/green]")


@model.command()
@click.argument("model_name", default="", callback=existing_local_model_name_callback)
@click.option("--host", default="localhost", help="The host on which the demo server will listen")
@click.option(
    "--port", "-p", default=3300, help="The port on which the demo server will listen", type=int
)
@common_options
def demo(model_name: str, host: str, port: int, **kwargs):
    """
    Start a demo service for a model

    \b
    'MODEL_NAME' should be in the '<repo name>[:<tag>]' format.
    If not set, the latest model is selected.
    """
    print_pretty(f"Start demo for model '{model_name}'\n")

    store = LocalStore()
    stored_model = store.get_model(model_name)

    # Start demo app
    # NOTE We create tempdir in current directory since docker desktop doesn't allow
    # to bind host dirs outside the user home directory
    with tempfile.TemporaryDirectory(
        prefix=".tungsten-container-volume-",
        dir=".",
    ) as container_tmp_dir:
        with start_model_service(
            name=stored_model.name, bind_dir_in_host=Path(container_tmp_dir)
        ) as service:
            with tempfile.TemporaryDirectory() as server_tmp_dir:
                app = create_demo_app(
                    model_service=service,
                    tmp_dir=Path(server_tmp_dir),
                )
                print(TUNGSTEN_LOGO)
                uvicorn.run(app, host=host, port=port)


@model.command()
@click.argument("project", callback=project_full_slug_callback)
@click.option(
    "--model-name",
    "-n",
    help="Name of the model in '<repo name>[:<tag>]' format",
    callback=existing_local_model_name_callback,
)
@common_options
def push(project: str, model_name: str, **kwargs):
    """
    Push a model

    'PROJECT' should be in the '<namespace slug>/<project slug>' format
    """
    # TODO validate project
    # TODO print the pushed model in server
    tungsten_client = TungstenClient.from_env()
    print(TUNGSTEN_LOGO)
    tungsten_client.push_model(model_name=model_name, project=project)


@model.command()
@click.argument("remote_model", callback=remote_model_name_callback)
@common_options
def pull(remote_model: str, **kwargs):
    """
    Pull a model

    'REMOTE_MODEL' should be in the '<repo name>[:<tag>]' format
    """
    project, version = remote_model.split(":", maxsplit=1)
    tungsten_client = TungstenClient.from_env()
    print(TUNGSTEN_LOGO)
    tungsten_client.pull_model(project=project, model_version=version)


@model.command()
@common_options
def list(**kwargs):
    """
    List models
    """
    store = LocalStore()
    table_headers = [
        "Repository",
        "Tag",
        "Description",
        "Model Class",
        "Created",
        "Docker Image ID",
    ]
    table = []
    for m in store.list_models():
        table.append(
            [
                m.repo_name,
                m.tag,
                m.description,
                f"{m.module_name}:{m.class_name}",
                m.created_at.replace(tzinfo=timezone.utc)
                .astimezone()
                .strftime("%Y-%m-%d %H:%M:%S"),
                f"{removeprefix(m.docker_image_id, 'sha256:')[:12]}",
            ]
        )
    # TODO sort table (repo_name -> latest tag first -> created)
    print(tabulate(table, headers=table_headers))


@model.command()
@click.argument("model_name", type=str)
@common_options
def remove(model_name: str, **kwargs):
    """
    Remove a model

    'MODEL_NAME' should be in the '<repo name>[:<tag>]' format
    """
    store = LocalStore()
    model = store.get_model(model_name)
    store.delete_model(model.name)
    print_pretty(f"Removed: '{model.name}'")


@model.command()
@click.argument("repo_name", default="")
@common_options
def clear(repo_name: str, **kwargs):
    """
    Remove all models in a repository

    If 'REPO_NAME' is not set, try to remove all models.
    """
    if not repo_name and not yes_or_no_prompt("Remove all models?"):
        return

    store = LocalStore()
    removed_model_names = store.clear_model_repo(repo=repo_name if repo_name else None)
    if len(removed_model_names) == 0:
        return

    print_pretty("Removed: " + ", ".join([f"'{n}'" for n in removed_model_names]))


@model.command
@click.argument("model_name", default="", callback=existing_local_model_name_callback)
@click.option("--port", "-p", default=3000, type=int)
@click.option(
    "--log-level",
    default="info",
    type=click.Choice(["trace", "debug", "info", "warning", "error"], case_sensitive=False),
    help="Log level",
    show_default=True,
    callback=lambda _, __, v: v.upper(),
)
@common_options
def serve(model_name: str, port: int, log_level: str, **kwargs):
    """
    Start a prediction service for a model

    \b
    'MODEL_NAME' should be in the '<repo name>[:<tag>]' format.
    If not set, the latest model is selected.
    """
    store = LocalStore()
    model = store.get_model(model_name)
    args = [
        "docker",
        "run",
        "-it",
        "--rm",
        "-p",
        f"{port}:{port}",
    ]
    if model.gpu:
        args += ["--gpus", "all"]
    args += [model.docker_image_id, "--http-port", f"{port}", "--log-level", log_level]
    print(TUNGSTEN_LOGO)
    subprocess.run(args)


# @model.command()
# @click.argument("model_name", default="", callback=_validate_stored_model_name)
# @click.option(
#     "--input",
#     "-i",
#     multiple=True,
#     help="Input in the format of '<name>=<value>' or '<name>=@<file_path>'",
# )
# @common_options
# def predict(model_name: str, input: t.Iterable[str], **kwargs):
#     """
#     Run a prediction with a model

#     'MODEL_NAME' should be in the '<repo name>[:<tag>]' format
#     """
#     # TODO move detailed implementations to another module
#     # TODO save data uris to files
#     print(TUNGSTEN_LOGO)
#     print_pretty(f"Predict with model '{model_name}'")

#     store = LocalStore()
#     model = store.get_model(model_name)

#     inputs: t.Dict[str, str] = dict()
#     container_tmp_dir = PurePosixPath(f"/tmp/tungsten-cli-predict-{uuid4().hex}")
#     with tempfile.TemporaryDirectory() as host_tmp_dir_str:
#         with ThreadPoolExecutor(max_workers=4) as executor:
#             host_tmp_dir = Path(host_tmp_dir_str)
#             for input_str in input:
#                 splitted = input_str.split("=", maxsplit=1)
#                 if len(splitted) < 2:
#                     raise click.BadOptionUsage(
#                         "--input", f"'{input_str}' is not in the format of '<name>=<value>'"
#                     )
#                 name, val = splitted[0], splitted[1]
#                 if val.startswith("@"):
#                     file_path_in_orig_fs = Path(val[1:]).resolve()
#                     if not file_path_in_orig_fs.exists():
#                         raise click.BadOptionUsage(
#                             "--input", f"'{file_path_in_orig_fs}' is not found"
#                         )
#                     if not file_path_in_orig_fs.is_file():
#                         raise click.BadOptionUsage(
#                             "--input", f"'{file_path_in_orig_fs}' is not a file"
#                         )
#                     file_path_in_host_tmp_dir = host_tmp_dir / file_path_in_orig_fs.parts[-1]
#                     file_path_in_host_tmp_dir = convert_to_unique_path(file_path_in_host_tmp_dir)
#                     file_path_in_host_tmp_dir.touch()
#                     executor.submit(shutil.copy, file_path_in_orig_fs, file_path_in_host_tmp_dir)
#                     file_path_in_container_tmp_dir = (
#                         container_tmp_dir / file_path_in_host_tmp_dir.parts[-1]
#                     )
#                     file_uri = file_path_in_container_tmp_dir.as_uri()
#                     val = file_uri

#                 inputs[name] = val

#         docker_run_kwargs = {
#             "volumes": {host_tmp_dir_str: {"bind": str(container_tmp_dir), "mode": "ro"}}
#         }
#         with _start_model_server(
#             model.name, model.gpu, docker_run_kwargs=docker_run_kwargs
#         ) as server:
#             model_server_inference_endpoint = f"http://localhost:{server.port}/prediction"
#             resp = requests.post(url=model_server_inference_endpoint, json=[inputs])
#             # TODO complete this
#             if resp.ok:
#                 print_pretty(resp.text)
#             else:
#                 print_pretty(f"Failed to predict: {resp.status_code} {resp.reason}")
#                 if resp.status_code == 500:
#                     print_container_logs(server.container.id)
#                 else:
#                     print_pretty(resp.text)
