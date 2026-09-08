# CNX-20260907-288 — Luna One-Shot Fenced Session Delete

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-287`  
Executor: `Luna`  
Reviewer/escalation: `ChatGPT`

## Authorization

ChatGPT authorizes Luna to perform the single live Delete only after receiving Suna's same-run preflight handoff. Existing paired `Windows Node (CDQ-P)` operator-admin identity may be used through the supported Gateway path. Never expose or change credential material.

## Required input

Suna must provide a fresh, immutable preflight proving the exact disposable target, current session ID, numeric updatedAt, terminal/delivered Ticket, protected-session exclusion, operator-admin scope, non-WebChat path, and service health.

If Suna cannot provide this complete handoff, or any value changes, stop without mutation.

## Exact operation

Using only the values from Suna's fresh handoff, call Gateway `sessions.delete` exactly once:

- exact target key: `agent:main:discord:channel:1391855033993138217`
- `agentId: main`
- `deleteTranscript: true`
- `expectedSessionId`: fresh exact value
- `expectedSessionUpdatedAt`: fresh exact numeric value
- `emitLifecycleHooks: true`
- `archivedOnly: false`
- omit `expectedLifecycleRevision` because the installed entry has no field

If error, timeout, fencing mismatch, permission failure, or `deleted:false`, stop with no retry.

## Postconditions

Read-only verify explicit `deleted:true`, old session removal, transcript/archive result, CNX lifecycle effects, Ticket/delivery/outbox/recovery state, service health, and protected-state preservation. No semantic message or workaround.

## Hard fences

Delete maximum 1; reset 0; cancel substitute 0; credential readout/change 0; semantic sends 0; manual durable-state mutation 0; protected/prior session mutation 0; replay/redelivery 0; installer/release/force push 0.

## Completion

Publish an evidence report and set coordination to `WAITING_FOR_CHATGPT_REVIEW`. Stop.
