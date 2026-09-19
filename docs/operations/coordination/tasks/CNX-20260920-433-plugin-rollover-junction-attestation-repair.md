# CNX-20260920-433 — Preserve Windows Junctions in Plugin Rollover Backup

Status: `COMPLETE`

Parent: `CNX-20260919-432`

## Trigger

The supported install-over attempt from exact source HEAD:

`3d084b1311d4d7dbdebe7d77ab3986e0f25e2594`

crossed the CNX-430/431/432 lifecycle and Gateway readiness defects, then stopped before plugin replacement at:

`plugin-rollover-prepare`

Installer terminal result:

- installer exit: `1`;
- skill install: PASS;
- validation: PASS;
- Ticket DB bootstrap: PASS;
- plugin npm pack: PASS;
- plugin rollover prepare: FAIL;
- no plugin replacement mutation was started.

The exact failure was:

`pre-install backup project-tree attestation mismatch`

## Root cause

The retired direct plugin root contains:

`node_modules/openclaw`

as an npm peer-dependency Windows Junction targeting:

`C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw`

The rollover implementation used:

`shutil.copytree(retired_project, backup_path)`

Python `shutil.copytree` dereferences Windows directory junctions even when `symlinks=True`.

Therefore the source project tree contained one reparse/junction entry while the backup materialized the entire OpenClaw global package as ordinary directories/files.

That violated both:

1. exact project-tree attestation; and
2. ownership semantics, because the CNX backup must not claim/copy the OpenClaw peer package as CNX-owned content.

## Exact live proof

Failed backup created:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\cogentnexus-openclaw-49084ae878554c62829ed4cf170bebda`

The application-data rollover root is already redirected to the canonical T: storage boundary.

Source peer metadata:

- LinkType: `Junction`
- target: `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw`

Failed backup peer metadata:

- LinkType: none
- ordinary directory containing materialized OpenClaw files

A dedicated probe also proved that Python 3.14 `shutil.copytree(..., symlinks=True)` still dereferences Windows junctions, so the standard option is insufficient.

## Runtime-version compatibility defect

The installer uses PATH Python:

- `C:\DATAstore\Python\Python3-14-3\python.exe`
- Python `3.14.6`
- `os.path.isjunction` available

The CNX runtime Python is:

- `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe`
- Python `3.11.15`
- `os.path.isjunction` unavailable

Before CNX-433, `_project_tree_entries()` used `os.path.isjunction` directly. Under Python 3.11 it treated a Windows junction as a normal directory and followed it, despite the function contract saying reparse points are not followed.

The module already had `_is_reparse_point()`, which includes a Win32 `FILE_ATTRIBUTE_REPARSE_POINT` fallback. CNX-433 makes the tree scanner use this canonical detector.

## Required semantics

1. Project-tree snapshots never follow symlinks or Windows reparse/junction points.
2. Rollover backups preserve symlinks/reparse semantics rather than materializing their targets.
3. A Windows junction is recreated as a Windows junction with the same target.
4. The OpenClaw peer dependency remains OpenClaw-owned.
5. Source and backup exact project-tree snapshots must match before rollover authority is granted.
6. Existing concurrent-mutation fail-closed tests must remain effective.
7. Backup paths remain outside the OpenClaw state boundary and under the external CogentNexus application-data backup root.
8. No routing, provider, Ticket, delivery, or lifecycle ownership semantics change.

## TDD RED

Added:

`tests/test_task433_rollover_junction_backup.py`

Initial installer-Python RED:

- junction snapshot test: PASS under Python 3.14;
- junction-preserving copy test: FAIL because `_copy_project_tree_preserving_reparse_points` did not exist.

Additional Python 3.11 RED demonstrated that the old tree snapshot followed a Windows junction and hashed the external target file as an owned project entry.

## Production repair

Changed:

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

Changes:

- tree scanning now uses canonical `_is_reparse_point()`;
- unreadable reparse targets fail closed;
- added `_windows_junction_target()` for Windows namespace normalization;
- added `_copy_project_tree_preserving_reparse_points()`;
- Windows junctions are recreated via bounded argv-based `cmd.exe /d /c mklink /J`;
- symlinks remain symlinks;
- ordinary files use `shutil.copy2(..., follow_symlinks=False)`;
- ordinary directories recurse without following reparse points;
- rollover prepare now uses the junction-preserving project-tree copy helper.

Updated historical race tests:

- `tests/test_task225_rollover_prepare_attestation.py`
- `tests/test_task250_hash_input_snapshot_diagnostic.py`

They now monkeypatch the new copy boundary and continue to prove that a source mutation after backup creation fails exact attestation.

## GREEN evidence

Focused installer-Python tests:

- `4 passed`

Expanded rollover/ownership regression:

- `135 passed`
- `1 skipped`
- `0 failed`

Python 3.11 runtime direct proof:

- source and backup snapshot equal: `true`;
- backup peer remains a reparse point;
- junction target preserved;
- no traversal into peer target.

## Live extension proof

The repaired helper was applied read-only/copy-only to the exact current live extension.

Evidence:

- source tree SHA-256:
  `36619fae0730f3933b5f1f02c61a2d2320d09619ef34023361072ac446297319`
- copied tree SHA-256:
  `36619fae0730f3933b5f1f02c61a2d2320d09619ef34023361072ac446297319`
- entry count: `1774`
- source peer reparse: `true`
- copied peer reparse: `true`
- source/copy peer target: exact match
- nested copied `node_modules/openclaw/*` entries: `0`
- elapsed copy proof: approximately `7.4s`

Proof artifact:

`T:\CogentNexus\CogentNexus-OpenClaw\diagnostics\CNX-20260920-433\live-extension-copy-proof.json`

The temporary copy was removed after proof generation.

## Live qualification plan

1. run Python 3.11 and 3.14 compile gates;
2. run `git diff --check`;
3. freeze exact CNX-433 implementation commit;
4. verify Gateway/PASSTHROUGH state;
5. retry exactly one supported install-over from the frozen candidate;
6. require `plugin-rollover-prepare` to pass;
7. require plugin replacement/finalization and complete installer exit `0`;
8. only after installation GREEN, re-enable/qualify MANAGED runtime and continue final Discord Ticket-first acceptance.

## Final classification target

`PLUGIN_ROLLOVER_JUNCTION_ATTESTATION_GREEN`

## Live qualification result

The supported installer crossed `plugin-rollover-prepare` twice after the repair:

- candidate `c77f393e0d46ff86731cb47e0fd9ffad98499fe3`: exit `0`, elapsed `1042ms`;
- candidate `076d76d5465798753eda5146cdaa9cf7da72b5ff`: exit `0`, elapsed `873ms`.

The second run continued through local-package installation and rollover finalization.

Classification: `PLUGIN_ROLLOVER_JUNCTION_ATTESTATION_GREEN`
