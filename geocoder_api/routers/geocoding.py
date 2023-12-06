from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi_cache.decorator import cache
from typing_extensions import Annotated
from geocoder_api.settings import settings
from httpx import AsyncClient
from geocoder_api.models.photon import FeatureCollection


router = APIRouter(tags=["geocoding"])


async def get_shared_query_params(
    lang: Annotated[
        str | None,
        Query(description='Set preferred language (e.g. "default", "en", "de", "fr")'),
    ] = None,
    limit: Annotated[int | None, Query(description="Limit number of results")] = None,
) -> dict:
    return {"lang": lang, "limit": limit}


@router.get(
    "/",
    description="Returns a GeoJSON FeatureCollection of places matching the search query",
)
@cache(expire=3600)  # Expires after 1 hour
async def get_geocoding(
    q: Annotated[str, Query(description="Search query")],
    shared_params: Annotated[dict, Depends(get_shared_query_params)],
    lat: Annotated[
        float | None, Query(description="Geocode with priority to this latitude")
    ] = None,
    lon: Annotated[
        float | None, Query(description="Geocode with priority to this longitude")
    ] = None,
) -> FeatureCollection:
    async with AsyncClient() as client:
        # Remove None-parameters
        params = {
            k: v
            for k, v in {"q": q, "lon": lon, "lat": lat, **shared_params}.items()
            if v is not None
        }
        res = await client.get(f"{settings.photon_url}/api", params=params)
        if res.status_code == 200:
            return res.json()
        else:
            raise HTTPException(status_code=res.status_code, detail=res.text)


@router.get(
    "/reverse",
    description="Returns a GeoJSON FeatureCollection of places near the provided coordinate",
)
@cache(expire=3600)  # Expires after 1 hour
async def get_reverse_geocoding(
    lat: Annotated[float, Query(description="Latitude")],
    lon: Annotated[float, Query(description="Longitude")],
    shared_params: Annotated[dict, Depends(get_shared_query_params)],
) -> FeatureCollection:
    async with AsyncClient() as client:
        # Remove None-parameters
        params = {
            k: v
            for k, v in {"lon": lon, "lat": lat, **shared_params}.items()
            if v is not None
        }
        res = await client.get(f"{settings.photon_url}/reverse", params=params)
        if res.status_code == 200:
            return res.json()
        else:
            raise HTTPException(status_code=res.status_code, detail=res.text)
