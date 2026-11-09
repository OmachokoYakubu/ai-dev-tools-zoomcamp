# Multi-Agent Team Specification & Collaboration Protocol

ShelfSync is built and operated by a **six-role agent team** coordinated through explicit artifacts (`product-spec.md`, `openapi.yaml`, GitHub Issues, and structured telemetry) so implementation agents never grade their own work.

---

## 1. Agent Roles & Ownership Boundaries

| Agent Role | Definition | Owned Artifacts | Forbidden Actions |
| :--- | :--- | :--- | :--- |
| **1. PM / Spec Architect** | Translates user pain points into testable user stories, state machines, and GitHub Issues with acceptance criteria checklists. | `product-spec.md`, GitHub Issues | Writing application code or modifying tests. |
| **2. Contract & Backend Agent** | Authors `openapi.yaml`, SQLAlchemy PostgreSQL models, state-machine transactions, and OpenTelemetry/Prometheus instrumentation. | `openapi.yaml`, `backend/` | Weakening test assertions or disabling PII redaction. |
| **3. Frontend UX Agent** | Builds the responsive Operations & Inventory SPA strictly against `openapi.yaml` schemas and surfaces `X-Trace-Id` diagnostics. | `frontend/` | Bypassing API validation or hardcoding mocked persistence. |
| **4. QA & Security Verifier** | Independently writes unit, integration, contract, and PII-redaction regression suites (`tests/`) and audits GitHub Issue acceptance criteria. | `tests/` | Editing production `backend/` routes to make failing tests pass without filing defects. |
| **5. DevOps & Observability Agent** | Owns `Dockerfile`, `compose.yaml`, Prometheus alert rules (`promtool`), Tempo/Grafana provisioning, and staged `dev` → `prod` CI/CD pipelines. | `observability/`, `.github/workflows/`, `compose.yaml` | Deploying unverified builds or skipping promotion gates. |
| **6. On-Call Responder Agent** | Runtime autonomous SRE service (`oncall_agent/responder.py`) woken up by Alertmanager/Prometheus alerts to diagnose `trace_id` failures and execute bounded rollbacks. | `oncall_agent/`, `_docs/runbook.md` | Mutating customer inventory tables or reading unredacted PII. |

---

## 2. Collaboration Graph & Handover Loop

```text
  [1. PM / Spec Architect]
        │  Creates product-spec.md + GitHub Issues (#AC checklists)
        ▼
  [2. Contract & Backend Agent] ──► Publishes openapi.yaml
        │                                  │
        ▼                                  ▼
  PostgreSQL + FastAPI + OTel      [3. Frontend UX Agent]
        │                                  │
        └──────────────┬───────────────────┘
                       ▼
           [4. QA & Security Verifier]
        (Unit + Postgres Integration + Zero-PII Audit)
                       │
          ┌────────────┴────────────┐
          │ Fail: reopen Issue      │ Pass: close Issue with evidence
          ▼                         ▼
  Return to Builder       [5. DevOps & Observability Agent]
                          (CI -> Auto-Deploy Dev -> Manual Gate Prod)
                                    │
                                    ▼ (5xx User-Impact Alert Fires)
                          [6. On-Call Responder Agent]
                          (Diagnose Trace -> Rollback Config -> Verify HTTP 200)
```
