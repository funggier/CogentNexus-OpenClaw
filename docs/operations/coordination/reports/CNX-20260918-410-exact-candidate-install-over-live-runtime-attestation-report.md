# CNX-20260918-410 — Exact Candidate Install-Over and Live Runtime Attestation

## Final classification

`BLOCKED_DELIVERY_HAZARD`

The authorized install-over and attestation RPC were not started. The fresh read-only preflight found an active maintenance/restart recovery marker, so the required delivery/recovery hazard gate was not satisfied.

## Authority and source binding

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Fresh remote branch HEAD before publication: `42f01b863e7340c24d35806564b2d19a12adea3c`
- Exact qualified candidate: `3d27ee85ff84ff2bf80d537e9046fb25e7a260ff`
- Candidate checkout: fresh disposable detached checkout at the exact candidate SHA; clean before observation
- Candidate is an ancestor of the coordination HEAD
- Candidate-to-HEAD drift was documentation only: ACTIVE, STATUS, CNX-409 review, and CNX-410 task files
- `scripts/install.ps1` was resolved from the exact detached candidate checkout
- No mutable working tree was used as an install source

## Fresh preflight evidence

Observed read-only through the installed OpenClaw/CogentNexus control surfaces:

- OpenClaw CLI/Gateway version: `2026.7.1-2`
- Gateway: healthy/reachable, Scheduled Task registered, PID `24336`, port `18789`, runtime state `Ready`
- Controller: `cnxMode=active`, derived `mode=managed`, desired Gateway `running`, generation `105`
- Supervisor: installed and Ready; last supervisor snapshot reported healthy
- Installed plugin inventory: `cogentnexus-openclaw`, version `0.9.5`, enabled, source under `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Delivery: pending outbox `0`
- Ticket store: read-only integrity check `ok`
- Provider/model state was observed only for invariance; no provider/model selection or credential change was made

The supported recovery check returned:

```json
{
  "check": "recovery",
  "verdict": "READY_WITH_WARNINGS",
  "exitCode": 1,
  "readOnly": true,
  "stateChanged": false,
  "checks": [
    {
      "name": "Maintenance/recovery fence",
      "status": "WARN",
      "summary": "Intentional maintenance/restart marker is present",
      "details": {
        "marker": {
          "active": true,
          "reason": "CogentNexus-OpenClaw external supervisor confirmed an unresponsive Gateway",
          "owner": "operator",
          "recoveryPolicy": "healthy-runtime"
        }
      }
    },
    {
      "name": "Supervisor health snapshot",
      "status": "PASS",
      "summary": "Last supervisor status: healthy"
    },
    {
      "name": "Provider recovery incident",
      "status": "PASS",
      "details": {"incidentOpen": false}
    }
  ],
  "stateChanged": false
}
```

This active maintenance/restart marker is an unresolved recovery hazard for the task's required pre-install gate. The marker was not cleared, repaired, or otherwise mutated. No manual Ticket, outbox, recovery, or SQLite operation was performed.

## Install and RPC ledger

| Operation | Result | Count |
|---|---|---:|
| `scripts/install.ps1` invocation | Not started because Phase C failed | 0 |
| Installer retry after start | Not applicable | 0 |
| Manual Gateway restart/repair | Not performed | 0 |
| `openclaw gateway call cogentnexus.runtimeAttestation --params '{}' --json` | Not called because Gateway attestation is authorized only after the hazard gate and installer-owned convergence | 0 |
| Web Chat semantic submissions | Not performed | 0 |
| Ollama semantic/model requests | Not performed | 0 |
| OpenAI semantic/model requests | Not performed | 0 |
| Provider/model selection changes | 0 |
| Provider credential/auth changes | 0 |
| Manual durable delivery/replay | 0 |
| Manual plugin copy/replace | 0 |
| OpenClaw dependency patch/version change | 0 |
| Release/tag/main changes | 0 |
| Force push/history rewrite | 0 |
| CNX-411 created/started | 0 |

## Required candidate identity and live attestation

Not applicable because the task stopped at the authorized delivery/recovery hazard gate. No candidate build/install was performed, no installed candidate identity was asserted, and no live classification (`PRESENT`, `ABSENT`, `AMBIGUOUS`, or `RUNNER_UNAVAILABLE`) was produced.

## Closeout

This report is the only new report published for CNX-410. ACTIVE.md and STATUS.md were changed from `READY_FOR_HERMES` to `WAITING_FOR_CHATGPT_REVIEW`. No product files, installer files, plugin files, provider configuration, or durable runtime state were changed by this task.

## Final classification

`BLOCKED_DELIVERY_HAZARD`
