# CNX-20260824-051 — Align Canonical Check Help and Usage

Status: **COMPLETED**

Result: `PASS_CANONICAL_CHECK_HELP_ALIGNED`

Fetched start HEAD: `1a71acacdfb048c823922ff869e66f2802f23e9f`

Repository: `C:\Users\CDQ-P\AppData\Local\Temp\cnx051-clone-20260824T122432Z`

Branch: `agent/v0.9.3-recovery-reality-tests`

Implementation commit: `6d90025f832bb36c477176809a0af2e6c1858c19`

## Source and duplicate fence

The exact coordination `ACTIVE.md`, coordination `STATUS.md`, and Task 051 identified `CNX-20260824-051` as `READY_FOR_CODEX`. Review commit `65209cec1888b01c732ce8f383ff20b069d8a5c8` was an ancestor. No matching report existed, the new isolated full clone was clean, and parallel implementation/publisher count was zero.

No Git worktree was created. No live workspace installation, primary repository checkout, OpenClaw/Gateway/Ollama/scheduler/controller/plugin/config, Task 049 backup, or retained evidence was accessed or mutated for implementation/testing.

## Root cause and inventory

The confirmed mapping remained unchanged: `checks.component_check()` accepts canonical component `cogentnexus-openclaw` and rejects generic `cogentnexus`. Current base/v0.9.3 CLI help and base missing-component usage advertised the rejected generic component.

Initial command:

`rg -n --pcre2 "check cogentnexus(?!-openclaw)"`

classified occurrences as:

- current operational source requiring correction: `skills/cogentnexus-openclaw/scripts/cnxclaw.py` and `skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py`;
- immutable/historical coordination evidence: Task 050 task/report/review and Task 051/coordination status text;
- no other current operator documentation/template/example occurrence.

Final inventory contains only classified coordination history/spec evidence. Test fixtures construct the generic component from fragments and do not appear as current operator commands. Historical coordination and release notes were not edited.

## Strict TDD evidence

### Canonical help RED

After adding `tests/test_canonical_check_help.py`, before production edits:

`python -m pytest -q tests/test_canonical_check_help.py`

exited `1`: `2 failed, 1 passed`. The observed failures were exactly the stale contract:

- base/current help lacked `check cogentnexus-openclaw`;
- base missing-component usage returned `...|cogentnexus|...`.

The third mapping test passed, proving canonical mapping acceptance and generic rejection already behaved as designed.

### Canonical help GREEN

After changing only the stale spellings in the two CLI facades, the same command exited `0`: `3 passed`.

The focused test exercises base CLI functions and v0.9.3 real subprocess help output. It asserts canonical help/usage, rejects complete-token generic advertising, calls `do_check()` with missing/canonical/generic components, and preserves generic rejection.

### Namespace lint RED

Added a focused fixture for a current migration-documentation path:

`python -m pytest -q tests/test_namespace_lint.py::test_generic_check_component_fails_even_in_current_migration_documentation`

Before lint production edits it exited `1`: the generic operator command incorrectly returned no violation because the path's migration exception blanket-allowed it.

### Namespace lint GREEN

Added one command-specific regex before migration-literal exceptions, while retaining historical coordination exclusions. The focused lint plus canonical-help command exited `0`: `4 passed`; standalone namespace lint also exited `0` with PASS.

The lint rejects generic `check cogentnexus` when it is a complete component token, allows `check cogentnexus-openclaw`, and does not rewrite or reject historical coordination evidence.

## Implementation paths

Commit `6d90025f832bb36c477176809a0af2e6c1858c19` changes exactly:

- `skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- `skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py`
- `scripts/check_namespace_isolation.py`
- `tests/test_canonical_check_help.py`
- `tests/test_namespace_lint.py`

Production changes are limited to three stale operator-facing component spellings and the command-specific lint guard. No alias, check mapping, verdict, exit-code, provider, lifecycle, controller, plugin, or installer behavior changed.

## Validation

Final focused command:

`python -m pytest -q tests/test_canonical_check_help.py tests/test_namespace_lint.py`

exit `0`: `6 passed`.

The first full-suite run exposed a test-only isolation defect: importing `cnxclaw_v093` in-process intentionally rebinds base provider modules, causing 9 unrelated v0.9.2 tests to observe the Ollama-only adapter (`9 failed, 243 passed, 1 skipped, 4 subtests passed`). The test was corrected to execute v0.9.3 help in a subprocess; no production behavior was changed for this correction.

Fresh final full suite:

`python -m pytest -q`

exit `0`: `252 passed, 1 skipped, 4 subtests passed`.

Other final validation:

- `python scripts/check_namespace_isolation.py` — exit `0`, PASS;
- `python scripts/check_baseline_consistency.py` — exit `0`, v0.9.3 PASS;
- `python -m compileall -q skills/cogentnexus-openclaw/scripts scripts tests/test_canonical_check_help.py tests/test_namespace_lint.py` — exit `0`;
- `git diff --check` — exit `0`;
- final invalid-command inventory — only coordination historical/spec evidence;
- implementation path/scope fence — exactly five authorized paths.

Plugin validation/build/evaluation/production audit was not run because no plugin code, manifest, package, installer, runtime integration, or plugin contract changed; the complete Python suite and repository namespace/baseline contracts cover this help/lint-only diff.

## Publication and safety accounting

Implementation commit message: `fix: align canonical CogentNexus-OpenClaw check help`.

No live installer, installed-file edit, update, repair, enable/disable/restart, OpenClaw plugin/config action, Gateway/Ollama/scheduler/controller action, reset/uninstall, Procmon access, primary-repository mutation, excluded-project action, merge, tag, Release, or archive occurred. No external side effect was executed or repeated.

Remaining uncertainty: none within repository help/usage and lint scope. The installed live copy remains at the reviewed Task 050 version and was deliberately not updated.

Recommended next step: ChatGPT should review this implementation/report. Updating the already-installed copy requires a separate exact ownership-preserving task and explicit human authorization; do not edit installed files manually.

Human decision required: **NO** for Task 051 completion. A later installed-copy update remains a separate human gate.
