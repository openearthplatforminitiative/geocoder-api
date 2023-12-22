import logging
import os
from pathlib import Path
from string import Template

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from geocoder_api.settings import settings

supported_languages = {"cURL": "sh", "JavaScript": "js", "Python": "py"}


def custom_openapi(app: FastAPI, example_code_dir: Path):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Geocoder API",
        version=settings.version,
        description=settings.api_description,
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://api-test.openepi.io/assets/icons/open-epi-logo.svg"
    }

    api_routes = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_routes:
        code_samples = []
        for lang, file_ext in supported_languages.items():
            file_with_code_sample = (
                example_code_dir / lang.lower() / f"{route.name}.{file_ext}"
            )
            if os.path.isfile(file_with_code_sample):
                with open(file_with_code_sample) as f:
                    code_template = Template(f.read())
                    code_samples.append(
                        {
                            "lang": lang,
                            "source": code_template.safe_substitute(
                                endpoint_url=f"{settings.api_url}{route.path}",
                            ),
                        }
                    )
            else:
                logging.warning(
                    "No code sample found for route %s and language %s",
                    route.path,
                    lang,
                )

        if code_samples:
            openapi_schema["paths"][route.path]["get"]["x-codeSamples"] = code_samples

    return openapi_schema
