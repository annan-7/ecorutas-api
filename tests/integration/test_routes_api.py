from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.infrastructure.database.connection import Base, get_session
from src.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with sessions() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    await engine.dispose()


ROUTE_PAYLOAD = {
    "name": "Sendero de integración",
    "description": "Descripción completa de la ruta",
    "interesting_fact": "Un dato suficientemente interesante",
    "image_url": "https://example.com/ruta.jpg",
    "location": "Maule",
    "distance_km": 12.5,
    "difficulty": "moderada",
    "route_type": "senderismo",
    "duration_hours": 4,
    "latitude": -35.4,
    "longitude": -71.0,
    "altitude_meters": 800,
}


@pytest.mark.asyncio
async def test_route_lifecycle(client: AsyncClient) -> None:
    created = await client.post("/api/v1/routes", json=ROUTE_PAYLOAD)
    assert created.status_code == 201
    route = created.json()
    assert route["estimated_calories"] == 1500

    listing = await client.get("/api/v1/routes?difficulty=moderada")
    assert listing.status_code == 200
    assert listing.json()["total"] == 1

    fetched = await client.get(f"/api/v1/routes/{route['id']}")
    assert fetched.status_code == 200

    deleted = await client.delete(f"/api/v1/routes/{route['id']}")
    assert deleted.status_code == 204
    assert (await client.get(f"/api/v1/routes/{route['id']}")).status_code == 404


@pytest.mark.asyncio
async def test_duplicate_route_returns_conflict(client: AsyncClient) -> None:
    assert (await client.post("/api/v1/routes", json=ROUTE_PAYLOAD)).status_code == 201
    assert (await client.post("/api/v1/routes", json=ROUTE_PAYLOAD)).status_code == 409
