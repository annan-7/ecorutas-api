from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Response, status

from src.application.dto.route_dtos import CreateRouteDTO
from src.domain.value_objects.difficulty import DifficultyLevel
from src.presentation.dependencies import RouteServiceDependency
from src.presentation.schemas.requests import CreateRouteRequest
from src.presentation.schemas.responses import (
    ErrorResponse,
    RoutePageResponse,
    RouteResponse,
)

router = APIRouter(prefix="/routes", tags=["Rutas"])


@router.post(
    "",
    response_model=RouteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear ruta",
    description="Crea una ruta de naturaleza validada y geolocalizada.",
    responses={409: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
async def create_route(
    request: CreateRouteRequest, service: RouteServiceDependency
) -> RouteResponse:
    dto = CreateRouteDTO(
        name=request.name,
        description=request.description,
        interesting_fact=request.interesting_fact,
        image_url=str(request.image_url),
        location=request.location,
        distance_km=request.distance_km,
        difficulty=request.difficulty.value,
        route_type=request.route_type.value,
        duration_hours=request.duration_hours,
        latitude=request.latitude,
        longitude=request.longitude,
        altitude_meters=request.altitude_meters,
    )
    return RouteResponse.model_validate(await service.create_route(dto))


@router.get(
    "",
    response_model=RoutePageResponse,
    summary="Listar rutas",
    description="Lista rutas activas con paginación y filtros opcionales.",
)
async def list_routes(
    service: RouteServiceDependency,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    difficulty: DifficultyLevel | None = None,
    location: Annotated[str | None, Query(min_length=2)] = None,
) -> RoutePageResponse:
    page = await service.get_routes(
        skip, limit, difficulty.value if difficulty else None, location
    )
    return RoutePageResponse.model_validate(page, from_attributes=True)


@router.get(
    "/search",
    response_model=list[RouteResponse],
    summary="Buscar rutas",
    description="Busca rutas activas por coincidencia parcial de nombre.",
)
async def search_routes(
    service: RouteServiceDependency,
    q: Annotated[str, Query(min_length=2, max_length=100)],
) -> list[RouteResponse]:
    return [
        RouteResponse.model_validate(item) for item in await service.search_routes(q)
    ]


@router.get(
    "/{route_id}",
    response_model=RouteResponse,
    summary="Obtener ruta",
    description="Obtiene una ruta por UUID.",
    responses={404: {"model": ErrorResponse}},
)
async def get_route(route_id: UUID, service: RouteServiceDependency) -> RouteResponse:
    return RouteResponse.model_validate(await service.get_route(route_id))


@router.delete(
    "/{route_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar ruta",
    description="Elimina una ruta por UUID.",
    responses={404: {"model": ErrorResponse}},
)
async def delete_route(route_id: UUID, service: RouteServiceDependency) -> Response:
    await service.delete_route(route_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
