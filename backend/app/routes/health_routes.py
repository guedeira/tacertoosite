from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database import get_session_factory

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.get("/health/database")
def database_health_check() -> dict:
    try:
        with get_session_factory()() as session:
            session.execute(text("select 1"))
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "database": "unavailable",
            },
        ) from error

    return {
        "status": "ok",
        "database": "available",
    }
