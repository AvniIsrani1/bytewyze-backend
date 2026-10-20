from pydantic import BaseModel, Field

class GroceryItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(default=1, ge=1)


class GroceryItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    quantity: int | None = Field(default=None, ge=1)
    is_completed: bool | None = None


class GroceryItem(BaseModel):
    id: int
    name: str
    quantity: int
    is_completed: bool = False