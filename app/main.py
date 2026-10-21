from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

<<<<<<< HEAD
from app.api.routes import auth, products, users, grocery_items
=======
from app.api.routes import auth, health, products, users
>>>>>>> main
from app.services.product_lookup import REQUEST_TIMEOUT_SECONDS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # one client for whole process - reused across requests so connections to Open Food Facts are pooled instead of reopened per scan
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        app.state.http_client = client
        yield


app = FastAPI(title="Local Fork", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
<<<<<<< HEAD
app.include_router(grocery_items.router, prefix="/grocery-items", tags=["grocery-items"])
=======
app.include_router(health.router, tags=["health"])
>>>>>>> main


@app.get("/health")
async def health():
    return {"status": "ok"}
