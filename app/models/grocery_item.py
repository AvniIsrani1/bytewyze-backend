from pydantic import BaseModel


class GroceryItem(BaseModel):
    name: str
    id: int
    quantity: int | None = None