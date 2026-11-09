"""Pytest fixtures providing isolated test databases for ShelfSync."""

from __future__ import annotations

from collections.abc import Generator
import os
from pathlib import Path
import sys

import pytest
from sqlalchemy.orm import sessionmaker

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import backend.database as db_module  # noqa: E402
from backend.main import RUNTIME_STATE, seed_if_empty  # noqa: E402
from backend.telemetry import (  # noqa: E402
    IN_MEMORY_SPAN_EXPORTER,
    RECENT_5XX_TRACES,
    STRUCTURED_LOG_BUFFER,
)


@pytest.fixture(autouse=True)
def isolated_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    test_db_url = os.environ.get("TEST_POSTGRES_URL")
    if not test_db_url:
        sqlite_file = tmp_path / "test_shelfsync.db"
        test_db_url = f"sqlite:///{sqlite_file}"

    test_engine = db_module.build_engine(test_db_url)
    TestSessionLocal = sessionmaker(
        bind=test_engine, autoflush=False, autocommit=False, expire_on_commit=False
    )
    db_module.Base.metadata.drop_all(bind=test_engine)
    db_module.Base.metadata.create_all(bind=test_engine)

    monkeypatch.setattr(db_module, "engine", test_engine)
    monkeypatch.setattr(db_module, "SessionLocal", TestSessionLocal)

    with TestSessionLocal() as session:
        seed_if_empty(session)

    RUNTIME_STATE["supplier_gateway_mode"] = "healthy"
    IN_MEMORY_SPAN_EXPORTER.clear()
    STRUCTURED_LOG_BUFFER.clear()
    RECENT_5XX_TRACES.clear()

    yield

    test_engine.dispose()
