from typing import Callable, Optional

from starlette.requests import Request
from starlette.responses import Response
from acb import hash
from . import StarletteCache


def key_name(self, name: AsyncPath | str, prefix: str = None) -> str:
    prefix = prefix if prefix else self.prefix
    if isinstance(name, str):
        if name.startswith(f"{prefix}:"):
            return name
        return f"{prefix}:{hash.blake2b([name])}"
    parent = name.parent if "base" in name.parts else name.parent.parent
    return f"{prefix}:{hash.blake2b([parent.stem, name.stem])}"


def default_key_builder(
    func: Callable,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> str:
    prefix = f"{StarletteCache.get_prefix()}:{namespace}:"
    cache_key = prefix + hash.blake2b(
        f"{func.__module__}:{func.__name__}:{args}:{kwargs}"
    )
    return cache_key
