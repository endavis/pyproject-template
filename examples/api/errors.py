"""Custom exceptions and error handlers.

This module defines application-specific exceptions and registers
FastAPI exception handlers for consistent error responses.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    """Resource not found."""

    def __init__(self, resource: str, id: int | str) -> None:
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} with id {id} not found")


class ConflictError(Exception):
    """Resource conflict (e.g., duplicate)."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ValidationError(Exception):
    """Business logic validation error."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the FastAPI app."""

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "not_found",
                "message": f"{exc.resource} with id {exc.id} not found",
            },
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "conflict",
                "message": exc.message,
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "validation_error",
                "message": exc.message,
                "details": exc.details,
            },
        )
