from pydantic import BaseModel


class Product(BaseModel):
    barcode: str
    found: bool
    name: str | None = None
    brand: str | None = None
    image_url: str | None = None
    size: str | None = None
