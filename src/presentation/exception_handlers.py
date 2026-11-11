from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions.domain_exceptions import (
    DomainError,
    DuplicateRouteError,
    RouteNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RouteNotFoundError)
    async def route_not_found(
        request: Request, exc: RouteNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
        )

    @app.exception_handler(DuplicateRouteError)
    async def duplicate_route(
        request: Request, exc: DuplicateRouteError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
        )

    @app.exception_handler(DomainError)
    async def domain_error(request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc)},
        )
