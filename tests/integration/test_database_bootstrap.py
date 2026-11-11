import asyncio
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.infrastructure.database import bootstrap, connection
from src.main import app


@pytest.mark.asyncio
async def test_cold_requests_without_lifespan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'cold.db'}")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(connection, "engine", engine)
    monkeypatch.setattr(connection, "async_session", sessions)
    monkeypatch.setattr(bootstrap, "async_session", sessions)
    monkeypatch.setattr(bootstrap, "_ready", False)
    monkeypatch.setattr(bootstrap, "_lock", asyncio.Lock())
    monkeypatch.setattr(bootstrap.settings, "initialize_database", True)
    monkeypatch.setattr(bootstrap.settings, "seed_database", True)
    try:
        # ASGITransport deliberately does not dispatch lifespan events.
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            responses = await asyncio.gather(
                *(client.get("/api/v1/routes") for _ in range(3))
            )
            for response in responses:
                assert response.status_code == 200
                assert response.json()["total"] == 65

            # A new initialization against the same database must not duplicate seeds.
            monkeypatch.setattr(bootstrap, "_ready", False)
            response = await client.get("/api/v1/routes")
            assert response.status_code == 200
            assert response.json()["total"] == 65
    finally:
        await engine.dispose()
