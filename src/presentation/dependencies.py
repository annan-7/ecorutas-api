from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.route_service import RouteService
from src.infrastructure.database.connection import get_session
from src.infrastructure.repositories.sqlalchemy_route_repo import (
    SQLAlchemyRouteRepository,
)

SessionDependency = Annotated[AsyncSession, Depends(get_session)]


def get_route_service(session: SessionDependency) -> RouteService:
    return RouteService(SQLAlchemyRouteRepository(session))


RouteServiceDependency = Annotated[RouteService, Depends(get_route_service)]
