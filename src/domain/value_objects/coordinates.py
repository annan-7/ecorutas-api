from dataclasses import dataclass

from src.domain.exceptions.domain_exceptions import InvalidRouteError


@dataclass(frozen=True, slots=True)
class Coordinates:
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise InvalidRouteError("Latitud fuera de rango")
        if not -180 <= self.longitude <= 180:
            raise InvalidRouteError("Longitud fuera de rango")
