# AI Dev Tools Zoomcamp 2026 — Project 2 Peer-Review Evaluations

**Reviewer:** Omachoko Yakubu  
**Review Date:** 22 November 2026  
**Course Portal:** [DataTalks.Club AI Dev Tools Zoomcamp 2026 — Project 2 Evaluations](https://courses.datatalks.club/ai-dev-tools-2026/project/project2/eval)  
**Review Deadline:** Tuesday, 24 November 2026, 00:00  
**Rubric Source:** Project 2 Peer Evaluation Form (12 Criteria, 24 Points Maximum)

---

## 1. Assigned Submissions Summary

| Assignment | Peer Pseudonym | Project / Repository | Evaluated Commit | Portal Link | Score |
| :--- | :--- | :--- | :---: | :--- | :---: |
| **#14617** | **Kind Swartz** | [**Agrivanta** (`TheRevenant04/agrivanta`)](https://github.com/TheRevenant04/agrivanta) | `6c2dc95` | [Eval #14617](https://courses.datatalks.club/ai-dev-tools-2026/project/project2/eval/14617) | **21 / 24** |
| **#14618** | **Brave Lederberg** | [**FinPath** (`alicephoo/FinPath_Website`)](https://github.com/alicephoo/FinPath_Website) | `30d2d90` | [Eval #14618](https://courses.datatalks.club/ai-dev-tools-2026/project/project2/eval/14618) | **21 / 24** |
| **#14619** | **Jovial Bassi** | [**ContactHub** (`Source-C0de/contact-connect`)](https://github.com/Source-C0de/contact-connect) | `94fd20f` | [Eval #14619](https://courses.datatalks.club/ai-dev-tools-2026/project/project2/eval/14619) | **14 / 24** |

---

## 2. Comparative Score Matrix (12 Criteria)

| # | Criterion | Max Pts | #14617 (`Agrivanta`) | #14618 (`FinPath`) | #14619 (`ContactHub`) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | **Problem Description** | 2 | **2** | **2** | **2** |
| **2** | **Product Specification** | 2 | **2** | **2** | **1** |
| **3** | **Agent Team Specification** | 2 | **2** | **2** | **0** |
| **4** | **Context Management** | 2 | **2** | **2** | **0** |
| **5** | **Application** | 2 | **2** | **2** | **2** |
| **6** | **Testing** | 2 | **2** | **2** | **1** |
| **7** | **Containerization** | 2 | **2** | **2** | **2** |
| **8** | **Deployment** | 2 | **1** | **2** | **1** |
| **9** | **CI/CD** | 3 | **1** | **1** | **0** |
| **10** | **Observability** | 2 | **2** | **1** | **2** |
| **11** | **Alerting on User Impact** | 1 | **1** | **1** | **1** |
| **12** | **On-Call Agent** | 2 | **2** | **2** | **2** |
| | **Total Score** | **24** | **21 / 24** | **21 / 24** | **14 / 24** |

---

## 3. Detailed Evaluation #14617 — `Agrivanta` (Kind Swartz)

- **Repository URL:** `https://github.com/TheRevenant04/agrivanta`
- **Commit ID:** `6c2dc95`

### Criterion-by-Criterion Breakdown
1. **Problem Description (2/2 — `radio-197-3`):** `README.md` clearly explains the commercial crop-farm operations, inventory, and crop-cycle profitability problem, system features, data domains, and request/AI analyst flows.
2. **Product Specification (2/2 — `radio-198-3`):** `_docs/plan.md` and `_docs/tasks.md` (63 tasks) are paired with public GitHub Issues/PRs (`#1`–`#152`) and a dedicated backlog MCP server (`mcp-server/server.py`) + issue orchestrator (`custom-agent/agent.py`).
3. **Agent Team Specification (2/2 — `radio-199-3`):** `_docs/process.md`, `_docs/team/` (`pm.md`, `software-engineer.md`, `qa-engineer.md`, `code-reviewer.md`), `.agents/agents/`, `.opencode/agent/`, and `custom-agent/agent.py` define a complete 4-role multi-agent workflow.
4. **Context Management (2/2 — `radio-200-3`):** `AGENTS.md` defines repository conventions and links to modular policy docs (`_docs/plan.md`, `_docs/tasks.md`, `_docs/process.md`, `_docs/permissions.md`, `_docs/branching-strategy.md`, `_docs/commit-message-guidelines.md`, `_docs/agent-extension-pack.md`).
5. **Application (2/2 — `radio-201-3`):** Full-stack React 18 + TypeScript (Vite) frontend + Django 5.2 / DRF backend + PostgreSQL 17 + Redis 7 + Celery worker (`docker-compose.yml`).
6. **Testing (2/2 — `radio-202-3`):** Unit and integration test suites for both backend (`backend/api/tests/unit`, `backend/api/tests/integration`) and frontend (`frontend/src/tests/unit`, `frontend/src/tests/integration`) plus Playwright E2E (`frontend/e2e/success-workflow.spec.ts`).
7. **Containerization (2/2 — `radio-203-3`):** `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`, `docker-compose.ci.yml`, and `docker-compose.prod.yml` boot the entire application stack with a single command.
8. **Deployment (1/2 — `radio-204-2`):** `docs/deployment.md` and `docs/ci-cd.md` thoroughly document cloud deployment options (AWS ECS, Azure Container Apps, GCP Cloud Run, Kubernetes), and explicitly note: *"There is currently no active cloud deployment or automated CD pipeline in this repository."*
9. **CI/CD (1/3 — `radio-205-2`):** `.github/workflows/ci.yml` runs backend unit tests, frontend lint/build/unit tests, and full Docker Compose integration + Playwright E2E checks on every pull request (`docs/ci-cd.md`: *"CD is not yet implemented in this repository"*).
10. **Observability (2/2 — `radio-206-3`):** `backend/api/observability.py`, `backend/api/telemetry.py`, and `observability/docker-compose.yml` (OpenTelemetry Collector, Tempo, Loki, Prometheus, and provisioned Grafana dashboards) correlate metrics, traces, and structured logs with PII redaction.
11. **Alerting on User Impact (1/1 — `radio-207-2`):** `observability/prometheus/alerts.yml` defines user-impact alert rules.
12. **On-Call Agent (2/2 — `radio-208-2`):** `on-call-engineer/on_call_agent.py` (tested in `on-call-engineer/tests/test_on_call_agent.py`) wakes up on alerts to diagnose and remediate incidents.

- **Note to Peer:**
  > Outstanding AI-native engineering! The Module 5 extension pack (`.agents/skills/`, `.opencode/plugins/guardrails.js`, `mcp-server/server.py`, and `custom-agent/agent.py`), full OpenTelemetry Collector + Tempo + Loki + Prometheus + Grafana observability stack, and `on-call-engineer/on_call_agent.py` are top-notch. Adding an automated dev CD deployment and manual prod promotion gate in GitHub Actions would bring this to a full 24/24.

---

## 4. Detailed Evaluation #14618 — `FinPath` (Brave Lederberg)

- **Repository URL:** `https://github.com/alicephoo/FinPath_Website`
- **Commit ID:** `30d2d90`
- **Live Frontend:** `https://finpath-website.pages.dev`
- **Live Backend:** `https://finpath-website.onrender.com` (`/health`, `/ready`)

### Criterion-by-Criterion Breakdown
1. **Problem Description (2/2 — `radio-197-3`):** `README.md` ("The Problem" and "Key Features") and `PROJECT_SPEC.md` §1 clearly explain the personal finance and goal-planning problem in Myanmar Kyat (MMK), how available cash is derived from a unified ledger across transactions, loans, savings goals, and trips, and what behavior is expected.
2. **Product Specification (2/2 — `radio-198-3`):** `PROJECT_SPEC.md` is an authoritative 13-section product specification with explicit acceptance criteria (`AC-1`–`AC-16`), paired with a public GitHub Projects v2 board (`https://github.com/users/alicephoo/projects/1`) containing scoped tasks, acceptance criteria, and assigned agent roles.
3. **Agent Team Specification (2/2 — `radio-199-3`):** `AGENTS.md` §3 and `AI_WORKFLOW.md` define a 6-role agent team (Coordinator/Orchestrator, Frontend Engineer, Backend Engineer, QA & Testing Engineer, Security & Reliability Reviewer, Documentation & Context Manager) with clear boundaries, delegation packets, handoff templates, and review gates.
4. **Context Management (2/2 — `radio-200-3`):** `AGENTS.md` §2 defines a strict 7-level documentation precedence chain and links to modular specifications (`PROJECT_SPEC.md`, `API_CONTRACTS.md`, `BACKEND_ARCHITECTURE.md`, `AI_WORKFLOW.md`, `PROGRESS.md`, `docs/ALERTING_RUNBOOK.md`, `docs/ONCALL_RUNBOOK.md`).
5. **Application (2/2 — `radio-201-3`):** Complete 5-tab React 19 + TypeScript + Vite frontend connected to a FastAPI + SQLAlchemy 2 + PostgreSQL 17 backend with Argon2id/JWT auth, ETag concurrency, and single-command local Compose boot.
6. **Testing (2/2 — `radio-202-3`):** Comprehensive unit, integration (543 PostgreSQL-backed Pytest tests), frontend component (330 Vitest tests), and Playwright Chromium E2E tests passing in GitHub Actions (`Run #43782171763`).
7. **Containerization (2/2 — `radio-203-3`):** `backend/Dockerfile`, `frontend/Dockerfile`, and `compose.yaml` start PostgreSQL 17 (with role initialization and healthchecks), apply Alembic migrations and reference seeds automatically, and serve the full stack via `docker compose up --build`.
8. **Deployment (2/2 — `radio-204-3`):** Deployed and reachable at `https://finpath-website.pages.dev` (Cloudflare Pages + Pages Function proxy) and `https://finpath-website.onrender.com` (Render FastAPI + Neon PostgreSQL 17).
9. **CI/CD (1/3 — `radio-205-2`):** `.github/workflows/ci.yml` automatically runs 5 CI jobs (backend Pytest, frontend Vitest/build, Playwright E2E, Docker build, and container staging-lite) on every push and PR. As transparently documented in `README.md` and `PROGRESS.md`, automated CD deployment to dev/prod is not wired in GitHub Actions.
10. **Observability (1/2 — `radio-206-2`):** Emits structured JSON logs with `X-Request-ID` correlation, privacy-safe allowlisted domain events, and an in-process Prometheus metrics registry (`/metrics`). As noted in `README.md` ("This is request correlation and in-process metrics, not distributed tracing... Metrics are disabled in production; no tracing, dashboard, log aggregation/retention"), distributed tracing and a telemetry visualization UI are not yet included.
11. **Alerting on User Impact (1/1 — `radio-207-2`):** `.github/workflows/alerting.yml` and `backend/app/core/alerting.py` run four hourly user-impact synthetic probes (`frontend`, `backend_health`, `backend_ready`, `auth_smoke`) backed by 90 unit tests and `docs/ALERTING_RUNBOOK.md`.
12. **On-Call Agent (2/2 — `radio-208-2`):** `.github/workflows/oncall-agent.yml`, `backend/app/core/oncall_agent.py`, and `docs/ONCALL_RUNBOOK.md` implement a `workflow_run`-triggered on-call responder that classifies probe failures and generates/verifies bounded fixture repairs (verified by 95 tests and local CLI simulations).

- **Note to Peer:**
  > Exceptionally well-engineered and transparently documented project! The 6-role `AGENTS.md` architecture, least-privilege PostgreSQL role separation (`finpath_migrator`, `finpath_app`, `finpath_registration`), and 880+ automated Pytest/Vitest/Playwright tests are outstanding. To reach a full 24/24, consider adding OpenTelemetry trace export + a Grafana/Tempo Compose profile for visual trace-log-metric correlation and wiring an automated dev deployment + manual prod promotion gate in GitHub Actions.

---

## 5. Detailed Evaluation #14619 — `ContactHub` (Jovial Bassi)

- **Repository URL:** `https://github.com/Source-C0de/contact-connect`
- **Commit ID:** `94fd20f`

### Criterion-by-Criterion Breakdown
1. **Problem Description (2/2 — `radio-197-3`):** `README.md` clearly describes ContactHub—an office-wide employee and department contact directory with a React/TypeScript SPA, Node/Express REST API, PostgreSQL persistence, sync/activity logs, and offline `localStorage` fallback.
2. **Product Specification (1/2 — `radio-198-2`):** Detailed architectural and migration plans with Mermaid diagrams and verification gates exist in `.puku/plans/postgres_database_migration_2ee98fb5.plan.md` and `docker_production_setup_249d4bdd.plan.md`, but there is no public task tracker with agent activity.
3. **Agent Team Specification (0/2 — `radio-199-1`):** No agent team or multi-agent collaboration workflow is documented (`project-guide.md` is a copy of the course rubric).
4. **Context Management (0/2 — `radio-200-1`):** No `AGENTS.md` (or equivalent project context management document) is present in the repository.
5. **Application (2/2 — `radio-201-3`):** Full-stack React/Vite SPA + Express API (`server/index.js`) + PostgreSQL (`server/db.js`) with 7 relational tables, PBKDF2 authentication, and one-command Docker Compose startup.
6. **Testing (1/2 — `radio-202-2`):** Frontend unit tests exist in `src/test/department-colors.test.tsx` and `src/test/example.test.ts` (run via `npm test` / Vitest), but backend/database integration tests are missing.
7. **Containerization (2/2 — `radio-203-3`):** Multi-stage `Dockerfile`, `oncall-agent/Dockerfile`, and `docker-compose.yml` launch `app`, `db` (`postgres:16-alpine` with healthcheck), and the `--profile observability` stack cleanly.
8. **Deployment (1/2 — `radio-204-2`):** `README.md` Part 2 and `scripts/deploy-prod.sh` / `scripts/diagnose-prod.sh` thoroughly document Ubuntu LAN deployment, backups, and troubleshooting, though no live public URL or deployment demo video is provided.
9. **CI/CD (0/3 — `radio-205-1`):** No `.github/workflows/` or CI/CD pipeline exists in the repository.
10. **Observability (2/2 — `radio-206-3`):** `server/observability.js` implements correlated structured JSON logs, spans, and Prometheus metrics (`/api/v1/metrics`) sharing a 128-bit `traceId` (`x-request-id` / `traceparent`), strict allowlist PII scrubbing + HMAC `subjectHash`, and a full Prometheus + Loki + Promtail + Grafana Compose stack.
11. **Alerting on User Impact (1/1 — `radio-207-2`):** `observability/prometheus/rules/` and `observability/alertmanager/alertmanager.yml` define user-impact alerts routed to the on-call responder.
12. **On-Call Agent (2/2 — `radio-208-2`):** `oncall-agent/agent.js` receives Alertmanager webhooks and executes `api-recover` and `auth-recover` runbooks (checking DB health, probing `/api/v1/auth/login`, restarting `app`, and verifying `/api/v1/health` recovery).

- **Note to Peer:**
  > Great full-stack implementation and impressive zero-dependency observability (`server/observability.js` with allowlist PII redaction, HMAC subject hashing, and Loki/Prometheus/Grafana/Alertmanager integration) plus a clean `oncall-agent/agent.js` responder! To strengthen the project further, add an `AGENTS.md` + agent team documentation, backend integration tests for `server/index.js`, and a GitHub Actions CI/CD workflow.
