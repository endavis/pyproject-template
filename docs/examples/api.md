---
title: API Development Guide
description: Building REST APIs with FastAPI - patterns, testing, and best practices
audience:
  - users
  - contributors
tags:
  - examples
  - api
  - fastapi
---

# API Development Guide

This guide covers building REST APIs with FastAPI, including application structure, validation, authentication, error handling, and testing patterns.

## Why FastAPI?

- **Automatic OpenAPI/Swagger docs** at `/docs` and `/redoc`
- **Type-based validation** via Pydantic
- **Async support** out of the box
- **Dependency injection** for clean, testable code
- **Modern Python** - type hints drive the framework

## Quick Start

### Installation

```bash
# Add FastAPI and uvicorn to your project
uv add fastapi uvicorn[standard]

# For testing
uv add --dev httpx pytest-asyncio
```

### Minimal Example

```python
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}
```

Run with:

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Application Structure

For larger applications, organize code into modules:

```
src/myapp/
├── __init__.py
├── main.py              # Application factory
├── config.py            # Settings/configuration
├── deps.py              # Shared dependencies
├── schemas/             # Pydantic models
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── routes/              # API routers
│   ├── __init__.py
│   ├── users.py
│   └── items.py
├── services/            # Business logic
│   ├── __init__.py
│   └── user_service.py
└── models/              # Database models (if using ORM)
    └── __init__.py
```

### Application Factory Pattern

```python
# main.py
from fastapi import FastAPI

from myapp.config import settings
from myapp.routes import users, items


def create_app() -> FastAPI:
    """Application factory for creating FastAPI instances."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Include routers
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(items.router, prefix="/items", tags=["items"])

    return app


app = create_app()
```

### Configuration with Pydantic Settings

```python
# config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "My API"
    version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./app.db"

    # Security
    secret_key: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
```

## Request/Response Handling

### Pydantic Models for Validation

```python
# schemas/user.py
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """Schema for user responses (excludes password)."""

    id: int
    username: str
    email: EmailStr
    is_active: bool = True

    class Config:
        from_attributes = True  # Allows ORM model conversion


class UserUpdate(BaseModel):
    """Schema for updating a user (all fields optional)."""

    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    is_active: bool | None = None
```

### Path and Query Parameters

```python
from fastapi import APIRouter, Query, Path

router = APIRouter()


@router.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., gt=0, description="The user ID"),
    include_inactive: bool = Query(False, description="Include inactive users"),
):
    """Get a user by ID."""
    return {"user_id": user_id, "include_inactive": include_inactive}


@router.get("/users")
def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    search: str | None = Query(None, min_length=1, description="Search term"),
):
    """List users with pagination."""
    return {"skip": skip, "limit": limit, "search": search}
```

### Request Body

```python
from fastapi import APIRouter, status

from myapp.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Create a new user."""
    # user is already validated by Pydantic
    new_user = {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "is_active": True,
    }
    return new_user
```

## Dependency Injection

Dependencies are reusable components injected into route handlers:

```python
# deps.py
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_api_key(x_api_key: str = Header(...)) -> str:
    """Validate API key from header."""
    if x_api_key != "secret-api-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return x_api_key


# Type aliases for cleaner signatures
DB = Annotated[Session, Depends(get_db)]
APIKey = Annotated[str, Depends(get_api_key)]
```

Usage in routes:

```python
from myapp.deps import DB, APIKey


@router.get("/protected")
def protected_route(api_key: APIKey, db: DB):
    """Route requiring API key authentication."""
    return {"message": "Access granted", "api_key": api_key[:4] + "..."}
```

## Authentication & Security

### JWT Authentication

```python
# auth.py
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from myapp.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decode JWT and return the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch user from database
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
```

### Login Endpoint

```python
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token login."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
```

## Error Handling

### Custom Exception Handlers

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    """Resource not found."""

    def __init__(self, resource: str, id: int | str):
        self.resource = resource
        self.id = id


class ValidationError(Exception):
    """Business logic validation error."""

    def __init__(self, message: str):
        self.message = message


def create_app() -> FastAPI:
    app = FastAPI()

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "not_found",
                "message": f"{exc.resource} with id {exc.id} not found",
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "validation_error",
                "message": exc.message,
            },
        )

    return app
```

### Standard Error Response Format

```python
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    error: str
    message: str
    details: dict | None = None


# Document in OpenAPI
@router.get(
    "/users/{user_id}",
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def get_user(user_id: int):
    ...
```

## Testing APIs

### Using TestClient

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient

from myapp.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_create_user(client):
    """Test user creation."""
    response = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "password" not in data  # Should not expose password


def test_create_user_invalid_email(client):
    """Test validation error for invalid email."""
    response = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "not-an-email",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 422


def test_get_user_not_found(client):
    """Test 404 for non-existent user."""
    response = client.get("/users/99999")
    assert response.status_code == 404
```

### Async Test Client

For async endpoints, use `pytest-asyncio` with `httpx`:

```python
import pytest
from httpx import AsyncClient, ASGITransport

from myapp.main import app


@pytest.fixture
async def async_client():
    """Create async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_async_endpoint(async_client):
    """Test an async endpoint."""
    response = await async_client.get("/async-endpoint")
    assert response.status_code == 200
```

### Mocking Dependencies

```python
from unittest.mock import MagicMock

from myapp.deps import get_db
from myapp.main import app


def test_with_mock_db(client):
    """Test with mocked database."""
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = {
        "id": 1,
        "username": "mockuser",
    }

    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get("/users/1")
    assert response.status_code == 200

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def override_auth():
    """Override authentication for testing."""
    from myapp.auth import get_current_user

    mock_user = {"id": 1, "username": "testuser", "is_active": True}
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    app.dependency_overrides.clear()


def test_protected_route(client, override_auth):
    """Test protected route with mocked auth."""
    response = client.get("/protected")
    assert response.status_code == 200
```

## OpenAPI Documentation

FastAPI automatically generates OpenAPI documentation. Enhance it with:

### Adding Examples

```python
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., examples=["johndoe"])
    email: str = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["SecurePass123!"])

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123!",
            }
        }
```

### Route Documentation

```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account. Email must be unique.",
    response_description="The created user",
    tags=["users"],
)
def create_user(user: UserCreate):
    """
    Create a new user with the following information:

    - **username**: unique username (3-50 characters)
    - **email**: valid email address
    - **password**: secure password (minimum 8 characters)
    """
    ...
```

### Exporting OpenAPI Schema

```bash
# Get the OpenAPI JSON
curl http://localhost:8000/openapi.json > openapi.json

# Or programmatically
python -c "from myapp.main import app; import json; print(json.dumps(app.openapi()))"
```

## Running in Production

### With Uvicorn

```bash
# Development
uvicorn myapp.main:app --reload

# Production
uvicorn myapp.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Gunicorn + Uvicorn Workers

```bash
gunicorn myapp.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application
COPY src/ ./src/

# Run
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## See Also

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Production Deployment Guide](../deployment/production.md)
- [Testing Guide](../development/ci-cd-testing.md)
