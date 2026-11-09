"""Unit tests for ShelfSync domain rules, OpenAPI parity, and PII redaction."""

from __future__ import annotations

from pathlib import Path
import yaml

from backend.main import app
from backend.models import compute_stock_status, validate_restock_transition
from backend.telemetry import redact_pii


def test_stock_status_thresholds() -> None:
    assert compute_stock_status(0, 10) == "critical_out"
    assert compute_stock_status(10, 10) == "low_stock"
    assert compute_stock_status(4, 10) == "low_stock"
    assert compute_stock_status(11, 10) == "healthy"


def test_restock_state_machine_rules() -> None:
    assert validate_restock_transition("requested", "approved") is True
    assert validate_restock_transition("approved", "fulfilled") is True
    assert validate_restock_transition("requested", "fulfilled") is False
    assert validate_restock_transition("fulfilled", "approved") is False


def test_recursive_pii_and_credential_redaction() -> None:
    raw_event = {
        "sku": "VAC-FLU26",
        "supplier_email": "private.vendor@biopharma.example",
        "headers": {"Authorization": "Bearer super-secret-jwt-123"},
        "notes": ["Contact alice.smith@clinic.org for cold-chain key"],
    }
    cleaned = redact_pii(raw_event)
    serialized = str(cleaned)
    assert "private.vendor@biopharma.example" not in serialized
    assert "super-secret-jwt-123" not in serialized
    assert "alice.smith@clinic.org" not in serialized
    assert cleaned["supplier_email"] == "[REDACTED]"


def test_openapi_contract_matches_registered_routes() -> None:
    spec_path = Path(__file__).resolve().parents[2] / "openapi.yaml"
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    declared_paths = set(spec["paths"].keys())
    registered_paths = {route.path for route in app.routes if hasattr(route, "path")}
    assert declared_paths.issubset(registered_paths)
