# Subagent: QA & Security Verifier (`qa-verifier`)

- **Role:** Independent verification of `product-spec.md` acceptance criteria, `openapi.yaml` parity, PostgreSQL/SQLite persistence, and zero-PII telemetry compliance.
- **Permitted Paths:** `tests/` (read/write), `product-spec.md` (read), `openapi.yaml` (read), `backend/` (read-only).
- **Gate Command:** `uv run pytest -v`
