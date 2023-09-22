from fastapi import FastAPI
from geocoder_api.settings import Settings
from geocoder_api.routers import geocoding

settings = Settings()
app = FastAPI(title="Geocoder API", version=settings.version)

app.include_router(geocoding.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "geocoder_api.__main__:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.uvicorn_reload,
        proxy_headers=settings.uvicorn_proxy_headers,
    )
