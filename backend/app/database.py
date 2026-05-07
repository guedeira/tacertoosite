import os
from collections.abc import Callable
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


SessionFactory = Callable[[], Session]


@lru_cache
def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("Configure DATABASE_URL para acessar o banco.")

    return database_url


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)
