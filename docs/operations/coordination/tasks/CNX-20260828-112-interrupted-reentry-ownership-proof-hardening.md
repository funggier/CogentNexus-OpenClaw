# CNX-20260828-112 — Interrupted Re-entry Ownership-Proof Hardening

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_ONLY_TDD`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Close the residual ownership-proof defect found by independent review of Task 111 before any live Windows acceptance is authorized.

Task 111 established the correct positive shape for re-entering the preserved Task-107 interrupted rollover when the retired manifest-owned plugin path is already missing and one exact replacement is active. The remaining defect is that the new shortcut proves the replacement child payload but does not prove npm-wrapper ownership when that replacement lives under OpenClaw's managed npm-project boundary.

This task is source/test/CI only. It does not authorize any real-Windows mutation.

## Authoritative predecessor evidence

Task-107 live report:

`docs/operations/coordination/reports/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`

Task-111 report:

`docs/operations/coordination/reports/CNX-20260828-111-interrupted-rollover-reentry-repair.md`

Task-111 independent review:

`docs/operations/coordination/reviews/CNX-20260828-111-interrupted-rollover-reentry-repair-review.md`

Task-111 source candidate:

`f4c8c993be80eaf54468f5b2630fd107050a1385`

Task-111 report-only descendant:

`2840f427b310a45d02b20419dc201de274fce56c`

Task-111 review verdict:

`REJECTED — RESIDUAL RE-ENTRY OWNERSHIP-PROOF DEFECT + INCOMPLETE NEGATIVE CONTRACT COVERAGE`

Task-111 artifact `9683680142` is historical proof only and is not live-authorized.

## Confirmed defect

At Task-111 source, `_classify_interrupted_rollover_reentry(...)` accepts a replacement using:

- `_active_registered_plugin(...)` for exact registration/payload and OpenClaw containment;
- `plugin_candidate_roots(...)` + `_plugin_payload(...)` for exact candidate counting.

For npm-project replacements, those checks prove the child plugin payload but do not prove the owning project wrapper.

The codebase already has the stricter normal-rollover proof:

- `_npm_project_for_plugin(...)` proves exact managed npm layout;
- `_managed_wrapper_proof(...)` rejects foreign package fields, undeclared dependencies, unapproved peers/overrides, lockfile mismatch, and invalid project naming.

A foreign/shared wrapper may therefore contain an exact child CogentNexus payload and satisfy the Task-111 shortcut even though unrelated user-owned dependency evidence exists in the same wrapper.

This violates the no-generic-adoption and no-shared-wrapper invariant.

## Required invariant

The interrupted-rollover re-entry shortcut may accept an active replacement only when its storage/ownership boundary is exact:

### Direct extension case

A direct replacement may be accepted only when its active root is exactly the canonical product extension path under OpenClaw state:

`<openclaw-state>/extensions/cogentnexus-openclaw`

It must still satisfy all Task-111 id/package/version/payload/fingerprint/uniqueness checks.

### Managed npm-project case

If the active replacement is under:

`<openclaw-state>/npm/projects/<project>/node_modules/openclaw-plugin-cogentnexus-openclaw`

then re-entry must additionally prove the exact wrapper using the existing managed-wrapper contract. Foreign/shared wrappers must fail closed.

### All other storage shapes

Any other contained-but-noncanonical active root must remain non-zero/fail-closed.

No shortcut may adopt unrelated user-owned data merely because the child payload is exact.

## Phase 0 — Reconcile current repository

Before editing:

1. fetch current remote branch HEAD;
2. confirm Task 112 is active in both `ACTIVE.md` and `STATUS.md`;
3. read Task-107 report, Task-111 report, and Task-111 independent review;
4. compare production/test source with candidate `f4c8c993be80eaf54468f5b2630fd107050a1385` and stop `BLOCKED` on unexplained production drift;
5. inspect completely:
   - `_classify_interrupted_rollover_reentry`;
   - `_active_registered_plugin`;
   - `plugin_candidate_roots`;
   - `_npm_project_for_plugin`;
   - `_managed_wrapper_proof`;
   - `classify_install`;
   - installer action selection and final `resolve-plugin -> ownership create -> verify` path;
   - current rollover and namespace tests.

No live machine action.

## Phase 1 — Separate TEST-ONLY RED commit

The first Task-112 implementation commit must contain tests only. Push it before any production edit.

### Mandatory RED — foreign/shared npm wrapper

Create a production-shaped Task-107 re-entry fixture:

1. coherent v0.9.3 manifest/controller/skill/launcher;
2. retired manifest-owned old npm generation specifically missing;
3. exactly one active replacement child payload matching the candidate fingerprint;
4. replacement child located under an npm project whose wrapper also contains an unrelated dependency or otherwise violates `_managed_wrapper_proof`;
5. no second canonical product payload;
6. call actual `classify_install(...)` with real plugin inventory and expected fingerprint.

Current Task-111 candidate is expected to incorrectly return:

- `mode=upgrade`;
- `pluginAlreadyExact=True`;
- `interruptedRolloverReentry=True`.

Desired repaired behavior: `RuntimeError` / non-zero fail-closed before installer mutation.

The RED must fail semantically on the actual classification result, not by source-string matching.

### Focused negative re-entry matrix

In the same test-only commit, add direct `classify_install(...)` coverage for the Task-111 shortcut rejecting at least:

- foreign/shared npm wrapper;
- more than one canonical product payload;
- non-unique active registration;
- active root outside OpenClaw state;
- wrong id/package/version;
- controller mode other than `passthrough`;
- corrupted or mismatched ownership manifest metadata;
- missing `SKILL.md`;
- missing launcher;
- mixed legacy/new namespace.

Cases that already fail under current source may pass immediately in the RED commit; that is acceptable. The mandatory foreign/shared-wrapper case must demonstrate the real current defect.

Also retain explicit coverage that an exact canonical direct extension replacement remains valid.

### RED evidence

Record:

- test-only commit SHA;
- exact failing selector/command;
- exit code;
- failing assertion/output proving the foreign/shared wrapper is incorrectly accepted.

Do not edit production before this evidence exists in Git history.

## Phase 2 — Minimal production repair

Implement the smallest boundary proof necessary.

Preferred surface:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

Use existing ownership helpers rather than duplicating wrapper rules.

Expected design:

1. after `_active_registered_plugin(...)` proves the active payload, determine its canonical storage shape;
2. if root equals the exact direct extension path, accept that storage boundary;
3. if root is an exact npm-project child path, call the existing `_npm_project_for_plugin(...)` / `_managed_wrapper_proof(...)` contract and require success;
4. otherwise fail closed;
5. only after storage ownership proof continue candidate-count/fingerprint re-entry acceptance.

Do not weaken `_managed_wrapper_proof` to make the new test pass.

Do not introduce mutation into classification.

Do not change Task-111's valid missing-retired-path requirement, passthrough requirement, candidate attestation, uniqueness, or no-second-install behavior.

Do not change Task-110 retired-state finalization checks.

## Phase 3 — GREEN targeted validation

Run at minimum:

1. all direct interrupted re-entry tests including the new negative matrix;
2. all `tests/test_plugin_generation_rollover.py`;
3. `tests/test_installer_transaction_wiring.py`;
4. namespace install/ownership contract tests;
5. fresh transaction recovery/rollback tests;
6. npm-12 local archive boundary tests;
7. plugin lifecycle action resolver tests.

Explicitly prove:

- exact direct extension Task-107-style re-entry remains accepted;
- exact managed npm wrapper may be accepted when all wrapper proof passes;
- foreign/shared wrapper is rejected;
- no redundant external install is selected for valid `pluginAlreadyExact=True` re-entry.

Record exact commands and counts.

## Phase 4 — Full repository validation

Run full repository validation and record exact results:

- full pytest suite;
- Python compile for modified ownership source;
- installer AST/lifecycle analysis;
- `npm ci`;
- `npm run plugin:validate`;
- `git diff --check`.

No PASS from targeted tests alone.

## Phase 5 — Exact same-source CI/package proof

Push one exact GREEN candidate and require all three workflows successful for that same SHA:

- Validate;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

Obtain a new package-proof artifact from that exact candidate. Do not reuse artifact `9683680142`.

Record and independently verify:

- candidate SHA;
- artifact ID/name;
- outer artifact SHA256/digest;
- inner v0.9.3 ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source/version;
- payload count/fingerprint;
- packaged re-entry storage-boundary proof;
- packaged Task-110 retired-state exactness proof;
- installer local archive invocation remains `openclaw plugins install $packagePath --force` when installation is actually required;
- recovery harness Git blob identity remains recorded.

## Phase 6 — Report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-112-interrupted-reentry-ownership-proof-hardening.md`

The report must include:

- exact root cause;
- separate test-only RED commit and failure;
- negative matrix outcomes;
- minimal production fix commit/files;
- GREEN targeted/full results;
- exact CI candidate and run IDs;
- new artifact identities/hashes/fingerprint;
- residual uncertainty;
- final `PASS`, `FAIL`, or `BLOCKED`.

After report publication, stop for independent ChatGPT review. Do not create or execute a real-Windows task.

## Hard fence — NOT authorized

Task 112 does not authorize:

- any real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery action;
- replay of Task 107;
- manual cleanup/normalization of Task-107 residue;
- Dashboard semantic Send;
- OpenClaw/Ollama update, reinstall, uninstall, stop, or rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/tokens/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening wrapper, namespace, manifest, or ownership validation.

If the re-entry shortcut cannot prove storage ownership without broad adoption, publish `BLOCKED` rather than weaken the boundary.
