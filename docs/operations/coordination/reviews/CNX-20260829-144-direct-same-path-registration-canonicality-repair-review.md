# CNX-20260829-144 — Independent Review

Disposition: **ACCEPT**

Reviewed: 2026-08-30 ICT
Reviewer: ChatGPT

## Scope

Independent review of:

- Task: `docs/operations/coordination/tasks/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`
- Report: `docs/operations/coordination/reports/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`
- Production repair SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Task 144 is accepted as an **offline source/test repair only**. This review does not claim a successful live install or authorize Dashboard semantic traffic by itself.

## Accepted root cause

Task 143 correctly repaired direct in-place A -> B rollover for covered cases, but its finalizer did not require the raw OpenClaw inventory `plugins[].rootDir` itself to be the canonical direct registration path before direct same-path mutation authority.

Because `_active_registered_plugin()` resolves `rootDir`, a noncanonical alias/symlink/junction path could resolve to the canonical direct root and lose its lexical noncanonical identity. The same-path check could then authorize the direct transaction even though active registration was not lexically canonical.

## Genuine RED

A test-only RED was committed before Task-144 production repair:

`b4ff7ea6bea1dea2e7d161bdecc5bcfebe94e797`

The actual finalizer was exercised with a singular raw inventory `rootDir` that was a noncanonical alias resolving to the canonical direct plugin root.

Validate run `33264410835` produced the expected pre-fix failure on macOS:

```text
test_direct_same_path_rejects_in_state_symlink_registration_alias
Failed: DID NOT RAISE RuntimeError
1 failed, 467 passed, 33 skipped, 4 subtests passed
```

The Task-144 executor also exercised the Windows junction/reparse alias case before production repair rather than silently skipping Windows proof.

## Minimal production repair

Production repair:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

The production delta is narrowly confined to `finalize_plugin_rollover_transaction()` in:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

It adds the direct-transaction lexical canonicality gate:

```python
if direct_transaction and registration_key != direct_key:
    raise RuntimeError("direct same-path rollover requires canonical active registration")
```

This occurs before the existing direct-root real/non-reparse identity attestation and before direct same-path authority. No broad global alias prohibition was introduced.

## Preserved invariants

Independent inspection confirmed preservation coverage for:

- canonical direct A -> B same-path success;
- A -> A/no-generation-transition rejection;
- managed same-path rejection;
- managed distinct-generation behavior;
- expected replacement fingerprint matching;
- retired backup/fingerprint proof;
- backup tamper rejection;
- ownership-manifest drift rejection;
- conflicting product storage rejection;
- direct canonical root symlink/junction/reparse rejection;
- singular plugin identity/package/version proof;
- Task-142 partial-state re-entry classification with exact-candidate/no-unnecessary-replay behavior.

The earlier Dashboard durable-capture regression tests also remained GREEN in the exact production-SHA plugin suite.

## Exact production-SHA verification

Exact production SHA `fb5781c1abd68280760bd5b3b4a65fabd8a60e58` completed successfully:

- Validate: `33264956365`
- Windows Installer Pack Smoke: `33264956369`
- PS5.1 Acceptance Smoke: `33264956375`

The Windows Validate job independently showed the full Python suite, plugin tests, build, evaluation, audit, plugin validation, and package proof GREEN. The plugin suite remained `269` tests and included the Task-138 Dashboard durable-capture regression.

## Review-added outside-state preservation proof

The executor's original Task-144 test surface covered the required in-state POSIX alias and real Windows junction alias, but the task also requested an outside-state lexical alias case where testable.

Under `EXECUTION_OWNERSHIP.md`, this repository-only coverage gap was closed directly by ChatGPT without returning the work to the live executor:

`b4e943b20e699dd19707b80a6b6f2d395c75b03a`

This added only a POSIX regression test proving that an alias located outside the OpenClaw state tree, but resolving to the canonical direct root, is rejected by the actual finalizer. No production code changed.

A later staged Task-145 documentation commit produced current verification HEAD:

`1a8834e7f5a9083ec427bab2357d1ea0a83a3020`

Compare from production SHA `fb5781c1...` to this verification HEAD shows only:

- the Task-144 report;
- the Task-145 task document;
- the additional Task-144 test coverage.

There is **no later production-source delta** after `fb5781c1...`.

Fresh exact-HEAD verification on `1a8834e7...` completed successfully:

- Validate: `33265799943` — `completed / success`, all Windows/Linux/macOS Python 3.11/3.14 jobs and package dry-run GREEN;
- Windows Installer Pack Smoke: `33265800014` — GREEN;
- PS5.1 Acceptance Smoke: `33265799941` — GREEN.

This fresh run supersedes the earlier amendment run whose Windows npm tail was cancelled only because a newer documentation commit triggered workflow concurrency.

## Safety review

Task 144 and the review-added coverage were offline/repository-only:

- live installer invocations: `0`;
- live plugin/controller/manifest mutation: `0`;
- Dashboard semantic Sends: `0`;
- Ticket/workflow/outbox/delivery/recovery semantic mutation: `0`.

The Task-142 partial live state remains intentionally preserved until a separately authorized live task re-verifies it.

## Accepted implementation provenance

The accepted implementation/deployment source remains exactly:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

The later report/test/task-document descendants do not redefine the production candidate.

## Next disposition

Task 144 is **ACCEPT**.

The narrow successor is:

`CNX-20260830-145 — Accepted Candidate Partial-Install Re-entry and Health Proof`

Task 145 must use the real Windows machine only after a fresh read-only drift/classification gate, then execute **exactly one** supported normal installer invocation from the detached accepted implementation SHA. It must not manually normalize the preserved Task-142 state, retry a failure, perform uninstall/reset/clean reinstall, or send a Dashboard semantic message.
