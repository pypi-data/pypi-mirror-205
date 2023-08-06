import typing as t
from abc import ABC, abstractmethod


class Backend(ABC):
    @abstractmethod
    async def get_with_ttl(self, key: str) -> t.Tuple[int, t.Optional[str]]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> t.Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: str, expire: t.Optional[int] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear(
        self, namespace: t.Optional[str] = None, key: t.Optional[str] = None
    ) -> int:
        raise NotImplementedError
