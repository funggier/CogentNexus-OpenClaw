# CNX-20260918-420 — ChatGPT Review

## Decision

`ACCEPTED_PASS`

Accepted final classification:

`PASS_OPERATOR_FRESH_SESSION_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

Accepted route classification:

`FRESH_SESSION_ROUTE_OLLAMA_CONFIRMED`

Accepted Ticket-first classification:

`FRESH_SESSION_TICKET_FIRST_CONFIRMED`

## Independent verification

The authoritative branch and CNX-420 report were re-read from GitHub at branch HEAD:

`8fd0df466c639f54ab78355f3e9094fe6457cba8`

Verified from the published evidence:

- the Operator created exactly one fresh Dashboard session after a browser refresh;
- exactly one semantic message was sent;
- native execution used provider `ollama`, model `qwen3.8:27b`, API `ollama`;
- exactly one CogentNexus Ticket was accepted and routed before the correlated model call;
- exactly one direct model call and one inference attempt occurred;
- exactly one durable assistant delivery and one visible assistant response occurred;
- no semantic retry/resend occurred;
- no outbox row or direct-recovery row was required;
- the returned assistant text matched the nonce exactly after removal of the delivery marker.

The required vertical lineage is therefore proven:

`Dashboard/WebChat -> admission trace -> Ticket accepted/routed -> Ollama qwen3.8:27b -> response_ready -> durable direct result -> delivery_confirmed -> Ticket completed -> visible response`

## Long-latency / timeout-authority observation remains open

The PASS does not close the runtime timing anomaly.

The correlated model call required:

`2,682,699 ms = 44m 42.699s`

while the emitted timeout/deadline was:

`900,000 ms = 15m`

The model therefore completed approximately:

`29m 42.700s`

after the emitted deadline.

This was not a retry or recovery artifact: semantic sends, model calls, inference attempts, and visible responses each remained cardinality one.

Accepted observation:

`MODEL_CALL_DEADLINE_NOT_ENFORCED_OR_NOT_AUTHORITATIVE`

This requires later characterization, but it does not invalidate the route/Ticket-first acceptance result.

## Reconciliation with CNX-419

CNX-420 does not invalidate CNX-419.

CNX-419 proved that a reused Dashboard session executed through the Codex/OpenAI harness without traversing CogentNexus Ticket-first admission:

- actual runtime: `codex`;
- actual provider/model: `openai/gpt-5.6-luna`;
- CogentNexus admission trace: absent;
- CogentNexus Ticket: absent.

CNX-420 proves that a refreshed, Operator-created fresh session selected for Ollama did traverse the existing built-in path and produced the complete Ticket-first lineage.

Together these results support two distinct facts:

1. the fresh Ollama path is healthy enough to satisfy the intended Ticket-first vertical slice;
2. Ticket-first is still not harness-agnostic because the Codex/plugin-harness path demonstrated by CNX-419 can bypass the current `before_agent_run` admission boundary.

The CNX-419 route mismatch was not reproduced in CNX-420. This is consistent with stale browser/session presentation being involved, but it does not prove stale presentation was the sole cause.

## Architecture conclusion

The current primary admission boundary in CogentNexus is still too deep:

`before_agent_run`

OpenClaw's current hook contract explicitly documents that `before_agent_run` is not a universal input gate for Codex/Copilot harnesses.

The target invariant remains:

`NO TICKET = NO MODEL EXECUTION`

The architecture should therefore move owner-turn Ticket admission to a harness-agnostic pre-model dispatch boundary, while retaining `before_agent_run` as a deeper compatibility/deduplication fence for runners that emit it.

### Candidate seam ordering

For normal Dashboard/channel owner turns:

`inbound dispatch -> pre-model admission -> Ticket accept/route -> OpenClaw harness/provider selection and execution -> durable delivery`

The strongest currently known candidate is `reply_dispatch` because:

- it executes before normal model/harness dispatch;
- it carries the same Dashboard `runId` later used by the model-call lineage;
- `TicketStore.accept()` is idempotent for the same owner session + run ID;
- it does not require CogentNexus to become a provider router.

`before_dispatch` is even earlier and is useful for canonical inbound identity/trust characterization, but its current event contract does not provide the same run ID. It should not replace the run-correlated Ticket intake without an explicitly proven binding mechanism.

OpenClaw must remain authoritative for provider/model selection. CogentNexus must enforce durable admission and continuity, not silently force Ollama/OpenAI or duplicate OpenClaw routing.

## OpenClaw current-version direction

The Operator explicitly authorized moving to the current OpenClaw generation when its structure is materially better.

Current upstream qualification target:

`OpenClaw v2026.9.4`

Installed/live baseline remains:

`OpenClaw 2026.7.1-2 (0790d9f)`

The newer generation is materially relevant to CogentNexus because it contains a substantially revised dispatch/session/plugin architecture and clearer hook-boundary contracts. However, the 2026.8.1 generation boundary also introduced major session/transcript persistence and Plugin SDK changes.

Therefore:

`QUALIFY_CURRENT_OPENCLAW_BEFORE_LIVE_UPGRADE`

Do not mutate the live OpenClaw installation yet.

The upgrade is not a substitute for the harness-agnostic admission repair; both must qualify.

## Successor authorization

Authorize CNX-421 as a repository/read-only + isolated-candidate qualification task.

CNX-421 may:

- compare exact 2026.7.1-2 and v2026.9.4 upstream contracts;
- characterize the earliest safe, run-correlated owner-turn admission seam;
- build repository characterization tests and, only where proven, a bounded source candidate on the working branch;
- test v2026.9.4 against isolated/copy state only;
- produce an explicit go/no-go recommendation for a controlled live upgrade.

CNX-421 must not:

- upgrade or mutate the live OpenClaw installation;
- migrate live session/transcript state;
- restart the live Gateway for an upgrade;
- send a semantic acceptance message;
- change live provider/model selection;
- merge/tag/release/main;
- force push or rewrite history.

A controlled live upgrade, if qualified, belongs to a separately reviewed successor task.

## Reviewer

ChatGPT

Human final authority: Operator
