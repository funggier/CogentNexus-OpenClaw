# CNX-20260828-114 — Interrupted Re-entry Direct Matrix Validation

- Status: `READY_FOR_HERMES`
- Execution mode: `TEST_MATRIX_GATE`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Goal

Complete the direct `classify_install(...)` interrupted-rollover re-entry matrix that Task 113 required but did not commit, while preserving the already-supported Task-113 source repair unless the new matrix exposes an actual defect.

This is a validation-first repository task. It does not authorize live Windows mutation.

## Authoritative predecessor evidence

Task-113 report:

`docs/operations/coordination/reports/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure.md`

Task-113 independent review:

`docs/operations/coordination/reviews/CNX-20260828-113-interrupted-reentry-conflicting-wrapper-matrix-closure-review.md`

Task-113 source candidate:

`d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`

Task-113 report descendant:

`20d2734a4ae62086d8af3ca2768f9c844361fbf7`

Task-113 review verdict:

`SOURCE REPAIR ACCEPTED; TASK COMPLETION BLOCKED — REQUIRED DIRECT CLASSIFY_INSTALL MATRIX INCOMPLETE`

Task-113 artifact `9685376213` is historical source/package evidence only until Task 114 closes this gate.

## Core rule

The first and only implementation commit before validation must be **tests only** and must contain the complete direct matrix below.

Do not edit production source preemptively.

After committing/running the complete matrix:

- if every case is GREEN on current production, no production edit is authorized or needed;
- if any case is RED because current behavior violates the stated invariant, that same tests-only commit is legitimate RED evidence, and only then may a separate minimal production repair commit follow;
- if a test fails because the fixture/test is wrong rather than production, repair the test while remaining tests-only and document why.

Never fabricate retroactive TDD evidence.

## Phase 0 — fresh reconcile

Before editing:

1. fetch current remote branch HEAD;
2. confirm Task 114 is active in both `ACTIVE.md` and `STATUS.md`;
3. read Task-107 report, Task-113 report, and Task-113 independent review;
4. compare production source with candidate `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06` and stop `BLOCKED` on unexplained production drift;
5. inspect current direct re-entry helpers/tests and the complete `_classify_interrupted_rollover_reentry(...)` path;
6. no live machine action.

## Phase 1 — complete TEST-ONLY direct matrix commit

Modify tests only, preferably:

`tests/test_plugin_generation_rollover.py`

Helpers may be added in the same test file to avoid duplication.

Every case below must call the actual production `classify_install(...)` surface. Source-string/order-only tests do not satisfy this task.

### Positive cases

Add explicit direct cases proving:

1. canonical direct extension + no conflicting product evidence -> accepted;
2. exact managed npm child + its exact proven wrapper + no conflicting evidence -> accepted.

Both must assert all four result fields:

```text
mode == "upgrade"
pendingRollover is False
pluginAlreadyExact is True
interruptedRolloverReentry is True
```

Also assert `replacementPluginPath` equals the active replacement and `manifestPluginPath` remains the missing retired manifest path.

### Required negative matrix

Commit direct `classify_install(...)` coverage for all of these:

1. active replacement itself is inside a foreign/shared wrapper;
2. valid direct active replacement + separate conflicting CogentNexus wrapper;
3. valid managed active replacement + separate conflicting CogentNexus wrapper;
4. more than one exact canonical product payload;
5. non-unique active registration in supplied OpenClaw inventory;
6. active root outside OpenClaw state;
7. active root contained by OpenClaw state but not a canonical direct path or exact managed npm child;
8. wrong plugin id;
9. wrong package name when inventory supplies package identity;
10. wrong installed version;
11. candidate fingerprint mismatch;
12. controller mode not `passthrough`;
13. ownership manifest metadata corrupted or mismatched;
14. required `SKILL.md` missing;
15. launcher missing;
16. mixed legacy/new namespace residue;
17. old manifest-owned retired plugin path still exists but is altered/incomplete -> must not use interrupted re-entry shortcut; it must remain on the normal rollover/fail-closed path as appropriate;
18. ordinary unrelated OpenClaw npm project that does **not** reference the CogentNexus package -> must not be treated as conflicting product evidence.

For every rejection case, assert a semantic `RuntimeError` relevant to the violated boundary and assert no test fixture mutation performed by classification beyond what the fixture itself created.

### Matrix commit evidence

The matrix commit must:

- contain tests only;
- list every changed file;
- be pushed before any production edit;
- record exact SHA in the report.

Run a selector that executes all Task-114 matrix cases and record exact count/result.

## Phase 2 — conditional source repair only if matrix finds a real defect

### If all matrix tests pass

Production source must remain unchanged from Task-113 candidate semantics. Proceed directly to Phase 3.

### If any matrix test exposes a real production defect

1. preserve the tests-only commit as RED evidence;
2. identify the exact root cause;
3. implement the smallest repair in a separate production commit;
4. do not weaken manifest, payload, containment, wrapper, product-evidence, namespace, retired-state, or final ownership checks;
5. rerun the complete Task-114 matrix to GREEN.

Preferred production surface if needed:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

No unrelated refactor.

## Phase 3 — targeted validation

Run at minimum:

1. all Task-114 direct matrix tests;
2. all `tests/test_plugin_generation_rollover.py`;
3. `tests/test_namespace_ownership.py`;
4. `tests/test_namespace_install_contract.py`;
5. `tests/test_installer_transaction_wiring.py`;
6. fresh install transaction recovery/failure coverage;
7. npm-12 local archive boundary tests;
8. plugin lifecycle action resolver tests.

Explicitly prove valid re-entry action selection remains:

```json
{"mode":"upgrade","pendingRollover":false,"pluginAlreadyExact":true,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":false}
```

No redundant external `openclaw plugins install` may be selected for an already-exact valid re-entry.

## Phase 4 — full repository validation

Run fresh and record exact outputs:

- full pytest suite;
- Python compile for ownership source if production changed, otherwise still run compile as verification;
- installer lifecycle/AST analysis;
- `npm ci`;
- `npm run plugin:validate`;
- `git diff --check`.

No PASS from matrix/targeted tests alone.

## Phase 5 — exact same-source CI/package proof

Push one exact candidate containing the completed matrix (and a production repair only if Phase 2 legitimately required one).

Require all three workflows successful on the same exact candidate SHA:

- Validate;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

A rerun is allowed only for demonstrated test/infrastructure flakiness on unchanged source and must be recorded transparently.

Produce a **new** package-proof artifact. Do not reuse Task-113 artifact `9685376213`.

Record and verify:

- exact candidate SHA;
- exact workflow run IDs/attempts/results;
- artifact ID/name;
- outer artifact SHA256/digest;
- inner v0.9.3 ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source/version;
- payload count/fingerprint;
- packaged Task-113 conflicting-product-evidence rejection;
- packaged Task-112 active-wrapper proof;
- packaged Task-110 retired-tree exactness;
- installer local archive invocation remains `openclaw plugins install $packagePath --force` when installation is required;
- recovery harness Git blob identity.

## Phase 6 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-114-interrupted-reentry-direct-matrix-validation.md`

The report must include:

- reconciliation HEAD;
- tests-only matrix commit SHA and changed-file list;
- a table of every required positive/negative case and observed result;
- whether any production repair was required;
- production repair SHA/files if applicable;
- targeted/full validation results;
- exact candidate SHA;
- exact workflow runs/attempt history;
- new package-proof identity/hashes/fingerprint;
- residual uncertainty;
- final `PASS`, `FAIL`, or `BLOCKED`.

Then stop for independent ChatGPT review. Do not create or execute a live-Windows task.

## Hard fence — NOT authorized

Task 114 does not authorize:

- any real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery action;
- replay of Task 107;
- manual live cleanup/normalization;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update, reinstall, uninstall, stop, or rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening namespace, wrapper, manifest, payload, ownership, product-evidence, or final verification boundaries.

If the matrix reveals a state that cannot be handled safely without generic adoption or destructive cleanup, publish `BLOCKED` rather than weaken the boundary.
