import os
import typing as t
from pathlib import Path

from rich import print as rprint

from tungstenkit import exceptions
from tungstenkit._internal.constants import default_model_repo
from tungstenkit._internal.local_store import LocalStore


def project_full_slug_callback(ctx, param, project_full_slug: str) -> str:
    slash_separated = project_full_slug.split("/")
    if len(slash_separated) != 2:
        raise exceptions.InvalidName(
            f"Invalid project name: {project_full_slug}\nFormat: <namespace slug>/<project slug>"
        )
    return project_full_slug


def remote_model_name_callback(ctx, param, model_name: str) -> str:
    format_help_msg = (
        "Format of remote model name: <namespace slug>/<project slug>:<model version>"
    )
    invalid_format_msg = f"Invalid remote model name: {model_name}\n" + format_help_msg
    colon_separated = model_name.split(":")
    if len(colon_separated) != 2:
        raise exceptions.InvalidName(invalid_format_msg)

    full_slug = colon_separated[0]
    slash_separated = full_slug.split("/")
    if len(slash_separated) != 2:
        raise exceptions.InvalidName(invalid_format_msg)

    return model_name


def existing_local_model_name_callback(ctx, param, model_name: t.Optional[str]) -> str:
    """
    Parse a model name or set the default.

    Raise an exception if the model is not found.
    """
    store = LocalStore()

    if model_name:
        try:
            m = store.get_model(model_name)
        except exceptions.ModelNotFound:
            raise exceptions.ModelNotFound(model_name)
        return m.name

    wd = Path(os.getcwd()).resolve().parts[-1]

    try:
        default_repo = default_model_repo()
        rprint(
            f"Finding the latest model image built in the directory '{wd}' "
            f"(tag: '{default_repo}:latest')... ",
            end="",
        )

        store.get_model(f"{default_repo}:latest")
        rprint("[bold green]succeeded[/bold green]")
        return f"{default_repo}:latest"

    except exceptions.ModelNotFound:
        rprint("[bold red]failed[/bold red]")

    # TODO prompt to request to ask whether to use the latest model or not
    rprint("Finding the latest model image... ", end="")
    models = sorted(store.list_models(), key=lambda m: m.created_at, reverse=True)

    if len(models) == 0:
        raise exceptions.ModelNotFound("No available models. Please build or pull first.")

    m = models[0]
    for _m in models:
        if _m.id == m.id and _m.name == "latest":
            m = _m

    rprint("[bold green]succeeded[/bold green]")
    rprint(f"Use model {m.name}")
    return m.name
