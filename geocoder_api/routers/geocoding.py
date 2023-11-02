from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache
from typing_extensions import Annotated
from geocoder_api.settings import Settings
from httpx import AsyncClient
from geojson_pydantic import FeatureCollection

settings = Settings()
router = APIRouter(tags=["geocoding"])


@router.get(
    "/",
    description="Returns a GeoJSON FeatureCollection of places matching the search query",
)
@cache(expire=3600)  # Expires after 1 hour
async def geocode(
    q: Annotated[str, Query(description="Search query")]
) -> FeatureCollection:
    async with AsyncClient() as client:
        params = {"q": q}
        res = await client.get(f"{settings.photon_url}/api", params=params)
        if res.status_code == 200:
            return res.json()
        else:
            raise HTTPException(status_code=res.status_code, detail=res.content)


@router.get(
    "/reverse",
    description="Returns a GeoJSON FeatureCollection of places near the provided coordinate",
)
@cache(expire=3600)  # Expires after 1 hour
async def reverse_geocode(
    lat: Annotated[float, Query(description="Latitude")],
    lon: Annotated[float, Query(description="Longitude")],
) -> FeatureCollection:
    async with AsyncClient() as client:
        params = {"lon": lon, "lat": lat}
        res = await client.get(f"{settings.photon_url}/reverse", params=params)
        if res.status_code == 200:
            return res.json()
        else:
            raise HTTPException(status_code=res.status_code, detail=res.json())
