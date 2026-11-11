import asyncio

from src.application.services.route_service import RouteService
from src.infrastructure.database.connection import async_session, create_tables
from src.infrastructure.repositories.sqlalchemy_route_repo import (
    SQLAlchemyRouteRepository,
)
from src.infrastructure.seeders.routes_seeder import seed_routes


async def main() -> None:
    await create_tables()
    async with async_session() as session:
        created, skipped = await seed_routes(
            RouteService(SQLAlchemyRouteRepository(session))
        )
    print(f"Seeder terminado: {created} creadas, {skipped} omitidas")


if __name__ == "__main__":
    asyncio.run(main())
