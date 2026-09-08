# CNX-20260907-287 — Suna Fresh Preflight for Fenced Delete

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-286`  
Executor: `Suna`  
Next executor: `Luna`  
Reviewer/escalation: `ChatGPT`

## Objective

Perform only the fresh read-only preflight needed before Luna's one-shot live Delete task CNX-20260907-288.

## Authorization

The existing paired `Windows Node (CDQ-P)` operator-admin identity may be selected through the supported client path, without exposing, copying, rotating, revoking, or changing any credential. No `sessions.delete` call is authorized in this task.

## Required evidence

Freshly prove and publish a handoff containing:

- exact disposable session key and current session ID;
- numeric updatedAt;
- absent lifecycleRevision (do not synthesize);
- terminal, durably delivered setup Ticket;
- protected Ticket/session exclusion;
- operator-admin scope and non-WebChat client path;
- Gateway/Ollama/Host/Supervisor health;
- exact timestamp and remote HEAD.

If credential use requires new material or an additional security decision, set `NEEDS_CHATGPT` and stop.

## Hard fences

`sessions.delete=0`; reset/cancel substitute=0; semantic sends=0; credential exposure/change=0; Ticket/session/SQLite/transcript mutation=0; protected/prior session mutation=0; replay/redelivery=0; installer/release/force push=0.

## Completion

Publish the preflight report, then set the active task to CNX-20260907-288 for Luna with the exact immutable values. If any fence fails, stop and request ChatGPT.
