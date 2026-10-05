import logging
import time

import httpx

from app.models.product import Product

logger = logging.getLogger(__name__)

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

USER_AGENT = "LocalFork/0.1 (https://github.com/AvniIsrani1/bytewyze-frontend)"

# only request the fields we actually show to keep responses small
REQUESTED_FIELDS = "product_name,brands,image_small_url,quantity"

REQUEST_TIMEOUT_SECONDS = 5.0

CACHE_TTL_SECONDS = 60 * 60 * 24
CACHE_MAX_ENTRIES = 5000

# barcode -> (expires_at, product)
_cache: dict[str, tuple[float, Product]] = {}


class ProductLookupError(Exception):
    """Open Food Facts was unreachable or returned something unusable."""


def _cache_get(barcode: str) -> Product | None:
    entry = _cache.get(barcode)
    if entry is None:
        return None

    expires_at, product = entry
    if expires_at < time.monotonic():
        del _cache[barcode]
        return None

    return product


def _cache_put(barcode: str, product: Product) -> None:
    _cache.pop(barcode, None)

    while len(_cache) >= CACHE_MAX_ENTRIES:
        _cache.pop(next(iter(_cache)))

    _cache[barcode] = (time.monotonic() + CACHE_TTL_SECONDS, product)


def clear_cache() -> None:
    _cache.clear()


def _to_product(barcode: str, payload: dict) -> Product:
    # status is 1 when the product exists, 0 when the barcode is unknown.
    if payload.get("status") != 1:
        return Product(barcode=barcode, found=False)

    raw = payload.get("product") or {}

    # Open Food Facts returns "" for missing text fields and comma-separates multiple brands
    def text(key: str) -> str | None:
        value = raw.get(key)
        if not isinstance(value, str):
            return None
        value = value.strip()
        return value or None

    brand = text("brands")
    if brand is not None:
        brand = brand.split(",")[0].strip() or None

    return Product(
        barcode=barcode,
        found=True,
        name=text("product_name"),
        brand=brand,
        image_url=text("image_small_url"),
        size=text("quantity"),
    )


async def lookup_product(barcode: str, client: httpx.AsyncClient) -> Product:
    cached = _cache_get(barcode)
    if cached is not None:
        logger.debug("Product cache hit for %s", barcode)
        return cached

    logger.debug("Product cache miss for %s, checking Open Food Facts", barcode)
    try:
        response = await client.get(
            OPEN_FOOD_FACTS_URL.format(barcode=barcode),
            params={"fields": REQUESTED_FIELDS},
            headers={"User-Agent": USER_AGENT},
        )
    except httpx.HTTPError as exc:
        raise ProductLookupError(f"Could not reach Open Food Facts: {exc}") from exc

    # OFF answers 404 for unknown barcodes
    if response.status_code == httpx.codes.NOT_FOUND:
        product = Product(barcode=barcode, found=False)
        _cache_put(barcode, product)
        return product

    if response.status_code >= httpx.codes.BAD_REQUEST:
        raise ProductLookupError(
            f"Open Food Facts returned {response.status_code} for {barcode}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise ProductLookupError("Open Food Facts returned invalid JSON") from exc

    if not isinstance(payload, dict):
        raise ProductLookupError("Open Food Facts returned an unexpected payload")

    product = _to_product(barcode, payload)
    _cache_put(barcode, product)
    return product
