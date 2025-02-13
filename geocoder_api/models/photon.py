from typing import Literal, Annotated

from pydantic import BaseModel, Field, ConfigDict

BBox = tuple[float, float, float, float]
Position = tuple[float, float]
LineStringCoords = Annotated[list[Position], Field(min_length=2)]
LinearRing = Annotated[list[Position], Field(min_length=4)]
MultiPointCoords = list[Position]
MultiLineStringCoords = list[LineStringCoords]
PolygonCoords = list[LinearRing]
MultiPolygonCoords = list[PolygonCoords]


class Point(BaseModel):
    type: Literal["Point"]
    coordinates: Position = Field(description="Coordinates in the format (lon, lat)")


class MultiPoint(BaseModel):
    type: Literal["MultiPoint"]
    coordinates: MultiPointCoords


class LineString(BaseModel):
    type: Literal["LineString"]
    coordinates: LineStringCoords


class MultiLineString(BaseModel):
    type: Literal["MultiLineString"]
    coordinates: MultiLineStringCoords


class Polygon(BaseModel):
    type: Literal["Polygon"]
    coordinates: PolygonCoords


class MultiPolygon(BaseModel):
    type: Literal["MultiPolygon"]
    coordinates: MultiPolygonCoords


Geometry = Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon


PlaceType = (
    Literal["house"]
    | Literal["street"]
    | Literal["locality"]
    | Literal["district"]
    | Literal["city"]
    | Literal["county"]
    | Literal["state"]
    | Literal["country"]
    | Literal["other"]
)


class Properties(BaseModel):
    name: str | None = Field(None, description="Name of the OSM-object")
    osm_type: Literal["N"] | Literal["W"] | Literal["R"] = Field(
        description="Whether the OSM object is an OSM node (N), way (W), or relation (R)"
    )
    osm_id: int = Field(
        description="An ID uniquely identifies the OSM-object within the OSM-type"
    )
    type: PlaceType | None = Field(
        None,
        description="The type of the place (e.g. house, street, city, country)",
    )
    country: str | None = Field(
        None, description="Name of the country that the OSM-object is in"
    )
    county: str | None = Field(
        None, description="Name of the county that the OSM-object is in"
    )
    city: str | None = Field(
        None, description="Name of the city that the OSM-object is in"
    )
    countrycode: str | None = Field(
        None, description="Country code for the country that the OSM-object is in"
    )
    osm_key: str | None = Field(
        None,
        description="Key of the main tag of the OSM object (e.g. boundary, highway, amenity)",
    )
    osm_value: str | None = Field(
        None,
        description="Value of the main tag of the OSM object (e.g. residential, restaurant)",
    )
    postcode: str | None = Field(
        None,
        description="Postal code of the OSM-object",
    )
    extent: BBox | None = Field(
        None,
        description="The bounding box formatted as (min latitude, max latitude, min longitude, max longitude)",
    )

    model_config = ConfigDict(extra="allow")


class Feature(BaseModel):
    type: Literal["Feature"]
    geometry: Geometry
    properties: Properties


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"]
    features: list[Feature]

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "coordinates": [13.438596, 52.519854],
                                "type": "Point",
                            },
                            "properties": {
                                "city": "Berlin",
                                "country": "Germany",
                                "name": "Berlin",
                            },
                        },
                        {
                            "type": "Feature",
                            "geometry": {
                                "coordinates": [61.195088, 54.005826],
                                "type": "Point",
                            },
                            "properties": {
                                "country": "Russia",
                                "name": "Berlin",
                                "postcode": "457130",
                            },
                        },
                    ],
                }
            ]
        }
    )
