# CNX-20260828-115 — Interrupted Re-entry Semantic Matrix Hardening

- Status: `READY_FOR_HERMES`
- Execution mode: `TEST_SEMANTIC_GATE`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Goal

Repair the fidelity of the interrupted-rollover direct `classify_install(...)` regression matrix without changing the accepted Task-113 production semantics unless corrected tests expose a genuine source defect.

Task 114 demonstrated that the broad matrix is GREEN, but independent review found several fixtures can pass for the wrong reason and do not assert semantic failure/non-mutation strongly enough. This task converts that matrix into durable boundary-specific regression coverage before any live Windows acceptance.

This is repository test/validation work only. It does not authorize live Windows mutation.

## Authoritative predecessor evidence

- Task-113 production source repair: `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`
- Task-114 tests-only candidate: `83e8452de116bf6204be884e4cddf9f3b92b90da`
- Task-114 report: `docs/operations/coordination/reports/CNX-20260828-114-interrupted-reentry-direct-matrix-validation.md`
- Task-114 independent review: `docs/operations/coordination/reviews/CNX-20260828-114-interrupted-reentry-direct-matrix-validation-review.md`

Task-114 review verdict:

`SOURCE BEHAVIOR ACCEPTED; LIVE GATE BLOCKED — MATRIX FIDELITY / SEMANTIC ASSERTION DEFECTS`

Task-114 artifact `9686448746` is reproducible historical evidence only and is not live-authorized.

## Core rule

The first implementation commit must be **tests only**.

Correct the semantic fixtures/assertions first and run them on current production:

- if every corrected case is GREEN, do not modify production;
- if a corrected test exposes a genuine production defect, preserve that tests-only commit as RED evidence and only then make one minimal source repair in a separate commit;
- never relax a test merely because it exposes a real defect;
- never manufacture retroactive TDD provenance.

## Phase 0 — fresh reconciliation

1. Fetch the remote branch immediately before editing.
2. Confirm Task 115 is active in both `ACTIVE.md` and `STATUS.md`.
3. Read Task-114 report and independent review completely.
4. Compare production source with `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06`; only test/docs drift from Task 114/115 is expected. Stop `BLOCKED` on unexplained production drift.
5. Inspect `current_inventory(...)`, `_active_registered_plugin(...)`, `_classify_interrupted_rollover_reentry(...)`, `classify_install(...)`, and current Task-113/114 test helpers before changing tests.
6. No live-machine action.

## Phase 1 — tests-only semantic matrix correction

Preferred file:

`tests/test_plugin_generation_rollover.py`

The Task-115 test commit must replace or supplement the Task-114 generic matrix so every case proves the intended boundary rather than merely observing some `RuntimeError`.

### A. Explicit positive direct shape

Create the Task-107-shaped canonical direct-extension fixture and call actual `classify_install(...)`.

Assert exactly:

```python
assert result["mode"] == "upgrade"
assert result["pendingRollover"] is False
assert result["pluginAlreadyExact"] is True
assert result["interruptedRolloverReentry"] is True
assert Path(result["replacementPluginPath"]) == paths["new_plugin"].resolve()
assert Path(result["manifestPluginPath"]) == paths["old_plugin"].resolve()
```

### B. Explicit positive managed shape

Use one exact managed replacement whose wrapper passes `_managed_wrapper_proof(...)`, with the retired manifest-owned generation specifically absent.

Assert the same six result/path bindings as the direct case.

### C. Real mixed legacy/new namespace residue

Do not simulate this using a second current-product registration.

Create actual production-recognized legacy residue after the new installation fixture exists. Parameterize at least these forms:

```text
<workspace>/cnx.cmd
<workspace>/cnx
<workspace>/skills/cogentnexus
<workspace>/.cogent
<openclaw-state>/extensions/cogentnexus-rotation
```

For every form:

1. prove `current_inventory(...)["legacy"]` is non-empty and contains the expected legacy entry;
2. call actual `classify_install(...)`;
3. assert `RuntimeError` matches `mixed legacy state`;
4. assert the legacy sentinel and all pre-call owned/new artifacts remain unchanged after the exception.

### D. Exact payload outside OpenClaw state

The fixture must contain a real exact product payload at the out-of-bound path; a nonexistent path does not satisfy this case.

1. Copy the exact active candidate payload to a path outside `<openclaw-state>`.
2. Remove the normal replacement root so the supplied active registration is genuinely the external exact payload rather than coexisting with the normal candidate.
3. Point the OpenClaw registration at the copied payload with correct id/package/version.
4. Use its real fingerprint as expected candidate attestation.
5. Prove the payload itself is exact with `_plugin_payload(...)` before classification.
6. Assert classification raises a containment/storage-boundary `RuntimeError` relevant to being outside OpenClaw state.
7. Assert the external sentinel/payload is unchanged after classification.

### E. Exact payload contained by OpenClaw but noncanonical

The fixture must contain a real exact product payload at a contained but unsupported storage shape.

Example shape:

```text
<openclaw-state>/other/cogentnexus-openclaw
```

1. Copy the exact candidate payload there.
2. Remove the normal managed replacement root.
3. Bind the active registration to this exact contained payload.
4. Prove `_plugin_payload(...)` succeeds before classification.
5. Assert classification rejects it because it is not one canonical direct extension and not one exact managed npm child. A semantic match such as `canonical active replacement` / `storage ownership` is acceptable only if it identifies this boundary.
6. Assert no mutation.

### F. Active foreign/shared wrapper

Keep the active child payload exact while making its owning wrapper foreign/shared (for example unrelated undeclared dependency evidence). Assert the error is wrapper/storage-ownership related, not merely any `RuntimeError`. Preserve a sentinel in the foreign wrapper and prove it remains unchanged.

### G. Separate conflicting wrapper

For both direct-active and managed-active valid replacement shapes, create a separate wrapper that identifies the CogentNexus package but contains unrelated user dependency evidence and no second exact child payload.

Assert `RuntimeError` matches `conflicting product storage evidence`, and prove the foreign wrapper/sentinel remains unchanged.

### H. Duplicate exact payload

Create a second exact canonical product payload while retaining one active registration. Prove both payloads are exact before classification. Assert error matches the canonical-replacement/candidate ambiguity boundary and no payload is removed or modified.

### I. Duplicate active registration

Supply two registrations that both describe the same exact active payload. Assert the active-registration uniqueness error rather than accepting any unrelated exception. Confirm registration input object is unchanged by classification.

### J. Identity/version/attestation cases

Keep the underlying payload/storage otherwise valid and test separately:

- wrong plugin id;
- wrong package name when package identity is supplied in inventory;
- wrong inventory version;
- candidate fingerprint mismatch.

Each must assert an error whose message identifies registration/identity/version/attestation rather than generic failure.

### K. Controller/manifest/artifact cases

Test separately:

- controller not `passthrough` -> message identifies PASSTHROUGH requirement;
- corrupted/mismatched ownership manifest -> message identifies manifest/schema/mismatch;
- missing `SKILL.md` -> message identifies required artifact/skill;
- missing launcher -> message identifies required artifact/launcher.

For each case, snapshot after fixture setup and prove classification adds/deletes/modifies nothing.

### L. Altered retired path

Use the already production-shaped altered-retired fixture: keep the retired project path present but make the manifest-owned plugin payload incomplete (for example remove one required installable file).

Call `classify_install(...)` and assert specifically that the interrupted re-entry shortcut is **not** selected:

```python
assert result["pendingRollover"] is True
assert result.get("interruptedRolloverReentry", False) is False
```

If current production instead fail-closes with a semantic retired-state error, that is acceptable only after confirming the path did not enter the re-entry success branch; document the exact reason.

### M. Unrelated npm project

Add an ordinary OpenClaw npm project whose package metadata does not reference `openclaw-plugin-cogentnexus-openclaw`.

Assert valid re-entry remains accepted with all six positive result/path bindings. Prove `product_plugin_inventory(...)` does not include the unrelated project.

## Phase 2 — classification non-mutation helper

Add a test helper that snapshots the fixture **after setup but before** `classify_install(...)`.

At minimum capture immutable evidence sufficient to detect classification mutation:

- ownership manifest bytes;
- controller bytes;
- `current_inventory(...)` output;
- product inventory keys/paths;
- selected sentinels used by foreign/legacy/external fixtures;
- existence + bytes for launcher and `SKILL.md` when present.

After every rejection call, compare the snapshot and sentinels. Classification must not perform deletion, normalization, manifest rewrite, controller rewrite, or user-data mutation.

Do not use filesystem mtimes as the primary assertion.

## Phase 3 — corrected-matrix decision gate

Run the corrected Task-115 semantic matrix first.

### If all corrected tests GREEN

- record the exact count;
- production source remains unchanged;
- proceed to targeted/full validation.

### If any corrected test RED because source behavior is wrong

- preserve the tests-only commit as genuine RED evidence;
- identify root cause with systematic debugging;
- make the smallest production repair in a separate commit;
- rerun the corrected semantic matrix to GREEN;
- do not broaden scope.

### If a test fails because the fixture/assertion is wrong

- fix tests only;
- document why the test changed;
- rerun before any production edit.

## Phase 4 — targeted/full validation

Run and record exact results for:

1. all Task-115 semantic matrix tests;
2. all `tests/test_plugin_generation_rollover.py`;
3. `tests/test_namespace_ownership.py`;
4. `tests/test_namespace_install_contract.py`;
5. `tests/test_installer_transaction_wiring.py`;
6. fresh install transaction recovery/failure suites;
7. npm-12 local archive boundary tests;
8. plugin lifecycle action resolver tests;
9. full pytest suite;
10. Python compile for ownership source;
11. installer lifecycle AST analysis;
12. `npm ci`;
13. `npm run plugin:validate`;
14. `git diff --check`.

Explicitly re-prove valid action selection:

```json
{"mode":"upgrade","pendingRollover":false,"pluginAlreadyExact":true,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":false}
```

No redundant external `openclaw plugins install` may be selected for valid already-exact re-entry.

## Phase 5 — exact same-source CI/package proof

Push one exact final candidate containing the corrected semantic tests and production changes only if a genuine RED required them.

Require all on exactly that SHA:

- Validate — success;
- Windows Installer Pack Smoke — success;
- PS5.1 Acceptance Smoke — success.

Produce a **new** package-proof artifact. Do not reuse `9686448746`.

Verify and report:

- candidate SHA;
- workflow run IDs/attempts/results;
- artifact ID/name;
- outer artifact SHA256/digest;
- inner ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source/version;
- payload count/fingerprint;
- packaged Task-113 conflict rejection;
- packaged Task-112 active-wrapper proof;
- packaged Task-110 retired-tree exactness;
- installer local archive invocation remains exactly `openclaw plugins install $packagePath --force` when installation is required;
- recovery harness Git blob identity.

## Phase 6 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening.md`

The report must include:

- reconciliation HEAD;
- tests-only semantic-matrix commit SHA and changed files;
- per-boundary semantic assertion/result table;
- actual legacy fixtures used;
- exact-payload out-of-bound and noncanonical fixture proof;
- non-mutation evidence;
- whether corrected tests were all GREEN or exposed a genuine RED;
- production repair SHA/files if one became necessary;
- targeted/full validation results;
- exact CI candidate and run IDs;
- new artifact identities/hashes/fingerprint;
- residual uncertainty;
- final `PASS`, `FAIL`, or `BLOCKED`.

Then stop for independent ChatGPT review. Do not open or execute a live-Windows acceptance task.

## Hard fence — NOT authorized

Task 115 does not authorize:

- real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery;
- replay or manual normalization of Task 107 residue;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update, reinstall, uninstall, stop, or rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/tokens/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening namespace, wrapper, manifest, payload, product-evidence, ownership, or final verification boundaries.

If corrected tests reveal a state that cannot be handled safely without generic adoption or destructive cleanup, publish `BLOCKED` rather than weaken the boundary.
