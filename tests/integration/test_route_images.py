import json
from importlib.resources import files
from urllib.parse import urlsplit

from src.data.catalog import ROUTES


def test_images_are_distinct_and_have_source_credits() -> None:
    credits = json.loads(files("src.data").joinpath("image_credits.json").read_text())
    by_id = {item["route_id"]: item for item in credits}
    assert len(credits) == len(by_id) == len(ROUTES) == 65
    assert len({route.image_url for route in ROUTES}) == 65
    for route in ROUTES:
        credit = by_id[str(route.id)]
        assert credit["image_url"] == route.image_url
        assert credit["route_name"] == route.name
        assert credit["author"]
        assert credit["license"]
        assert credit["source_url"].startswith("https://commons.wikimedia.org/")
        assert urlsplit(route.image_url).hostname == "upload.wikimedia.org"
