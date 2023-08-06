import typing as t
from pathlib import Path

from pathspec import PathSpec


def format_file_size(size_in_bytes: int, suffix="B"):
    num = float(size_in_bytes)
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"


def list_files(dir: Path) -> t.List[Path]:
    return [p for p in dir.iterdir() if p.is_file()]


def list_dirs(dir: Path) -> t.List[Path]:
    return [p for p in dir.iterdir() if p.is_dir()]


def convert_to_unique_path(path: Path) -> Path:
    parent = path.parent
    file_name = path.name
    ret_path = path
    while ret_path.exists():
        splitted_by_dot = file_name.split(".")
        splitted_by_dash = file_name.split("-")
        if len(splitted_by_dot) > 2 and splitted_by_dot[-2].isdigit():
            splitted_by_dot[-2] = str(int(splitted_by_dot[-2]) + 1)
            ret_path = parent / ".".join(splitted_by_dot)
        elif len(splitted_by_dot) > 1:
            splitted_by_dot[-1] = f"1.{splitted_by_dot[-1]}"
            ret_path = parent / ".".join(splitted_by_dot)
        elif len(splitted_by_dash) > 1 and splitted_by_dash[-1].isdigit():
            splitted_by_dash[-1] = str(int(splitted_by_dash[-1]) + 1)
            ret_path = parent / "-".join(splitted_by_dash)
        else:
            ret_path = Path(str(ret_path) + "-1")
        file_name = ret_path.name
    return ret_path


def get_tree_size_in_bytes(root_dir: Path, ignore_patterns: t.Optional[t.List[str]] = None) -> int:
    ignore_spec = PathSpec.from_lines("gitwildmatch", ignore_patterns) if ignore_patterns else None
    return sum(
        (f.stat().st_size if f.is_file() else f.lstat().st_size)
        for f in root_dir.glob("**/*")
        if (f.is_symlink() or f.is_file())
        and (ignore_spec is None or not ignore_spec.match_file(f.as_posix()))
    )


def is_relative_to(path: Path, start: Path):
    try:
        path.relative_to(start)
        return True
    except ValueError:
        return False
