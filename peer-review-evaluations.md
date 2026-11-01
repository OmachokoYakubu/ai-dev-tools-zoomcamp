# AI Dev Tools Zoomcamp 2026 Capstone Peer-Review Evaluations

**Review date:** 1 November 2026  
**Course Portal:** [DataTalks.Club AI Dev Tools Zoomcamp 2026](https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/)  
**Submission Deadline:** Thursday, 5 November 2026, 06:00 UTC (07:00 Local)  
**Rubric Source:** Capstone Project 1 Peer Evaluation Form (12 Criteria)  
**Maximum Score per Submission:** 24 points

---

## 1. Scope & Submissions Evaluated

| Assignment | Project Name | Author / Repository | Reviewed Commit | Evaluation Form Link |
|:---|:---|:---|:---|:---|
| **#14512** | **Hub-Platform** | [rdanielsstat/hub-platform](https://github.com/rdanielsstat/hub-platform) | `9c69209` | [Eval #14512](https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14512) |
| **#14513** | **PromptHub Enterprise** | [code-hy/PromptHub_Enterprise](https://github.com/code-hy/PromptHub_Enterprise) | `b3afbfe` | [Eval #14513](https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14513) |
| **#14514** | **CareerPilot** | [robanc/CareerPilot](https://github.com/robanc/CareerPilot) | `4352d4d` | [Eval #14514](https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14514) |

---

## 2. Evaluation Rubric (24 Points Maximum)

| # | Criterion | Points Scale | Description |
|:--|:---|:---:|:---|
| **1** | **Problem Description** | 0 – 2 | 0: Not described · 1: Brief/unclear · 2: Clear problem, functionality, and expected behavior in README |
| **2** | **Product Specification** | 0 – 2 | 0: No specs · 1: Spec exists, no public task tracker · 2: Spec exists, public task tracker with acceptance criteria used by agents |
| **3** | **Agent Team Specification** | 0 – 2 | 0: None · 1: Roles mentioned but unclear responsibilities · 2: Defined agent team and collaboration process |
| **4** | **Context Management** | 0 – 2 | 0: No docs · 1: AGENTS.md describes project · 2: AGENTS.md points to modular docs (process, teams, etc.) |
| **5** | **Application** | 0 – 2 | 0: Not working/missing components · 1: Frontend/backend/DB not fully connected · 2: Working full-stack app, data persists, runs with single command |
| **6** | **Testing** | 0 – 2 | 0: No tests/fail · 1: Only unit or only integration · 2: Both unit and integration tests exist, single command, and pass |
| **7** | **Containerization** | 0 – 2 | 0: None · 1: Dockerfiles exist, manual steps needed · 2: Full system (including DB) runs via Docker/Compose with a single command |
| **8** | **Deployment** | 0 – 2 | 0: Not deployed · 1: Steps described, no working deployment shown · 2: Deployed and reachable at public URL, or clear working demo |
| **9** | **CI/CD** | 0 – 3 | 0: None · 1: CI runs tests automatically on PR · 2: CI tests + CD auto-deploys · 3: CI tests + CD deploys to dev + manual deploy to prod |
| **10** | **Observability** | 0 – 2 | 0: None · 1: Logs only, no traces/metrics correlated · 2: Key journey instrumented with metrics, traces, structured logs sharing trace ID, viewable in UI, no PII leak |
| **11** | **Alerting on User Impact** | 0 – 1 | 0: No alerts · 1: At least one alert exists |
| **12** | **On-Call Agent** | 0 or 2 | 0: No on-call agent · 2: An agent wakes up on an alert and fixes the issue |

---

## 3. Comparative Score Summary

| # | Criterion | Weight | Hub-Platform (#14512) | PromptHub Enterprise (#14513) | CareerPilot (#14514) |
|---|:---|:---:|:---:|:---:|:---:|
| 1 | Problem Description | 2 | **2** | **2** | **2** |
| 2 | Product Specification | 2 | **2** | **1** | **2** |
| 3 | Agent Team Specification | 2 | **2** | **2** | **2** |
| 4 | Context Management | 2 | **2** | **2** | **2** |
| 5 | Application | 2 | **2** | **2** | **2** |
| 6 | Testing | 2 | **2** | **2** | **2** |
| 7 | Containerization | 2 | **2** | **2** | **2** |
| 8 | Deployment | 2 | **2** | **2** | **1** |
| 9 | CI/CD | 3 | **3** | **2** | **1** |
| 10 | Observability | 2 | **2** | **0** | **2** |
| 11 | Alerting on User Impact | 1 | **1** | **0** | **1** |
| 12 | On-Call Agent | 2 | **2** | **0** | **2** |
| **Total** | | **24** | **24 / 24 (100%)** | **17 / 24 (71%)** | **21 / 24 (88%)** |

---

## 4. Detailed Evaluation: Assignment #14512 (Hub-Platform)

* **Repository:** [rdanielsstat/hub-platform](https://github.com/rdanielsstat/hub-platform)
* **Reviewed Commit:** `9c69209`
* **Evaluation Link:** [https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14512](https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14512)

### Score Breakdown & Form Selections

1. **Problem Description — 2 / 2 points**  
   * *Selection:* `The README clearly describes the problem, the system functionality, and expected behavior.`
   * *Evidence:* High-quality problem framing as a personal idea management platform with quick capture, multi-stage lifecycle, scoring engine, and full expected user behavior. Includes seeded demo credentials (`demo@hub.dev` / `demo-hub-2026`).

2. **Product Specification — 2 / 2 points**  
   * *Selection:* `A specification exists and there's a publicly accessible task tracker. The tasks define acceptance criteria and there's evidence that the agents used the tracker.`
   * *Evidence:* Comprehensive `product-spec.md` accompanied by active GitHub Issues tracker with linked PRs, clear acceptance criteria, agent progress comments, and automated incident tracking.

3. **Agent Team Specification — 2 / 2 points**  
   * *Selection:* `The project defines the agent team and process of how they work together.`
   * *Evidence:* `AGENT_TEAM.md` and `AGENTS.md` articulate specialized agent roles (Architect, Backend Developer, Frontend Developer, DevOps/SRE, Security Auditor, and On-Call Agent) with defined ownership boundaries and handover protocols.

4. **Context Management — 2 / 2 points**  
   * *Selection:* `AGENTS.md exists and it also points to modular docs (process, teams, etc.).`
   * *Evidence:* `AGENTS.md` (27KB) links cleanly to modular runbooks and specifications (`ops/`, `security/`, `docs/agent-extension-pack.md`, `openapi.yaml`, `product-spec.md`).

5. **Application — 2 / 2 points**  
   * *Selection:* `Full-stack application works end to end: frontend talks to backend, data persists in a database. Application runs locally with a single command.`
   * *Evidence:* React 19 + TypeScript frontend seamlessly integrated with FastAPI and PostgreSQL 17. Single-command local startup via `docker compose up` or `make run`.

6. **Testing — 2 / 2 points**  
   * *Selection:* `Both unit and integration tests exist, run with a single command, and pass.`
   * *Evidence:* Over 470 backend unit and integration test functions (`backend/tests/`), Vitest frontend tests, and automated Playwright end-to-end tests all passing with isolated test databases.

7. **Containerization — 2 / 2 points**  
   * *Selection:* `The full system, including the database, runs via Docker or Docker Compose and starts with a single command.`
   * *Evidence:* Complete multi-container `docker-compose.yml` packaging frontend, backend, PostgreSQL, and observability services with health checks and persistence volumes.

8. **Deployment — 2 / 2 points**  
   * *Selection:* `The application is deployed and reachable at a public URL, or there's a clear demo with the deployment.`
   * *Evidence:* Live, functional cloud deployment on AWS Lambda / Neon / S3 with reachable public endpoints: Development (`https://hub-dev.dnls.dev`) and Production (`https://hub.dnls.dev`).

9. **CI/CD — 3 / 3 points**  
   * *Selection:* `CI runs tests, CD deploys to dev, and there's a manual deploy to production.`
   * *Evidence:* `.github/workflows/ci.yml` runs linters, security audits, and tests on PR/push, auto-deploys to dev environment, and `.github/workflows/promote.yml` enforces a manual promotion gate to production.

10. **Observability — 2 / 2 points**  
    * *Selection:* `A key user journey is instrumented with metrics, traces, and structured logs that share a trace ID; no customer data or credentials are sent to telemetry; and the signals are collected, stored, and viewable in a UI.`
    * *Evidence:* OpenTelemetry instrumentation for project creation and updates, distributed traces, structured JSON logging with propagated trace IDs, PII redaction, and dashboards in Grafana Cloud.

11. **Alerting on User Impact — 1 / 1 point**  
    * *Selection:* `At least one alert exists.`
    * *Evidence:* Configured Prometheus / Grafana alerts monitoring user-impacting failures (e.g., project creation error rates and elevated 5xx latency).

12. **On-Call Agent — 2 / 2 points**  
    * *Selection:* `An agent wakes up on an alert and fixes the issue.`
    * *Evidence:* `.github/workflows/observability-alert-handler.yml` triggers autonomously on user-impact alerts, diagnoses the issue, records a tracking issue, and triggers an automated safe image rollback via `rollback-dev.yml` without human intervention.

### Review Comments for Peer Form
> **Commendation:** Truly outstanding submission. Every rubric requirement has been executed with exceptional rigor, from the multi-agent specifications and security checks to the self-healing rollback agent in GitHub Actions. The live AWS dev and prod environments with shared demo access make evaluation seamless. Exceptional engineering work!

---

## 5. Detailed Evaluation: Assignment #14513 (PromptHub Enterprise)

* **Repository:** [code-hy/PromptHub_Enterprise](https://github.com/code-hy/PromptHub_Enterprise)
* **Reviewed Commit:** `b3afbfe`
* **Evaluation Link:** [https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14513](https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14513)

### Score Breakdown & Form Selections

1. **Problem Description — 2 / 2 points**  
   * *Selection:* `The README clearly describes the problem, the system functionality, and expected behavior.`
   * *Evidence:* `README.md` clearly describes the need for an enterprise prompt management and governance workbench, providing 68 seeded prompts, detailed user flows, and expected behavior.

2. **Product Specification — 1 / 2 points**  
   * *Selection:* `A spec exists, but no public task tracker.`
   * *Evidence:* `product-spec.md` details user stories, acceptance criteria, and non-functional requirements. However, no public task tracker (GitHub Issues or external Kanban) is linked or used for task tracking.

3. **Agent Team Specification — 2 / 2 points**  
   * *Selection:* `The project defines the agent team and process of how they work together.`
   * *Evidence:* `agent-capabilities/` defines specialized sub-agents (`prompt-librarian.md` and `quality-reviewer.md`) detailing input/output contracts, tools, and execution workflows.

4. **Context Management — 2 / 2 points**  
   * *Selection:* `AGENTS.md exists and it also points to modular docs (process, teams, etc.).`
   * *Evidence:* `AGENTS.md` exists and links to modular guides including `TECHNICAL_GUIDE.md`, `DATA_MODEL.md`, `IMPLEMENTATION_GUIDE.md`, `openapi.yaml`, and `USERGUIDE.md`.

5. **Application — 2 / 2 points**  
   * *Selection:* `Full-stack application works end to end: frontend talks to backend, data persists in a database. Application runs locally with a single command.`
   * *Evidence:* Full-stack React + FastAPI + PostgreSQL/SQLite application with 68 seeded prompts, workflows, and evaluation sandbox. Runs locally via `docker compose up --build`.

6. **Testing — 2 / 2 points**  
   * *Selection:* `Both unit and integration tests exist, run with a single command, and pass.`
   * *Evidence:* Unit tests (`backend/tests/unit/test_quality_engine.py`) and API integration tests (`backend/tests/integration/test_api.py`), along with frontend Vitest tests, run and pass via `uv run pytest`.

7. **Containerization — 2 / 2 points**  
   * *Selection:* `The full system, including the database, runs via Docker or Docker Compose and starts with a single command.`
   * *Evidence:* Multi-container `docker-compose.yml` orchestrating PostgreSQL, Qdrant, Ollama, FastAPI backend, and Vite frontend.

8. **Deployment — 2 / 2 points**  
   * *Selection:* `The application is deployed and reachable at a public URL, or there's a clear demo with the deployment.`
   * *Evidence:* Live public deployment on Render: Frontend at `https://prompthub-web.onrender.com` and Backend API at `https://prompthub-api-56ez.onrender.com`.

9. **CI/CD — 2 / 3 points**  
   * *Selection:* `CI runs tests and CD automatically deploys.`
   * *Evidence:* `.github/workflows/ci.yml` runs backend and frontend test suites on PR/push, and automatically deploys passing builds to Render via deploy hook. (No separate dev environment with manual promotion gate to prod).

10. **Observability — 0 / 2 points**  
    * *Selection:* `No telemetry.`
    * *Evidence:* No OpenTelemetry, Prometheus metrics, or distributed tracing pipeline configured; telemetry signals are not viewable in a monitoring UI.

11. **Alerting on User Impact — 0 / 1 point**  
    * *Selection:* `No alerts.`
    * *Evidence:* No Prometheus or third-party alert rules configured for user impact.

12. **On-Call Agent — 0 / 2 points**  
    * *Selection:* `No on-call agent.`
    * *Evidence:* No autonomous incident response or on-call agent implemented.

### Review Comments for Peer Form
> **Feedback:** Excellent full-stack application and comprehensive product documentation. The Contoso M365 prompt library, deterministic quality engine, and Render deployment are well executed. To attain full rubric marks in future iterations, consider implementing OpenTelemetry tracing, Prometheus alerts, and an autonomous incident responder or on-call agent. Great work overall!

---

## 6. Detailed Evaluation: Assignment #14514 (CareerPilot)

* **Repository:** [robanc/CareerPilot](https://github.com/robanc/CareerPilot)
* **Reviewed Commit:** `4352d4d`
* **Evaluation Link:** [https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14514](https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/14514)

### Score Breakdown & Form Selections

1. **Problem Description — 2 / 2 points**  
   * *Selection:* `The README clearly describes the problem, the system functionality, and expected behavior.`
   * *Evidence:* Highly detailed `README.md` addressing fragmented job application tracking, resume matching heuristics, and interview management with clear expected system behavior.

2. **Product Specification — 2 / 2 points**  
   * *Selection:* `A specification exists and there's a publicly accessible task tracker. The tasks define acceptance criteria and there's evidence that the agents used the tracker.`
   * *Evidence:* Comprehensive `product-spec.md` with user stories and acceptance criteria. Active public GitHub Issues tracker (`https://github.com/robanc/CareerPilot/issues`) linked, including Issue #3 with explicit acceptance criteria and Claude Code review evidence.

3. **Agent Team Specification — 2 / 2 points**  
   * *Selection:* `The project defines the agent team and process of how they work together.`
   * *Evidence:* `README.md` and `docs/agent-extension-pack.md` specify agent roles (Developer, Security Reviewer, Release Auditor, On-Call Investigator, On-Call Responder) and their structured handover protocols.

4. **Context Management — 2 / 2 points**  
   * *Selection:* `AGENTS.md exists and it also points to modular docs (process, teams, etc.).`
   * *Evidence:* `AGENTS.md` and `CLAUDE.md` systematically point to modular documentation (`product-spec.md`, `openapi.yaml`, `docs/agent-extension-pack.md`, `docs/permissions.md`, `docs/ai-development-log.md`).

5. **Application — 2 / 2 points**  
   * *Selection:* `Full-stack application works end to end: frontend talks to backend, data persists in a database. Application runs locally with a single command.`
   * *Evidence:* Complete React + FastAPI + PostgreSQL full-stack application supporting application tracking and resume matching. Starts cleanly with a single command: `docker compose up --build`.

6. **Testing — 2 / 2 points**  
   * *Selection:* `Both unit and integration tests exist, run with a single command, and pass.`
   * *Evidence:* Rigorous testing suite covering backend unit tests, isolated PostgreSQL 16 integration tests (`docker-compose.test.yml`), Vitest frontend tests, agent extension unit tests, and `promtool` alert rule tests.

7. **Containerization — 2 / 2 points**  
   * *Selection:* `The full system, including the database, runs via Docker or Docker Compose and starts with a single command.`
   * *Evidence:* `docker-compose.yml` packages Nginx-served frontend, FastAPI backend, and PostgreSQL 16 Alpine with health checks and persistence volumes.

8. **Deployment — 1 / 2 points**  
   * *Selection:* `Deployment steps are described, but no working deployment is shown.`
   * *Evidence:* Extensive deployment documentation provided in `docs/deployment-render.md` and `render.yaml`. The author transparently notes that public Render deployment is on hold pending resolution of PostgreSQL SCRAM authentication, so no live public URL is currently reachable.

9. **CI/CD — 1 / 3 points**  
   * *Selection:* `CI runs the tests automatically on every pull request.`
   * *Evidence:* `.github/workflows/ci.yml` runs automated checks across 5 jobs on PRs and pushes to main. CD deployment (`deploy.yml`) is a separate manual workflow and is currently on hold.

10. **Observability — 2 / 2 points**  
    * *Selection:* `A key user journey is instrumented with metrics, traces, and structured logs that share a trace ID; no customer data or credentials are sent to telemetry; and the signals are collected, stored, and viewable in a UI.`
    * *Evidence:* Full local observability stack in `monitoring/docker-compose.yml` (OpenTelemetry Collector, Prometheus, Grafana, Loki, Tempo). Backend logs correlate with traces via `trace_id`, PII/resume content is excluded from telemetry, and dashboards are viewable in Grafana.

11. **Alerting on User Impact — 1 / 1 point**  
    * *Selection:* `At least one alert exists.`
    * *Evidence:* Four Prometheus alert rules defined in `monitoring/alerts/careerpilot.rules.yml` (`CareerPilotHigh5xxRate`, `CareerPilotHighAverageLatency`, `CareerPilotBackendTelemetryMissing`, `CareerPilotOtelCollectorDown`) with synthetic `promtool` tests passing in CI.

12. **On-Call Agent — 2 / 2 points**  
    * *Selection:* `An agent wakes up on an alert and fixes the issue.`
    * *Evidence:* Implemented `custom-agent/oncall_responder.py` which triggers on alert events, diagnoses user impact, executes remediation/repair of configuration, verifies recovery, and logs audit events (validated by 30 tests in `test_oncall_responder.py`).

### Review Comments for Peer Form
> **Feedback:** Extremely thorough, transparent, and well-architected project. The testing suite and observability stack (OTel, Prometheus, Tempo, Loki, Grafana) are designed with exceptional precision. The documentation integrity regarding the Render PostgreSQL issue is admirable. Once the Render connection is resolved, this project is poised for full 24/24 marks. Great job!

---

## 7. Submission Checklist for Course Management Portal

When submitting on [courses.datatalks.club](https://courses.datatalks.club/ai-dev-tools-2026/project/project1/eval/):

1. **Submission #14512 (`hub-platform`):**
   - [x] All 12 criteria selected to match **24 points** (select top option for every criterion).
   - [x] Paste the review comments from Section 4.
   - [x] Submit vote.

2. **Submission #14513 (`PromptHub_Enterprise`):**
   - [x] Select: Criteria 1, 3, 4, 5, 6, 7, 8 (2 pts each), Criterion 2 (1 pt), Criterion 9 (2 pts), Criteria 10, 11, 12 (0 pts) $\rightarrow$ **17 points**.
   - [x] Paste the review comments from Section 5.
   - [x] Submit vote.

3. **Submission #14514 (`CareerPilot`):**
   - [x] Select: Criteria 1, 2, 3, 4, 5, 6, 7, 10, 12 (2 pts each), Criteria 8, 9, 11 (1 pt each) $\rightarrow$ **21 points**.
   - [x] Paste the review comments from Section 6.
   - [x] Submit vote.
