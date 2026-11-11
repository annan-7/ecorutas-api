"""Compatibility helpers reading the same static catalog served by the API."""

import json
from dataclasses import fields
from importlib.resources import files

from src.application.dto.route_dtos import CreateRouteDTO
from src.application.services.route_service import RouteService


def build_seed_data() -> list[CreateRouteDTO]:
    data = json.loads(files("src.data").joinpath("routes.json").read_text("utf-8"))
    names = {field.name for field in fields(CreateRouteDTO)}
    return [
        CreateRouteDTO(**{key: value for key, value in row.items() if key in names})
        for row in data
    ]


async def seed_routes(service: RouteService) -> tuple[int, int]:
    return await service.create_missing_routes(build_seed_data())
