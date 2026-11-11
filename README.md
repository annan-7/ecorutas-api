# ECORUTAS API

Backend FastAPI para rutas de naturaleza en Chile. Usa DDD, SQLAlchemy async,
PostgreSQL en producción y SQLite durante desarrollo.

## Inicio local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
python -m src.infrastructure.seeders.run_seeders
uvicorn src.main:app --reload
```

Documentación: <http://localhost:8000/docs>

## Docker

```bash
docker compose up --build
docker compose exec api alembic upgrade head
docker compose exec api python -m src.infrastructure.seeders.run_seeders
```

## Endpoints

- `GET /health`
- `POST /api/v1/routes`
- `GET /api/v1/routes`
- `GET /api/v1/routes/search?q=torres`
- `GET /api/v1/routes/{route_id}`
- `DELETE /api/v1/routes/{route_id}`

Filtros de listado: `skip`, `limit`, `difficulty` y `location`.

## Calidad

```bash
ruff check src tests
black --check src tests
mypy src
pytest --cov=src
```
