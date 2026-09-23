# CNX-20260922-444 — v0.9.7 Exact Gateway-Interruption Direct Recovery

Status: `IN_PROGRESS`

Parent: `CNX-20260921-443`

Target release line: `v0.9.7`

## Trigger

A genuine Discord turn on 2026-09-22 exposed a production continuity gap after the external Host confirmed an unresponsive OpenClaw Gateway and restarted it while an Ollama Direct model call was in flight.

Observed production evidence:

- Ticket accepted at approximately `18:19:07 +07`;
- `ollama/qwen3.8:27b` model call started at approximately `18:19:10 +07`;
- external supervisor entered recoverable maintenance at approximately `18:21:16 +07`;
- Gateway process boundary was replaced at approximately `18:22:27–18:22:30 +07`;
- the original Direct model-call row remained `active`;
- no `model_call_ended` or failing `agent_end` arrived for the interrupted old Gateway generation;
- no `cnx_direct_recovery`, outbox, or delivery authority was created;
- OpenClaw eventually reached its configured whole-run timeout after about 2705 seconds (~45 minutes).

The CNX 15-minute model-call deadline is observational only and MUST NOT become destructive timeout authority. Historical qualification proved that a healthy local Qwen call may legitimately complete after more than 44 minutes.

## Root cause

The provider-neutral Host intentionally suppresses timer-only Direct model-call recovery. Exact terminal model-call errors are recoverable, but a Gateway restart can physically destroy an in-flight call before either `model_call_ended` or `agent_end` can persist terminal evidence.

The resulting state is stranded:

```text
active Direct model call
  -> confirmed Gateway hard hang
  -> Gateway restart
  -> old inference physically impossible
  -> DB call remains active
  -> no terminal_error evidence
  -> timer-only recovery remains correctly suppressed
  -> Ticket remains accepted indefinitely
```

## Required v0.9.7 semantics

1. A healthy Gateway plus elapsed observational model-call deadline MUST remain observe-only.
2. A confirmed hard-hang Gateway replacement is exact interruption evidence for Direct calls owned by the old runtime boundary.
3. Recovery authority MUST be created only after CNX/Gateway inference is quiesced.
4. The hard-hang path MUST order:
   - prepare recoverable maintenance;
   - stop/quiesce Gateway;
   - classify eligible active Direct calls as interrupted;
   - persist exactly-one pending Direct recovery per eligible Ticket;
   - start Gateway.
5. Recovery MUST remain provider-neutral. CNX must not select, start, stop, or reroute Ollama/OpenAI/other providers.
6. Response-ready, delivered, terminal, workflow-owned, cancelled, or otherwise fenced Tickets MUST never be regenerated.
7. Startup Direct-recovery liveness MUST see pending rows before the replacement Gateway becomes inference-capable.
8. Partial failure after Gateway stop MUST attempt bounded Gateway restoration.
9. A replacement Gateway started by another actor MAY reconcile an orphan only when the active Direct call belongs to the immediate predecessor Gateway boot window.
10. Current Gateway identity MUST be resolved by matching the live Gateway PID to `gateway_boot_lifecycle`.
11. Older historical active rows that predate the immediate predecessor boot MUST remain residue and MUST NOT be replayed automatically.
12. Existing v0.9.6 release/tag remain immutable.
13. A successfully persisted exact Direct model-call start MUST refresh liveness for the already-active owner session without changing state/generation, so startup recovery cannot be blocked solely by a stale heartbeat from before the live call.

## Evidence identity

The incident Ticket/run captured during diagnosis:

- Ticket: `CNXT-6866c23d-8c58-4a48-8699-2e48944ffb73`
- original run: `397c29b1-beeb-4421-b786-abb84c360f52`
- provider/model: `ollama/qwen3.8:27b`
- CNX recorded deadline: `2026-09-22T11:34:10.804Z`
- OpenClaw configured whole-run timeout: `2700s`

These values are diagnostic evidence only and MUST NOT be hard-coded into production behavior.

## TDD requirements

RED tests MUST prove:

- gateway-interruption claim can select an active Direct call before its observational deadline;
- classification writes gateway-interruption-specific event/outcome, not timeout evidence;
- Direct lane is preserved and exactly-one pending recovery is authorized;
- response-ready/terminal/delivery fences still win;
- confirmed hard-hang lifecycle orders `prepare -> stop -> classify -> start`;
- failure after stop still attempts start;
- healthy/slow inference is not recovered by time alone;
- current Gateway PID resolves to its exact boot row;
- only the immediate predecessor boot window is eligible for post-restart orphan recovery;
- older historical residue is excluded from automatic replay;
- a stale active owner-session heartbeat is refreshed by the exact Direct model-call start, and the resulting recovery becomes claimable without relaxing generation or stale-session fences;
- OpenClaw 2026.9.5 Direct Recovery uses detached embedded execution with no legacy JSONL `sessionFile`, while preserving the internal `:subagent:` admission fence and original provider/model;
- an authoritative assistant-delivery wake executes the Host delivery bridge exactly once instead of falling through to a health-only legacy Supervisor path, and the next scheduled tick returns idle after the delivery is consumed.

## Validation

Before any v0.9.7 candidate is accepted:

- focused Python recovery/supervisor tests PASS;
- full Python suite PASS;
- plugin Vitest suite PASS;
- namespace/baseline/version checks PASS;
- `git diff --check` PASS;
- production npm audit remains clean;
- source/installed parity PASS after deployment;
- live OpenClaw 2026.9.5 hard-hang/interruption acceptance demonstrates one recovery without duplicate inference/delivery;
- route remains OpenClaw-owned and unchanged unless the operator changes it.

## Current classification

`CNX444_V097_SUPERVISOR_DELIVERY_DISPATCH_LOCAL_GREEN_CANDIDATE_PENDING`
