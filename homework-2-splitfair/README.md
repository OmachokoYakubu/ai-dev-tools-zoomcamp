# SplitFair — AI-Assisted Full-Stack Expense Splitter

**Module 2 Project: Build and Ship an AI-Assisted Full-Stack App**  
*AI Dev Tools Zoomcamp 2026*

---

## 🎯 Overview
**SplitFair** is a full-stack group expense splitting application that tracks shared expenditures, calculates net balances, and generates optimal debt settlement plans for roommates, travel groups, and shared households.

Built using an AI-native end-to-end development cycle:
1. **Spec First**: `_docs/specs.md`
2. **Contract-Driven**: `openapi.yaml`
3. **Frontend Prototype**: `frontend/` (Modern interactive client with mock layer)
4. **FastAPI Backend**: `backend/` (Managed with `uv`, SQLite + SQLAlchemy ORM)
5. **Comprehensive Tests**: `backend/tests/` (100% passing tests via `pytest`)

---

## 🚀 Quickstart Guide

### 1. Start the Backend
```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```
API Documentation will be accessible at: `http://localhost:8000/docs`

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` (or the local Vite/dev URL) to interact with SplitFair.

### 3. Run Automated Tests
```bash
cd backend
uv run pytest
```
