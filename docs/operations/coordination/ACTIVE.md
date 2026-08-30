# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `REPOSITORY_NATIVE_DELIVERY_STAGING_ROOT_CAUSE_REPAIR_HERMES`
Current authorization: `CNX-20260831-167_HERMES_NATIVE_DELIVERY_STAGING_ROOT_CAUSE_REPAIR`
Task ID: `CNX-20260831-167`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md`](tasks/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md)

Task 167 is the repository-only root-cause investigation + production-faithful RED + minimal TDD repair for the durable-delivery staging/marker failure proven by Task 166.

## Standing execution model

Hermes/Codex is the primary technical investigator and implementer. It must perform the deep source/upstream/test analysis itself and publish a report compliant with:

- `EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
- `EXECUTION_OWNERSHIP.md`
- `EXECUTOR_REPORT_CONTRACT.md`
- `CODEX_BOOTSTRAP.md`

ChatGPT will review the final verification packet and expand review depth only where evidence/risk requires it.

## Accepted Task-166 failure

Task-166 report:

`reports/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance.md`

ChatGPT review:

`reviews/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance-review.md`

Accepted disposition:

`FAIL — DURABLE_DELIVERY_STAGING_NOT_CAPTURED`

Empirical boundary established by Task 166:

- exactly one authorized semantic Dashboard Send;
- exactly one completed model call;
- exactly one correct visible/native assistant semantic result;
- native assistant delivery-marker count `0`;
- no `cnx_assistant_delivery` row staged;
- `delivery_confirmed_at=null`;
- Ticket failed closed with `durableDelivery:false`;
- no retry, recovery injection, second inference, or duplicate assistant result.

The accepted Task-164 repair commit remains:

`80b87dfbe0d9176e421f3748b4cee0827db12d0c`

Pinned OpenClaw remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`2026.7.1-2`).

## Current gate

Hermes/Codex must trace the exact production data flow and identify the source-level cause before editing production code.

Required order:

`Task-166 evidence -> exact pinned source/data-flow trace -> explicit root-cause hypothesis -> production-faithful RED -> minimal production repair -> targeted/full GREEN -> exact-SHA CI -> verification report`

Do not patch merely because the marker was absent. The RED must reproduce the real correlation/staging miss using the public hook/event/context shapes proven from the exact OpenClaw target.

## Hard fence

Repository-only.

No Dashboard semantic Send; no semantic input via another live OpenClaw surface; no `chat.inject`; no install-over/uninstall/reinstall/reset; no live Gateway/Ollama/Supervisor/OpenClaw mutation; no manual live Ticket/workflow/result/outbox/delivery/database/transcript mutation; no OpenClaw patch/fork/upgrade; no dependency upgrade; no unrelated product repair; no release/promotion; no default/release-branch merge; no force push.

Even Task-167 PASS does not authorize install-over or another Dashboard Send. ChatGPT review is required first, followed by a separate repaired-candidate Windows installation/provenance checkpoint.
