"""Pydantic schemas for request/response validation.

Schemas define the shape of data for API requests and responses.
They provide automatic validation, serialization, and OpenAPI documentation.
"""

from pydantic import BaseModel, EmailStr, Field

# --- User Schemas ---


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        examples=["johndoe"],
        description="Unique username",
    )
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(
        ...,
        min_length=8,
        examples=["SecurePass123!"],
        description="Password (minimum 8 characters)",
    )


class UserUpdate(BaseModel):
    """Schema for updating a user (all fields optional)."""

    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    """Schema for user responses (excludes sensitive data)."""

    id: int
    username: str
    email: EmailStr
    is_active: bool = True

    class Config:
        from_attributes = True  # Enable ORM mode


# --- Item Schemas ---


class ItemCreate(BaseModel):
    """Schema for creating a new item."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Widget"],
        description="Item name",
    )
    description: str | None = Field(
        None,
        max_length=500,
        examples=["A useful widget"],
    )
    price: float = Field(..., gt=0, examples=[29.99], description="Price in USD")
    quantity: int = Field(default=0, ge=0, description="Stock quantity")


class ItemUpdate(BaseModel):
    """Schema for updating an item (all fields optional)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class ItemResponse(BaseModel):
    """Schema for item responses."""

    id: int
    name: str
    description: str | None = None
    price: float
    quantity: int = 0
    owner_id: int

    class Config:
        from_attributes = True


# --- Error Schemas ---


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    error: str = Field(..., description="Error type identifier")
    message: str = Field(..., description="Human-readable error message")
    details: dict | None = Field(None, description="Additional error details")
