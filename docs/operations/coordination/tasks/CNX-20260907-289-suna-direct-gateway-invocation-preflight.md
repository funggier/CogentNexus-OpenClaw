# CNX-20260907-289 — Suna Direct Gateway Invocation Preflight

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-288`  
Executor: `Suna`  
Next executor: `Luna`  
Reviewer/escalation: `ChatGPT`

## Objective

Prepare a safe direct Gateway invocation path for Luna's still-unused one-shot `sessions.delete`. Do not use browser Chat UI navigation or type operational commands into any chat input.

## Allowed work

- Read current remote state and inherited Task287 immutable fence.
- Inspect supported installed `openclaw gateway call` help/protocol and identify the direct non-WebChat operator-admin path.
- Use only harmless read-only capability/health probes if they require no credential exposure or mutation.
- Confirm how the already-authenticated paired `Windows Node (CDQ-P)` identity can be selected without printing/copying credentials.
- Publish an exact handoff to Luna.

## Stop conditions

If the direct path requires extracting, displaying, changing, or guessing a token/password, or requires a new security decision, set `NEEDS_CHATGPT` and stop. Do not open or use the Chat UI input for operational commands.

## Hard fences

- `sessions.delete=0`
- reset/cancel substitute=0
- semantic sends=0
- credential readout/change=0
- Ticket/session/SQLite/transcript mutation=0
- protected/prior session mutation=0
- replay/redelivery=0
- installer/release/force push=0

## Completion

Publish a report with exact supported invocation shape and handoff to Task290 (Luna). Do not perform Delete.
