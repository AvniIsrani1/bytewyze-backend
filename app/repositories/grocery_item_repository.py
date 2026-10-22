from app.models.grocery_item import (
    GroceryItem,
    GroceryItemCreate,
    GroceryItemUpdate,
)


class GroceryItemRepository:
    """Temporary in-memory storage for grocery items."""

    def __init__(self) -> None:
        self._items: dict[int, GroceryItem] = {}
        self._next_id = 0

    def list_items(self) -> list[GroceryItem]:
        return list(self._items.values())

    def get_item(self, item_id: int) -> GroceryItem | None:
        return self._items.get(item_id)

    def create_item(self, request: GroceryItemCreate) -> GroceryItem:
        item = GroceryItem(
            id=self._next_id,
            name=request.name,
            quantity=request.quantity,
            is_completed=False,
        )

        self._items[item.id] = item
        self._next_id += 1
        return item

    def update_item(
        self,
        item_id: int,
        request: GroceryItemUpdate,
    ) -> GroceryItem | None:
        existing = self.get_item(item_id)

        if existing is None:
            return None

        # exclude_unset ensures omitted fields keep their old values.
        updated = existing.model_copy(
            update=request.model_dump(exclude_unset=True),
        )
        self._items[item_id] = updated
        return updated

    def delete_item(self, item_id: int) -> bool:
        if item_id not in self._items:
            return False

        del self._items[item_id]
        return True


# One shared repository used by the router.
grocery_item_repository = GroceryItemRepository()