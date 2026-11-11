import pytest

from src.domain.exceptions.domain_exceptions import InvalidRouteError
from src.domain.value_objects.coordinates import Coordinates


def test_coordinates_validate_ranges() -> None:
    assert Coordinates(-33.4, -70.6).latitude == -33.4
    with pytest.raises(InvalidRouteError, match="Latitud"):
        Coordinates(-91, 0)
