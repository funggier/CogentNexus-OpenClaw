# CNX-342 — Installation Provenance Requalification Report

- **Task:** CNX-342
- **Verdict:** `PASS — pending independent ChatGPT review`
- **Execution boundary:** installation and one Gateway load-boundary restart only; no semantic test
- **Report timestamp:** 2026-09-14T09:54:42Z

## Authority and source

- Source branch: `agent/v0.9.6-direct-model-call-timeout-authority-repair`
- Exact repair commit: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
- Remote source ref verified before build: `460a8cd661d02ba419cc1eff13c0efc721cfa928`
- Source checkout: `C:/Users/CDQ-P/cnx342-source` (detached, clean)
- Source branch was not modified.

## Build and validation

Built from the exact repair commit without source or test edits.

| Check | Result |
|---|---|
| `npm ci` | PASS; 352 packages installed; npm reported 8 audit vulnerabilities, not acted on |
| `npm run plugin:build` | PASS |
| `npm run plugin:validate` | PASS |
| `npm test` | PASS — 76 test files, 367 tests |
| npm package dry-run | PASS — 246 package files; required entry, metadata, README and bootstrap files present |

Built artifact SHA-256:

- `dist/v091-release-entry.js`: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- `dist/v091-direct-model-call-lease.js`: `5380b34e477979fdb3ad9154728eba0a86a3fafca089e1b997df7dba4dc893ab`

The rebuilt lease module contains both required repaired-boundary checks:

- `runtimeModelCallTimeoutMs(api, event, ctx)`
- `timeoutMs: runtimeModelCallTimeoutMs(api, event, ctx)`

The hardcoded `DIRECT_MODEL_CALL_TIMEOUT_MS` symbol remains only as the documented backward-compatible fallback inside the resolver path; the compiled module does not use a legacy-only direct fallback at the event call site.

## Pre-install evidence

- Active plugin path: `C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw`
- Gateway PID before restart: `3172`
- Entry SHA-256 before install: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Lease SHA-256 before install: `943a6d0d71cf71e32d6d1a79722d6e25200d0419ebc5b15e4c144e654cfaa480`
- Package metadata was captured (`package.json`, `openclaw.plugin.json`).
- Related installed lease paths were enumerated.

Pre-install evidence file: `C:/Users/CDQ-P/cnx342-evidence/pre-install.json`.

## Installation and provenance

A rollback copy was created before replacement:

- `C:/Users/CDQ-P/cnx342-evidence/rollback-installed-plugin`
- Copy was created before the installation replacement step and exists as retained evidence.

The complete build artifact package was generated from the same build and its `dist`, scripts, README, and package metadata were installed. The installed active imported path is the installed `dist` tree.

Before restart, installed-versus-built verification passed:

- Installed entry SHA-256 = rebuilt entry SHA-256 = `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Installed lease SHA-256 = rebuilt lease SHA-256 = `5380b34e477979fdb3ad9154728eba0a86a3fafca089e1b997df7dba4dc893ab`
- Installed lease contains `runtimeModelCallTimeoutMs` resolver: `true`
- Active imported lease file is `dist/v091-direct-model-call-lease.js`; its hash is the repaired build hash.
- No legacy lease implementation remains at the active imported `dist` path.

Installation evidence: `C:/Users/CDQ-P/cnx342-evidence/post-install-pre-restart.json`.

Note: historical non-imported source/test residue under the installation root was observable during preflight. It is not in the OpenClaw imported path; the active imported `dist` tree was mirrored from the complete rebuilt `dist` artifact and independently hash-verified.

## Installation manifest

Manifest: `C:/Users/CDQ-P/cnx342-evidence/installation-manifest.json`

It binds:

- repair commit `460a8cd661d02ba419cc1eff13c0efc721cfa928`
- entry SHA-256 `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- lease SHA-256 `5380b34e477979fdb3ad9154728eba0a86a3fafca089e1b997df7dba4dc893ab`
- installation timestamp `2026-09-14T09:52:02.759023+00:00`
- rollback copy path

## Gateway load-boundary refresh

Exactly one restart action was issued:

```text
openclaw gateway restart
```

Result: `Restarted Scheduled Task: OpenClaw Gateway`

- Old Gateway PID: `3172`
- New Gateway PID: `17080`
- Restart timestamp: approximately `2026-09-14T09:53:06Z`
- Post-restart entry SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Post-restart lease SHA-256: `5380b34e477979fdb3ad9154728eba0a86a3fafca089e1b997df7dba4dc893ab`
- Post-restart resolver check: `true`

Load/startup evidence in the Gateway log includes:

- `loading configuration…`
- `starting...`
- plugin discovery of `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- `CogentNexus-OpenClaw delivery-observe {"event":"hook-registered","registrationCount":2,...}`
- `agent runtime plugins pre-warmed in 294ms`

The HTTP health endpoint returned `200` with `{"ok":true,"status":"live"}`. `openclaw gateway status` identified the new running PID and scheduled task; its authenticated WebSocket probe was refused by the CLI probe despite the live HTTP health endpoint. This transport/probe anomaly is recorded separately and does not replace the direct health and startup evidence.

Post-restart evidence: `C:/Users/CDQ-P/cnx342-evidence/post-restart-hashes.json`; log source: `C:/Users/CDQ-P/AppData/Local/Temp/openclaw/openclaw-2026-09-14.log`.

## Zero semantic traffic and inference

No Dashboard prompt was sent. No new Dashboard session was created. No model provider call, Ollama call, OpenAI call, inference attempt, retry, resend, fallback, recovery, or manual dispatch was performed.

Read-only SQLite observation against:

`C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/runtime/cogentnexus-openclaw.sqlite3`

For the post-restart window beginning `2026-09-14T09:53:06Z`, counts were:

| Durable table | New rows after restart |
|---|---:|
| `tickets` | 0 |
| `cnx_direct_model_call` | 0 |
| `cnx_assistant_delivery` | 0 |
| `ticket_events` | 0 |
| `cnx_inference_attempt` | 0 |

Evidence: `C:/Users/CDQ-P/cnx342-evidence/zero-semantic-after-restart.json`.

Gateway log review after restart showed startup, plugin-load, health/control reads, and no semantic request or model-call event. The pre-existing database totals are historical state, not CNX-342 traffic.

## Gate assessment

1. Repaired source built: **PASS**
2. Entry and imported lease from one build: **PASS**
3. Build/installed hashes match: **PASS**
4. Active lease is repaired: **PASS**
5. Legacy imported lease absent from active path: **PASS**
6. Rollback copy exists: **PASS**
7. Manifest binds commit, hashes, timestamp: **PASS**
8. Exactly one Gateway restart succeeded: **PASS**
9. Post-restart Gateway healthy and loaded installed artifact: **PASS**, with CLI WebSocket probe anomaly separately recorded
10. Semantic traffic = 0: **PASS**
11. Inference = 0: **PASS**

No self-acceptance is asserted. Stop here for independent ChatGPT review.
