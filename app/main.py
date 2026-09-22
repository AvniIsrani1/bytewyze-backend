from fastapi import FastAPI
from app.api.routes import auth, users

app = FastAPI(title="Local Fork")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/health")
async def health():
    return {"status": "ok"}