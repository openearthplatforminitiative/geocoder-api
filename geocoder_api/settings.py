from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.0.1"
    uvicorn_port: int = 8080
    uvicorn_host: str = "0.0.0.0"
    uvicorn_reload: bool = True
    uvicorn_proxy_headers: bool = False
    photon_url: str = "https://photon.komoot.io"
    api_root_path: str = ""
    api_description: str = (
        "<p>This is a RESTful service that provides geocoding and reverse geocoding using <a "
        'href="https://www.openstreetmap.org/copyright">OpenStreetMap<sup>®</sup></a> data. The data is licensed under '
        'the <a href="https://opendatacommons.org/licenses/odbl/">Open Data Commons Open Database License (ODbL)</a>, '
        'by the <a href="https://osmfoundation.org">OpenStreetMap Foundation (OSMF)</a>.</p>'
        '<p>The data is sourced from <a href="https://photon.komoot.io">https://photon.komoot.io</a>.</p>'
    )
    api_domain: str = "localhost"

    @property
    def api_url(self):
        if self.api_domain == "localhost":
            return f"http://{self.api_domain}:{self.uvicorn_port}"
        else:
            return f"https://{self.api_domain}{self.api_root_path}"


settings = Settings()
