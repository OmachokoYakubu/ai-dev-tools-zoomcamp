# Incident Response Runbook: 5xx Errors & Order Delivery Failures

* **Service:** Order Tracker (`order-tracker`)
* **Primary Alert:** `HighErrorRate5xx`
* **Severity:** Critical (User Impacting)
* **Automated Responder Endpoint:** `http://localhost:8001/alerts`

---

## 1. Trigger & Symptom Identification

### Alert Definition
```yaml
alert: HighErrorRate5xx
expr: rate(http_requests_total{status=~"5.."}[1m]) > 0
for: 30s
labels:
  severity: critical
  tier: user-impact
```

### Customer Impact
* Customers checking order details receive `500 Internal Server Error`.
* Order status page displays "Failed to load order details".

---

## 2. Autonomous Triage Procedure (On-Call Agent)

When Alertmanager dispatches a webhook to `POST /alerts`:

1. **Synthetic Test Check:**
   - If `labels.test == "true"`, the agent emits:
     > *"Received alert: ResponderTest (test=true). Summary: Test notification; no incident to fix. Verification successful. No action required."*
   - Return status 200 without escalating.

2. **Root Cause Analysis (Active 5xx Alert):**
   - Query logs for matching trace ID:
     ```text
     ValueError: day is out of range for month
     File "app/main.py", line 58, in order_detail
       estimated_at = placed_at.replace(day=placed_at.day + 2)
     ```
   - **Root Cause Identified:** Order `express-1002` created at month-end (`now.replace(day=1) - timedelta(days=1)`). Adding `+2` to the day index exceeds the days in month.

3. **Remediation Action:**
   - Swap integer day arithmetic with `timedelta(days=2)`:
     ```python
     # Correct:
     estimated_at = placed_at + timedelta(days=2)
     ```
   - Execute regression test suite:
     ```bash
     uv run pytest tests/test_api.py -k test_express_order_delivery_calculation
     ```
   - Verify health check: `GET /healthz` returns 200 OK.
