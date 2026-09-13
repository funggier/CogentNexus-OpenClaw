# CNX-20260914-338R — Installed Candidate Registration Verification Report

**Date:** 2026-09-14 (Asia/Bangkok)
**Verdict:** `PASS`
**Failure classification:** None

## Scope and safety fence

This rerun exercised the installed candidate registration entry point with a runtime-shaped API object. It did not send Dashboard requests, invoke model inference, create an intentional Ticket, exercise recovery or fallback, perform retry experiments, test duplicate delivery, or perform delivery actions. The registration callback itself was the only exercised boundary.

## Fixed provenance and preconditions

| Item | Observed |
|---|---|
| Repository | `funggier/CogentNexus-OpenClaw` |
| Candidate branch | `agent/v0.9.6-schema-authority-repair` |
| Candidate source HEAD | `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7` |
| Repair commit | `3efb971eeed55f0d48908281974577fdbed48612` |
| Installed entry | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` |
| Required installed SHA-256 | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| Observed installed SHA-256 | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| Plugin enabled | `true` |
| Plugin status | `loaded` (direct `openclaw plugins list --json` inventory) |
| Release tag | `v0.9.5 -> 50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` |

All preconditions passed. No configuration changes were made.

## Production controller and authority

Only the canonical production controller was used for this gate:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json`

| Field | Observed |
|---|---|
| `schemaVersion` | `2` |
| `cnxMode` | `active` |
| `generation` | `101` |
| Controller SHA-256 before | `1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98` |
| Controller SHA-256 after | `1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98` |

The alternate workspace-level schema-1 controller was not used by the registration probe.

The direct `hostPluginAuthority(api)` path resolved the canonical controller and returned:

```text
AUTHORIZED
reason=managed
mode=managed
schemaVersion=2
cnxMode=active
generation=101
controllerPath=C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json
```

`mode=managed` was an in-memory downstream translation only. The controller remained schema 2 with `cnxMode=active`; no legacy `mode` field was written.

## Registration boundary evidence

The installed module was imported from the fixed installed path and its actual `register(api)` entry point was invoked once with a runtime-shaped API object. The call completed without an authority-suppressed registration message.

The installed entry source order is exercised directly: authority validation precedes the delegated legacy registration call, and the resulting runtime API recorded registrations from the downstream boundary. Direct evidence that the legacy boundary was reached is the non-empty registration result below, together with the installed module's `delivery-observe` log:

```text
CogentNexus-OpenClaw delivery-observe {"event":"hook-registered","registrationCount":1,"hasReplyDispatch":true,"hasReplyPayloadSending":true}
```

This distinguishes:

- `MODULE_LOADED`: installed module imported successfully.
- `AUTHORITY_AUTHORIZED`: canonical schema-2 controller returned `authorized=true`, `reason=managed`, `mode=managed`.
- `LEGACY_REGISTRATION_REACHED`: downstream `register(runtimeApi)` produced runtime hook/service/tool registrations; `registrationCount=1` was emitted.

## Runtime registrations

The runtime API probe exposed:

- `before_agent_run`: present, 7 callback registrations across the legacy capability surfaces.
- Other event names: `before_message_write`, `reply_payload_sending`, `session_start`, `agent_end`, `session_end`, `before_tool_call`, `reply_dispatch`, `message_sent`, `subagent_spawned`, `subagent_ended`, `after_compaction`, `model_call_started`, `model_call_ended`, and `before_agent_finalize`.
- Services: 6
  - `cogentnexus-openclaw-workflow-completion`
  - `cogentnexus-openclaw-ticket-recovery`
  - `cogentnexus-openclaw-direct-recovery-v090`
  - `cogentnexus-openclaw-v090-host-reconciliation`
  - `cogentnexus-openclaw-context-maintenance-v091`
  - `cogentnexus-openclaw-direct-recovery-v097-liveness`
- Tools: 5 runtime registrations exposed by the API probe; the runtime API did not expose tool identifiers in this probe.
- Commands: 0
- CLI registrations: 0
- Gateway methods: 0

## Duplicate and partial-registration checks

The registration entry point was invoked once. The installed module emitted `registrationCount=1`. Service identifiers were unique; no duplicate service owner was observed. The seven `before_agent_run` callbacks are registrations from distinct legacy capability paths, not repeated invocations of the release entry point; no duplicate registration instance or duplicate service owner was observed.

Registration was not partial: authority was accepted, the legacy boundary produced hooks/services/tools, and the required `before_agent_run` hook was present. No `PARTIAL_REGISTRATION` condition was observed.

## Provider/model/timeouts and release fence

Observed active configuration remained:

```text
provider/model = ollama/qwen3.8:27b
provider timeout = 2700s
agent timeout = 2700s
```

The v0.9.5 tag remained exactly:

```text
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95
```

No tag movement, release mutation, merge, history rewrite, provider change, model inference, or timeout change occurred.

## Controller integrity

The canonical controller's before and after SHA-256 values are byte-identical:

```text
before = 1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98
after  = 1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98
```

The after-state remained `schemaVersion=2`, `cnxMode=active`, `generation=101`, with no `mode` field introduced.

## Semantic-traffic statement

No Dashboard request, model inference, intentional Ticket, recovery, fallback, retry experiment, duplicate-delivery test, or delivery action occurred. Only the registration boundary was exercised.

## Final verdict

`CNX-338R = PASS`

All thirteen stated success criteria are satisfied. `CNX-339` may advance only under its separate authorization; this report does not independently authorize any other gate beyond the task's stated `CNX-338R = PASS` transition.
