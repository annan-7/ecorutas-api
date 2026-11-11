import importlib
from dataclasses import asdict
from uuid import UUID, uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from src.data import catalog
from src.infrastructure.seeders.routes_seeder import build_seed_data


@pytest.mark.asyncio
async def test_public_catalog_without_lifespan_or_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Exercise the Vercel entry point without lifespan events or authentication.
    monkeypatch.setenv("CORS_ORIGINS", "*")
    from src.shared.config import settings

    monkeypatch.setattr(settings, "cors_origins", "*")
    from api.index import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://test"
    ) as client:
        assert (await client.get("/health")).json() == {"status": "ok"}
        response = await client.get("/api/v1/routes?limit=100")
        assert response.status_code == 200
        page = response.json()
        assert page["total"] == len(page["items"]) == 65
        by_name = {row["name"]: row for row in page["items"]}
        for seed in build_seed_data():
            row = by_name[seed.name]
            for key, value in asdict(seed).items():
                assert row[key] == value
            detail = await client.get(f"/api/v1/routes/{row['id']}")
            assert detail.status_code == 200
            assert detail.json() == row
        default = (await client.get("/api/v1/routes")).json()
        assert default["items"] == page["items"][:20]
        next_page = (await client.get("/api/v1/routes?skip=20&limit=20")).json()
        assert next_page["items"] == page["items"][20:40]
        assert (await client.get("/api/v1/routes?skip=100")).json()["items"] == []
        assert (await client.get(f"/api/v1/routes/{uuid4()}")).status_code == 404
        for path in [
            "/api/v1/routes/not-a-uuid",
            "/api/v1/routes?limit=101",
            "/api/v1/routes?skip=-1",
            "/api/v1/routes?difficulty=unknown",
        ]:
            assert (await client.get(path)).status_code == 422
        filtered = (
            await client.get("/api/v1/routes?difficulty=facil&location=magallanes")
        ).json()
        assert filtered["total"] > 0
        assert all(
            row["difficulty"] == "facil" and row["location"] == "Magallanes"
            for row in filtered["items"]
        )
        search = (await client.get("/api/v1/routes/search?q=TORRES")).json()
        assert len(search) == 3
        assert all("torres" in row["name"].casefold() for row in search)
        assert (await client.post("/api/v1/routes", json={})).status_code == 405
        assert (
            await client.delete(f"/api/v1/routes/{page['items'][0]['id']}")
        ).status_code == 405
        preflight = await client.options(
            "/api/v1/routes",
            headers={
                "Origin": "https://any-client.example",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert preflight.status_code == 200
        assert preflight.headers["access-control-allow-origin"] == "*"


def test_catalog_ids_survive_reload() -> None:
    before = tuple(route.model_dump() for route in catalog.ROUTES)
    importlib.reload(catalog)
    assert tuple(route.model_dump() for route in catalog.ROUTES) == before
    assert len({UUID(str(route.id)) for route in catalog.ROUTES}) == 65
