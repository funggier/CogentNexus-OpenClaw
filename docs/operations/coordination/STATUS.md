# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_ONLY_TDD`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 110 authorizes source/test/CI repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-110-rollover-retired-state-exactness-repair.md`](tasks/CNX-20260828-110-rollover-retired-state-exactness-repair.md)

Task ID:

`CNX-20260828-110`

## Task 109 closure

Task 109 report:

`docs/operations/coordination/reports/CNX-20260828-109-rollover-finalize-failclosed-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-109-rollover-finalize-failclosed-repair-review.md`

Review verdict:

`REJECTED — TDD PROVENANCE FAILURE + RESIDUAL RETIRED-STATE EXACTNESS DEFECT`

The Task-109 candidate `dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce` passed its reported CI/package proof, but it is not accepted for live Windows use.

Two independent reasons block it:

1. Task 109 required a separate test-only RED commit; Git history instead shows `dcca49d4...` directly following the Task-109 coordination HEAD and changing production plus test in one commit.
2. Task-109 failure handling restores `manifestBefore` whenever `retiredProjectRoot` merely exists. The transaction already records the exact retired project tree hash, so existence does not prove the retired state is still the exact pre-mutation generation.

## Confirmed Task-110 defect

The remaining unsafe boundary is:

`retired path still present but retired project changed/incomplete -> final replacement verification fails -> current code sees exists() -> restores old normal manifest`

This can reassert durable ownership without re-proving the old state that the manifest originally described.

Task 110 must use exact transaction evidence for any restoration decision. If the old state cannot be proven exact, normal ownership must remain quarantined/fail-closed.

## Authorized Task-110 sequence

Only source/test/CI work is authorized:

`reconcile remote -> separate test-only RED commit -> prove semantic RED -> minimal exactness repair -> GREEN targeted -> full validation -> exact same-candidate Actions/package proof -> report`

The RED must leave the old project directory present while changing/incompleting its tree after prepare, then inject final ownership verification failure and prove the current source restores `manifestBefore` incorrectly.

The RED commit must be pushed separately before production source is changed.

## Source boundary

Reviewed Task-109 source candidate:

`dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce`

Task-109 report-only descendant before Task-110 coordination:

`2b198632bc2cbe7b485ce56e0ac046b0ceb545e7`

Executor must fetch current GitHub state before editing and stop `BLOCKED` on unexplained production drift.

## Historical package proof — not live-authorized

Task-109 evidence includes artifact `9681526010`, bound to source `dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce`.

It is historical evidence only. Task 110 must produce a new exact package proof after the exactness repair.

## Preserved live boundary

No new live action was authorized or performed during Tasks 108–109/reviews. The last recorded machine boundary remains Task-107 post-failure evidence. Task 110 must not touch or normalize that live state.

## Hard fence

Task 110 does **not** authorize:

- any real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery action;
- replaying Task 107/109;
- manual live cleanup/normalization;
- Dashboard semantic Send;
- OpenClaw/Ollama update, reinstall, uninstall, stop, or rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening ownership validation.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-110-rollover-retired-state-exactness-repair.md`

The report must include the separate RED commit and exact RED failure, root cause, minimal production fix commit/files, GREEN targeted/full validation, exact GREEN candidate, exact three workflow run IDs/results, and a new package-proof artifact identity/hashes/fingerprint.

After report publication, stop for independent ChatGPT review. No real-Windows lifecycle acceptance task is authorized until that review accepts a new exact candidate.
