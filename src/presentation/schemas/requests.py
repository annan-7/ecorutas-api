from pydantic import BaseModel, Field, HttpUrl, model_validator

from src.domain.value_objects.difficulty import DifficultyLevel
from src.domain.value_objects.route_type import RouteType


class CreateRouteRequest(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)
    interesting_fact: str = Field(min_length=10)
    image_url: HttpUrl
    location: str = Field(min_length=2, max_length=120)
    distance_km: float = Field(gt=0)
    difficulty: DifficultyLevel
    route_type: RouteType
    duration_hours: int = Field(ge=0)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    altitude_meters: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def coordinates_must_be_complete(self) -> "CreateRouteRequest":
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("Latitud y longitud deben enviarse juntas")
        return self
