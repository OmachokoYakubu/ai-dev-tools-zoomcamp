"""SQLAlchemy 2.0 database engine and session management (PostgreSQL & SQLite)."""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


def resolve_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        if url.startswith("postgresql://") and "+psycopg" not in url:
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url
    default_sqlite = Path(__file__).resolve().parents[1] / "data" / "shelfsync.db"
    default_sqlite.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{default_sqlite}"


def build_engine(db_url: str | None = None):
    target_url = db_url or resolve_database_url()
    connect_args = {"check_same_thread": False} if target_url.startswith("sqlite") else {}
    return create_engine(target_url, connect_args=connect_args, pool_pre_ping=True)


engine = build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
