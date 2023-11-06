from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from geocoder_api.settings import settings
from geocoder_api.routers import geocoding, healthcheck


@asynccontextmanager
async def lifespan(_: FastAPI):
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Geocoder API",
    lifespan=lifespan,
    version=settings.version,
    root_path=settings.api_root_path,
)

app.include_router(geocoding.router)
app.include_router(healthcheck.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "geocoder_api.__main__:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.uvicorn_reload,
        proxy_headers=settings.uvicorn_proxy_headers,
    )
