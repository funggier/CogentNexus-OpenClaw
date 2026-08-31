# CNX-20260828-108 — Windows Plugin Rollover Transaction Repair

- Status: `READY_FOR_HERMES`
- Execution mode: `SOURCE_ONLY_TDD`
- Owner: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-28 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Repair the source-level Windows plugin ownership rollover transaction defect exposed by Task 107, using strict RED -> minimal fix -> GREEN development.

This task is **source/test/CI only**. It does not authorize any real-Windows lifecycle mutation or any replay of Task 107.

## Authoritative predecessor evidence

Task 107 report:

`docs/operations/coordination/reports/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry.md`

Report commit:

`582acb72dd09d1e3753452afcb5f76aa72929d5d`

Independent Task 107 review:

`docs/operations/coordination/reviews/CNX-20260828-107-v093-real-windows-lifecycle-acceptance-retry-review.md`

Review commit:

`b0487da1aacb5cd3663a6e7e6b2f3caed1db1ef0`

Review verdict:

`ACCEPTED FAIL — SOURCE DEFECT CONFIRMED`

The old Task 107 acceptance candidate remains immutable historical evidence:

`b14a711f24b3fd1cd0aaa51ce636c8502ba42404`

Comparison from that source through the Task 107 report/review boundary contains only coordination documents; no production/source drift occurred before Task 108 authorization.

## Confirmed defect

The npm 12 / `npm-pack:` defect from Task 105 is repaired. Task 107 proved the local package invocation reached the real OpenClaw boundary successfully:

```powershell
openclaw plugins install $packagePath --force
```

The newly exposed defect is different.

Current install-over ordering effectively performs:

1. package candidate plugin;
2. invoke external `openclaw plugins install $packagePath --force`;
3. query the registered replacement inventory;
4. construct CogentNexus ownership `rollover-plan`;
5. apply/verify ownership transition.

With OpenClaw `2026.7.1-2`, step 2 may remove/replace the previously installed plugin generation. The durable CogentNexus ownership manifest can therefore still point to the old owned installation after its path has disappeared. The subsequent ownership planner correctly fails closed because the manifest-owned installation is incomplete.

The ownership layer is behaving correctly. The integration transaction is not.

## Required invariant

The repair must preserve, not weaken, all of these properties:

- The old durable ownership state must be validated before an install-over is authorized.
- A missing or altered owned installation before the external mutation remains a hard failure.
- The exact local `.tgz` candidate must remain the install source; do not restore the old `npm-pack:` invocation.
- The external OpenClaw install command is executed at most once per install-over attempt.
- The replacement generation must be independently verified after the external install.
- Durable ownership must not switch to the replacement until post-install proof succeeds.
- A failure after the external command has mutated OpenClaw must remain fail-closed; do not falsely reassert a manifest for a generation that no longer exists.
- Fresh install behavior, namespace isolation, rollback/failure handling, package provenance, and existing ownership verification must remain intact.

## Important design constraint

Do **not** repair this by merely moving the existing `rollover-plan` call above `plugins install`.

The current rollover model expects both the old owned installation and the registered replacement to be provable. Before the external install the replacement is not yet live; after the external install the old generation may already be gone.

Task 108 must create a safe transaction bridge across that external mutation boundary. The expected semantic shape is:

1. pre-install proof/prepare of the currently owned state;
2. one external install mutation;
3. post-install proof of the exact expected replacement;
4. atomic durable ownership commit;
5. fail-closed handling when any post-mutation proof fails.

Command names, data structures, and file layout are implementation details to derive through TDD. Do not weaken the existing planner merely to make the test pass.

## Phase 0 — Reconcile repository state

Before editing:

1. fetch the current remote branch HEAD;
2. confirm this Task 108 is still the active authorization in both `ACTIVE.md` and `STATUS.md`;
3. inspect the Task 107 report and independent review;
4. compare current production source with `b14a711f24b3fd1cd0aaa51ce636c8502ba42404` and stop `BLOCKED` if unexplained production drift exists;
5. inspect current `scripts/install.ps1`, ownership helper implementation, and all ownership/install transaction tests before selecting a patch.

Do not rely on stale local SHA/status if GitHub has newer state.

## Phase 1 — RED regression

Create a production-shaped regression that fails for the confirmed Task 107 defect before changing production behavior.

The RED evidence must cover the real semantic boundary, not just a string-order assertion. At minimum demonstrate that:

- an install-over starts from a valid old manifest-owned generation;
- the external plugin install can replace/remove that old generation while registering a new generation;
- the old implementation cannot safely complete ownership rollover after that mutation;
- the desired repaired contract requires a pre-mutation proof bound to the intended transition and a post-mutation replacement proof;
- a mismatched/unexpected replacement or a failed post-install proof cannot commit new durable ownership.

Add structural/order assertions only as supporting coverage, not as the sole regression.

Run the smallest relevant test set and record the expected RED failure. The RED commit must contain tests only unless a test fixture/helper change is strictly necessary to express the regression. Do not manufacture RED through syntax errors or unrelated failures.

## Phase 2 — Minimal production fix

Implement the smallest safe transaction change that makes the RED regression pass.

Likely permitted production surfaces include:

- `scripts/install.ps1`;
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` if the ownership API needs an explicit prepare/finalize transaction contract;
- directly related ownership/install transaction support only when required by the proven design.

Do not broaden this task into unrelated refactoring.

The repair must keep the local archive command form:

```powershell
openclaw plugins install $packagePath --force
```

and must not accept a missing pre-install owned root as valid state.

## Phase 3 — GREEN targeted validation

After the minimal fix:

1. run the new regression tests;
2. run all namespace ownership tests;
3. run Windows installer/fresh/install-over/failure-rollback contract tests relevant to the changed surfaces;
4. run npm-12 local-archive regression coverage;
5. run namespace/baseline invariant checks.

All must be GREEN before broad validation.

## Phase 4 — Full repository validation

Run the repository's normal full validation suite, including full pytest or its repository-equivalent validation entry point.

Do not report PASS from targeted tests alone.

## Phase 5 — Exact CI/package proof

Push the GREEN source and obtain exact successful GitHub Actions evidence for the new candidate:

- `Validate`;
- `Windows Installer Pack Smoke`;
- `PS5.1 Acceptance Smoke`.

All three must be successful for the **same exact candidate source commit**.

From that exact candidate, record a new package-proof artifact and verify at minimum:

- artifact ID and name;
- outer artifact SHA256/digest;
- inner v0.9.3 ZIP SHA256;
- tar.gz SHA256;
- `PACKAGE_IDENTITY.json` source commit and version;
- payload file count;
- payload fingerprint;
- packaged `scripts/install.ps1` contains the repaired transaction contract and local `.tgz` invocation;
- packaged recovery harness identity remains the expected source unless Task 108 legitimately changes it.

Do not reuse Task 107 artifact `9677072214` as the next acceptance candidate.

## Phase 6 — Report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`

The report must include:

- root cause confirmed;
- RED test/commit and exact failing evidence;
- minimal production fix and files changed;
- GREEN targeted/full test evidence;
- exact GREEN candidate source commit;
- exact GitHub Actions run IDs/results;
- exact new package-proof artifact identity/hashes/fingerprint;
- any residual uncertainty;
- final `PASS`, `FAIL`, or `BLOCKED` verdict.

After publishing the report, stop for independent ChatGPT review. Do **not** create or execute the next real-Windows acceptance task yourself.

## Hard fence — NOT authorized

Task 108 does not authorize:

- any real Windows install-over, reset, uninstall, reinstall, stop/start/restart, or disruptive recovery action;
- replaying any Task 107 destructive phase;
- manual cleanup or normalization of Task 105/107 live residue;
- Dashboard semantic nonce/message/Send or semantic artifact reuse;
- OpenClaw or Ollama update/reinstall/uninstall;
- model/provider/timeout changes;
- credential/token/password access or re-entry;
- LM Studio management;
- direct live SQLite/config/session mutation;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- weakening namespace ownership validation to accommodate missing evidence.

If a safe source-only transaction design cannot be proven, publish `BLOCKED` with evidence instead of weakening these fences.

## Completion condition

Task 108 is complete only when its report is committed and pushed. Until an independent ChatGPT review accepts a new exact GREEN candidate, **no further real-Windows lifecycle attempt is authorized**.
