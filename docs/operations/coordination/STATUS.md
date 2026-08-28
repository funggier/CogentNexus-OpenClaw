# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_ONLY_TDD`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 112 authorizes source/test/CI repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md`](tasks/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md)

Task ID:

`CNX-20260828-112`

## Task 111 closure

Task-111 report:

`docs/operations/coordination/reports/CNX-20260828-111-interrupted-rollover-reentry-repair.md`

Task-111 independent review:

`docs/operations/coordination/reviews/CNX-20260828-111-interrupted-rollover-reentry-repair-review.md`

Review verdict:

`REJECTED — RESIDUAL RE-ENTRY OWNERSHIP-PROOF DEFECT + INCOMPLETE NEGATIVE CONTRACT COVERAGE`

Task 111 did establish several accepted facts:

- test-only RED `a7dace1ed86580c6ab39d72283eace3d7e76a02d`;
- source candidate `f4c8c993be80eaf54468f5b2630fd107050a1385`;
- exact Validate `33166203340` success;
- exact Windows Installer Pack Smoke `33166203285` success;
- exact PS5.1 Acceptance Smoke `33166203316` success;
- artifact `9683680142` bound to that source;
- independently verified outer SHA256 `096b194423b83d14adf4dd26eb000612d53d31ef3f7f8c5385eb00e74756b422`;
- inner ZIP SHA256 `9ebbaac9c222f79d2291b6dfeb54791777abe1052b9c71614a9cff21239ade2e`;
- tar.gz SHA256 `503be3b917993ce3d22d5ca8f5bb8bc878eee0b8048582e52c9dd6b13c1a483e`;
- payload count `178`, fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- recovery harness Git blob `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

These are historical reproducibility facts only. Candidate/artifact are not accepted for live Windows use.

## Confirmed Task-112 gap

The Task-111 shortcut accepts a valid missing-retired-generation state by proving one active replacement payload and its candidate fingerprint. For npm-project replacements, however, the shortcut does not call the strict managed-wrapper ownership proof used by normal rollover.

`plugin_candidate_roots(...)` enumerates npm child payloads regardless of wrapper ownership. `_active_registered_plugin(...)` validates the child payload and registration but not the containing npm wrapper. An exact child payload inside a wrapper with unrelated/foreign dependency evidence can therefore be accepted as `interruptedRolloverReentry=True`.

Task 112 must close this without rejecting the legitimate direct canonical extension shape used by supported OpenClaw installation.

## Authorized Task-112 sequence

Only source/test/CI work is authorized:

`reconcile -> separate TEST-ONLY RED commit -> foreign/shared-wrapper semantic RED -> focused re-entry negative matrix -> minimal storage-boundary proof -> GREEN -> full validation -> exact Actions/package proof -> report`

Required valid storage shapes:

- exact direct product extension path under OpenClaw state; or
- exact managed npm child whose wrapper passes the existing `_npm_project_for_plugin/_managed_wrapper_proof` contract.

All other contained/noncanonical/foreign/shared states remain fail-closed.

The focused negative matrix must exercise the actual new `classify_install(...)` early-return surface for wrapper ownership, duplicate/ambiguous state, out-of-bound root, wrong identity/version, wrong controller mode, bad manifest metadata, missing skill/launcher, and mixed legacy state.

## Preserved live boundary

No live mutation is authorized by Task 112. Task 107 remains the last authoritative machine evidence. A future live acceptance must re-prove current machine state read-only before any mutation.

## Hard fence

Task 112 does **not** authorize:

- real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery;
- replay of Task 107;
- manual cleanup/normalization;
- Dashboard semantic Send;
- OpenClaw/Ollama update, reinstall, uninstall, stop, or rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening wrapper, namespace, manifest, or ownership verification.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md`

The report must include the separate RED commit, exact semantic failure, negative matrix, minimal production fix, GREEN/full validation, exact candidate, exact three workflow run IDs, and a new package-proof artifact identity/hashes/fingerprint.

After report publication, stop for independent ChatGPT review. No real-Windows lifecycle acceptance is authorized until a reviewed candidate passes this gate.
