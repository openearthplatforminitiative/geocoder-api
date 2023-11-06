from fastapi import APIRouter, Response
from httpx import Client
from healthcheck import HealthCheck

from geocoder_api.settings import settings


router = APIRouter(tags=["health"])


def photon_healthcheck() -> (bool, str):
    with Client() as client:
        params = {"q": "berlin"}
        res = client.get(f"{settings.photon_url}/api", params=params)
        if res.status_code == 200:
            return True, "Connected to Photon-service"
        else:
            return False, "Photon-service not available"


# Set high success_ttl to avoid straining external Photon-service too much
health = HealthCheck(success_ttl=120)
health.add_check(photon_healthcheck)
health.add_section("version", settings.version)


@router.get("/ready")
def readiness() -> Response:
    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)


@router.get("/health")
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}
