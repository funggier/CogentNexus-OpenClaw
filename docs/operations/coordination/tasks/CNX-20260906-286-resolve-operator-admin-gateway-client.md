# CNX-20260906-286 — Resolve Operator-Admin Gateway Client Boundary

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-285`  
Executor: `Luna`  
Next executor after normal completion: `Suna`  
Reviewer/escalation: `ChatGPT`

## Objective

Resolve the Task285 preflight block where the connected Gateway client lacked `operator.admin`, so a future bounded `sessions.delete` can use the required identity fencing.

## Allowed work

- Read current coordination state and exact installed OpenClaw auth/client configuration.
- Identify the supported non-WebChat Gateway client path that can hold `operator.admin`.
- Verify required scopes and explain the supported acquisition/configuration boundary.
- Perform only harmless read-only probes; do not call `sessions.delete`.
- Publish evidence and a precise next-task proposal.

## Stop and ask ChatGPT

Set `NEEDS_CHATGPT` and notify the human to call ChatGPT if obtaining operator-admin authority requires new credentials, human approval, external account action, or any ambiguous security decision. Do not invent credentials or alter auth state.

## Hard fences

- `sessions.delete`: 0
- reset/cancel substitute: 0
- semantic sends: 0
- Ticket/session/SQLite/transcript mutation: 0
- protected or sacrificial session mutation: 0
- installer/uninstall/release/force push: 0

## Handoff

On normal completion, publish a report, update coordination to the next bounded task assigned to `Suna`, and include exact evidence and remaining authority requirements. If blocked by a decision or credential boundary, stop and request ChatGPT.
