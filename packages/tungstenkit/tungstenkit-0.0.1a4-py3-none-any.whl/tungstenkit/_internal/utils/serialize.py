import json
import os
import typing as t
from datetime import datetime
from pathlib import Path

import cattrs
import yaml
from packaging.version import Version

T = t.TypeVar("T")

attrs_converter = cattrs.Converter()
attrs_converter.register_structure_hook(Path, lambda d, _: Path(d))
attrs_converter.register_unstructure_hook(Path, lambda p: os.fspath(p))
attrs_converter.register_structure_hook(Version, lambda _str, _: Version(_str))
attrs_converter.register_unstructure_hook(Version, lambda _ver: str(_ver))
attrs_converter.register_structure_hook(datetime, lambda val, _: datetime.fromisoformat(val))
attrs_converter.register_unstructure_hook(datetime, lambda dt: dt.isoformat())


def register_structure_hook(type_, hook):
    attrs_converter.register_structure_hook(type_, hook)


def register_unstructure_hook(type_, hook):
    attrs_converter.register_unstructure_hook(type_, hook)


def save_attrs_to_yaml(obj, path: Path):
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    dict = attrs_converter.unstructure_attrs_asdict(obj)
    with open(path, "w") as f:
        dumped = yaml.dump(dict, default_flow_style=False)
        f.write(dumped)


def load_attrs_from_yaml(cls, path: Path):
    with open(path, "r") as f:
        dict = yaml.load(f, Loader=yaml.Loader)

    return attrs_converter.structure(dict, cls)


def save_attrs_to_json(obj, path: Path):
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    dict = attrs_converter.unstructure_attrs_asdict(obj)
    with open(path, "w") as f:
        json.dump(dict, f, indent=2)


def load_attrs_from_json(cls, path: Path):
    with open(path, "r") as f:
        dict = json.load(f)

    return attrs_converter.structure(dict, cls)


def convert_attrs_to_json(obj: object) -> str:
    dict = attrs_converter.unstructure_attrs_asdict(obj)
    return json.dumps(dict)


def convert_json_to_attrs(json_: t.Union[str, bytes], cls: t.Type[T]) -> T:
    return attrs_converter.structure_attrs_fromdict(json.loads(json_), cls)
