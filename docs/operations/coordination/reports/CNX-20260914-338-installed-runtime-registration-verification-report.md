# CNX-20260914-338 — Installed Runtime Registration Verification Report

**Date:** 2026-09-14 (Asia/Bangkok)
**Candidate branch:** `agent/v0.9.6-schema-authority-repair`
**Fresh remote coordination HEAD:** `967c67e76aa12b6916a8fa9b5d37c034a2513a0c`
**Verifier:** Hermes Agent
**Final verdict:** `BLOCKED`

## Scope and safety boundary

This was a registration-only verification. No Dashboard semantic request, prompt, Send action, WebChat invocation, model inference, retry, recovery, fallback, Ticket acceptance, or database write was performed. No runtime restart was used. The installed runtime was not modified.

## Candidate / release fence

| Field | Observed |
|---|---|
| Requested source candidate | `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7` |
| Fresh remote branch tip | `967c67e76aa12b6916a8fa9b5d37c034a2513a0c` |
| Repair commit named by task | `3efb971eeed55f0d48908281974577fdbed48612` |
| Installed plugin path | `C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw` |
| Installed artifact | `C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw/dist/v091-release-entry.js` |
| Installed artifact size | `8,734` bytes |
| Installed artifact SHA-256 | `da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef` |
| Expected candidate artifact SHA-256 | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| Installed package version | `0.9.5` |
| Installed plugin manifest version | `0.9.5` |
| Expected task candidate | v0.9.6 candidate |

The installed artifact does not equal the expected candidate artifact. The installed package is v0.9.5. This satisfies the task's explicit BLOCK condition and prevents a CNX-338 PASS.

The immutable release fence was not changed. Fresh `git ls-remote` showed:

```text
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95 refs/tags/v0.9.5
```

No tag, release, main branch, or history was modified.

## Installed controller and authority

The intended installed workspace controller was read from:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/host/controller.json
```

Observed JSON:

```json
{
  "cnxMode": "active",
  "desiredGateway": "running",
  "generation": 101,
  "managedLocalAdapters": { "ollama": "auto" },
  "providerOwnership": "openclaw",
  "schemaVersion": 2,
  "updatedAt": "2026-09-13T15:09:06.411038+00:00"
}
```

The production controller therefore has `schemaVersion=2`, `cnxMode=active`, and `generation=101`.

A controlled, non-production fixture copied this controller to a temporary workspace and loaded the actual installed artifact. The installed runtime produced:

```text
CogentNexus-OpenClaw v0.9.1 runtime registration suppressed: Host authority=invalid mode=unknown
```

Observed result:

```json
{
  "authority": "invalid / unauthorized (from suppression log)",
  "events": [],
  "services": 0,
  "tools": 0,
  "controllerUnchanged": true,
  "error": null
}
```

Thus the actual installed runtime still rejects the production schema-2 controller. The expected `authorized=true`, `reason=managed`, `mode=managed` result was not reached.

## Registration

The actual installed module imported successfully and exposed the plugin entry. Registration was invoked against the controlled temporary fixture only, with an instrumented API:

```text
module: C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw/dist/v091-release-entry.js
entry: default.register(api)
fixture: C:/Users/CDQ-P/AppData/Local/Temp/cnx338-rWiq6T
```

Actual registration evidence:

```text
api.on events: []
registerService calls: 0
registerTool calls: 0
suppression: Host authority=invalid mode=unknown
controller fixture unchanged: true
```

`before_agent_run` was not registered. This is correct fail-closed behavior for the installed v0.9.5 artifact, but it is a CNX-338 BLOCK because the requested v0.9.6 candidate was not installed.

The required negative matrix was **not run against the real installed candidate**, because the positive schema-2 gate failed at installed-artifact identity and the installed runtime already rejected schema 2. Running the remaining fixtures could not cure the blocking provenance failure and would not authorize a PASS.

## Disk integrity

No production controller write occurred. The production controller was read-only inspected. The registration probe used a copied controller in a temporary directory; the probe reported byte-identical before/after fixture content.

Production observed state remains:

```text
schemaVersion = 2
cnxMode = active
generation = 101
legacy mode persisted by compatibility translation = not observed
```

No `mode=managed` was written to the production controller by this task.

## Workspace / database

The intended OpenClaw workspace path resolved to:

```text
C:/Users/CDQ-P/.openclaw/workspace
```

The intended CogentNexus state directory is:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw
```

The controller path above was verified. No Ticket records were created or mutated. No SQLite write or recovery action was performed. A complete database health determination was not required after the installed-candidate identity gate blocked the task; it is not claimed as PASS evidence.

## Runtime health / configuration

No restart or debugging lifecycle action was used. No provider, model, provider timeout, or agent timeout configuration was changed. The task expected `ollama`, `ollama/qwen3.8:27b`, and 2700-second provider/agent timeouts; this verification did not alter those settings, but it does not claim a complete health PASS because the candidate was not installed and registration was suppressed.

## Safety confirmations

* No Dashboard semantic traffic: **confirmed**.
* No database mutation: **confirmed**.
* No recovery: **confirmed**.
* No provider/model/timeout change: **confirmed**.
* No restart used as a debugging action: **confirmed**.
* v0.9.5 immutable: **confirmed** by fresh tag lookup; tag remains `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`.

## Final verdict

# `BLOCKED`

CNX-338 cannot PASS because the actual installed runtime is v0.9.5, its artifact SHA-256 is `da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef`, and it rejects the real schema-2 controller with `authority=invalid`. The required v0.9.6 artifact SHA-256 `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` is not installed. CNX-339 is not authorized.
