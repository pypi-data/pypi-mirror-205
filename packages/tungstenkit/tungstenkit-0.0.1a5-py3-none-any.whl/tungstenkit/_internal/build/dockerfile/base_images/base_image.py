from abc import ABC

import attrs

from tungstenkit._internal.utils.string import removesuffix


@attrs.frozen
class BaseImage(ABC):
    @property
    def name(self) -> str:
        return self.get_repository() + ":" + self.get_tag()

    def get_repository(self) -> str:
        raise NotImplementedError

    def get_tag(self) -> str:
        raise NotImplementedError

    @property
    def type(self) -> str:
        return removesuffix(self.__class__.__name__, "Image").lower()
