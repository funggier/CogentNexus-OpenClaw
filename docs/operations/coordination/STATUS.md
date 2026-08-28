# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_TDD_REPAIR`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 117 authorizes source/diagnosis/test/CI/package repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-117-installer-provider-binding-origin-repair.md`](tasks/CNX-20260828-117-installer-provider-binding-origin-repair.md)

Task ID:

`CNX-20260828-117`

## Task 116 accepted failure

Task-116 report:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate-review.md`

Verdict:

`ACCEPTED FAIL — CLEAN PRE-BODY PARAMETER-BINDING FAILURE; SUCCESSOR DIAGNOSIS/REPAIR REQUIRED`

Task 116 proved the live Windows state coherent and then stopped safely when its single install-over attempt failed before installer-body execution because the installer exposed a Provider parameter and PowerShell bound `3D Objects` to it. No destructive replay or later lifecycle phase occurred.

## Task 117 responsibility-locality gate

Task 117 now adopts the architectural invariant:

**A subsystem should define only information it actually needs to perform or verify its own responsibility.**

Provider selection is not installation responsibility. Therefore the target installer boundary is provider-neutral, not Ollama-hardcoded and not multi-provider aware.

Required Task-117 outcome:

- remove installer `Provider` parameter/ValidateSet/default;
- no provider auto-detection/inference;
- no direct provider executable prerequisite merely because runtime uses it;
- no provider-specific lifecycle argument from installer;
- no provider-specific installation completion claim;
- provider-free canonical install command/documentation;
- provider/runtime policy stays in the layer where it is actually needed;
- no new provider abstraction/fallback is added to installer.

This design decision does not claim current runtime support for LM Studio or another provider. It only removes unnecessary cross-layer provider coupling from installation.

Task 117 must still inspect preserved Task-116 evidence and trace the origin of `3D Objects` as far as evidence permits. Production repair must follow a tests-only RED that proves current installer violates the provider-neutral boundary.

Required order:

`preserved Task-116 evidence -> root-cause trace -> TESTS-ONLY RED -> minimal provider-neutral repair -> GREEN -> targeted/full validation -> exact candidate CI/package proof -> report`

## Live mutation fence

Task 117 does not authorize any live lifecycle mutation:

- no Task-116 install-over replay;
- no reset/uninstall/reinstall;
- no live stop/start/restart or recovery harness;
- no manual cleanup/normalization;
- no OpenClaw/provider-runtime changes;
- no provider/model/endpoint/timeout changes;
- no live SQLite/manifest/plugin/session mutation;
- no credential/secret access;
- no Dashboard semantic Send.

Read-only inspection of preserved Task-116 evidence and isolated Windows diagnostic reproduction is allowed.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

After publishing, stop for independent ChatGPT review. A new real-Windows lifecycle retry may be opened only after Task 117 passes independent review on an exact repaired candidate.
