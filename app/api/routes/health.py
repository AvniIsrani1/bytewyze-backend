import logging

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from sqlmodel import Session

from app.db.session import get_engine

logger = logging.getLogger(__name__)

router = APIRouter()


# plain def (not async) on purpose: PyMySQL blocks while it waits, so FastAPI runs this in a worker thread
@router.get("/health/db")
def db_health() -> dict[str, str]:
    try:
        with Session(get_engine()) as session:
            session.connection().execute(text("SELECT 1")).scalar_one()
    except Exception as exc:
        logger.exception("Database health check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable.",
        ) from exc
    return {"database": "ok"}
