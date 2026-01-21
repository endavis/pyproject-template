"""Shared dependencies for dependency injection.

Dependencies are reusable components that FastAPI injects into route handlers.
This keeps routes clean and makes testing easier through dependency overrides.
"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, Query, status


def get_api_key(x_api_key: str = Header(None)) -> str | None:
    """Extract API key from header (optional).

    In a real application, you would validate this against a database
    or authentication service.
    """
    return x_api_key


def require_api_key(x_api_key: str = Header(..., description="API key for authentication")) -> str:
    """Require and validate API key.

    Raises:
        HTTPException: If API key is missing or invalid.
    """
    # In production, validate against database/service
    valid_keys = {"test-api-key", "dev-key-12345"}
    if x_api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return x_api_key


def get_pagination(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
) -> dict[str, int]:
    """Common pagination parameters."""
    return {"skip": skip, "limit": limit}


# Type aliases for cleaner route signatures
APIKey = Annotated[str, Depends(require_api_key)]
OptionalAPIKey = Annotated[str | None, Depends(get_api_key)]
Pagination = Annotated[dict[str, int], Depends(get_pagination)]
