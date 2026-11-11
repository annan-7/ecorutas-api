from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.domain.exceptions.domain_exceptions import InvalidRouteError
from src.domain.value_objects.coordinates import Coordinates
from src.domain.value_objects.difficulty import Difficulty
from src.domain.value_objects.route_type import RouteTypeVO


@dataclass(slots=True)
class Route:
    name: str
    description: str
    interesting_fact: str
    image_url: str
    location: str
    distance_km: float
    difficulty: Difficulty
    route_type: RouteTypeVO
    duration_hours: int
    coordinates: Coordinates | None = None
    altitude_meters: int = 0
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if len(self.name) < 3:
            raise InvalidRouteError("El nombre debe tener al menos 3 caracteres")
        if self.distance_km <= 0:
            raise InvalidRouteError("La distancia debe ser mayor a 0")
        if self.duration_hours < 0:
            raise InvalidRouteError("La duración no puede ser negativa")
        if self.altitude_meters < 0:
            raise InvalidRouteError("La altitud no puede ser negativa")

    @property
    def is_long_route(self) -> bool:
        return self.distance_km > 20

    @property
    def estimated_calories(self) -> int:
        return int(self.distance_km * 60 * self.difficulty.numeric_value)

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now(UTC)
