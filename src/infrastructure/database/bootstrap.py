import asyncio

from src.application.services.route_service import RouteService
from src.infrastructure.database.connection import async_session, create_tables
from src.infrastructure.repositories.sqlalchemy_route_repo import (
    SQLAlchemyRouteRepository,
)
from src.infrastructure.seeders.routes_seeder import seed_routes
from src.shared.config import settings

_ready = False
_lock = asyncio.Lock()


async def ensure_database_ready() -> None:
    """Initialize once per process, including runtimes without ASGI lifespan."""
    global _ready
    if _ready:
        return
    async with _lock:
        if _ready:
            return
        if settings.initialize_database:
            await create_tables()
        if settings.seed_database:
            async with async_session() as session:
                await seed_routes(RouteService(SQLAlchemyRouteRepository(session)))
        _ready = True
