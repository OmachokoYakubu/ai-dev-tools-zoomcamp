# AGENTS.md — SplitFair Development Instructions

This file guides AI coding agents in maintaining and developing the SplitFair application.

## 📋 Architecture & Principles

1. **Contract-Driven Development**:
   - `openapi.yaml` at the root of `homework-2-splitfair/` is the single source of truth for all API requests and responses.
   - Any API change must first be reflected in `openapi.yaml`.

2. **Frontend Architecture**:
   - Located in `frontend/`.
   - Built with lightweight modern JavaScript, HTML5, and CSS.
   - Centralizes all API communication in an API client module with support for mock fallback.
   - Dev server started with: `npm run dev`.

3. **Backend Architecture**:
   - Located in `backend/`.
   - FastAPI framework managed via `uv`.
   - SQLAlchemy ORM with SQLite for database-agnostic persistence.
   - Dev server started with: `uv run uvicorn main:app --reload`.

4. **Testing Standards**:
   - All endpoints covered with unit and integration tests under `backend/tests/`.
   - Run tests with: `uv run pytest`.
   - 100% tests must pass before pushing code.
