from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from src.data.catalog import ROUTES, ROUTES_BY_ID
from src.domain.value_objects.difficulty import DifficultyLevel
from src.presentation.schemas.responses import (
    ErrorResponse,
    RoutePageResponse,
    RouteResponse,
)

router = APIRouter(prefix="/routes", tags=["Rutas"])


@router.get("", response_model=RoutePageResponse, summary="Listar rutas")
async def list_routes(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    difficulty: DifficultyLevel | None = None,
    location: Annotated[str | None, Query(min_length=2)] = None,
) -> RoutePageResponse:
    routes = [
        route
        for route in ROUTES
        if (difficulty is None or route.difficulty == difficulty.value)
        and (location is None or location.casefold() in route.location.casefold())
    ]
    return RoutePageResponse(
        items=routes[skip : skip + limit], total=len(routes), skip=skip, limit=limit
    )


@router.get("/search", response_model=list[RouteResponse], summary="Buscar rutas")
async def search_routes(
    q: Annotated[str, Query(min_length=2, max_length=100)],
) -> list[RouteResponse]:
    return [route for route in ROUTES if q.strip().casefold() in route.name.casefold()]


@router.get(
    "/{route_id}",
    response_model=RouteResponse,
    summary="Obtener ruta",
    responses={404: {"model": ErrorResponse}},
)
async def get_route(route_id: UUID) -> RouteResponse:
    route = ROUTES_BY_ID.get(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return route
