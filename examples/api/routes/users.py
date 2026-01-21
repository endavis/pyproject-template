"""User management routes.

This module demonstrates:
- CRUD operations
- Request/response validation with Pydantic
- Dependency injection
- Error handling
"""

from fastapi import APIRouter, Path, status

from examples.api.deps import APIKey, Pagination
from examples.api.errors import ConflictError, NotFoundError
from examples.api.schemas import ErrorResponse, UserCreate, UserResponse, UserUpdate

router = APIRouter()

# In-memory "database" for demonstration
_users_db: dict[int, dict] = {
    1: {"id": 1, "username": "alice", "email": "alice@example.com", "is_active": True},
    2: {"id": 2, "username": "bob", "email": "bob@example.com", "is_active": True},
}
_next_id = 3


@router.get(
    "",
    response_model=list[UserResponse],
    summary="List all users",
    description="Retrieve a paginated list of all users.",
)
def list_users(pagination: Pagination):
    """List users with pagination."""
    users = list(_users_db.values())
    skip = pagination["skip"]
    limit = pagination["limit"]
    return users[skip : skip + limit]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
    summary="Get a user by ID",
)
def get_user(user_id: int = Path(..., gt=0, description="The user ID")):
    """Get a specific user by their ID."""
    if user_id not in _users_db:
        raise NotFoundError("User", user_id)
    return _users_db[user_id]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"model": ErrorResponse, "description": "Username already exists"}},
    summary="Create a new user",
)
def create_user(user: UserCreate):
    """Create a new user account.

    - **username**: Must be unique, 3-50 characters
    - **email**: Valid email address
    - **password**: Minimum 8 characters (not stored in response)
    """
    global _next_id

    # Check for duplicate username
    for existing in _users_db.values():
        if existing["username"] == user.username:
            raise ConflictError(f"Username '{user.username}' already exists")

    new_user = {
        "id": _next_id,
        "username": user.username,
        "email": user.email,
        "is_active": True,
    }
    _users_db[_next_id] = new_user
    _next_id += 1

    return new_user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
    summary="Update a user",
)
def update_user(
    user_id: int = Path(..., gt=0),
    user_update: UserUpdate = ...,
):
    """Update an existing user. Only provided fields are updated."""
    if user_id not in _users_db:
        raise NotFoundError("User", user_id)

    user = _users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    user.update(update_data)

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse, "description": "User not found"}},
    summary="Delete a user",
)
def delete_user(
    user_id: int = Path(..., gt=0),
    api_key: APIKey = ...,  # Require authentication for delete
):
    """Delete a user (requires API key authentication)."""
    if user_id not in _users_db:
        raise NotFoundError("User", user_id)

    del _users_db[user_id]
    return None
