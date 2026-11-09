---
name: contract-first-api
description: Enforce OpenAPI-first design, SQLAlchemy persistence, correlated OpenTelemetry spans/logs/metrics, and zero-PII redaction before exposing FastAPI endpoints.
---

# Contract-First API Skill

## Workflow
1. Read `product-spec.md` and confirm the target GitHub Issue acceptance criteria.
2. Add or update the endpoint, request body, and status-code schemas in `openapi.yaml` first.
3. Implement SQLAlchemy 2.0 transactional persistence in `backend/` without raw string SQL interpolation.
4. Instrument the route with OpenTelemetry span attributes and Prometheus counters while passing payloads through `redact_pii()`.
5. Hand off to `qa-verifier` to execute contract + integration + PII redaction assertions via `uv run pytest -v`.
