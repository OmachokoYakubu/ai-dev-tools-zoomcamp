# AGENTS.md

Welcome to the AI Dev Tools Zoomcamp 2026 repository. This file serves as operating instructions and guidelines for AI coding agents (Claude Code, Antigravity, Cursor, Codex, OpenCode, etc.) working on this repository.

## 🎯 Repository Principles

1. **Spec-First Development**:
   - Never write code before writing or validating a specification.
   - Specifications live in `_docs/` or `docs/` and outline user stories, acceptance criteria, error conditions, and non-goals.

2. **Durable Contracts**:
   - In full-stack applications, the OpenAPI specification (`openapi.yaml`) is the single source of truth between frontend and backend.
   - Backend endpoints and schemas must strictly adhere to the OpenAPI contract.

3. **Test-Driven Delivery**:
   - Write tests for key endpoints and models before or alongside implementation.
   - All tests must pass before declaring a task complete.
   - Use `uv` for managing Python dependencies and running test runners:
     - Django: `uv run python manage.py test`
     - FastAPI: `uv run pytest`

4. **Package Management & Tooling**:
   - Python: use `uv` exclusively. Avoid raw `pip install` without lockfile updates.
   - Frontend: Node.js (npm / vite) with vanilla CSS or cleanly scoped styling.

5. **Commit Discipline**:
   - Commit logical units of work with clear, descriptive commit messages.
   - Spec changes, prototypes, backends, and tests should be committed in structured phases.
