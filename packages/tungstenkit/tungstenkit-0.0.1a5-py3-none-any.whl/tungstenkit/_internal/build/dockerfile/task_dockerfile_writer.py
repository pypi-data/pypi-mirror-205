from tungstenkit._internal.servers import task_server

from .base_dockerfile import BaseDockerfile


class TaskDockerfile(BaseDockerfile):
    @classmethod
    def entrypoint(cls) -> str:
        mod = task_server.__name__
        return f"python -m {mod}"
