# CNX-20260919-424 — Dual-Session Cross-Adapter Run Idempotency Repair

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260919-423`
- Reviewer decision: `REJECT_READY__DUAL_SESSION_ADAPTER_IDEMPOTENCY_REPAIR_REQUIRED`
- Parent report: `docs/operations/coordination/reports/CNX-20260919-423-reply-dispatch-provenance-and-acp-identity-semantics-repair-report.md`
- Parent review: `docs/operations/coordination/reviews/CNX-20260919-423-chatgpt-review.md`
- Executor: `ChatGPT via LConnect / authorized repository executor`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`

GitHub remote is authoritative.

## Objective

Repair cross-adapter idempotency for legitimate dual-session ACP dispatch.

One OpenClaw host run must produce one logical Ticket even when:

- `reply_dispatch` admits the run using source owner session identity;
- a later `before_agent_run` for the same run exposes the effective ACP target session.

Invariant:

`ONE HOST RUN -> ONE TICKET -> ONE ROUTE EVENT`

without collapsing source-owner and effective-dispatch identities.

## Stage 1 — RED

Before production change, add a regression that performs:

1. bound ACP `reply_dispatch`
   - source owner session A;
   - effective ACP session B;
   - runId R;

2. `before_agent_run`
   - session B;
   - same runId R;
   - same prompt.

Required assertions:

- Ticket count = 1;
- Ticket owner session = A;
- routed event count = 1.

Also retain controls proving:

- same-session cross-adapter idempotency remains one Ticket;
- `before_agent_run` alone still admits when no prior reply-dispatch admission exists.

Record exact RED output.

## Stage 2 — Minimal repair

Preferred repair:

- in `before_agent_run`, before shared Ticket admission, detect whether the exact real runId is already present in the in-process admitted-run fence populated by `reply_dispatch`;
- if already admitted, return/pass without second Ticket persistence;
- preserve existing run/session/workspace delivery correlation from the earlier reply-dispatch admission.

Do not:

- rewrite provider/model/harness;
- fabricate run IDs;
- weaken provenance exclusions;
- disable `before_agent_run` fallback for paths that do not emit `reply_dispatch`;
- change Ticket DB schema unless strictly necessary.

## Stage 3 — GREEN and regressions

Run at minimum:

- CNX-424 new regression;
- CNX-423 suite;
- CNX-422 suite;
- `index.test.ts`;
- Dashboard delivery;
- direct model-call lease;
- direct recovery;
- session ownership/generation;
- Discord Ticket/delivery regressions;
- package validation.

Run full plugin suite and characterize the historical CNX-383 RED separately.

## Stage 4 — OpenClaw v2026.9.4 target qualification

Against exact target 2026.9.4:

- build PASS;
- CNX-424/CNX-423/CNX-422 tests PASS;
- plugin load PASS;
- reply_dispatch registration PASS;
- isolated fresh Gateway reaches ready;
- health PASS;
- clean SIGINT shutdown PASS;
- semantic provider sends = 0.

CNX-422 copied-state migration/rollback evidence may be reused if no storage/schema/startup migration code changes.

## PASS classification

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_REVIEW`

## BLOCKED classification

`BLOCKED_DUAL_SESSION_CROSS_ADAPTER_IDEMPOTENCY_REPAIR`

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

## Required closeout

Publish:

`docs/operations/coordination/reports/CNX-20260919-424-dual-session-cross-adapter-run-idempotency-repair-report.md`

Set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify exact local/remote HEAD and clean worktree, then stop before live upgrade.
