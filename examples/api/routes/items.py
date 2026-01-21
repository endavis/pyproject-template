"""Item management routes.

This module demonstrates:
- CRUD operations with owner relationship
- Query parameters for filtering
- Multiple response types in OpenAPI
"""

from fastapi import APIRouter, Path, Query, status

from examples.api.deps import Pagination
from examples.api.errors import NotFoundError
from examples.api.schemas import ErrorResponse, ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()

# In-memory "database" for demonstration
_items_db: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Widget",
        "description": "A useful widget",
        "price": 29.99,
        "quantity": 100,
        "owner_id": 1,
    },
    2: {
        "id": 2,
        "name": "Gadget",
        "description": "An amazing gadget",
        "price": 49.99,
        "quantity": 50,
        "owner_id": 1,
    },
    3: {
        "id": 3,
        "name": "Gizmo",
        "description": None,
        "price": 19.99,
        "quantity": 200,
        "owner_id": 2,
    },
}
_next_id = 4


@router.get(
    "",
    response_model=list[ItemResponse],
    summary="List all items",
    description="Retrieve items with optional filtering by owner or price range.",
)
def list_items(
    pagination: Pagination,
    owner_id: int | None = Query(None, description="Filter by owner ID"),
    min_price: float | None = Query(None, ge=0, description="Minimum price filter"),
    max_price: float | None = Query(None, ge=0, description="Maximum price filter"),
):
    """List items with pagination and optional filters."""
    items = list(_items_db.values())

    # Apply filters
    if owner_id is not None:
        items = [i for i in items if i["owner_id"] == owner_id]
    if min_price is not None:
        items = [i for i in items if i["price"] >= min_price]
    if max_price is not None:
        items = [i for i in items if i["price"] <= max_price]

    # Apply pagination
    skip = pagination["skip"]
    limit = pagination["limit"]
    return items[skip : skip + limit]


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    responses={404: {"model": ErrorResponse, "description": "Item not found"}},
    summary="Get an item by ID",
)
def get_item(item_id: int = Path(..., gt=0, description="The item ID")):
    """Get a specific item by ID."""
    if item_id not in _items_db:
        raise NotFoundError("Item", item_id)
    return _items_db[item_id]


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
)
def create_item(
    item: ItemCreate,
    owner_id: int = Query(..., gt=0, description="ID of the item owner"),
):
    """Create a new item.

    - **name**: Item name (1-100 characters)
    - **description**: Optional description (up to 500 characters)
    - **price**: Price in USD (must be positive)
    - **quantity**: Stock quantity (default: 0)
    """
    global _next_id

    new_item = {
        "id": _next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "quantity": item.quantity,
        "owner_id": owner_id,
    }
    _items_db[_next_id] = new_item
    _next_id += 1

    return new_item


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    responses={404: {"model": ErrorResponse, "description": "Item not found"}},
    summary="Update an item",
)
def update_item(
    item_id: int = Path(..., gt=0),
    item_update: ItemUpdate = ...,
):
    """Update an existing item. Only provided fields are updated."""
    if item_id not in _items_db:
        raise NotFoundError("Item", item_id)

    item = _items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)
    item.update(update_data)

    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse, "description": "Item not found"}},
    summary="Delete an item",
)
def delete_item(item_id: int = Path(..., gt=0)):
    """Delete an item."""
    if item_id not in _items_db:
        raise NotFoundError("Item", item_id)

    del _items_db[item_id]
    return None
