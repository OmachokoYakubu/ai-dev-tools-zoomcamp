# 📘 AI Dev Tools Zoomcamp 2026: Master Course Playbook

Welcome to the **AI Dev Tools Zoomcamp 2026** master playbook. This living document tracks all course resources, weekly modules, workshop streams, technical architectures, homework instructions, and delivery milestones.

---

## 📌 Course Directory & Official Portals

* **Course Platform**: [courses.datatalks.club/ai-dev-tools-2026/](https://courses.datatalks.club/ai-dev-tools-2026/)
* **Course FAQ**: [datatalks.club/faq/ai-dev-tools-zoomcamp.html](https://datatalks.club/faq/ai-dev-tools-zoomcamp.html)
* **Official Syllabus Repo**: [github.com/DataTalksClub/ai-dev-tools-zoomcamp](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp)
* **Student Repository**: [github.com/OmachokoYakubu/ai-dev-tools-zoomcamp](https://github.com/OmachokoYakubu/ai-dev-tools-zoomcamp)
* **Telegram Announcements**: [t.me/aidevtoolszoomcamp](https://t.me/aidevtoolszoomcamp)
* **Community Slack**: [DataTalks.Club Slack](https://datatalks-club.slack.com/) (Channel: `#course-ai-dev-tools-zoomcamp`)

---

## 📅 Cohort 2026 Master Timeline

| Module | Title | Dates / Deadline | Status | Deliverables |
| :--- | :--- | :--- | :--- | :--- |
| **Kickoff** | Official Course Launch | **2026-08-31** | Completed | Setup environments & tools |
| **Module 1** | **AI-Native Developer Workflow** | **Due: 2026-09-07** | Completed | `homework-1-choreflow` (Django + `uv`) |
| **Module 2** | **Build & Ship an AI-Assisted Full-Stack App** | **Due: 2026-09-14** | Completed | `homework-2-splitfair` (FastAPI + SQLite + Frontend) |
| **Module 3** | **Test, Containerize, and Deploy** | **Due: 2026-09-21** | **COMPLETED** | `homework-3-agent-relay` (FastAPI + Docker + K8s + PostgreSQL) |
| **Module 4** | **DevOps & Observability for AI-Built Apps** | **Due: 2026-09-28** | Upcoming | Prometheus, Grafana, OpenTelemetry, Tracing |

---

## 🎥 Workshops, Video Recordings & Long-Form Articles

### 1. Module 1: AI-Native Workflow
* **Stream Recording**: [AI-Native Developer Workflow (YouTube)](https://www.youtube.com/watch?v=VUJxJGpaDEs)
* **In-Depth Article**: [AI-Native Development: Specifications, Loop and Graph Engineering](https://aishippingblog.com/p/ai-native-development-specifications)
* **Reference Repositories**:
  * [weekly-feedback (Unspecified CLI)](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/tree/main/cohorts/2026/01-ai-native-workflow/weekly-feedback)
  * [retroloop (Specified Django Retrospective App)](https://github.com/alexeygrigorev/retroloop)

### 2. Module 2: Full-Stack Application Development
* **Stream Recording**: [Build & Ship an AI-Assisted Full-Stack App (YouTube)](https://www.youtube.com/watch?v=x9dq5nBpDg8)
* **In-Depth Article**: [Build and Ship a Full-Stack App with AI Coding Assistants](https://alexeyondata.substack.com/p/build-and-ship-a-full-stack-app-with)
* **Reference Repository**: [interview-canvas-share (FastAPI + SQLite + WebSocket)](https://github.com/alexeygrigorev/interview-canvas-share)

### 3. Module 3: Deployment & Delivery
* **Stream Recording**: [Deploying Full-Stack Application with AI (YouTube)](https://www.youtube.com/watch?v=gxt5ZDVnBMM)
* **In-Depth Article**: [Deploy a Full-Stack App with AI Coding](https://alexeyondata.substack.com/p/deploy-a-full-stack-app-with-ai-coding)

### 4. Module 4: DevOps & Observability
* **Stream Recording**: [DevOps and Observability for AI-Built Apps (YouTube)](https://www.youtube.com/watch?v=YkxLo_FRoQw)
* **In-Depth Article**: [DevOps and Observability for an AI-Built App](https://alexeyondata.substack.com/p/devops-and-observability-for-an-ai)

---

## 🛠️ Recommended Tech Stack & Tooling Standards

* **Package Management**: Use Python `uv` for lightning-fast, reproducible dependency management and execution (`uv run ...`).
* **Coding Agents**: Antigravity, Claude Code, Cursor, Codex, OpenCode.
* **Backend Frameworks**: FastAPI (Module 2) and Django (Module 1).
* **Databases**: SQLite (local development) via SQLAlchemy ORM (database-agnostic for PostgreSQL migration).
* **Frontend**: Vanilla HTML5/CSS3/JavaScript or lightweight modern Vite.
* **Testing**: `pytest` for FastAPI, Django Test Runner (`manage.py test`), and Playwright for browser validation.

---

## 📂 Repository Layout

```
ai-dev-tools-zoomcamp/
├── PLAYBOOK.md                      # This master reference guide
├── README.md                        # Primary project navigation
├── AGENTS.md                        # AI coding assistant guidelines
├── .gitignore                       # Universal repository exclusions
├── homework-1-choreflow/            # Module 1 Homework Project
│   ├── _docs/
│   │   ├── plan.md                  # Brainstormed 3-feature specification
│   │   └── backlog.md               # Sequenced task backlog
│   ├── choreflow_project/           # Django project configuration (settings.py, urls.py)
│   ├── chores/                      # Django app (models, views, templates, tests)
│   ├── manage.py                    # Django management script
│   └── README.md                    # Setup and run instructions
└── homework-2-splitfair/            # Module 2 Homework Project
    ├── _docs/
    │   └── specs.md                 # Product specification (user stories, AC, schema)
    ├── openapi.yaml                 # OpenAPI 3.1 Contract (Source of Truth)
    ├── frontend/                    # Interactive web UI (Vite / Vanilla JS + CSS)
    │   ├── index.html
    │   ├── app.js
    │   ├── style.css
    │   └── package.json
    ├── backend/                     # FastAPI backend (uv managed)
    │   ├── main.py                  # API routes and WebSocket handlers
    │   ├── models.py                # SQLAlchemy DB models
    │   ├── schemas.py               # Pydantic validation schemas
    │   ├── database.py              # SQLite / SQLAlchemy connection
    │   ├── pyproject.toml           # uv project configuration
    │   └── tests/                   # Automated pytest suite
    └── docs/
        └── ai-usage-report.md       # AI agent prompting and iteration report
├── homework-3-agent-relay/          # Module 3 Homework Project
│   ├── Dockerfile                   # Multi-stage container build (uv, uvicorn)
│   ├── compose.yaml                 # Multi-container stack (Agent Relay + PostgreSQL)
│   ├── k8s/                         # Kubernetes manifests (Deployments, Services, PVC)
│   │   ├── postgres-pvc.yaml
│   │   ├── postgres-deployment.yaml
│   │   ├── postgres-service.yaml
│   │   ├── relay-deployment.yaml
│   │   ├── relay-service.yaml
│   │   └── kustomization.yaml
│   ├── tests/
│   │   └── test_integration.py      # End-to-end task exchange lifecycle test
│   ├── main.py                      # FastAPI application and CLI worker
│   ├── database.py                  # SQLAlchemy models (SQLite & PostgreSQL compatible)
│   ├── storage.py                   # Atomic claim and task lifecycle persistence
│   └── README.md                    # Setup, Docker, Compose, and K8s guides
└── .github/workflows/
    └── ci.yml                       # Gated test execution & container/manifest verification
```

---

## 📣 Learning in Public Checklist

DataTalks.Club strongly encourages learning in public to build visibility, accountability, and network connections.

### Demonstration Video Checklist (30–90 seconds)
1. Showcase the primary user flow (e.g. creating an expense, splitting it, viewing balance summaries).
2. Demonstrate real-time or multi-session persistence (e.g. refreshing the browser or opening in two windows).
3. Conclude by highlighting the automated test passing output in the terminal.

### Social Media Template (LinkedIn / X)
```text
🚀 Building full-stack software with AI in @DataTalksClub AI Dev Tools Zoomcamp!

From spec-driven design to a working full-stack application:
✅ Spec first with acceptance criteria
✅ OpenAPI contract as the single source of truth
✅ FastAPI backend managed via uv
✅ SQLite persistence via SQLAlchemy
✅ Automated test suite with 100% green tests

Check out the code: https://github.com/OmachokoYakubu/ai-dev-tools-zoomcamp
#AIDevTools #FastAPI #Python #DataTalksClub #LearningInPublic
```

---

## 📝 Homework 3: Agent Relay Deliverables & Submission Reference

* **Course Portal Form:** [AI Dev Tools Zoomcamp Homework 3](https://courses.datatalks.club/ai-dev-tools-2026/homework/hw3)
* **Status:** Verified & Complete

| # | Question | Solution / Answer | Form Option |
| :--- | :--- | :--- | :--- |
| **Q1** | **How does the Agent Relay work?** | Agents claim tasks from a DB through an HTTP API | **Option 2** |
| **Q2** | **Full Task Lifecycle Status** | `completed` | **Option 3** |
| **Q3** | **Port Mapping in `docker run`** | `-p` | **Option 2** |
| **Q4** | **Database Hostname in `compose.yaml`** | `postgres` | **Option 2** |
| **Q5** | **Kubernetes Resource Type** | `Deployment` | **Option 3** |
| **Q6** | **CI/CD Behavior on Test Failure** | Keep the existing version running and stop the deployment | **Option 2** |

