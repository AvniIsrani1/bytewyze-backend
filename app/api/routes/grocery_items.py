from fastapi import APIRouter, HTTPException, Response, status

from app.models.grocery_item import (
    GroceryItem,
    GroceryItemCreate,
    GroceryItemUpdate,
)

router = APIRouter()

# Temporary development storage. Everything resets when the server restarts.
items: dict[int, GroceryItem] = {
    0: GroceryItem(
        id=0,
        name="Apples",
        quantity=5,
        is_completed=False,
    ),
}
next_item_id = 1


def find_item(item_id: int) -> GroceryItem:
    item = items.get(item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grocery item not found",
        )

    return item


@router.get("", response_model=list[GroceryItem])
async def get_grocery_items() -> list[GroceryItem]:
    return list(items.values())


@router.get("/{item_id}", response_model=GroceryItem)
async def get_grocery_item(item_id: int) -> GroceryItem:
    return find_item(item_id)


@router.post(
    "",
    response_model=GroceryItem,
    status_code=status.HTTP_201_CREATED,
)
async def create_grocery_item(
    request: GroceryItemCreate,
) -> GroceryItem:
    global next_item_id

    item = GroceryItem(
        id=next_item_id,
        name=request.name,
        quantity=request.quantity,
        is_completed=False,
    )

    items[item.id] = item
    next_item_id += 1
    return item


@router.patch("/{item_id}", response_model=GroceryItem)
async def update_grocery_item(
    item_id: int,
    request: GroceryItemUpdate,
) -> GroceryItem:
    existing_item = find_item(item_id)

    updated_item = existing_item.model_copy(
        update=request.model_dump(exclude_unset=True),
    )
    items[item_id] = updated_item
    return updated_item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_grocery_item(item_id: int) -> Response:
    find_item(item_id)
    del items[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)