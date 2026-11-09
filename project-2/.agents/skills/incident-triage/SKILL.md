---
name: incident-triage
description: Diagnose user-impacting 5xx alerts using correlated trace IDs and execute bounded, verified runtime rollbacks without touching customer PII.
---

# Incident Triage & Autonomous Remediation Skill

## Workflow
1. Verify that the incoming alert represents real user impact (`5xx` error rate or `p95` latency breach, never `404`/`422` client lookups).
2. Query `/ops/diagnostics` to inspect redacted error logs, correlated `trace_id` values, and current `runtime_config`.
3. Execute only allowlisted remediation actions (`rollback_supplier_gateway`) via `/ops/remediate`.
4. Run a synthetic post-remediation probe against `/healthz` and `/api/restocks` to confirm HTTP `200` recovery before marking the incident resolved.
