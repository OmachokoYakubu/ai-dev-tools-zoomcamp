# ChoreFlow — Shared Household Chore Manager

**Module 1 Project: AI-Native Developer Workflow**  
*AI Dev Tools Zoomcamp 2026*

---

## 🎯 Overview
ChoreFlow is an AI-assisted Django web application designed to eliminate household friction by organizing, scheduling, and verifying shared chores among housemates.

Built according to the spec-driven AI-native workflow outlined in Module 1:
1. **Brainstormed Spec** (`_docs/plan.md`)
2. **Backlog Decomposition** (`_docs/backlog.md`)
3. **Agent-Guided Implementation** with Django & `uv`
4. **Automated Test Coverage**

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+
- `uv` (Fast Python package manager)

### 1. Run Migrations
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 2. Start the Development Server
```bash
uv run python manage.py runserver
```
Open your browser at `http://127.0.0.1:8000/` to view ChoreFlow.

### 3. Run Automated Tests
```bash
uv run python manage.py test
```

---

## 🧪 Verified Test Scenarios
- ✅ Housemate registration & unique email constraint
- ✅ Chore assignment, recurrence types, and initial pending status
- ✅ Web dashboard chore rendering
- ✅ Chore completion toggle and automatic audit logging
