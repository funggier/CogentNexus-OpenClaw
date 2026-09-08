# CNX-20260907-297 — Live Worker Runtime Alignment Requalification

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-296`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authorization

ChatGPT authorizes a bounded live deployment/requalification of the already-tested Task296 resolver. Scope is limited to the CogentNexus detached delivery worker runtime path. Do not perform installer/uninstall/reset or unrelated service changes.

## Objective

Install/activate the tested worker resolver in the live worker so it explicitly uses the Gateway server Node runtime:

`C:\Program Files\nodejs\node.exe`

Then observe whether the pending delivery's `chat.history` no-JSON failure resolves.

## Preconditions

Before mutation, re-anchor and verify:

- Task296 TDD tests and aligned-runtime probe are present and GREEN;
- exact live worker and repository file identities;
- Gateway Node path exists and is the intended server runtime;
- target session/Ticket and protected state;
- Gateway/Ollama/Host/Supervisor health;
- no newer remote coordination state supersedes this task.

If any precondition is unclear, stop.

## Allowed live changes

- Deploy only the tested `host_delivery_v092.py` resolver change through the canonical supported worker update mechanism.
- Configure only the worker's `OPENCLAW_GATEWAY_NODE_PATH` to the verified Gateway Node path, without printing credentials.
- Restart/reload only the affected detached delivery worker using its canonical lifecycle mechanism, if required for adoption.
- Observe the existing pending worker behavior and collect sanitized process/stream evidence.

Natural worker continuation after the bounded restart may process the existing pending Ticket; do not manually replay, redeliver, cancel, dispose, or settle it.

## Observation

Capture:

- deployed file/config hashes;
- worker and Gateway executable paths/versions;
- process start/exit and stdout/stderr byte evidence;
- `chat.history` response status;
- pending Ticket/delivery status and timestamps;
- whether durable delivery confirms naturally;
- service health and protected-state preservation.

Do not treat response-ready or visible Discord text as durable delivery confirmation.

## Hard fences

- no new semantic message;
- no manual replay/redelivery/disposition;
- no manual Ticket/SQLite/session/transcript mutation;
- no session creation/delete/reset;
- no credential exposure/change;
- no protected-session mutation;
- no installer/uninstall/broad cleanup;
- no unrelated service/process mutation;
- no release or force push.

## Failure/stop rules

If deployment cannot be performed through the canonical mechanism, or if worker restart scope is ambiguous, stop with `NEEDS_CHATGPT`. Do not guess or broaden scope. If the no-JSON error persists, capture evidence and stop; do not add retries or workarounds.

## Completion

Publish an evidence-rich requalification report with exact hashes, tests, live adoption proof, delivery result, and residual uncertainty. Then set coordination to `WAITING_FOR_CHATGPT_REVIEW`.
