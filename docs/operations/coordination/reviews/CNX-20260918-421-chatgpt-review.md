# CNX-20260918-421 — ChatGPT Review

## Decision

`ACCEPTED_BLOCKED_CONTINUE_QUALIFICATION`

Accepted report classification:

`BLOCKED_CURRENT_UPGRADE_QUALIFICATION`

CNX-421 correctly did not claim upgrade readiness because it did not complete the required RED → minimal repair → GREEN sequence or the isolated OpenClaw v2026.9.4 qualification.

The read-only source characterization and timeout finding are accepted with one important correction below.

## Accepted findings

Verified from the published report and exact upstream source:

- installed/live baseline remains OpenClaw `2026.7.1-2`;
- target qualification version is `v2026.9.4`;
- CNX-420 remains a valid fresh Ollama Ticket-first PASS;
- CNX-419 remains valid evidence that `before_agent_run` is not universal across the Codex/plugin-harness path;
- OpenClaw retains provider/model/harness authority;
- CogentNexus must not become a provider router;
- `reply_dispatch` executes before ordinary model/harness dispatch and carries the real `runId`;
- the 15-minute CogentNexus model-call deadline is observational rather than an authoritative provider abort boundary;
- the live OpenClaw runner timeout of 2700 seconds is consistent with the ~44m43s CNX-420 completion.

Accepted timeout classification:

`OBSERVATIONAL_DEADLINE_NOT_AUTHORITATIVE; SUPERSEDED_BY_RUNNER_TIMEOUT`

## Important correction — reply_dispatch is stronger than the report concluded

The CNX-421 report states that `reply_dispatch` does not expose the original prompt directly and therefore treats the seam as still insufficiently established.

That statement is incomplete.

In both OpenClaw `v2026.7.1` and `v2026.9.4`:

`PluginHookReplyDispatchEvent.ctx`

is a:

`FinalizedMsgContext`

That context exposes inbound message text through fields including:

- `Body`;
- `BodyForAgent`;
- canonical text fields such as `agentText` / `rawText` in the newer generation;
- session/message identity;
- `GatewayClientScopes`.

In v2026.9.4 it additionally exposes:

`InboundAccessAuthorized`

which is explicitly documented as an internal proof that channel ingress admitted the sender/event.

At the same time, `reply_dispatch` carries the real dispatch `runId`.

Therefore v2026.9.4 provides a materially stronger single seam for CogentNexus:

`Finalized trusted owner context + exact runId + pre-model takeover capability`

This is stronger than the CNX-421 report's “prompt unavailable at reply_dispatch” interpretation.

## Architecture conclusion

The leading admission design is now:

`reply_dispatch -> shared Ticket admission kernel -> Ticket accept/route -> host model/harness dispatch`

with `before_agent_run` retained as a deeper idempotent/defense-in-depth boundary for runners that emit it.

For v2026.9.4, the early adapter should prefer explicit trust proof:

`InboundAccessAuthorized === true`

plus the applicable owner/channel/session constraints.

For compatibility with older 2026.7.1-2 behavior, `GatewayClientScopes` and existing authenticated Dashboard constraints may be characterized, but the migration should not weaken the v2026.9.4 trust contract merely to preserve old behavior.

Target invariant remains:

`NO TICKET = NO MODEL EXECUTION`

for eligible external owner turns.

## Current-version direction

OpenClaw v2026.9.4 is now materially favored as the target architecture because it improves the exact boundary CogentNexus needs:

- canonical inbound text is clearer;
- ingress authorization proof is explicit;
- dispatch/session ownership is more structured;
- `reply_dispatch` retains run correlation before normal model execution.

This does not authorize a live upgrade yet.

The next task must prove the design through TDD and isolated target-version qualification.

## Live residue note

The old pending delivery/direct-recovery rows are a live-state cleanliness concern, but they do not justify abandoning isolated qualification.

CNX-422 may use:

- a fresh isolated state;
- a copied state;
- or a copied state with explicitly characterized stale residue,

provided the live database/state is never mutated.

The residue should be treated as migration test input, not as a reason to skip isolated qualification.

## Successor authorization

Authorize CNX-422 to:

1. implement a RED characterization suite for a `reply_dispatch`-based shared admission kernel;
2. make the minimum source repair only after RED is proven;
3. prove GREEN across Ollama-style and Codex/plugin-harness dispatch paths without provider routing;
4. update the plugin development target to OpenClaw v2026.9.4 in an isolated qualification branch/worktree context as needed;
5. run isolated/fresh and copied-state v2026.9.4 plugin qualification;
6. characterize migration/rollback;
7. stop for ChatGPT review before any live upgrade.

No semantic provider request or live OpenClaw mutation is authorized in CNX-422.

## Reviewer

ChatGPT

Human final authority: Operator
