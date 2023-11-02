from fastapi import APIRouter, HTTPException
from httpx import AsyncClient

from geocoder_api.settings import Settings

settings = Settings()
router = APIRouter(tags=["health"])


@router.get("/health")
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}


@router.get("/ready")
async def readiness() -> dict[str, str]:
    async with AsyncClient() as client:
        params = {"q": "berlin"}
        res = await client.get(f"{settings.photon_url}/api", params=params)
        if res.status_code == 200:
            return res.json()
        else:
            raise HTTPException(status_code=res.status_code, detail=res.content)
