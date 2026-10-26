# Agent Team Specification

This project utilizes a multi-agent autonomous engineering workflow. Each agent operates with defined responsibilities, constrained tool access, and structured communication protocols.

---

## 👥 Agent Roster & Roles

```
┌────────────────────────────────────────────────────────┐
│                    Human Operator                      │
└───────────────────────────┬────────────────────────────┘
                            │ (Requirements & Feedback)
┌───────────────────────────▼────────────────────────────┐
│               Lead Architect Agent                     │
│         - System design & modular documentation        │
│         - Context engineering & AGENTS.md curation     │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
    ┌─────────▼─────────┐        ┌─────────▼─────────┐
    │  Backend Agent    │        │    DevOps/SRE     │
    │  - FastAPI routes │        │  - Docker/Compose │
    │  - SQLite queries │        │  - Telemetry      │
    │  - Business logic │        │  - Alertmanager   │
    └─────────┬─────────┘        └─────────┬─────────┘
              │                            │
              └──────────────┬─────────────┘
                             │
                  ┌──────────▼──────────┐
                  │      QA Agent       │
                  │  - Pytest suites    │
                  │  - Regressions      │
                  │  - Integration test │
                  └──────────┬──────────┘
                             │
                  ┌──────────▼──────────┐
                  │    On-Call Agent    │
                  │  - Webhook listener │
                  │  - Automated triage │
                  │  - Incident runbook │
                  └─────────────────────┘
```

---

## 🛠️ Detailed Role Definitions

### 1. Lead Architect Agent
* **Primary Scope:** Product framing, context engineering, architecture oversight.
* **Responsibilities:**
  - Converts user stories into technical specifications (`_docs/specs.md`).
  - Maintains `AGENTS.md` and repository guidelines.
  - Ensures clean separation of concerns between business logic, data models, and observability layers.

### 2. Backend Engineering Agent
* **Primary Scope:** Application logic and API implementation.
* **Responsibilities:**
  - Implements FastAPI routes, dependency injection, and Pydantic validation.
  - Manages SQLite schema migrations and connection lifecycles.
  - Implements bug fixes and performance optimizations.

### 3. DevOps & SRE Agent
* **Primary Scope:** Infrastructure, containerization, and observability.
* **Responsibilities:**
  - Maintains multi-stage `Dockerfile` and `compose.yaml`.
  - Configures OpenTelemetry, Prometheus scrapers, and Alertmanager rules.
  - Configures CI/CD workflows for automated build and test pipelines.

### 4. QA & Test Automation Agent
* **Primary Scope:** Verification, regression testing, and quality gates.
* **Responsibilities:**
  - Authors unit and integration tests using `pytest` and `fastapi.testclient`.
  - Implements regression assertions for reported edge cases (e.g. date boundary rollovers).
  - Ensures 100% test pass rate before pull requests are merged.

### 5. Autonomous On-Call Incident Responder Agent
* **Primary Scope:** Continuous operational monitoring and automated self-healing.
* **Responsibilities:**
  - Runs as an active daemon listening to Grafana / Alertmanager webhooks.
  - Parses alert context: identifies offending endpoint, timestamp, error frequency, and trace ID.
  - Queries local database or application state to confirm incident legitimacy.
  - Executes predefined runbook remediation steps.

---

## 🔄 Inter-Agent Workflow & Communication Protocol

1. **Handoff from Architect to Backend & DevOps:**
   - Architect creates specification and tasks in `_docs/backlog.md`.
   - Backend and DevOps agents review acceptance criteria and build in parallel.
2. **Handoff from Backend to QA:**
   - Once code is staged, QA agent runs test suite, checks for uncovered branches, and adds regression cases.
3. **Continuous Handshake between SRE and On-Call Agent:**
   - SRE sets operational thresholds in `telemetry/alerts.yml`.
   - When an anomaly crosses the threshold, Alertmanager notifies the On-Call Agent via HTTP webhook.
   - On-Call Agent investigates logs, verifies pipeline integrity, and logs diagnostic findings.
