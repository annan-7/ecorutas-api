from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.exception_handlers import register_exception_handlers
from src.presentation.routers.routes_router import router as routes_router
from src.presentation.schemas.responses import HealthResponse
from src.shared.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API de turismo de naturaleza y senderismo en Chile.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Accept", "Content-Type"],
)
app.include_router(routes_router, prefix=settings.api_v1_prefix)
register_exception_handlers(app)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Sistema"],
    summary="Comprobar salud",
    description="Confirma que el proceso HTTP responde.",
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
