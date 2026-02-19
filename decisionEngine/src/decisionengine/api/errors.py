from fastapi import Request
from fastapi.responses import JSONResponse
from decisionengine.core.exceptions import (
    DomainError,
    NoVehicleAvailableError,
    RouteNotFoundError,
)


def register_exception_handlers(app):

    @app.exception_handler(NoVehicleAvailableError)
    async def no_vehicle_handler(request: Request, exc: NoVehicleAvailableError):
        return JSONResponse(
            status_code=404,
            content={
                "error": "no_vehicle_available",
                "message": str(exc),
            },
        )

    @app.exception_handler(RouteNotFoundError)
    async def route_not_found_handler(request: Request, exc: RouteNotFoundError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "route_not_found",
                "message": str(exc),
            },
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "domain_error",
                "message": str(exc),
            },
        )
