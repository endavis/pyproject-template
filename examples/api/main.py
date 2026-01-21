#!/usr/bin/env python3
"""FastAPI example application.

This example demonstrates:
- Application factory pattern
- Router organization
- Pydantic validation
- Dependency injection
- Error handling
- OpenAPI documentation

Run with:
    uvicorn examples.api.main:app --reload

Visit http://localhost:8000/docs for Swagger UI.
"""

from fastapi import FastAPI

from examples.api.config import settings
from examples.api.errors import register_exception_handlers
from examples.api.routes import items, users


def create_app() -> FastAPI:
    """Application factory for creating FastAPI instances."""
    app = FastAPI(
        title=settings.app_name,
        description="Example FastAPI application demonstrating best practices",
        version=settings.version,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Include routers
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(items.router, prefix="/items", tags=["items"])

    @app.get("/", tags=["health"])
    def root():
        """Health check endpoint."""
        return {"status": "ok", "app": settings.app_name, "version": settings.version}

    @app.get("/health", tags=["health"])
    def health_check():
        """Detailed health check."""
        return {
            "status": "healthy",
            "checks": {
                "app": "ok",
                "config": "ok",
            },
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("examples.api.main:app", host="127.0.0.1", port=8000, reload=True)
