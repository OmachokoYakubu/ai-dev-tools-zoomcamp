# AGENTS.md — Agent Operating Instructions & Context Management

Welcome to the **Order Tracker & Incident Response** project. This document guides AI coding agents working on this codebase to ensure architectural alignment, testing rigor, and context preservation.

---

## 🧭 Modular Documentation Sitemap

Agents **must** consult these documents before modifying or extending system components:

| Topic | Document Path | Summary |
| :--- | :--- | :--- |
| **Product Specification** | [`_docs/specs.md`](./_docs/specs.md) | User stories, acceptance criteria, endpoint contracts, error specifications. |
| **Task Tracker / Backlog** | [`_docs/backlog.md`](./_docs/backlog.md) | Current sprint board, task ownership, and completed agent logs. |
| **Agent Team Roles** | [`_docs/agent-team.md`](./_docs/agent-team.md) | Multi-agent collaboration model, responsibilities, and handoff protocols. |
| **System Architecture** | [`_docs/architecture.md`](./_docs/architecture.md) | Data flow, container topology, telemetry signals, and alert wiring. |
| **Incident Response** | [`incident-response/runbook.md`](./incident-response/runbook.md) | Triage procedures, alert parsing, and automated diagnostic workflows. |

---

## ⚙️ Engineering Rules & Constraints

### 1. Spec-First & Contract Adherence
- Do not add or change API behavior without first updating [`_docs/specs.md`](./_docs/specs.md).
- Status field transitions are strictly constrained to: `received` ➔ `preparing` ➔ `shipped` ➔ `delivered`.

### 2. Dependency Management via `uv`
- Manage all Python dependencies with `uv`. Do not run unpinned `pip install`.
- Run tests via `uv run pytest -v`.

### 3. Date & Time Arithmetic
- All timestamps must be timezone-aware UTC (`timezone.utc`).
- Never perform date manipulation via `.replace(day=day+N)` due to month-boundary overflow bugs. Always use `timedelta(days=N)`.

### 4. Telemetry & Data Privacy
- Never log passwords, tokens, or customer personal identifiers (PII) in trace spans or metrics.
- Keep operational alerts bounded to genuine user impact (5xx errors); 404 client lookups must never trip alerts.

### 5. Automated Verification
- Before submitting any change, run:
  ```bash
  uv run pytest -v
  ```
- Verify Docker container builds cleanly:
  ```bash
  docker compose build
  ```
