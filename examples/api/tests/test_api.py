"""Tests for the FastAPI example application.

These tests demonstrate how to test FastAPI applications using TestClient.
To run these tests, install the required dependencies:

    uv add fastapi uvicorn[standard] httpx pytest

Then run:

    pytest examples/api/tests/
"""

import pytest

# Skip all tests if FastAPI is not installed
pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from examples.api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_root_returns_ok(self, client):
        """Test the root endpoint returns status ok."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "app" in data
        assert "version" in data

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "checks" in data


class TestUserEndpoints:
    """Tests for user CRUD endpoints."""

    def test_list_users(self, client):
        """Test listing users."""
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) >= 2  # We have 2 default users

    def test_list_users_with_pagination(self, client):
        """Test listing users with pagination."""
        response = client.get("/users?skip=1&limit=1")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 1

    def test_get_user(self, client):
        """Test getting a single user."""
        response = client.get("/users/1")
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == 1
        assert "username" in user
        assert "email" in user

    def test_get_user_not_found(self, client):
        """Test 404 when user doesn't exist."""
        response = client.get("/users/99999")
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "not_found"

    def test_create_user(self, client):
        """Test creating a new user."""
        response = client.post(
            "/users",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 201
        user = response.json()
        assert user["username"] == "newuser"
        assert user["email"] == "newuser@example.com"
        assert "password" not in user  # Password should not be returned
        assert user["is_active"] is True

    def test_create_user_invalid_email(self, client):
        """Test validation error for invalid email."""
        response = client.post(
            "/users",
            json={
                "username": "testuser",
                "email": "not-an-email",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 422  # Validation error

    def test_create_user_password_too_short(self, client):
        """Test validation error for short password."""
        response = client.post(
            "/users",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "short",
            },
        )
        assert response.status_code == 422

    def test_create_user_duplicate_username(self, client):
        """Test conflict error for duplicate username."""
        # First create a user
        client.post(
            "/users",
            json={
                "username": "duplicateuser",
                "email": "dup1@example.com",
                "password": "securepassword123",
            },
        )
        # Try to create another with same username
        response = client.post(
            "/users",
            json={
                "username": "duplicateuser",
                "email": "dup2@example.com",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 409
        data = response.json()
        assert data["error"] == "conflict"

    def test_update_user(self, client):
        """Test updating a user."""
        response = client.patch("/users/1", json={"username": "updated_alice"})
        assert response.status_code == 200
        user = response.json()
        assert user["username"] == "updated_alice"

    def test_update_user_not_found(self, client):
        """Test 404 when updating non-existent user."""
        response = client.patch("/users/99999", json={"username": "ghost"})
        assert response.status_code == 404

    def test_delete_user_requires_api_key(self, client):
        """Test that delete requires API key."""
        response = client.delete("/users/2")
        assert response.status_code == 422  # Missing required header

    def test_delete_user_invalid_api_key(self, client):
        """Test delete with invalid API key."""
        response = client.delete("/users/2", headers={"x-api-key": "invalid-key"})
        assert response.status_code == 401

    def test_delete_user_with_valid_api_key(self, client):
        """Test delete with valid API key."""
        # First create a user to delete
        create_response = client.post(
            "/users",
            json={
                "username": "tobedeleted",
                "email": "delete@example.com",
                "password": "securepassword123",
            },
        )
        user_id = create_response.json()["id"]

        # Delete with valid API key
        response = client.delete(f"/users/{user_id}", headers={"x-api-key": "test-api-key"})
        assert response.status_code == 204

        # Verify user is gone
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404


class TestItemEndpoints:
    """Tests for item CRUD endpoints."""

    def test_list_items(self, client):
        """Test listing items."""
        response = client.get("/items")
        assert response.status_code == 200
        items = response.json()
        assert isinstance(items, list)
        assert len(items) >= 3  # We have 3 default items

    def test_list_items_filter_by_owner(self, client):
        """Test filtering items by owner."""
        response = client.get("/items?owner_id=1")
        assert response.status_code == 200
        items = response.json()
        for item in items:
            assert item["owner_id"] == 1

    def test_list_items_filter_by_price(self, client):
        """Test filtering items by price range."""
        response = client.get("/items?min_price=25&max_price=40")
        assert response.status_code == 200
        items = response.json()
        for item in items:
            assert 25 <= item["price"] <= 40

    def test_get_item(self, client):
        """Test getting a single item."""
        response = client.get("/items/1")
        assert response.status_code == 200
        item = response.json()
        assert item["id"] == 1
        assert "name" in item
        assert "price" in item

    def test_get_item_not_found(self, client):
        """Test 404 when item doesn't exist."""
        response = client.get("/items/99999")
        assert response.status_code == 404

    def test_create_item(self, client):
        """Test creating a new item."""
        response = client.post(
            "/items?owner_id=1",
            json={
                "name": "New Product",
                "description": "A brand new product",
                "price": 99.99,
                "quantity": 10,
            },
        )
        assert response.status_code == 201
        item = response.json()
        assert item["name"] == "New Product"
        assert item["price"] == 99.99
        assert item["owner_id"] == 1

    def test_create_item_minimal(self, client):
        """Test creating item with only required fields."""
        response = client.post(
            "/items?owner_id=2",
            json={
                "name": "Minimal Item",
                "price": 9.99,
            },
        )
        assert response.status_code == 201
        item = response.json()
        assert item["name"] == "Minimal Item"
        assert item["quantity"] == 0  # Default value

    def test_create_item_invalid_price(self, client):
        """Test validation error for invalid price."""
        response = client.post(
            "/items?owner_id=1",
            json={
                "name": "Free Item",
                "price": -5.00,  # Negative price not allowed
            },
        )
        assert response.status_code == 422

    def test_update_item(self, client):
        """Test updating an item."""
        response = client.patch("/items/1", json={"price": 34.99})
        assert response.status_code == 200
        item = response.json()
        assert item["price"] == 34.99

    def test_delete_item(self, client):
        """Test deleting an item."""
        # First create an item to delete
        create_response = client.post(
            "/items?owner_id=1",
            json={"name": "To Delete", "price": 1.00},
        )
        item_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404


class TestOpenAPIDocumentation:
    """Tests for OpenAPI documentation endpoints."""

    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
        assert "info" in schema

    def test_swagger_ui_available(self, client):
        """Test that Swagger UI is available in debug mode."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

    def test_redoc_available(self, client):
        """Test that ReDoc is available in debug mode."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "redoc" in response.text.lower()
