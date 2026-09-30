# Order Tracker

A small order tracking app for the AI Dev Tools Zoomcamp observability homework. It includes a web page, API, tests, and a Docker Compose setup. You add telemetry, alerts, and an incident responder in Homework 4.

The main user flow is creating an order and checking its status. Three sample orders are created on first startup.

## Run it

You need Docker with Compose. To run the tests, you also need Python 3.11+ and `uv`.

```bash
docker compose up --build -d --wait
```

Open <http://127.0.0.1:8000>. The API is at `/api/orders`, and the health check is at `/healthz`. Data is stored in a Docker volume and survives container recreation.

If port 8000 is occupied, set `ORDER_TRACKER_PORT`, for example:

```bash
ORDER_TRACKER_PORT=18080 docker compose up --build -d --wait
```

Run tests with `uv run --frozen pytest -q`. Stop the app with `docker compose down`. Add `-v` only if you also want to delete the order data.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Web page |
| GET | `/healthz` | Database health check |
| GET | `/api/orders` | List orders |
| POST | `/api/orders` | Create an order |
| GET | `/api/orders/{id}` | Check an order |
| PATCH | `/api/orders/{id}` | Change an order status |

The app uses SQLite to keep setup small. Run one app container at a time. The course exercise is about detecting and handling an incident, not scaling the database.

---

## Homework 4: DevOps, Observability & Incident Response

### 1. Telemetry Pipeline
- **Signals:** Metrics, Logs, and Traces instrumented via OpenTelemetry.
- **Components:** OpenTelemetry Collector, Prometheus (metrics), Loki (logs), Tempo (traces), and Grafana (unified dashboards & alerts).
- **Health Check (`GET /healthz`):** Verifies SQLite connectivity (`SELECT 1`) and returns `{"status": "ok"}`.
- **Endpoints & Status Tracking:**
  - `GET /api/orders/standard-1001`: Returns `200 OK`.
  - `GET /api/orders/standard-1002`: Returns `404 Not Found` (non-existent seeded order).
  - Grafana 5xx alert remains in `Normal` state because 404 is a client error, not a 5xx server failure.

### 2. Incident Responder (`incident-response/`)
- Listens for webhook alerts from Grafana at `POST http://localhost:8001/alerts`.
- Gathers bounded incident context (route, timestamp, request ID, error logs, and traces).
- Handles synthetic test alerts (`alertname: ResponderTest`, `test: true`) cleanly by confirming pipeline health:
  > *"Received alert: ResponderTest (test=true). Summary: Test notification; no incident to fix. Verification successful. No action required."*

### 3. Incident Investigation & Root Cause Fix
- **Symptom:** Lookups for `GET /api/orders/express-1002` failed with HTTP `500 Internal Server Error`, triggering the 5xx Grafana alert.
- **Root Cause:** In `app/main.py`, `order_detail()` calculated express estimated delivery dates using:
  ```python
  # Faulty:
  estimated_at = placed_at.replace(day=placed_at.day + 2)
  ```
  Because `express-1002` was created on the last day of the previous month (`previous_month_end`), adding 2 exceeded the maximum days in that month, raising `ValueError: day is out of range for month`.
- **Resolution:** Replaced the day substitution with datetime arithmetic using `timedelta`:
  ```python
  # Fixed:
  estimated_at = placed_at + timedelta(days=2)
  ```
- **Verification:** Added `test_express_order_delivery_calculation` in `tests/test_api.py`, which validates that express orders across month boundaries return HTTP 200 with valid `estimated_delivery`. All tests pass cleanly.

