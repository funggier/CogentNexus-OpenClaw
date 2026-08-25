# CNX-20260825-067 — Repair Install Reproducibility and Partial-Install Recovery

Result: `PASS_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY_FIXED`

Executor: Hermes
Report date: 2026-08-26 ICT
Fetched execution HEAD: `347c6d7798f324060094a1e2bbfaf1536cd49c78` (== local HEAD at start; Task 066 review commit `21971ff` verified ancestor; no prior Task 067 report)
Isolated worktree: `%LOCALAPPDATA%\Temp\cnx067-worktree`, branch `cnx067-repair`
Implementation HEAD: `ec51d7b20c228070a95a6cf0987cebd7e71cbfaf`

## D1 — plugin lockfile reproducibility

### RED (defective baseline)

Clean isolated copy of `plugins/cogentnexus-openclaw` at `21686f7` source; node v22.23.2 / npm 12.0.2:

```
npm error code EUSAGE
npm error Missing: @types/retry@0.12.0 from lock file
```

Reproduced deterministically (matches accepted Task 066 evidence).

### Fix

- `package.json`: devDependency `openclaw` pinned from `latest` to exact `2026.7.1-2` (the version the reviewed lock already resolved to; no drift). Justification: `latest` made lock regeneration non-deterministic and is what allowed the nested `@types/retry@0.12.5` vs p-retry's exact `0.12.0` divergence to persist.
- `package-lock.json`: regenerated with npm 12 (the stricter toolchain). Result: top-level `@types/retry@0.12.0` satisfying `p-retry@4.6.2` exactly; openclaw entry exactly `2026.7.1-2`; plugin version unchanged at `0.9.3`.
- `scripts/verify-package-contents.mjs`: normalize `npm pack --json` single-entry-object shape (npm ≥ 12) in addition to array shape (npm 11) so package-content validation is reproducible on both toolchains. Found during L4 under npm 12 (`Unexpected npm pack --dry-run shape`); fixed, both toolchains now pass.

### GREEN evidence (all clean installs with no preexisting node_modules)

| Test | npm 11.16.0 / node v24.18.0 | npm 12.0.2 / node v22.23.2 |
|---|---|---|
| L1/L2 clean `npm ci` | PASS (exit 0) | PASS (exit 0) |
| lockfile unchanged by ci after install | PASS | PASS |
| L4 `plugin:validate` | PASS (packedFileCount 176) | PASS (packedFileCount 176) |
| L4 `npm test` | 49 files / **237 tests passed** | 49 files / **237 tests passed** |
| L4 `npm pack --json` | PASS | PASS |

L3 no-drift: plugin version `0.9.3`; openclaw resolves exactly `2026.7.1-2`; `typebox ^1.1.38` unchanged; no other direct dependency changed.

## D2 — fresh-install transaction/recovery contract

Implemented in `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` (production surface), integrated into `scripts/install.ps1`.

### Contract

1. `begin_fresh_transaction()` writes `install-transaction.json` inside the CNX-owned state root BEFORE any residue-capable mutation. Marker fields: schemaVersion(1), transactionId, productId, installedVersion, workspace, stateRoot, skillPath, applicationData, state(`incomplete`), createdAt, createdPaths. It never claims ownership and is a distinct file from `ownership.json`.
2. `record_transaction_path()` appends each created path during install.
3. `commit_transaction()` retires the marker to `committed` only after `verify_manifest` passes.
4. `rollback_transaction()` removes ONLY marker-recorded paths (deepest-first) plus now-empty owned boundaries; unrelated paths untouched; archived marker retains provenance with cleared createdPaths.
5. `recovery_preflight()` runs before `classify-install` on installer rerun: ownership present → coherent (marker authorizes nothing); valid incomplete marker → bounded recovery → fresh; no marker / tampered marker / out-of-bound marker / committed-marker-without-manifest → fail-closed RuntimeError.
6. Boundary safety: marker workspace roots must equal canonical expected paths; every recorded path must be contained within stateRoot/skillPath/launchers boundaries. Crafted markers pointing outside are rejected before any deletion.
7. CLI subcommands: `transaction-begin`, `transaction-record`, `transaction-commit`, `recovery-preflight`.
8. `install.ps1` runs `recovery-preflight` before `classify-install` and begins a transaction for fresh installs.

### R-test results (RED → GREEN)

Strict TDD: tests written first against defective baseline.

| Test | RED (baseline) | GREEN (fix) |
|---|---|---|
| R1 marker exists before residue-capable mutation + exact schema | AttributeError (surface absent) | PASS |
| R1b ordering proof (fresh → marker → residue) | AttributeError | PASS |
| R2 crash simulation → recovery_preflight → classify=fresh | dead end (manifest missing) | PASS |
| R3 rollback leaves unrelated files, coherent fresh | AttributeError | PASS |
| R4 committed marker does not authorize cleanup | AttributeError | PASS (fail-closed without manifest; no adoption) |
| R5 out-of-bound markers (workspace parent / sibling skill / %USERPROFILE%) rejected before deletion, sentinels intact | AttributeError | PASS (3 parametrized cases) |
| R5b invalid marker schema rejected | AttributeError | PASS |
| R6 unmarked Task-066-shaped residue remains fail-closed (no adopt, no delete) | AttributeError | PASS |

End-to-end CLI smoke: transaction-begin → create residue → record ×3 → recovery-preflight returns `RECOVERED_FRESH` with empty new inventory → `classify-install` returns `fresh`. (One robustness fix found here: recovery now also removes owned boundary dirs left empty by bounded rollback.)

## Full verification

- `pytest tests/ -q`: **312 passed, 2 skipped** (skips are platform-gated Windows-lifecycle tests pre-existing; not related to this change), 4 subtests passed — isolated dev venv (Python 3.11, requirements-dev.txt installed).
- `python scripts/check_baseline_consistency.py`: PASS (Bridge v0.9.3).
- `git diff --check`: clean.
- Worktree clean after implementation commit (`git status --porcelain` empty).
- Canonical Node/plugin tests: covered by L4 `npm test` (237 tests × 2 toolchains).

## No-live-mutation accounting

Live machine re-verified post-execution:

- Task-066 partial residue still present untouched (`workspace\.cogentnexus-openclaw\{host,install-staging}`, `workspace\skills\cogentnexus-openclaw`);
- no Supervisor Scheduled Task registered;
- no launcher/plugin registration created;
- Gateway/Ollama untouched; AGENTS.md untouched; SQLite untouched.

All testing used isolated worktree/temp dirs only. R7 compatibility plan for the pre-existing Task-066 residue (which predates the marker): per the task's stated approach, the live successor performs one-time bounded cleanup only after re-proving the two reported roots, absence of `ownership.json`, absence of task/launcher/plugin registration, tree-shape consistency with Task 066 evidence, and no unrelated content inside those roots — then fresh-installs this repaired source.

## Publication fence

This commit adds ONLY:
`docs/operations/coordination/reports/CNX-20260825-067-repair-install-reproducibility-and-partial-recovery.md`

Implementation commit: `ec51d7b20c228070a95a6cf0987cebd7e71cbfaf` (parent `347c6d7...`).
