import pathlib
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from geocoder_api.settings import settings
from geocoder_api.routers import geocoding, healthcheck
from geocoder_api.openapi import custom_openapi
from fastapi.openapi.docs import get_redoc_html


@asynccontextmanager
async def lifespan(_: FastAPI):
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield


app = FastAPI(
    lifespan=lifespan,
    root_path=settings.api_root_path,
    redoc_url=None,
)

app.include_router(geocoding.router)
app.include_router(healthcheck.router)

example_code_dir = pathlib.Path(__file__).parent / "example_code"
app.openapi_schema = custom_openapi(app, example_code_dir)


@app.get("/redoc", include_in_schema=False)
def redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Geocoder API",
        redoc_favicon_url="https://www.openepi.io/favicon.ico",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "geocoder_api.__main__:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.uvicorn_reload,
        proxy_headers=settings.uvicorn_proxy_headers,
    )
