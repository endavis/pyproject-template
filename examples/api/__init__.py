"""FastAPI example application package.

This package demonstrates best practices for building REST APIs with FastAPI:

- Application factory pattern (main.py)
- Configuration with Pydantic Settings (config.py)
- Request/response validation with Pydantic (schemas.py)
- Dependency injection (deps.py)
- Custom error handling (errors.py)
- Router organization (routes/)

To run:
    uvicorn examples.api.main:app --reload

Then visit http://localhost:8000/docs for Swagger UI.
"""
