# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_ONLY_TDD`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 113 authorizes source/test/CI repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md`](tasks/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md)

Task ID:

`CNX-20260828-113`

## Task 112 closure

Task-112 report:

`docs/operations/coordination/reports/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md`

Task-112 independent review:

`docs/operations/coordination/reviews/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening-review.md`

Review commit:

`ee3f0dca79929ce771add3381d1817766b2ff8f7`

Review verdict:

`REJECTED — RESIDUAL CONFLICTING-WRAPPER RE-ENTRY DEFECT + REQUIRED MATRIX NOT COMMITTED`

## Accepted historical facts from Task 112

Task 112 correctly closed the active-wrapper storage proof defect:

- test-only RED `bb8212584b1b7934cc2d9e1d7bc6b5e0303699f2`;
- production candidate `023be1a8075c0aa602adda357db9924c170ffb8e`;
- exact Validate run `33167878659` successful on attempt 2;
- exact Windows Installer Pack Smoke `33167878626` success;
- exact PS5.1 Acceptance Smoke `33167878630` success;
- artifact `9684336683` bound to exact candidate;
- independently verified outer SHA256 `2be47e00db355be28a782096bd1ab866c787b768f8eb0c3ecaa131a3802e91bf`;
- inner ZIP `2240348a163c356fc7958c04f645b9a1f406db6c842fdbd86b4dd3efdeecc8c5`;
- tar.gz `b6433b4a6c3d91a6185b3048146243b079b66015d5f7a76564ddf726fc4e81e0`;
- payload count `178`, fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- recovery harness Git blob `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

These remain historical reproducibility evidence only; candidate/artifact are not accepted for live Windows use.

## Confirmed Task-113 defect

The current re-entry shortcut proves the one **active** replacement storage boundary but does not prove that all other CogentNexus-specific OpenClaw storage evidence is absent or attributable to it.

Independent production-shaped reviewer tests against exact Task-112 packaged source showed:

- valid managed-npm active replacement alone -> accepted;
- valid canonical direct active replacement alone -> accepted;
- active replacement inside foreign/shared wrapper -> rejected;
- duplicate registration/out-of-bound root/wrong identity or version/wrong mode/bad manifest/missing skill/missing launcher/mixed legacy/second exact payload -> rejected;
- **valid active replacement + separate foreign/shared `npmWrapper:*` product evidence -> incorrectly accepted**.

The defect reproduces for both managed-npm and canonical-direct active replacement shapes. The direct shape matches Task-107 evidence: OpenClaw installed the replacement to `~\.openclaw\extensions\cogentnexus-openclaw` before the old rollover failed.

## Missing Task-112 contract evidence

Task 112 required its RED commit to add the complete direct `classify_install(...)` negative matrix plus explicit direct-extension success coverage. Git history shows the RED commit added only the active foreign/shared-wrapper case. Existing older rollover tests are not equivalent to direct coverage of the new early-return re-entry surface.

Task 113 must close both the source defect and the missing matrix in one strict TDD sequence.

## Authorized Task-113 sequence

Only source/test/CI work is authorized:

`reconcile -> separate TEST-ONLY direct matrix commit -> direct+managed conflicting-wrapper RED -> minimal exact product-evidence proof -> GREEN -> full validation -> exact Actions/package proof -> report`

For a valid re-entry, all CogentNexus-specific storage evidence must be exactly attributable to:

- the canonical direct extension only; or
- one exact managed npm child plus its exact proven wrapper only.

Any additional direct/npm-package/npm-wrapper CogentNexus evidence is ambiguous and must fail closed without mutation or cleanup.

## Preserved live boundary

No live mutation is authorized by Task 113. Task 107 remains the last authoritative machine evidence. A future real-Windows task must re-prove the current machine state read-only before mutation; it must not assume the historical residue still exists.

## Hard fence

Task 113 does **not** authorize:

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
- weakening namespace, wrapper, manifest, payload, ownership, or final verification.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md`

The report must include the separate test-only matrix commit, exact RED A/B evidence, complete direct matrix results, minimal production fix, targeted/full validation, exact candidate, exact workflow runs/attempts, and a new package-proof artifact identity/hashes/fingerprint.

After report publication, stop for independent ChatGPT review. No real-Windows lifecycle acceptance is authorized until that review accepts a new exact candidate.
