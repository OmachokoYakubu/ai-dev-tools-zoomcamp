# AI Usage & Prompt Engineering Report — SplitFair

**Course:** AI Dev Tools Zoomcamp 2026 — Module 2 (Development)  
**Project:** SplitFair (Expense Splitter)  
**Author:** Omachoko Yakubu  

---

## 1. Executive Summary
This report documents the end-to-end AI-assisted workflow utilized to design, specify, prototype, build, and test **SplitFair**, a full-stack group expense splitting application.

---

## 2. Phase 1: Spec-First Ideation & Backlog
* **Tool Used**: Antigravity / Gemini 3.8 Coding Assistant
* **Prompt Strategy**:
  ```text
  I want to build an Expense Splitter application for shared households and trips.
  Help me set the scope precisely. Ask me questions one by one about key requirements,
  non-goals, and edge cases. Then compile everything into a structured product specification.
  ```
* **Outcome**:
  - Settled on 4 core features: Group management, expense splits, net balance calculation, and debt minimization settlement recommendations.
  - Defined strict non-goals (e.g. real banking integration, multi-currency live forex) to maintain a focused, achievable v1 delivery.

---

## 3. Phase 2: Contract-Driven Design (`openapi.yaml`)
* **Strategy**: Use OpenAPI 3.1 as the single source of truth before writing any application code.
* **Key Contracts Established**:
  - `GET /api/groups`, `POST /api/groups`
  - `GET /api/groups/{id}`, `POST /api/groups/{id}/members`
  - `GET /api/groups/{id}/expenses`, `POST /api/groups/{id}/expenses`
  - `GET /api/groups/{id}/balances` (Net balances + Greedy debt simplification)
  - `POST /api/groups/{id}/settle` (Debt settlement)

---

## 4. Phase 3: Frontend Prototype with Mock API
* **Strategy**:
  - Build an interactive, modern user interface in `frontend/` using Vanilla JavaScript, HTML5, and CSS.
  - Implement a mock store layer inside `app.js` that intercepts API calls when the backend is offline.
  - Enable instant interactive prototyping for UI reviews.

---

## 5. Phase 4: FastAPI Backend & SQLAlchemy Persistence
* **Tool**: Python with `uv` package manager.
* **Prompt Strategy**:
  ```text
  Based on openapi.yaml, create a FastAPI backend. Use uv for package management.
  Write tests for the key endpoints first, then implement them with SQLAlchemy models
  using SQLite for persistence.
  ```
* **Implementation Highlights**:
  - Greedy debt minimization matching algorithm (`calculate_balances`).
  - Strict Pydantic validation on request bodies.
  - 100% test coverage with in-memory SQLite isolation.

---

## 6. Key Takeaways & Lessons Learned
1. **Spec First Saves Hours**: Writing acceptance criteria and non-goals upfront prevented scope creep and eliminated refactoring loops.
2. **OpenAPI as the Anchor**: The contract allowed the frontend and backend to be developed and tested independently with zero integration surprises.
3. **uv Velocity**: Dependency resolution and test execution with `uv` was nearly instantaneous compared to legacy virtualenv managers.
