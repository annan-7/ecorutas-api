from uuid import UUID

from src.application.dto.route_dtos import (
    CreateRouteDTO,
    RoutePageDTO,
    RouteResponseDTO,
)
from src.domain.entities.route import Route
from src.domain.exceptions.domain_exceptions import (
    DuplicateRouteError,
    InvalidRouteError,
    RouteNotFoundError,
)
from src.domain.repositories.i_route_repository import IRouteRepository
from src.domain.value_objects.coordinates import Coordinates
from src.domain.value_objects.difficulty import Difficulty, DifficultyLevel
from src.domain.value_objects.route_type import RouteTypeVO


class RouteService:
    def __init__(self, repository: IRouteRepository) -> None:
        self._repository = repository

    async def create_route(self, dto: CreateRouteDTO) -> RouteResponseDTO:
        if await self._repository.search_by_name(dto.name):
            raise DuplicateRouteError(f"Ya existe una ruta llamada '{dto.name}'")
        route = self._build_route(dto)
        return self._map_to_dto(await self._repository.save(route))

    async def create_missing_routes(
        self, dtos: list[CreateRouteDTO]
    ) -> tuple[int, int]:
        existing = await self._repository.find_all(0, 10_000)
        existing_names = {route.name.casefold() for route in existing}
        missing = [dto for dto in dtos if dto.name.casefold() not in existing_names]
        if missing:
            await self._repository.save_many(
                [self._build_route(dto) for dto in missing]
            )
        return len(missing), len(dtos) - len(missing)

    def _build_route(self, dto: CreateRouteDTO) -> Route:
        coordinates = self._coordinates(dto.latitude, dto.longitude)
        return Route(
            name=dto.name,
            description=dto.description,
            interesting_fact=dto.interesting_fact,
            image_url=dto.image_url,
            location=dto.location,
            distance_km=dto.distance_km,
            difficulty=Difficulty.from_string(dto.difficulty),
            route_type=RouteTypeVO.from_string(dto.route_type),
            duration_hours=dto.duration_hours,
            coordinates=coordinates,
            altitude_meters=dto.altitude_meters,
        )

    async def get_route(self, route_id: UUID) -> RouteResponseDTO:
        route = await self._repository.find_by_id(route_id)
        if route is None:
            raise RouteNotFoundError("Ruta no encontrada")
        return self._map_to_dto(route)

    async def get_routes(
        self,
        skip: int,
        limit: int,
        difficulty: str | None = None,
        location: str | None = None,
    ) -> RoutePageDTO:
        level = DifficultyLevel(difficulty) if difficulty else None
        routes = await self._repository.find_all(skip, limit, level, location)
        total = await self._repository.count(level, location)
        return RoutePageDTO(
            items=[self._map_to_dto(route) for route in routes],
            total=total,
            skip=skip,
            limit=limit,
        )

    async def search_routes(self, term: str) -> list[RouteResponseDTO]:
        return [
            self._map_to_dto(route)
            for route in await self._repository.search_by_name(term)
        ]

    async def delete_route(self, route_id: UUID) -> None:
        if not await self._repository.delete(route_id):
            raise RouteNotFoundError("Ruta no encontrada")

    @staticmethod
    def _coordinates(
        latitude: float | None, longitude: float | None
    ) -> Coordinates | None:
        if latitude is None and longitude is None:
            return None
        if latitude is None or longitude is None:
            raise InvalidRouteError("Latitud y longitud deben enviarse juntas")
        return Coordinates(latitude, longitude)

    @staticmethod
    def _map_to_dto(route: Route) -> RouteResponseDTO:
        return RouteResponseDTO(
            id=route.id,
            name=route.name,
            description=route.description,
            interesting_fact=route.interesting_fact,
            image_url=route.image_url,
            location=route.location,
            distance_km=route.distance_km,
            difficulty=route.difficulty.level.value,
            route_type=route.route_type.value.value,
            duration_hours=route.duration_hours,
            latitude=route.coordinates.latitude if route.coordinates else None,
            longitude=route.coordinates.longitude if route.coordinates else None,
            altitude_meters=route.altitude_meters,
            is_active=route.is_active,
            created_at=route.created_at,
            updated_at=route.updated_at,
            is_long_route=route.is_long_route,
            estimated_calories=route.estimated_calories,
        )
