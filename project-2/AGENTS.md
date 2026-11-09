# AGENTS.md — ShelfSync Context Index & Operating Rules

**ShelfSync** is an AI-natively engineered full-stack clinic and cold-chain inventory management, automated restock workflow, and self-healing observability platform built for **AI Dev Tools Zoomcamp 2026 (Project 2)**.

Agents must treat this file as the **entry-point routing table** and load only the modular document relevant to their active task.

---

## 🧭 Modular Documentation Map

| Domain | Document | Purpose & When to Read |
| :--- | :--- | :--- |
| **Product Specification** | [`product-spec.md`](./product-spec.md) | User stories, acceptance criteria (`AC-1`..`AC-6`), state transitions, and public GitHub Issues tracker links. Read before any feature change. |
| **API Source of Truth** | [`openapi.yaml`](./openapi.yaml) | OpenAPI 3.1 contract for Frontend ↔ Backend ↔ On-Call Agent communication. Update contract *before* route code. |
| **Agent Team & Process** | [`_docs/agent-team.md`](./_docs/agent-team.md) | Six-role multi-agent collaboration graph, tool permissions, and QA verification handoffs. |
| **System Architecture** | [`_docs/architecture.md`](./_docs/architecture.md) | PostgreSQL persistence, OpenTelemetry `trace_id` correlation, PII redaction boundary, and CI/CD topology. |
| **Incident Runbook** | [`_docs/runbook.md`](./_docs/runbook.md) | Diagnostic steps and bounded remediation rules executed by the autonomous On-Call Responder Agent. |
| **Reusable Agent Skills** | [`.agents/skills/`](./.agents/skills/) | Discoverable `SKILL.md` workflows (`contract-first-api`, `incident-triage`) and subagent definitions. |
| **Public Task Tracker** | [GitHub Issues](https://github.com/OmachokoYakubu/ai-dev-tools-zoomcamp/issues) | Live public issue board with acceptance criteria checklists and agent execution logs. |

---

## 🛡️ Non-Negotiable Engineering Guardrails

1. **Contract-First Development:** Every HTTP route in `backend/` must conform to [`openapi.yaml`](./openapi.yaml) and carry automated integration test coverage.
2. **Database Agnosticism with Production PostgreSQL:** Use SQLAlchemy 2.0 ORM (`DATABASE_URL`). Production and Docker Compose run **PostgreSQL 16**; fast local unit tests may use isolated temporary SQLite databases.
3. **Correlated Telemetry & Zero PII Leakage:**
   - Every request on the key user journey (`SKU create` → `drawdown` → `restock create` → `fulfill`) must emit structured JSON logs, Prometheus metrics, and OpenTelemetry spans sharing the same `trace_id` (`X-Trace-Id` response header).
   - Never emit `supplier_email`, `supplier_phone`, `authorization`, `cookie`, or `api_key` values to logs, spans, or metrics (`[REDACTED]`).
4. **Actionable User-Impact Alerting:** Client validation errors (`400`/`404`/`422`) must never trigger page alerts; alerts fire strictly on user-impacting `5xx` error rates or `p95` latency breaches.
5. **Single-Command Verification:**
   - Run all unit + integration + self-healing tests: `uv run pytest -v`
   - Run full multi-container stack (App + PostgreSQL 16 + Prometheus + Tempo + Grafana + On-Call Agent): `docker compose up --build -d`
