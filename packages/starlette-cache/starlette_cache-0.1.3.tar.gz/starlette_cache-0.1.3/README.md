# starlette-cache

Starlette fork of Starlette Cache was originally a fork of fastapi-cache with the fastapi-cache dependency removed.
It is now being completed rebuilt around cashews with starlette-async-jinja support.


Stay tuned...

## Introduction



## Features



## Requirements


## Install

```shell
> pdm add startlette-cache
```

## Usage

### Quick Start

```python
from starlette import Starlette
from starlette.requests import Request
from starlette.responses import Response

from starlette_cache import StarletteCache
from starlette_cache.backends.redis import RedisBackend
from starlette_cache.decorator import cache

from redis import asyncio as aioredis

app = Starlette()


@cache()
async def get_cache():
    return 1


@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="world")


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    StarletteCache.init(RedisBackend(redis), prefix="fastapi-cache")

```

### Initialization

Firstly you must call `StarletteCache.init` on startup event of `fastapi`, there are some global config you can pass in.

### Use `cache` decorator

If you want cache `fastapi` response transparently, you can use `cache` as decorator between router decorator and view
function and must pass `request` as param of view function.

Parameter | type, description
------------ | -------------
expire | int, states a caching time in seconds
namespace | str, namespace to use to store certain cache items
coder | which coder to use, e.g. JsonCoder
key_builder | which key builder to use, default to builtin

You can also use `cache` as decorator like other cache tools to cache common function result.

### Custom coder

By default use `JsonCoder`, you can write custom coder to encode and decode cache result, just need
inherit `fastapi_cache.coder.Coder`.

```python
@app.get("/")
@cache(expire=60, coder=JsonCoder)
async def index():
    return dict(hello="world")
```

### Custom key builder

By default, use builtin key builder. If you need, you can override this and pass in `cache` or `StarletteCache.init` to
take effect globally.

```python
def my_key_builder(
        func,
        namespace: Optional[str] = "",
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
):
    prefix = StarletteCache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"
    return cache_key


@app.get("/")
@cache(expire=60, coder=JsonCoder, key_builder=my_key_builder)
async def index():
    return dict(hello="world")
```

### InMemoryBackend

`InMemoryBackend` store cache data in memory and use lazy delete, which mean if you don't access it after cached, it
will not delete automatically.

## Tests and coverage

## Acknowlegdments
