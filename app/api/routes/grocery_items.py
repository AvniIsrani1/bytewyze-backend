from fastapi import APIRouter, HTTPException, Path, status
from app.models.grocery_item import GroceryItem

router = APIRouter()

items = []

@router.get("/{item_id}", response_model=GroceryItem)
async def get_grocery_item(item_id: int) -> GroceryItem:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@router.post("/f")