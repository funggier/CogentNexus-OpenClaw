# CNX-20260907-292 — Suna Fresh Read-Only Recreation Preflight

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-291`  
Executor: `Suna`  
Reviewer/escalation: `ChatGPT`

## Objective

Perform a fresh read-only preflight to determine whether a separately authorized clean recreation task may be drafted after the confirmed user deletion.

## Required evidence

Re-anchor from the current remote branch, then read-only verify:

- exact OpenClaw inventory has no target key, old session ID, or replacement;
- target CNX tombstone state, generation, old session ID, deletion timestamp, and reason;
- old Ticket status/delivery/outbox/recovery state;
- protected session/Ticket/recovery state and non-interference;
- Gateway/service health and any relevant operator-scope limitation.

## Decision boundary

Report whether the state is safe enough to propose a future clean recreation task. Do not perform recreation in this task. If any value drifts, evidence conflicts, protected state changes, or authority is insufficient, stop with `NEEDS_CHATGPT`.

## Hard fences

No session creation, `sessions.delete`, reset, semantic send, Ticket/session/SQLite/transcript mutation, replay/redelivery/disposition, credential action, installer, release, or protected-session mutation.

## Completion

Publish a read-only evidence report. If preflight is clean, hand off a separately bounded recreation proposal to ChatGPT for authority; do not authorize or execute it in Task292.
