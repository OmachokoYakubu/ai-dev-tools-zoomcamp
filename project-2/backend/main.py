"""ShelfSync FastAPI backend implementing OpenAPI contract, telemetry & ops endpoints."""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
import time
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse
from opentelemetry.trace import Status, StatusCode
from pydantic import BaseModel, Field
from sqlalchemy import select, text
from sqlalchemy.orm import Session

import backend.database as db_module
from backend.models import (
    InventoryItem,
    RestockOrder,
    StockLedgerEvent,
    VALID_CATEGORIES,
    compute_stock_status,
    utc_now,
    validate_restock_transition,
)
from backend.telemetry import (
    HTTP_REQUEST_DURATION,
    HTTP_REQUESTS_TOTAL,
    RECENT_5XX_TRACES,
    RESTOCK_JOURNEY_EVENTS,
    USER_IMPACT_5XX_TOTAL,
    configure_tracing,
    current_trace_ids,
    emit_structured_log,
    redact_pii,
    render_prometheus_metrics,
)

tracer = configure_tracing()
FRONTEND_HTML_PATH = Path(__file__).resolve().parents[1] / "frontend" / "index.html"

RUNTIME_STATE: dict[str, Any] = {
    "supplier_gateway_mode": "healthy",
    "last_updated_by": "bootstrap",
    "last_updated_at": datetime.now(timezone.utc).isoformat(),
    "remediation_count": 0,
}

SEED_ITEMS = [
    ("VAC-FLU26", "Quadrivalent Influenza Vaccine (10-Dose Vial)", "cold_chain", 14, 20, 4.0, "coldchain@medisupply.example"),
    ("INS-GLAR10", "Insulin Glargine 100U/mL Pens", "cold_chain", 32, 15, 4.0, "biologics@medisupply.example"),
    ("PCR-KIT96", "Respiratory Multiplex PCR Assay Plate", "reagent", 6, 12, -20.0, "reagents@labcore.example"),
    ("STR-GLV100", "Sterile Nitrile Exam Gloves (Box/100)", "consumable", 48, 20, 22.0, "ops@clinicsource.example"),
    ("EPI-PEN02", "Epinephrine Auto-Injector 0.3mg Twin-Pack", "cold_chain", 0, 8, 20.0, "emergency@medisupply.example"),
]


def seed_if_empty(session: Session) -> None:
    existing = session.scalar(select(InventoryItem.id).limit(1))
    if existing is not None:
        return
    for sku, name, category, qty, threshold, temp_c, email in SEED_ITEMS:
        session.add(
            InventoryItem(
                sku=sku,
                name=name,
                category=category,
                quantity=qty,
                reorder_threshold=threshold,
                storage_temp_c=temp_c,
                supplier_email=email,
            )
        )
    session.add(
        RestockOrder(
            sku="VAC-FLU26",
            order_qty=30,
            requested_by="Dr. Maya Lin",
            status="approved",
            trace_id="seed-trace-0001",
        )
    )
    session.add(
        RestockOrder(
            sku="EPI-PEN02",
            order_qty=16,
            requested_by="Lead Pharm. Tunde",
            status="requested",
            trace_id="seed-trace-0002",
        )
    )
    session.commit()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db_module.Base.metadata.create_all(bind=db_module.engine)
    with db_module.SessionLocal() as session:
        seed_if_empty(session)
    yield


app = FastAPI(
    title="ShelfSync Inventory & Autonomous Operations API",
    version="1.0.0",
    lifespan=lifespan,
)


def _route_template(request: Request) -> str:
    route = request.scope.get("route")
    if route and getattr(route, "path", None):
        return str(route.path)
    return request.url.path


@app.middleware("http")
async def telemetry_middleware(request: Request, call_next):
    start = time.perf_counter()
    method = request.method
    raw_path = request.url.path

    with tracer.start_as_current_span(f"{method} {raw_path}") as span:
        trace_id, _ = current_trace_ids()
        span.set_attribute("http.method", method)
        span.set_attribute("http.target", raw_path)

        try:
            response: Response = await call_next(request)
            status_code = response.status_code
        except Exception as exc:
            duration = time.perf_counter() - start
            route_label = _route_template(request)
            span.record_exception(exc)
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            HTTP_REQUESTS_TOTAL.labels(method, route_label, "5xx", "500").inc()
            HTTP_REQUEST_DURATION.labels(method, route_label).observe(duration)
            USER_IMPACT_5XX_TOTAL.labels(route_label, "unhandled_exception").inc()
            emit_structured_log(
                "http_request_failed",
                level="ERROR",
                method=method,
                route=route_label,
                status_code=500,
                latency_ms=round(duration * 1000.0, 2),
                error=str(exc),
            )
            raise

        duration = time.perf_counter() - start
        route_label = _route_template(request)
        status_class = f"{status_code // 100}xx"
        span.set_attribute("http.route", route_label)
        span.set_attribute("http.status_code", status_code)
        if status_code >= 500:
            span.set_status(Status(StatusCode.ERROR, f"HTTP {status_code}"))

        if route_label != "/metrics":
            HTTP_REQUESTS_TOTAL.labels(
                method, route_label, status_class, str(status_code)
            ).inc()
            HTTP_REQUEST_DURATION.labels(method, route_label).observe(duration)
            emit_structured_log(
                "http_request",
                level="ERROR" if status_code >= 500 else "INFO",
                method=method,
                route=route_label,
                status_code=status_code,
                latency_ms=round(duration * 1000.0, 2),
            )

        response.headers["X-Trace-Id"] = trace_id
        return response


class ItemCreate(BaseModel):
    sku: str = Field(..., min_length=3, max_length=32, pattern=r"^[A-Z0-9\-]+$")
    name: str = Field(..., min_length=2, max_length=120)
    category: str = Field(..., description="cold_chain | reagent | consumable")
    quantity: int = Field(..., ge=0, le=100_000)
    reorder_threshold: int = Field(..., ge=1, le=10_000)
    storage_temp_c: float = Field(..., ge=-90.0, le=50.0)
    supplier_email: str = Field(..., min_length=5, max_length=160)


class DrawdownRequest(BaseModel):
    units: int = Field(..., ge=1, le=10_000)
    reason: str = Field(..., min_length=2, max_length=120)


class RestockCreate(BaseModel):
    sku: str = Field(..., min_length=3, max_length=32)
    order_qty: int = Field(..., ge=1, le=50_000)
    requested_by: str = Field(..., min_length=2, max_length=80)


class RestockTransition(BaseModel):
    target_status: str = Field(..., description="approved | fulfilled")


class RuntimeConfigUpdate(BaseModel):
    supplier_gateway_mode: str = Field(..., pattern=r"^(healthy|degraded_timeout)$")


class RemediationAction(BaseModel):
    action: str = Field(..., pattern=r"^rollback_supplier_gateway$")
    triggered_by: str = Field(..., min_length=2, max_length=80)
    reason: str = Field(..., min_length=3, max_length=240)


@app.get("/", response_class=HTMLResponse)
def serve_frontend() -> HTMLResponse:
    if FRONTEND_HTML_PATH.exists():
        return HTMLResponse(FRONTEND_HTML_PATH.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>ShelfSync</h1><p>Visit /docs</p>")


@app.get("/healthz")
def healthz(db: Session = Depends(db_module.get_db)) -> dict[str, Any]:
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "service": "shelfsync-app",
        "supplier_gateway_mode": RUNTIME_STATE["supplier_gateway_mode"],
    }


@app.get("/metrics")
def metrics() -> Response:
    payload, content_type = render_prometheus_metrics()
    return Response(content=payload, media_type=content_type)


@app.get("/api/summary")
def get_summary(db: Session = Depends(db_module.get_db)) -> dict[str, Any]:
    items = list(db.scalars(select(InventoryItem)).all())
    restocks = list(db.scalars(select(RestockOrder)).all())
    low_or_out = sum(
        1
        for i in items
        if compute_stock_status(i.quantity, i.reorder_threshold) != "healthy"
    )
    open_restocks = sum(1 for r in restocks if r.status != "fulfilled")
    return {
        "total_skus": len(items),
        "attention_needed_skus": low_or_out,
        "open_restock_orders": open_restocks,
        "fulfilled_restock_orders": len(restocks) - open_restocks,
        "supplier_gateway_mode": RUNTIME_STATE["supplier_gateway_mode"],
    }


@app.get("/api/items")
def list_items(
    category: str | None = Query(default=None),
    low_stock_only: bool = Query(default=False),
    db: Session = Depends(db_module.get_db),
) -> list[dict[str, Any]]:
    stmt = select(InventoryItem).order_by(InventoryItem.sku)
    if category:
        stmt = stmt.where(InventoryItem.category == category)
    items = [item.to_public_dict() for item in db.scalars(stmt).all()]
    if low_stock_only:
        items = [i for i in items if i["stock_status"] != "healthy"]
    return items


@app.post("/api/items", status_code=201)
def create_item(
    payload: ItemCreate, db: Session = Depends(db_module.get_db)
) -> dict[str, Any]:
    if payload.category not in VALID_CATEGORIES:
        raise HTTPException(status_code=422, detail=f"Category must be one of {VALID_CATEGORIES}")

    existing = db.scalar(select(InventoryItem).where(InventoryItem.sku == payload.sku))
    if existing is not None:
        RESTOCK_JOURNEY_EVENTS.labels("sku_create", "conflict_409").inc()
        raise HTTPException(status_code=409, detail=f"SKU {payload.sku} already exists")

    with tracer.start_as_current_span("journey.create_sku") as span:
        safe_attrs = redact_pii(payload.model_dump())
        span.set_attribute("shelfsync.sku", payload.sku)
        span.set_attribute("shelfsync.category", payload.category)

        item = InventoryItem(
            sku=payload.sku,
            name=payload.name,
            category=payload.category,
            quantity=payload.quantity,
            reorder_threshold=payload.reorder_threshold,
            storage_temp_c=payload.storage_temp_c,
            supplier_email=payload.supplier_email,
            updated_at=utc_now(),
        )
        trace_id, _ = current_trace_ids()
        db.add(item)
        db.add(
            StockLedgerEvent(
                sku=payload.sku,
                delta=payload.quantity,
                event_type="initial_seed",
                note="SKU registered",
                trace_id=trace_id,
            )
        )
        db.commit()
        db.refresh(item)
        RESTOCK_JOURNEY_EVENTS.labels("sku_create", "created").inc()
        emit_structured_log("sku_created", payload=safe_attrs)
        return item.to_public_dict()


@app.post("/api/items/{sku}/drawdown")
def drawdown_item(
    sku: str, payload: DrawdownRequest, db: Session = Depends(db_module.get_db)
) -> dict[str, Any]:
    item = db.scalar(select(InventoryItem).where(InventoryItem.sku == sku))
    if item is None:
        raise HTTPException(status_code=404, detail=f"SKU {sku} not found")
    if payload.units > item.quantity:
        RESTOCK_JOURNEY_EVENTS.labels("stock_drawdown", "insufficient_stock_422").inc()
        raise HTTPException(
            status_code=422,
            detail=f"Cannot draw down {payload.units} units; only {item.quantity} available",
        )

    with tracer.start_as_current_span("journey.stock_drawdown") as span:
        span.set_attribute("shelfsync.sku", sku)
        span.set_attribute("shelfsync.drawdown_units", payload.units)
        trace_id, _ = current_trace_ids()

        item.quantity -= payload.units
        item.updated_at = utc_now()
        db.add(
            StockLedgerEvent(
                sku=sku,
                delta=-payload.units,
                event_type="drawdown",
                note=payload.reason,
                trace_id=trace_id,
            )
        )
        db.commit()
        db.refresh(item)
        result = item.to_public_dict()
        RESTOCK_JOURNEY_EVENTS.labels("stock_drawdown", result["stock_status"]).inc()
        emit_structured_log(
            "stock_drawdown_recorded",
            sku=sku,
            units=payload.units,
            remaining=item.quantity,
            stock_status=result["stock_status"],
        )
        return result


@app.get("/api/restocks")
def list_restocks(db: Session = Depends(db_module.get_db)) -> list[dict[str, Any]]:
    stmt = select(RestockOrder).order_by(RestockOrder.id.desc())
    return [order.to_dict() for order in db.scalars(stmt).all()]


@app.post("/api/restocks", status_code=201)
def create_restock(
    payload: RestockCreate, db: Session = Depends(db_module.get_db)
) -> dict[str, Any]:
    item = db.scalar(select(InventoryItem).where(InventoryItem.sku == payload.sku))
    if item is None:
        raise HTTPException(status_code=404, detail=f"SKU {payload.sku} not found")

    with tracer.start_as_current_span("journey.create_restock_order") as span:
        span.set_attribute("shelfsync.sku", payload.sku)
        span.set_attribute("shelfsync.order_qty", payload.order_qty)
        trace_id, _ = current_trace_ids()

        if RUNTIME_STATE["supplier_gateway_mode"] == "degraded_timeout":
            span.set_status(Status(StatusCode.ERROR, "supplier_gateway_degraded_timeout"))
            USER_IMPACT_5XX_TOTAL.labels(
                "/api/restocks", "supplier_gateway_degraded_timeout"
            ).inc()
            RESTOCK_JOURNEY_EVENTS.labels("restock_create", "error_503").inc()
            emit_structured_log(
                "restock_gateway_failure",
                level="ERROR",
                status_code=503,
                sku=payload.sku,
                supplier_gateway_mode=RUNTIME_STATE["supplier_gateway_mode"],
                supplier_email=item.supplier_email,
            )
            raise HTTPException(
                status_code=503,
                detail="Upstream supplier dispatch gateway timed out (degraded_timeout mode)",
            )

        order = RestockOrder(
            sku=payload.sku,
            order_qty=payload.order_qty,
            requested_by=payload.requested_by,
            status="requested",
            trace_id=trace_id,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        RESTOCK_JOURNEY_EVENTS.labels("restock_create", "requested").inc()
        emit_structured_log(
            "restock_order_created",
            restock_id=order.id,
            sku=order.sku,
            order_qty=order.order_qty,
            supplier_email=item.supplier_email,
        )
        return order.to_dict()


@app.patch("/api/restocks/{restock_id}/transition")
def transition_restock(
    restock_id: int,
    payload: RestockTransition,
    db: Session = Depends(db_module.get_db),
) -> dict[str, Any]:
    order = db.get(RestockOrder, restock_id)
    if order is None:
        raise HTTPException(status_code=404, detail=f"Restock order {restock_id} not found")

    if not validate_restock_transition(order.status, payload.target_status):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid transition from '{order.status}' to '{payload.target_status}'",
        )

    with tracer.start_as_current_span("journey.transition_restock") as span:
        span.set_attribute("shelfsync.restock_id", restock_id)
        span.set_attribute("shelfsync.target_status", payload.target_status)
        trace_id, _ = current_trace_ids()

        order.status = payload.target_status
        order.updated_at = utc_now()
        item_dict: dict[str, Any] | None = None

        if payload.target_status == "fulfilled":
            item = db.scalar(select(InventoryItem).where(InventoryItem.sku == order.sku))
            if item is not None:
                item.quantity += order.order_qty
                item.updated_at = utc_now()
                db.add(
                    StockLedgerEvent(
                        sku=item.sku,
                        delta=order.order_qty,
                        event_type="restock_fulfilled",
                        note=f"Fulfilled restock #{order.id}",
                        trace_id=trace_id,
                    )
                )
                item_dict = item.to_public_dict()

        db.commit()
        db.refresh(order)
        RESTOCK_JOURNEY_EVENTS.labels("restock_transition", payload.target_status).inc()
        emit_structured_log(
            "restock_order_transitioned",
            restock_id=order.id,
            sku=order.sku,
            new_status=order.status,
        )
        return {
            "restock": order.to_dict(),
            "updated_item": item_dict,
        }


@app.get("/ops/diagnostics")
def ops_diagnostics(db: Session = Depends(db_module.get_db)) -> dict[str, Any]:
    db.execute(text("SELECT 1"))
    return {
        "service": "shelfsync-app",
        "database": "connected",
        "runtime_config": dict(RUNTIME_STATE),
        "recent_5xx_traces": list(RECENT_5XX_TRACES)[-10:],
    }


@app.put("/ops/runtime-config")
def update_runtime_config(payload: RuntimeConfigUpdate) -> dict[str, Any]:
    RUNTIME_STATE["supplier_gateway_mode"] = payload.supplier_gateway_mode
    RUNTIME_STATE["last_updated_by"] = "ops-config-api"
    RUNTIME_STATE["last_updated_at"] = datetime.now(timezone.utc).isoformat()
    emit_structured_log(
        "runtime_config_updated",
        supplier_gateway_mode=payload.supplier_gateway_mode,
    )
    return dict(RUNTIME_STATE)


@app.post("/ops/remediate")
def remediate_runtime(payload: RemediationAction) -> dict[str, Any]:
    previous_mode = RUNTIME_STATE["supplier_gateway_mode"]
    RUNTIME_STATE["supplier_gateway_mode"] = "healthy"
    RUNTIME_STATE["last_updated_by"] = payload.triggered_by
    RUNTIME_STATE["last_updated_at"] = datetime.now(timezone.utc).isoformat()
    RUNTIME_STATE["remediation_count"] = int(RUNTIME_STATE["remediation_count"]) + 1
    emit_structured_log(
        "autonomous_remediation_applied",
        action=payload.action,
        previous_mode=previous_mode,
        new_mode="healthy",
        triggered_by=payload.triggered_by,
        reason=payload.reason,
    )
    return {
        "status": "remediated",
        "previous_mode": previous_mode,
        "current_mode": RUNTIME_STATE["supplier_gateway_mode"],
        "remediation_count": RUNTIME_STATE["remediation_count"],
    }


@app.get("/ops/console", response_class=HTMLResponse)
def ops_console(db: Session = Depends(db_module.get_db)) -> HTMLResponse:
    db.execute(text("SELECT 1"))
    metrics_raw, _ = render_prometheus_metrics()
    metric_lines = [
        ln
        for ln in metrics_raw.decode("utf-8").splitlines()
        if ln and not ln.startswith("#") and ln.startswith("shelfsync_")
    ][:14]
    traces = list(RECENT_5XX_TRACES)[-6:]
    traces_rows = "".join(
        f"<tr><td><code>{t.get('trace_id','')}</code></td>"
        f"<td><code>{t.get('route','')}</code></td>"
        f"<td style='color:#f87171;font-weight:700;'>{t.get('status_code','')}</td>"
        f"<td>{t.get('reason','')}</td>"
        f"<td>{t.get('timestamp','')}</td></tr>"
        for t in traces
    ) or "<tr><td colspan='5' style='color:#94a3b8;'>No 5xx spans recorded yet</td></tr>"

    routes_rows = "".join(
        f"<tr><td><span style='color:#38bdf8;font-weight:700;'>{m}</span></td>"
        f"<td><code>{p}</code></td><td>{desc}</td></tr>"
        for m, p, desc in [
            ("GET", "/api/summary", "KPI inventory & restock counters + gateway health"),
            ("GET / POST", "/api/items", "List or register cold-chain & clinic SKUs (PostgreSQL)"),
            ("POST", "/api/items/{sku}/drawdown", "Atomic stock drawdown + ledger trace correlation"),
            ("GET / POST", "/api/restocks", "List or submit restock orders (traced customer journey)"),
            ("PATCH", "/api/restocks/{id}/transition", "State machine: requested -> approved -> fulfilled"),
            ("GET", "/metrics", "Prometheus SLO & user-impact 5xx vs 4xx telemetry"),
            ("GET / POST", "/ops/diagnostics & /ops/remediate", "Autonomous On-Call Responder triage & rollback"),
        ]
    )
    gw = RUNTIME_STATE["supplier_gateway_mode"]
    gw_color = "#34d399" if gw == "healthy" else "#f87171"
    metrics_block = "\n".join(metric_lines) or "shelfsync_http_requests_total 0"
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>ShelfSync SRE Telemetry & OpenAPI Console</title>
<style>
body {{ margin:0; padding:24px; background:#080f1e; color:#f1f5f9; font-family:Inter,-apple-system,sans-serif; }}
.wrap {{ max-width:1200px; margin:0 auto; }}
.grid {{ display:grid; grid-template-columns:1.1fr 0.9fr; gap:16px; margin-top:16px; }}
.card {{ background:#111a2e; border:1px solid #1e2d4a; border-radius:12px; padding:16px; margin-bottom:16px; }}
h1 {{ margin:0; font-size:1.4rem; }} h2 {{ margin:0 0 10px; font-size:0.98rem; color:#e2e8f0; }}
table {{ width:100%; border-collapse:collapse; font-size:0.81rem; }}
th, td {{ text-align:left; padding:8px 6px; border-bottom:1px solid rgba(30,45,74,0.7); }}
th {{ color:#94a3b8; font-size:0.73rem; text-transform:uppercase; }}
pre {{ margin:0; background:#09101f; border:1px solid #1e2d4a; border-radius:8px; padding:12px; color:#38bdf8; font-size:0.75rem; overflow-x:auto; line-height:1.45; }}
.badge {{ display:inline-block; padding:4px 10px; border-radius:999px; font-size:0.75rem; font-weight:700; border:1px solid #1e2d4a; background:#0f172a; margin-left:8px; }}
</style></head><body><div class="wrap">
<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1e2d4a;padding-bottom:14px;">
  <div>
    <h1>🛰️ ShelfSync — OpenTelemetry, Prometheus SLO &amp; OpenAPI Contract Console</h1>
    <p style="margin:4px 0 0;color:#94a3b8;font-size:0.85rem;">Correlated trace_id across Spans + Structured JSON Logs + Stock Ledger · Zero-PII Redaction Enforced</p>
  </div>
  <div>
    <span class="badge" style="color:{gw_color};">Gateway: {gw}</span>
    <span class="badge" style="color:#a78bfa;">Auto-Remediations: {RUNTIME_STATE['remediation_count']}</span>
    <span class="badge" style="color:#34d399;">Updated By: {RUNTIME_STATE['last_updated_by']}</span>
  </div>
</div>
<div class="grid">
  <div>
    <div class="card">
      <h2>Correlated 5xx OpenTelemetry Incident Spans (/ops/diagnostics)</h2>
      <table><thead><tr><th>trace_id</th><th>Route</th><th>HTTP</th><th>Fault / Span Reason</th><th>Timestamp (UTC)</th></tr></thead>
      <tbody>{traces_rows}</tbody></table>
    </div>
    <div class="card">
      <h2>OpenAPI 3.1 Contract Surface (openapi.yaml)</h2>
      <table><thead><tr><th>Method</th><th>Endpoint</th><th>Contract Responsibility</th></tr></thead>
      <tbody>{routes_rows}</tbody></table>
    </div>
  </div>
  <div>
    <div class="card">
      <h2>Live Prometheus Telemetry Snapshot (/metrics)</h2>
      <pre>{metrics_block}</pre>
    </div>
    <div class="card">
      <h2>Autonomous On-Call Self-Healing Loop</h2>
      <p style="margin:0;color:#cbd5e1;font-size:0.83rem;line-height:1.55;">
        1. <strong>Alert Rule</strong>: <code>ShelfSyncRestockJourneyHigh5xxRate</code> fires only on sustained <code>5xx</code> user-impact errors (ignoring <code>4xx</code> client validation noise).<br/>
        2. <strong>Wake-Up &amp; Triage</strong>: Alertmanager webhooks <code>POST http://oncall-agent:8081/alerts</code>; agent inspects <code>/ops/diagnostics</code>.<br/>
        3. <strong>Safe Rollback &amp; Probe</strong>: Agent invokes <code>POST /ops/remediate</code> and verifies recovery with a live <code>201 Created</code> synthetic restock probe.
      </p>
    </div>
  </div>
</div>
</div></body></html>"""
    return HTMLResponse(html)
