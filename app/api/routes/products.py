from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.api.deps import get_http_client
from app.models.product import Product
from app.services.product_lookup import ProductLookupError, lookup_product

router = APIRouter()

# retail barcodes are 8-14 digits
BARCODE_PATTERN = r"^\d{8,14}$"


@router.get("/{barcode}", response_model=Product)
async def get_product(
    barcode: Annotated[str, Path(pattern=BARCODE_PATTERN, examples=["3017624010701"])],
    client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
) -> Product:
    try:
        return await lookup_product(barcode, client)
    except ProductLookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Product lookup is temporarily unavailable.",
        ) from exc
