# CNX-334 — Dashboard Integration Boundary Diagnostic Report

**Date:** 2026-09-14  
**Classification:** `HOOK_NOT_REGISTERED`  
**Scope:** read-only runtime and source diagnostic; no remediation

## Runtime provenance

| Item | Evidence |
|---|---|
| Published baseline | `v0.9.5`, requested immutable baseline `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` |
| Runtime plugin artifact | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw` |
| Runtime entry | `dist/v091-release-entry.js` from the installed package manifest |
| Installed version | `0.9.5` (`package.json`, `ownership.json`) |
| Plugin fingerprint | SHA-256 `d284291bef3d92cabd93b3fb9a4481436a00350e8fc04e7876e8da21f46e436d` for installed `dist/index.js`; the repository checkout's corresponding `dist/index.js` had the same SHA-256 |
| Config enabled state | `plugins.entries.cogentnexus-openclaw.enabled=true` |
| Host process/runtime | OpenClaw Gateway, Node `v24.18.0`, OpenClaw `2026.7.1-2`, Windows `10.0.19045`, invocation recorded in the CNX-332 trajectory metadata |
| Provider/model | `ollama/qwen3.8:27b` |
| Host authority state | `cnxMode=active`, `desiredGateway=running`, `providerOwnership=openclaw`, controller schema version `2` |

The artifact is installed and configured as enabled. However, source-level registration contains a fail-closed authority gate: `hostPluginAuthority()` accepts only `schemaVersion === 1`. The live controller is schema version `2`, so the release entry returns `authorized:false` with reason `invalid` before registering the bridge hooks.

## Hook trace

### Actual source path

```text
OpenClaw plugin loader
      ↓
installed dist/v091-release-entry.js → releaseEntry.register(api)
      ↓
hostPluginAuthority(api)
      ↓
controller.json schemaVersion=2 rejected by schemaVersion === 1 check
      ↓
register() returns without calling legacyEntry.register(runtimeApi)
      ↓
no CogentNexus before_agent_run registration
      ↓
no TicketStore.accept() for CNX-332
```

The relevant implementation is the installed `dist/v091-release-entry.js` and the corresponding repository source. `releaseEntry.register(api)` first calls `hostPluginAuthority(api)`. If unauthorized it logs a suppressed-registration message and returns at lines 125–129. The authority check at lines 101–104 requires schema version 1. The live `host/controller.json` reports schema version 2.

If authority passed, the intended downstream path would be:

```text
OpenClaw before_agent_run
      ↓
legacyEntry.register(runtimeApi)
      ↓
index.ts api.on("before_agent_run", ...)
      ↓
durableAdmissionEligible({sessionKey, senderIsOwner})
      ↓
classifyDurableRequest(...)
      ↓
TicketStore.accept({runId, ownerSessionKey, prompt, maxAttempts})
      ↓
TicketStore.route(...)
```

The registration callback is `api.on("before_agent_run", ...)` in `index.ts` lines 730–813. The admission call is `ticketStore.accept(...)` at lines 774–785, subject to `ticketFirst === true`, `ticketIntakeEligible(prompt)`, and the canonical dashboard owner-session eligibility check. Admission emits the normal Ticket event chain through `TicketStore`.

The Dashboard event recorded for CNX-332 is a runtime `prompt.submitted` trajectory event, with `data.messageProvider="webchat"`, `data.prompt`, the dashboard session key, session ID, run ID, and workspace. It is not itself the CogentNexus hook name; OpenClaw must translate the run into `before_agent_run` for the plugin. Because the plugin's release entry was suppressed before hook registration, no bridge callback could observe or adapt that event.

## Dashboard event compatibility

CNX-332 evidence:

- OpenClaw trajectory event: `prompt.submitted`
- `messageProvider`: `webchat`
- session key: `agent:main:dashboard:2fefcfd2-6819-4c21-a190-842ebc133f57`
- workspace: `C:\Users\CDQ-P\.openclaw\workspace`
- prompt: `CNX-332 lifecycle acceptance nonce 20260913-202936. Reply with exactly: CNX-332 accepted.`

The source contract expects the OpenClaw `before_agent_run` hook, with `ctx.sessionKey`, `ctx.runId`, and workspace metadata. The Dashboard trajectory proves that the event reached the OpenClaw runtime and model path, but it does not prove that the CogentNexus callback was invoked. The earlier registration gate proves the callback was not registered in this runtime. Therefore the first break is earlier than event filtering, identity translation, or Ticket admission.

## Database and workspace trace

| Item | Value |
|---|---|
| Configured OpenClaw workspace | `C:\Users\CDQ-P\.openclaw\workspace` |
| Plugin workspace resolution | configured `workspaceDir`, otherwise OpenClaw default workspace; live config supplies the same workspace |
| CogentNexus state root | `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw` |
| Intended/actual CogentNexus SQLite | `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3` |
| Database owner | CogentNexus-OpenClaw installed runtime under the OpenClaw workspace boundary |
| SQLite inspection | Opened read-only with `mode=ro`; schema contains `tickets`, `ticket_events`, `ticket_outbox`, `cnx_sessions`, `cnx_direct_model_call`, `cnx_inference_attempt`, and `cnx_assistant_delivery` |

The CNX-332 trajectory and the plugin configuration identify the same workspace. The inspected CogentNexus database is therefore the intended database, not a path-mismatch database. The absence of CNX-332 rows is a missing admission caused by the earlier registration gate, not evidence of a database-path gap.

## CNX-332 identifier mapping

| Identifier | OpenClaw host | CogentNexus runtime | CogentNexus SQLite |
|---|---|---|---|
| Dashboard session | `agent:main:dashboard:2fefcfd2-6819-4c21-a190-842ebc133f57` in `sessions.json`, trajectory, and session JSONL | No registered CogentNexus hook callback observed; no CNX identity created for this run | `N/A / not present` in `cnx_sessions` |
| Session ID | `59e80ea8-6151-4fc1-9de4-4d8c46ebcd9a` in session metadata and trajectory | No CogentNexus translation observed | `N/A / not present` |
| Run ID | `46a1470c-47f9-41dc-9f41-bade8742a24c` in trajectory and session JSONL; host run started/finished evidence | No CogentNexus admission/call binding | `N/A / not present` in `tickets`, `cnx_direct_model_call`, and `cnx_inference_attempt` |
| Ticket ID | `N/A / not present` | `N/A / not created` | `N/A / not present` |
| Model call ID | `N/A / not present` in CogentNexus; OpenClaw model completion is not a CogentNexus call | `N/A` | `N/A / not present` |
| Delivery ID | `N/A / not present` in CogentNexus | `N/A` | `N/A / not present` for this run |

The database does contain older, unrelated Dashboard and Discord CogentNexus records, confirming that the database is live and writable-capable in normal operation. No row matched any CNX-332 identifier.

## Admission boundary

The exact Ticket admission condition in the registered bridge is:

1. `releaseEntry.register(api)` must pass `hostPluginAuthority(api)`;
2. `legacyEntry.register(runtimeApi)` must register `before_agent_run`;
3. plugin configuration must leave `preInferenceAdmission` enabled and set `ticketFirst=true`;
4. `durableAdmissionEligible(...)` must accept the canonical owner session;
5. `ticketIntakeEligible(event.prompt)` must be true;
6. `TicketStore.accept({runId, ownerSessionKey, prompt, maxAttempts})` must execute.

For CNX-332, conditions 1–2 fail first: the runtime controller schema is 2 while the release-entry authority gate requires 1. Consequently condition 2 never occurs, so the Dashboard event cannot reach the admission function. No evidence supports classifying this as an event filter mismatch, identity translation gap, workspace/database path gap, or deeper Ticket admission gap.

## Boundary diagnosis

**First break:** `releaseEntry.register(api)` → `hostPluginAuthority(api)`.

The installed plugin artifact is present and enabled, but its runtime registration is suppressed because the live host controller has `schemaVersion: 2` and the release entry accepts only schema version 1. The Dashboard request therefore reached OpenClaw and the model, but no CogentNexus integration hook was registered to receive it.

Answer to the primary question: **the Dashboard event did not reach the CogentNexus integration hook; the hook was never registered in this runtime.**

## Classification

`HOOK_NOT_REGISTERED`

## Safety statement

This diagnostic performed no new semantic request. It performed no database mutation, no restart, no configuration mutation, no recovery, and no release/tag mutation. It did not modify source, model, provider, timeout, Git history, or published `v0.9.5`.
