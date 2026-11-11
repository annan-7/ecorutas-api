from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str
    interesting_fact: str
    image_url: str
    location: str
    distance_km: float
    difficulty: str
    route_type: str
    duration_hours: int
    latitude: float | None
    longitude: float | None
    altitude_meters: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    is_long_route: bool
    estimated_calories: int


class RoutePageResponse(BaseModel):
    items: list[RouteResponse]
    total: int
    skip: int
    limit: int


class HealthResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    detail: str
