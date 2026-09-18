# CNX-20260919-423 — Reply-Dispatch Provenance and ACP Identity Semantics Repair

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-422`
- Reviewer decision: `REJECT_READY__ADMISSION_SEMANTICS_REPAIR_REQUIRED`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-422-reply-dispatch-ticket-first-repair-and-openclaw-2026-9-4-isolated-qualification-report.md`
- Parent review: `docs/operations/coordination/reviews/CNX-20260918-422-chatgpt-review.md`
- Executor: `Hermes / authorized repository executor`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`

GitHub remote is authoritative.

## Objective

Repair the two admission-semantics defects found in CNX-422 review without changing provider/model/harness ownership:

1. internal/inter-session/control/recovery turns must not be admitted as fresh external-owner Tickets;
2. legitimate ACP retargeting must distinguish source owner session from effective dispatch session rather than treating every mismatch as contradictory identity.

Target invariant remains:

`NO TICKET = NO MODEL EXECUTION`

for **eligible external owner turns only**.

Internal/control/recovery/inter-session turns must preserve their existing host authority and must not be converted into fresh owner intent.

## Established OpenClaw v2026.9.4 facts to re-verify

### Provenance

`FinalizedMsgContext` exposes:

- `InputProvenance`;
- `InternalTurnSource`;
- `InboundAccessAuthorized`;
- `GatewayClientScopes`;
- source `SessionKey`.

`InputProvenance.kind` distinguishes:

- `external_user`;
- `inter_session`;
- `internal_system`.

OpenClaw restart recovery uses:

- `kind="internal_system"`;
- `sourceTool="restart-sentinel"`;
- privileged Gateway scopes;
- owner/canonical session key.

Privileged host scope does not turn internal recovery into external owner intent.

### ACP retargeting

`reply_dispatch.event.sessionKey` is the effective dispatch session.

For bound ACP routing it may differ legitimately from:

`reply_dispatch.event.ctx.SessionKey`

which remains the source owner session.

## Stage 1 — TDD RED matrix

Before production source changes, add focused RED regressions proving all of the following:

1. restart-sentinel internal recovery with `operator.admin` scope creates no ordinary Ticket and is not claimed by owner admission;
2. generic `internal_system` provenance is excluded;
3. `inter_session` subagent completion into an owner session is excluded;
4. valid source-owner -> bound ACP retargeting is accepted as a legitimate dual-session relation;
5. Ticket owner session is the source external-owner session;
6. the effective ACP target identity remains available to the host and is not rewritten by CogentNexus;
7. genuinely contradictory identity for the same semantic role still fails closed;
8. external Dashboard/Codex-style dispatch remains Ticket-first;
9. external Dashboard embedded dispatch remains Ticket-first;
10. reply_dispatch + before_agent_run remains one Ticket / one route event;
11. direct stays direct;
12. durable stays pre-inference claimed;
13. missing/untrusted external-owner ingress fails closed;
14. provider/model/harness values remain unchanged.

Record exact RED output.

## Stage 2 — minimal repair

Make the smallest source change needed.

Preferred design:

`reply_dispatch adapter -> classify provenance/control path -> normalize source-owner identity + effective-dispatch identity -> shared admission kernel`

Rules:

- explicit `InputProvenance.kind="internal_system"` is not external-owner intent;
- explicit `InputProvenance.kind="inter_session"` is not ordinary external-owner intent;
- known control/recovery source tools remain excluded;
- `InternalTurnSource` remains excluded when applicable;
- `InboundAccessAuthorized=true` proves ingress authorization only for an applicable external-owner turn;
- Gateway scopes are compatibility authority facts, not a substitute for external-user provenance when provenance explicitly says internal/inter-session;
- source/effective session difference caused by ACP binding is not itself a conflict;
- no fake run IDs;
- no provider/model/harness routing in CogentNexus.

Do not weaken existing delivery/continuation/direct-recovery exclusions.

## Stage 3 — GREEN and regressions

Run at minimum:

- new CNX-423 regressions;
- CNX-422 admission suite;
- `index.test.ts`;
- Dashboard delivery;
- direct model-call lease;
- direct recovery;
- session ownership/generation;
- Discord Ticket/delivery regressions;
- package build/typecheck/validation.

Run broader plugin suite and characterize the known CNX-383 RED separately.

## Stage 4 — OpenClaw v2026.9.4 target qualification

Against exact v2026.9.4:

- TypeScript compile PASS;
- public SDK imports resolve;
- candidate plugin loads;
- `reply_dispatch` registration succeeds;
- deterministic ACP/source-owner identity tests PASS;
- deterministic internal/control provenance tests PASS;
- fresh isolated Gateway reaches ready and shuts down cleanly;
- semantic provider sends remain zero.

The CNX-422 copied-state migration/rollback evidence may be reused if this task does not change storage/startup/migration behavior. If the repair changes those boundaries, rerun the affected isolated migration proof.

## Final classification

Use one:

### PASS

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_REVIEW`

Requires every CNX-423 RED to be GREEN and no new regression.

### BLOCKED

`BLOCKED_REPLY_DISPATCH_PROVENANCE_OR_ACP_IDENTITY_REPAIR`

## Hard fences

- semantic sends: 0;
- external provider probes: 0;
- browser mutation: 0;
- live OpenClaw upgrade: 0;
- live session/state migration: 0;
- live provider/model mutation: 0;
- live plugin lifecycle mutation for upgrade: 0;
- manual live Ticket/outbox/recovery/SQLite mutation: 0;
- release/tag/main: 0;
- force push/history rewrite: 0.

Repository source/tests/docs changes on the working branch are authorized.

## Required closeout

Publish:

`docs/operations/coordination/reports/CNX-20260919-423-reply-dispatch-provenance-and-acp-identity-semantics-repair-report.md`

Then set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify exact local/remote HEAD and clean worktree, and stop before any live upgrade.
