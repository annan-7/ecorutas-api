# ECORUTAS API

Backend FastAPI para rutas de naturaleza en Chile. Usa DDD, SQLAlchemy async
y SQLite.

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
```

El contenedor crea tablas y 65 rutas automáticamente. El volumen `sqlite_data`
conserva la base entre reinicios.

## Vercel con SQLite

Vercel solo permite escritura en `/tmp`. Usa estas variables en Production:

```env
APP_NAME=ECORUTAS API
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:////tmp/ecorutas.db
API_V1_PREFIX=/api/v1
CORS_ORIGINS=https://proyecto-front-end.vercel.app
INITIALIZE_DATABASE=true
SEED_DATABASE=true
```

Reemplaza `CORS_ORIGINS` por el dominio exacto del frontend. `api/index.py` y
`vercel.json` exponen FastAPI como función Python. Cada instancia crea tablas y
65 rutas iniciales.

Advertencia: `/tmp` no es almacenamiento persistente. Vercel puede borrar la
base en despliegues, reinicios o nuevas instancias. Altas y eliminaciones no
son durables. SQLite persistente requiere un host con disco, como Render.

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
