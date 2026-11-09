.PHONY: install run run-responder test compose-up compose-down

install:
	uv sync --locked

run:
	uv run uvicorn backend.main:app --host 0.0.0.0 --port 8080

run-responder:
	SHELFSYNC_APP_URL=http://127.0.0.1:8080 uv run uvicorn oncall_agent.responder:responder_app --host 0.0.0.0 --port 8081

test:
	uv run pytest -v

compose-up:
	docker compose up --build -d

compose-down:
	docker compose down -v
