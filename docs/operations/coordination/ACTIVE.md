# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX421_READY_FOR_HERMES`
Execution mode: `REPOSITORY_REPAIR_AND_ISOLATED_CURRENT_OPENCLAW_QUALIFICATION`
Task ID: `CNX-20260918-421`
Parent: `CNX-20260918-420`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Parent report: `docs/operations/coordination/reports/CNX-20260918-420-operator-fresh-session-ollama-route-ticket-first-discrimination-report.md`
Parent review: `docs/operations/coordination/reviews/CNX-20260918-420-chatgpt-review.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260918-421-openclaw-current-upgrade-qualification-and-harness-agnostic-ticket-first-admission.md`
Expected report: `docs/operations/coordination/reports/CNX-20260918-421-openclaw-current-upgrade-qualification-and-harness-agnostic-ticket-first-admission-report.md`

## Current position

CNX-420 is accepted PASS for the Operator-created fresh Ollama session:

`PASS_OPERATOR_FRESH_SESSION_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

It proved one complete Ticket-first lineage through `ollama/qwen3.8:27b`.

CNX-419 remains valid evidence that the Codex/OpenAI plugin-harness path can bypass the current `before_agent_run` admission boundary. Therefore the next problem is architectural coverage, not another semantic retry.

The Operator has authorized moving toward the current OpenClaw generation when its structure is materially better. CNX-421 will qualify upstream `v2026.9.4` against the installed `2026.7.1-2` baseline and prove a harness-agnostic, run-correlated Ticket-first admission seam before any live upgrade.

The CNX-420 model-call duration anomaly remains open: `44m 42.699s` completion despite an emitted 15-minute deadline.

## Current authorization

Hermes may begin CNX-421 immediately.

Allowed:

- exact upstream/source characterization;
- repository tests/docs;
- TDD repository repair candidate when the seam is proven;
- isolated/copy-state OpenClaw v2026.9.4 compatibility qualification;
- read-only live baseline inspection.

Not allowed:

- semantic send;
- live OpenClaw upgrade;
- live session/transcript migration;
- live provider/model mutation;
- live plugin install-over/uninstall;
- live Gateway restart for upgrade;
- release/tag/main;
- force push/history rewrite.

## Required target

Preserve OpenClaw as provider/model authority while moving CogentNexus Ticket admission ahead of harness-specific model execution.

Target invariant for eligible external owner turns:

`NO TICKET = NO MODEL EXECUTION`

Do not call a seam universal until the required reachability matrix proves coverage.

## Closeout

Publish the CNX-421 report, set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`, verify exact local/remote HEAD and a clean publication worktree, then stop. Do not perform the live upgrade or create its successor before ChatGPT review.
