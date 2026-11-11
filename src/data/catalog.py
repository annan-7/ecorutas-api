"""Read-only catalog bundled with the application; no runtime writes or database."""

from importlib.resources import files
from types import MappingProxyType

from pydantic import TypeAdapter

from src.presentation.schemas.responses import RouteResponse

ROUTES = tuple(
    sorted(
        TypeAdapter(list[RouteResponse]).validate_json(
            files("src.data").joinpath("routes.json").read_text(encoding="utf-8")
        ),
        key=lambda route: route.name,
    )
)
ROUTES_BY_ID = MappingProxyType({route.id: route for route in ROUTES})
if len(ROUTES_BY_ID) != len(ROUTES):
    raise ValueError("Duplicate route IDs in static catalog")
