# System Architecture & Telemetry Topology

This document describes the high-level architecture, network flows, and telemetry pipelines of the Order Tracker application.

---

## 🏗️ Architectural Topology

```mermaid
graph TD
    subgraph ClientLayer [Client Layer]
        Browser["Customer Browser / API Client"]
    end

    subgraph ContainerStack [Docker Compose Stack]
        FastAPI["Order Tracker Service (FastAPI)"]
        SQLite[("Persistent SQLite DB (/data/orders.db)")]
        OTel["OpenTelemetry Instrumentation"]
    end

    subgraph ObservabilityStack [Observability Pipeline]
        Prometheus["Prometheus (Metrics Scraper)"]
        AlertMgr["Alertmanager / Webhook Trigger"]
        Grafana["Grafana Dashboards"]
    end

    subgraph RemediationLayer [Automated Self-Healing]
        Responder["Autonomous On-Call Agent (Port 8001)"]
    end

    Browser -->|HTTP GET/POST/PATCH| FastAPI
    FastAPI <-->|SQLAlchemy/SQLite WAL| SQLite
    FastAPI -.->|Metrics & Traces| OTel
    OTel -->|Scraped by| Prometheus
    Prometheus -->|Visualize| Grafana
    Prometheus -->|5xx Error Rate > Threshold| AlertMgr
    AlertMgr -->|POST /alerts Webhook| Responder
    Responder -->|Diagnose & Remediate| FastAPI
```

---

## 💾 Data Persistence Seam
* **Engine:** SQLite with WAL mode.
* **Volume:** Named Docker volume `orders:/data`.
* **Health Check:** `GET /healthz` executes an active `SELECT 1` query to verify SQLite responsiveness before marking the container ready in Compose.

---

## 📡 Observability Architecture

### 1. Traces & Distributed Context
* Every incoming request receives a unique `X-Request-ID` and trace context.
* Traces correlate spans across database execution, business logic, and response formatting.

### 2. Metrics & Scraping
* Endpoint metrics tracked:
  - `http_requests_total{method, path, status}`
  - `http_request_duration_seconds{method, path}`
  - `orders_created_total{priority}`

### 3. Alert Routing
* **Rule:** `HighErrorRate5xx`
* **Condition:** Triggered when the 1-minute rate of 5xx responses exceeds 0.
* **Filter:** Excludes client 4xx errors (`GET /api/orders/missing` produces 404, preserving normal alert state).
* **Target:** Sends structured alert JSON to `http://localhost:8001/alerts`.
