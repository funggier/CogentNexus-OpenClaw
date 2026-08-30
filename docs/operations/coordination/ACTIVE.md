# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE_HERMES`
Current authorization: `CNX-20260831-166_HERMES_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE`
Task ID: `CNX-20260831-166`
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

[`tasks/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance.md`](tasks/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance.md)

Task 166 is the controlled exactly-one-Send Dashboard durable-delivery reacceptance against the repaired candidate proven installed by Task 165.

## Standing execution model

Hermes/Codex is the primary technical investigator and implementer for this delegated task. It must perform the deep correlation/analysis itself and publish a report compliant with:

- `EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
- `EXECUTION_OWNERSHIP.md`
- `EXECUTOR_REPORT_CONTRACT.md`
- `CODEX_BOOTSTRAP.md`

ChatGPT will verify the critical report claims and expand review depth only if evidence/risk requires it.

## Accepted parent checkpoints

Task 164 repository repair:

`PASS — REPOSITORY_NATIVE_TRANSCRIPT_AUTHORITY_REPAIR_ACCEPTED`

Accepted production repair SHA:

`80b87dfbe0d9176e421f3748b4cee0827db12d0c`

Task 165 Windows install-over/provenance/health:

`PASS — REPAIRED_CANDIDATE_WINDOWS_INSTALL_OVER_PROVENANCE_HEALTH_ACCEPTED`

Task-165 report:

`reports/CNX-20260830-165-hermes-windows-install-over-provenance-health.md`

Task-165 review:

`reviews/CNX-20260830-165-hermes-windows-install-over-provenance-health-review.md`

Accepted installed plugin fingerprint:

`5b23040f26ab1148c44647429cc5eff0ef89505e2f068b72d41d9a5fb0ee02e5`

Intended OpenClaw target remains `2026.7.1-2`.

## Current gate

Hermes/Codex must first re-read fresh remote state and prove the installed candidate/health still matches the accepted Task-165 checkpoint.

If preflight is valid, Task 166 authorizes **exactly one semantic Dashboard Send** using a unique nonce, followed by read-only deep analysis of UI, Ticket/model-call state, durable delivery, native transcript marker/persistence, recovery/duplicate safety, and post-test health.

After the one Send, there is no retry authorization under any outcome.

## Hard fence

Exactly one Dashboard semantic Send is authorized.

No second/retry Send; no semantic input via another live surface; no `chat.inject`; no manual Ticket/workflow/result/outbox/delivery/database mutation; no transcript editing; no install/uninstall/reinstall/reset; no independent Gateway/Ollama/Supervisor restart for acceptance convenience; no production/source repair; no OpenClaw/dependency upgrade; no unrelated change; no release/promotion; no default/release-branch merge; no force push.

If a defect is observed, preserve evidence, analyze it deeply, publish the Task-166 report, and stop. Do not repair or resend inside Task 166.
