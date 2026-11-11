from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateRouteDTO:
    name: str
    description: str
    interesting_fact: str
    image_url: str
    location: str
    distance_km: float
    difficulty: str
    route_type: str
    duration_hours: int
    latitude: float | None = None
    longitude: float | None = None
    altitude_meters: int = 0


@dataclass(frozen=True, slots=True)
class RouteResponseDTO:
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


@dataclass(frozen=True, slots=True)
class RoutePageDTO:
    items: list[RouteResponseDTO]
    total: int
    skip: int
    limit: int
