"""Correlated OpenTelemetry traces, Prometheus metrics, structured JSON logs & PII redaction."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import json
import os
import re
import sys
from typing import Any

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

SENSITIVE_KEYS = {
    "supplier_email",
    "email",
    "phone",
    "supplier_phone",
    "contact",
    "password",
    "secret",
    "token",
    "api_key",
    "authorization",
    "cookie",
}
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
BEARER_PATTERN = re.compile(r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*")

HTTP_REQUESTS_TOTAL = Counter(
    "shelfsync_http_requests_total",
    "Total HTTP requests handled by ShelfSync",
    ["method", "route", "status_class", "status_code"],
)
HTTP_REQUEST_DURATION = Histogram(
    "shelfsync_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "route"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)
RESTOCK_JOURNEY_EVENTS = Counter(
    "shelfsync_restock_events_total",
    "Business events across the ShelfSync inventory and restock user journey",
    ["stage", "outcome"],
)
USER_IMPACT_5XX_TOTAL = Counter(
    "shelfsync_user_impact_5xx_total",
    "Count of user-impacting 5xx failures (excludes 4xx client validation errors)",
    ["route", "reason"],
)

IN_MEMORY_SPAN_EXPORTER = InMemorySpanExporter()
STRUCTURED_LOG_BUFFER: deque[dict[str, Any]] = deque(maxlen=200)
RECENT_5XX_TRACES: deque[dict[str, Any]] = deque(maxlen=50)

_TRACER_INITIALIZED = False


def configure_tracing() -> trace.Tracer:
    global _TRACER_INITIALIZED
    if not _TRACER_INITIALIZED:
        resource = Resource.create(
            {
                "service.name": os.getenv("OTEL_SERVICE_NAME", "shelfsync-app"),
                "service.version": "1.0.0",
                "deployment.environment": os.getenv("APP_ENV", "dev"),
            }
        )
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(SimpleSpanProcessor(IN_MEMORY_SPAN_EXPORTER))

        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()
        if otlp_endpoint:
            traces_url = (
                otlp_endpoint
                if otlp_endpoint.endswith("/v1/traces")
                else f"{otlp_endpoint.rstrip('/')}/v1/traces"
            )
            provider.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporter(endpoint=traces_url, timeout=3))
            )

        trace.set_tracer_provider(provider)
        _TRACER_INITIALIZED = True
    return trace.get_tracer("shelfsync.telemetry")


def redact_pii(value: Any) -> Any:
    """Recursively scrub credentials and customer/supplier PII before telemetry export."""
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for k, v in value.items():
            if str(k).lower() in SENSITIVE_KEYS:
                sanitized[k] = "[REDACTED]"
            else:
                sanitized[k] = redact_pii(v)
        return sanitized
    if isinstance(value, (list, tuple)):
        return [redact_pii(item) for item in value]
    if isinstance(value, str):
        scrubbed = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", value)
        scrubbed = BEARER_PATTERN.sub("Bearer [REDACTED]", scrubbed)
        return scrubbed
    return value


def current_trace_ids() -> tuple[str, str]:
    span = trace.get_current_span()
    ctx = span.get_span_context() if span else None
    if ctx and ctx.is_valid:
        return f"{ctx.trace_id:032x}", f"{ctx.span_id:016x}"
    return "0" * 32, "0" * 16


def emit_structured_log(
    event: str,
    level: str = "INFO",
    **fields: Any,
) -> dict[str, Any]:
    trace_id, span_id = current_trace_ids()
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": "shelfsync-app",
        "event": event,
        "trace_id": trace_id,
        "span_id": span_id,
        **redact_pii(fields),
    }
    STRUCTURED_LOG_BUFFER.append(record)
    if record.get("status_code", 200) >= 500 or level == "ERROR":
        RECENT_5XX_TRACES.append(record)
    sys.stdout.write(json.dumps(record) + "\n")
    sys.stdout.flush()
    return record


def render_prometheus_metrics() -> tuple[bytes, str]:
    return generate_latest(), CONTENT_TYPE_LATEST
