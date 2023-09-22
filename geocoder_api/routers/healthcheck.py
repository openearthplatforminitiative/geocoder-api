from fastapi import APIRouter
from geocoder_api.settings import Settings

settings = Settings()
router = APIRouter(tags=["health"])


@router.get("/health")
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}
