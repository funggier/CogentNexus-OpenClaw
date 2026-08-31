# CNX-20260828-111 — Interrupted Rollover Re-entry Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_ONLY_TDD`
- Owner / reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Repair the installer re-entry gap exposed by comparing the accepted Task-110 source with the preserved Task-107 live post-failure boundary.

Task 110 itself is accepted. This task addresses a different condition: the machine has already experienced the old external plugin replacement from Task 107, so the old manifest-owned plugin generation is missing **before** a new installer attempt begins.

This task is source/test/CI only. It does not authorize any real-Windows lifecycle mutation.

## Authoritative predecessor evidence

Task-107 live report:

`docs/operations/coordination/reports/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`

Task-110 report:

`docs/operations/coordination/reports/CNX-20260828-110-rollover-retired-state-exactness-repair.md`

Task-110 independent review:

`docs/operations/coordination/reviews/CNX-20260828-110-rollover-retired-state-exactness-repair-review.md`

Task-110 accepted candidate:

`25d229cd496a11af37ea2ff556a0126dfc194377`

Task-110 report-only descendant:

`efbb8f19d19dfcb9ad8b8525a6393996db688324`

Task-110 review commit:

`ad9532fa88dcbc9b23db7abf0e47229794386b17`

Task-110 review verdict:

`ACCEPTED PASS — TASK-110 DEFECT REPAIRED; LIVE GATE BLOCKED BY PRE-EXISTING INTERRUPTED-ROLLOVER RE-ENTRY GAP`

## Confirmed live-boundary shape

Task 107 performed exactly one old-candidate install-over attempt. Its external local-archive OpenClaw plugin installation succeeded, then the old ownership rollover logic failed.

Observed Task-107 effects relevant to this task:

- CNX finished in `passthrough`, generation `25`;
- OpenClaw remained `2026.7.1-2` and healthy;
- Gateway remained healthy;
- Ollama remained healthy/ready;
- SQLite integrity remained `ok`;
- Supervisor remained absent;
- the replacement plugin was installed/registered by OpenClaw;
- the previous manifest-owned npm generation was removed during that external install;
- the normal ownership manifest remained from the pre-mutation state;
- staging/backup residue was preserved;
- no later live task changed this boundary.

Do not assume the machine still has this exact state when a future live task runs; it must be re-proved read-only. But this is the production-shaped state that Task 111 must model.

## Confirmed current source gap

At accepted source `25d229cd496a11af37ea2ff556a0126dfc194377`:

1. `scripts/install.ps1` calls `recovery-preflight` before classification.
2. `recovery_preflight()` only automatically rolls back an incomplete **fresh-install** transaction.
3. If a normal ownership manifest exists, it returns `OWNERSHIP_PRESENT` without repairing an interrupted upgrade/rollover.
4. `scripts/install.ps1` then gathers exact candidate fingerprint + OpenClaw plugin inventory and calls `classify-install`.
5. `classify_install()` enters attested upgrade classification when product state/registration exists.
6. It calls `verify_manifest(stateRoot, workspace=..., verify_plugin=False)` with `require_artifacts` still at its default `True`.
7. `verify_manifest()` therefore requires the manifest `pluginPath` itself to exist.
8. In the Task-107-shaped residue, that retired `pluginPath` is specifically the generation already removed by the previous external install.
9. Classification therefore fails closed before the Task-108/109/110 rollover transaction logic can run.

Failing closed is correct. The missing capability is a narrowly proven interrupted-upgrade re-entry path.

## Core invariant

Task 111 must make the exact Task-107-shaped interrupted rollover safely re-enterable **without turning partial-state detection into generic adoption**.

A recovery/re-entry classification may be accepted only if all required identity and boundary proofs are exact.

At minimum:

- the normal ownership manifest must still have exact schema/product/version/workspace/state/skill/launcher/task-service/migration metadata;
- controller mode must be exactly `passthrough`;
- the manifest-owned prior plugin path must be specifically **missing**; an existing-but-altered/incomplete retired path is not this recovery mode and remains fail-closed;
- state root, skill identity, launcher, and other required non-plugin owned artifacts must still be coherent;
- exactly one canonical active CogentNexus-OpenClaw plugin registration must exist;
- that active plugin must be contained by the OpenClaw state boundary;
- its id/package/version/payload must be exact;
- its fingerprint must equal the expected candidate plugin fingerprint supplied by the installer;
- there must be no second canonical product payload, conflicting wrapper, mixed legacy namespace, or ambiguous registration;
- unrelated OpenClaw/user-owned data must never be adopted, removed, or rewritten;
- no recovery decision may rely on product name alone;
- every mismatch remains non-zero/fail-closed.

When the exact already-active replacement is proven, installer re-entry must not execute an unnecessary second external `openclaw plugins install` merely to normalize state. The normal later ownership creation + exact verification must durably bind the manifest to the exact active replacement before MANAGED authority is granted.

## Phase 0 — Reconcile repository state

Before editing:

1. fetch current branch HEAD;
2. verify this Task 111 is active in both `ACTIVE.md` and `STATUS.md`;
3. read Task-107 report, Task-110 report, and Task-110 independent review;
4. compare production/test source against accepted Task-110 source `25d229cd496a11af37ea2ff556a0126dfc194377` and stop `BLOCKED` on unexplained production drift;
5. inspect completely:
   - `scripts/install.ps1` preflight/classification/action-selection path;
   - `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` recovery, manifest verification, classification, active registration, candidate discovery;
   - `scripts/resolve-plugin-lifecycle-actions.ps1`;
   - current classification/recovery/fresh/rollover tests.

No live Windows action in this task.

## Phase 1 — Separate TEST-ONLY RED commit

Create a production-shaped regression before changing production behavior.

The first Task-111 implementation commit must contain tests only (test fixtures/helpers only if strictly necessary). Push it as a distinct Git commit before any production edit.

### Required positive RED scenario

Model the Task-107-shaped state:

1. construct a previously coherent v0.9.3 owned installation with exact manifest, state, skill, launcher, controller `passthrough`, and an old managed npm plugin generation;
2. create/register one exact active replacement payload matching the candidate fingerprint;
3. simulate the old external install by deleting the manifest-owned old npm generation while leaving the normal manifest unchanged;
4. preserve the other normal owned artifacts;
5. call the actual production classification/re-entry surface using exact plugin inventory and expected replacement fingerprint;
6. verify the current source fails with the incomplete manifest-owned plugin boundary;
7. state desired repaired result: an explicit upgrade/re-entry classification proving the active replacement is already exact, with no pending external rollover/install required.

The RED must be semantic. A string/order-only test is insufficient.

### Required negative RED/contract coverage

Add focused cases proving this recovery path rejects at least:

- active replacement fingerprint mismatch;
- multiple canonical product payloads or non-unique active registrations;
- replacement outside the OpenClaw boundary;
- wrong package/id/version;
- controller not `passthrough`;
- corrupted/mismatched ownership manifest metadata;
- missing skill or launcher/non-plugin owned artifact;
- retired manifest plugin path still exists but is altered/incomplete rather than specifically missing;
- mixed legacy/new namespace or foreign/shared wrapper evidence.

Not every negative case must fail for the same reason, but each must remain fail-closed.

### RED proof

Run the smallest exact test selector that demonstrates the current source cannot safely classify the valid interrupted-rollover scenario. Record the exact command, exit code, assertion/failure message, and test-only RED commit SHA.

Do not change production source until this RED proof exists in Git history.

## Phase 2 — Minimal production repair

Implement the smallest safe re-entry contract that makes the RED regression GREEN.

Likely permitted surfaces:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `scripts/install.ps1` only if classification needs an explicit re-entry flag or a separate bounded pre-commit step;
- `scripts/resolve-plugin-lifecycle-actions.ps1` only if a new exact action state cannot be represented safely by existing `upgrade + pluginAlreadyExact` semantics;
- directly related tests only.

Prefer existing action semantics if sufficient. Do not add a second plugin install when an exact active replacement is already proven.

### Required repaired behavior

A valid Task-107-shaped state should be able to reach an explicit safe upgrade/re-entry classification whose downstream behavior:

- skips redundant external plugin installation if the replacement already exactly matches the current candidate;
- keeps CNX in passthrough through installer mutation until final ownership create+verify succeeds;
- resolves exactly one active plugin path;
- writes/replaces the ownership manifest only through the existing supported ownership creation path or an equivalently exact atomic path;
- verifies the final manifest/plugin binding before transaction completion/MANAGED enable;
- does not delete old residue merely to make classification pass;
- preserves externally owned OpenClaw/Ollama state.

### Forbidden repairs

Do not:

- make `verify_manifest` globally ignore missing artifacts;
- accept any registered plugin just because its id/name matches;
- adopt multiple/ambiguous plugin candidates;
- mutate or delete unrelated OpenClaw npm projects;
- manually normalize live Task-107 residue in this source-only task;
- rerun OpenClaw plugin install as a recovery substitute;
- weaken Task-110 retired-state exactness checks;
- turn a missing/corrupt skill/launcher/state into a valid upgrade;
- suppress final ownership verification.

## Phase 3 — GREEN targeted validation

Run the new interrupted-rollover tests plus all directly related suites, including at minimum:

- classification/install-state tests;
- namespace ownership tests;
- Task-108/109/110 rollover prepare/finalize/failure tests;
- installer transaction wiring;
- fresh transaction recovery/rollback coverage;
- npm-12 local-archive boundary;
- plugin lifecycle action resolver coverage.

Record exact commands and counts.

## Phase 4 — Full repository validation

Run repository full validation, plugin validation, installer structural/AST checks, and `git diff --check`.

No PASS from targeted tests alone.

## Phase 5 — Exact same-source CI/package proof

Push the GREEN candidate and require all three workflows successful for the exact same candidate source:

- `Validate`;
- `Windows Installer Pack Smoke`;
- `PS5.1 Acceptance Smoke`.

Obtain a **new** package-proof artifact from that exact source. Record and independently verify:

- candidate source SHA;
- artifact ID and name;
- outer artifact SHA256/digest;
- inner v0.9.3 ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source/version;
- payload file count/fingerprint;
- packaged installer re-entry contract;
- local archive command remains exactly `openclaw plugins install $packagePath --force` for cases where installation is actually required;
- Task-110 exact retired-state checks remain packaged;
- recovery harness Git blob identity.

Task-110 artifact `9683127656` is historical evidence only after Task 111 changes production source and must not be used as the next live acceptance artifact.

## Phase 6 — Report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-111-interrupted-rollover-reentry-repair.md`

The report must include:

- root cause and Task-107-shaped reproduction;
- separate test-only RED commit SHA and exact RED evidence;
- minimal production fix commit/files;
- positive and negative recovery semantics;
- GREEN targeted/full validation;
- exact candidate source;
- exact three Actions run IDs/results;
- new package-proof identity/hashes/fingerprint;
- packaged recovery harness identity;
- residual uncertainty;
- final `PASS`, `FAIL`, or `BLOCKED`.

After report publication, stop for independent ChatGPT review. Do not create or execute a live Windows acceptance task.

## Hard fence — NOT authorized

Task 111 does not authorize:

- any real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery action;
- replay of Task 107;
- manual cleanup/normalization of Task-107 live residue;
- Dashboard semantic nonce/message/Send;
- OpenClaw or Ollama update/reinstall/uninstall/stop/rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credentials/tokens/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- generic adoption of partial/unowned plugin state.

If exact interrupted-rollover re-entry cannot be proven without weakening ownership boundaries, publish `BLOCKED` rather than weakening them.
