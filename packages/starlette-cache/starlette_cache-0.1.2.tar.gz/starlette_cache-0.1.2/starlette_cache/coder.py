import typing as t

from starlette_async_jinja import _TemplateResponse as _AsyncTemplateResponse
import msgspec.json as json
from starlette.responses import JSONResponse
from starlette.templating import _TemplateResponse


class JsonResponse(JSONResponse):
    def render(self, content: t.Any) -> bytes:
        return json.encode(content)


class Coder:
    @classmethod
    def encode(cls, value: t.Any) -> str:
        raise NotImplementedError

    @classmethod
    def decode(cls, value: str) -> t.Any:
        raise NotImplementedError


class JsonCoder(Coder):  # move to cache
    @classmethod
    def encode(cls, value: t.Any) -> bytes:
        if isinstance(value, JsonResponse | JSONResponse):
            return value.body
        elif isinstance(value, _TemplateResponse | _AsyncTemplateResponse):
            value = value.body
        return json.encode(value)

    @classmethod
    def decode(cls, value: bytes) -> dict:
        return json.decode(value)
