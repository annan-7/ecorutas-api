from dataclasses import dataclass
from enum import StrEnum

from src.domain.exceptions.domain_exceptions import InvalidRouteError


class RouteType(StrEnum):
    SENDERISMO = "senderismo"
    TREKKING = "trekking"
    ALTA_MONTANA = "alta_montana"
    PASEO = "paseo"


@dataclass(frozen=True, slots=True)
class RouteTypeVO:
    value: RouteType

    @classmethod
    def from_string(cls, value: str) -> "RouteTypeVO":
        try:
            return cls(RouteType(value.lower()))
        except ValueError as exc:
            raise InvalidRouteError(f"Tipo de ruta inválido: {value}") from exc
