import mimetypes
from pathlib import Path, PurePath, PurePosixPath
from typing import List, TypeVar
from uuid import uuid4

from furl import furl
from w3lib.url import parse_data_uri

from .string import removeprefix

T = TypeVar("T", bound=PurePath)


def check_if_uri_in_allowed_schemes(obj, allowed_schemes: List[str]) -> bool:
    if isinstance(obj, str):
        for scheme in allowed_schemes:
            if obj.startswith(scheme + ":"):
                return True
    return False


def check_if_file_uri(obj) -> bool:
    return check_if_uri_in_allowed_schemes(obj, ["file"])


def check_if_data_uri(obj) -> bool:
    return check_if_uri_in_allowed_schemes(obj, ["data"])


def check_if_http_or_https_uri(obj) -> bool:
    return check_if_uri_in_allowed_schemes(obj, ["http", "https"])


def get_path_from_file_uri(file_uri: str) -> Path:
    return "/" / Path(*furl(file_uri).path.segments)


def get_pure_posix_path_from_file_uri(file_uri: str) -> PurePosixPath:
    return "/" / PurePosixPath(*furl(file_uri).path.segments)


def get_filename_from_uri(url: str) -> str:
    f = furl(url)
    if f.scheme == "http" or f.scheme == "https":
        filename = f.path.segments[-1] if len(f.path.segments) > 1 else None
        if not filename:
            filename = uuid4().hex
    elif f.scheme == "data":
        ext = mimetypes.guess_extension(
            parse_data_uri(url.split(",", maxsplit=1)[0] + ",").media_type
        )
        filename = uuid4().hex + (ext if ext else "")
    else:
        raise ValueError(f"Unsupported scheme {f.scheme}")

    # For the case where filename include directory separators
    filename = Path(filename).name
    return filename


def strip_scheme_in_http_url(http_url: str) -> str:
    f = furl(http_url)
    if f.scheme == "http" or f.scheme == "https":
        return removeprefix(http_url, f.scheme + "://")
    else:
        raise NotImplementedError("Unsupported scheme: " + f.scheme)
