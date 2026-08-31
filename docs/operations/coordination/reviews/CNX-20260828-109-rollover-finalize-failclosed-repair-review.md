# CNX-20260828-109 — Independent Review

## Verdict

`REJECTED — TDD PROVENANCE FAILURE + RESIDUAL RETIRED-STATE EXACTNESS DEFECT`

Task 109 is closed. Its source candidate and package artifact remain useful evidence, but they are **not authorized for real-Windows lifecycle acceptance**.

## Reviewed boundary

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260828-109`
- Task report: `docs/operations/coordination/reports/CNX-20260828-109-rollover-finalize-failclosed-repair.md`
- Reported source candidate: `dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce`
- Current report-only descendant at review start: `2b198632bc2cbe7b485ce56e0ac046b0ceb545e7`

The candidate contains the intended missing-retired-generation fix and a semantic regression. The later commits after the candidate only add/correct the Task-109 report.

## Finding 1 — required RED commit provenance is absent

Task 109 explicitly required:

> Commit RED tests separately. Production files must not be changed in the RED commit except a strictly necessary test fixture/helper.

Git history does not satisfy this gate.

`dcca49d43d95a0a34d8d460a4b9ab5ad88d036ce` has parent:

`1384ba1437731643bcfe8ef5aa60a738ed83b153`

and the `dcca49d4...` commit itself changes both:

- `tests/test_plugin_generation_rollover.py`; and
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`.

Therefore there is no separate test-only RED commit in the authoritative branch history between Task-109 authorization and the production fix.

The report states that a pre-fix run returned non-zero and later corrected its wording to `exit 1`, but a claimed local RED run is not equivalent to the separately committed RED evidence required by the task and by the project TDD contract.

This finding is a process/provenance rejection even if the implemented behavior were otherwise correct.

## Finding 2 — residual exactness defect remains in the failure rollback decision

Task 108 preparation already records exact pre-mutation evidence including:

- `retiredProjectTreeSha256`;
- `retiredFingerprint`;
- `backupProjectTreeSha256`;
- the previous manifest and its hash.

Task-109 finalization, however, decides whether the old durable manifest may be restored after a final verification failure using only:

```python
retired_project = Path(transaction["retiredProjectRoot"])
if retired_project.exists():
    _write_bytes_atomic(manifest_target, ... manifestBefore ...)
else:
    manifest_target.unlink(...)
```

Existence is weaker than the exact pre-mutation proof already available in the transaction.

If the retired project path still exists but was altered, partially removed, replaced in place, or otherwise no longer matches the pre-install project tree, the current failure handler can restore `manifestBefore` and therefore durably reassert normal ownership of state that is no longer the exact proven retired generation.

This is the same fail-closed class as the missing-path defect, narrowed to an **existing-but-no-longer-exact retired project**.

The current Task-109 regression covers the case where the old project directory is removed entirely. It does not cover the case where the directory still exists but its tree/payload no longer matches the transaction attestation.

## Why CI does not override the rejection

The Task-109 report records all three required workflows as successful for exact candidate `dcca49d4...`, plus a new exact package-proof artifact. Those are valid reproducibility/package signals.

They do not prove the uncovered existing-but-altered retired-state failure path, and they do not repair the missing separately committed RED provenance.

Therefore the exact candidate remains **historical evidence only** until a new source-only TDD task closes the residual exactness boundary.

## Accepted parts of Task 109

Preserve these behaviors unless new RED evidence proves otherwise:

- final verification failure remains non-zero;
- when the retired project is fully absent, the normal ownership manifest is removed rather than restoring a stale missing-path claim;
- successful prepare/install/finalize behavior remains unchanged;
- the local `.tgz` install path remains intact;
- transaction backup evidence remains retained;
- no live Windows lifecycle action was performed.

## Required next action

Open a new source-only TDD task that begins from the current reviewed source and proves this exact residual case:

`prepare exact retired state -> external mutation leaves retired project path present but changes/incompletes the retired tree -> replacement commit attempt -> injected final verification failure -> current code restores manifestBefore -> desired repaired behavior refuses to restore normal ownership unless the retired state is still exact`

The RED regression must be committed separately before any production change.

A minimal production repair should derive its restoration decision from exact transaction evidence, not path existence alone. If exact retired-state revalidation cannot be proven, normal ownership must remain quarantined/fail-closed while preserving transaction/backup evidence for later authorized recovery.

## Safety gate

No real-Windows install-over/reset/uninstall/reinstall/lifecycle/recovery replay is authorized by this review.

No Dashboard semantic Send is authorized.

Task 109 must not be replayed as a live acceptance task.
