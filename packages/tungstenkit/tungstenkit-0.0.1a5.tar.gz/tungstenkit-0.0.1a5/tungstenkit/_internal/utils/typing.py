import typing as t

from packaging.version import Version

from tungstenkit._versions import py_version


def get_type_args(type: "t.Type") -> "t.Tuple":
    if py_version >= Version("3.8"):
        return t.get_args(type)
    try:
        return type.__args__
    except AttributeError:
        return tuple()


def get_type_origin(type: "t.Type") -> "t.Type":
    if py_version >= Version("3.8"):
        origin = t.get_origin(type)
        if origin is None:
            return type
    try:
        if py_version >= Version("3.7"):
            return type.__origin__
        return type.__extra__
    except AttributeError:
        return type
