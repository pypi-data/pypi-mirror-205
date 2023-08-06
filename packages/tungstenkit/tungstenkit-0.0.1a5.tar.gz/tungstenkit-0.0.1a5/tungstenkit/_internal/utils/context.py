import os
import sys
import typing as t
from contextlib import AbstractContextManager, contextmanager

from tungstenkit._internal.utils.console import print_exception

if t.TYPE_CHECKING:
    from _typeshed import FileDescriptor, StrOrBytesPath


class chdir(AbstractContextManager):
    # Added for compatibility with python < 3.11

    def __init__(self, path: "t.Union[FileDescriptor, StrOrBytesPath]"):
        self.path = path
        self._old_cwd: t.List[str] = []

    def __enter__(self):
        self._old_cwd.append(os.getcwd())
        os.chdir(self.path)

    def __exit__(self, *excinfo):
        if self._old_cwd:
            os.chdir(self._old_cwd.pop())


@contextmanager
def hide_traceback():
    def handler(type, value, traceback):
        print_exception(type, value)

    prev_excepthook = sys.excepthook
    try:
        sys.excepthook = handler
        yield
    finally:
        sys.excepthook = prev_excepthook
