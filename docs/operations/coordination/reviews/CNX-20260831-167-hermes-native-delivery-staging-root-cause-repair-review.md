# CNX-20260831-167 — ChatGPT Review

Disposition: `REWORK_REQUIRED — EVIDENCE_CONTRACT_INCOMPLETE`

Reviewer: ChatGPT

Reviewed repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`

Reviewed report: `docs/operations/coordination/reports/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md`

## Review model

This review follows the executor-heavy / reviewer-light policy. ChatGPT does not reconstruct the full source investigation by default. The executor report is treated as the primary technical argument; ChatGPT verifies whether its critical claims and mandatory evidence satisfy the active task contract.

## What is accepted so far

The report provides a coherent root-cause hypothesis tied to the Task-166 empirical failure: the prior Task-164 model assumed `before_agent_finalize` supplied the final candidate before `before_message_write`, while the pinned production lifecycle places the native pre-write hook/persistence before the later terminal finalize boundary.

The report also supplies a production-shaped regression using the order:

`before_message_write -> native transcript update -> before_agent_finalize`

and records a pre-repair RED followed by local GREEN. The proposed repair is narrow and keeps settlement on the post-persistence transcript-update boundary rather than claiming delivery from the pre-write hook.

These points are sufficient to continue verification. They are not yet sufficient for final Task-167 acceptance.

## Blocking evidence gaps

The active Task-167 contract explicitly requires the report to include the following. The published report does not yet provide them completely:

1. `npm run build` result on the repair candidate;
2. `npm run plugin:validate` result;
3. baseline consistency validation required by the repository;
4. required package/installer validation appropriate to the changed source;
5. exact-SHA GitHub workflow IDs and final results for:
   - Validate;
   - Windows Installer Pack Smoke;
   - PS5.1 Acceptance Smoke;
6. an acceptance matrix covering every Task-167 criterion;
7. material alternatives/hypotheses rejected and contradictions encountered;
8. risk analysis including crash windows, duplicate/recovery safety, and ambiguity from session-based fallback correlation;
9. residual uncertainty;
10. the mandatory Reviewer Verification Packet containing 3–10 critical claims, each with an exact evidence pointer and narrow independent check.

At review time the exact repair SHA has three push workflows. PS5.1 Acceptance Smoke run `33330458475` is already `success`; Validate run `33330458434` and Windows Installer Pack Smoke run `33330458470` were still `in_progress`. Final acceptance cannot be claimed from incomplete exact-SHA CI.

## Important review boundary

This disposition does **not** reject the root-cause hypothesis or production repair. It rejects only the completeness of the acceptance evidence/report at this checkpoint.

ChatGPT is intentionally not expanding into a full source-level re-investigation while the executor-side verification packet is missing.

## Required next action

Use a separate verification-completion task against exact product repair SHA:

`231761fca24c315e90536955d3e384f55e2e232e`

The next task should be verification/report completion only by default. It must not modify production source merely to improve the report. If any required validation fails or new evidence contradicts the root-cause/repair claim, report that contradiction and stop for review rather than silently changing the product candidate.

No Windows install-over and no semantic Dashboard Send are authorized by this review.
