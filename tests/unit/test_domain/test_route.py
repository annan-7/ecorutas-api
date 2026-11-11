import pytest

from src.domain.entities.route import Route
from src.domain.exceptions.domain_exceptions import InvalidRouteError
from src.domain.value_objects.difficulty import Difficulty, DifficultyLevel
from src.domain.value_objects.route_type import RouteType, RouteTypeVO


def make_route(distance: float = 10.0) -> Route:
    return Route(
        name="Ruta de prueba",
        description="Descripción suficiente",
        interesting_fact="Un dato interesante",
        image_url="https://example.com/route.jpg",
        location="Maule",
        distance_km=distance,
        difficulty=Difficulty(DifficultyLevel.MODERADA),
        route_type=RouteTypeVO(RouteType.SENDERISMO),
        duration_hours=3,
    )


def test_route_estimated_calories() -> None:
    assert make_route().estimated_calories == 1200


def test_route_long_when_over_twenty_kilometers() -> None:
    assert make_route(20.1).is_long_route is True
    assert make_route(20).is_long_route is False


def test_route_rejects_non_positive_distance() -> None:
    with pytest.raises(InvalidRouteError, match="distancia"):
        make_route(0)
