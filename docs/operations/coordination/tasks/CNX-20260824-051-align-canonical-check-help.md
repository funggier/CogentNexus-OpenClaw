# CNX-20260824-051 — Align Canonical Check Help and Usage

Status: `READY_FOR_CODEX`

Execution mode: `MANUAL_REPOSITORY_ONLY`

Owner: ChatGPT

Executor: Codex after the operator's manual signal

## Goal

Repair the deterministic CogentNexus-OpenClaw v0.9.3 CLI help/usage defect exposed by Task 050: every current operator-facing check command must advertise the canonical component `cogentnexus-openclaw`, matching the existing check-engine mapping.

This task is repository-only. Do not update, reinstall, repair, restart, enable, disable, or otherwise touch the already-installed live CogentNexus-OpenClaw.

## Human authorization

After the Task 050 review presented the bounded repository-only design, the operator explicitly authorized immediate Codex execution:

> `ให้ codex ทำเลยก็ได้ครับ แล้วค่อยรายงานงาน`

## Predecessor and root cause

Required report:

`docs/operations/coordination/reports/CNX-20260824-050-fresh-install-current-v093.md`

Required review:

`docs/operations/coordination/reviews/CNX-20260824-050-fresh-install-current-v093.md`

Accepted disposition:

`ACCEPT_INSTALLED_RUNTIME_WITH_HELP_DEFECT`

Reviewed report commit:

`ab0264c11481ad2f31224e376da9b9b51d2fd1c8`

Required review commit:

`65209cec1888b01c732ce8f383ff20b069d8a5c8`

Confirmed root cause:

- `skills/cogentnexus-openclaw/scripts/checks.py` maps only canonical component key `cogentnexus-openclaw`;
- `cnxclaw.py` usage/help still advertises invalid generic `check cogentnexus`;
- `cnxclaw_v093.py` help still advertises invalid generic `check cogentnexus`;
- canonical `check cogentnexus-openclaw` works and returned `READY` on the installed system;
- Task 050 copied the stale help text.

Do not add a compatibility alias for `cogentnexus`. Explicit product identity is required for coexistence with CogentNexus-HermesAgent.

## Source and duplicate fence

1. Freshly fetch branch `agent/v0.9.3-recovery-reality-tests`.
2. Use one new isolated full clone under `%LOCALAPPDATA%\Temp`; do not create/register a Git worktree.
3. Record fetched start HEAD.
4. Require exact `ACTIVE.md` and `STATUS.md` to identify Task 051 as `READY_FOR_CODEX`.
5. Require review commit `65209cec1888b01c732ce8f383ff20b069d8a5c8` as an ancestor.
6. Stop if the matching Task 051 report already exists.
7. Require a clean clone and no parallel publisher/implementation operation.
8. Inventory all occurrences of the invalid current command with:

   `rg -n --pcre2 "check cogentnexus(?!-openclaw)"`

9. Classify every occurrence as current operational source/documentation or immutable historical coordination/release evidence before editing.

Do not mechanically rewrite historical coordination tasks/reports/reviews. Do not rewrite immutable already-published release notes solely to change historical evidence. Current v0.9.3 operator documentation is in scope.

## TDD requirement

Use a strict red-green cycle.

### RED

Create a focused regression test, preferably:

`tests/test_canonical_check_help.py`

It must exercise real current CLI functions/subprocess output rather than only searching source strings.

At minimum prove:

1. base `cnxclaw.py` help advertises `check cogentnexus-openclaw`;
2. v0.9.3 `cnxclaw_v093.py` help advertises `check cogentnexus-openclaw`;
3. neither help surface advertises generic `check cogentnexus|` or a whitespace/end-delimited generic component;
4. missing-component usage from `do_check(..., ["check"])` identifies `cogentnexus-openclaw`;
5. the canonical component is accepted by the actual check mapping;
6. generic component `cogentnexus` remains rejected as unsupported.

Run the focused test before production edits and require it to fail for the expected stale-help/usage reason. Record the exact RED command and failure.

### GREEN

Make the smallest production/documentation correction that satisfies the canonical contract.

Expected primary production files:

- `skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- `skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py`

Correct only the stale operator-facing component spelling. Do not change check verdicts, exit-code mapping, provider behavior, lifecycle behavior, aliases, controller state, plugin code, or installer flow.

Run the focused test and require PASS.

## Namespace lint defense

Strengthen the existing namespace lint only as much as required so a current non-historical `check cogentnexus` command cannot silently return.

Expected files if needed:

- `scripts/check_namespace_isolation.py`
- `tests/test_namespace_lint.py`

Add a failing lint regression first, prove RED, then implement the minimal command-specific detection and prove GREEN.

The lint must:

- reject `check cogentnexus` when generic is a complete component token;
- allow `check cogentnexus-openclaw`;
- keep existing historical coordination exclusions;
- avoid false positives for explanatory prose that is not an operator command where the existing lint contract excludes it.

## Current documentation sweep

Use the inventory to correct the exact invalid command in current operator-facing documentation/templates/examples, if present.

Do not alter:

- Task 050 task/report/review;
- earlier coordination history;
- immutable past release notes;
- machine-specific evidence.

Report every changed documentation path. If no current documentation outside the two CLI facades contains the invalid command, state that explicitly.

## Validation

Run and report at minimum:

1. focused canonical-help regression RED before production edits;
2. focused canonical-help regression GREEN after edits;
3. namespace-lint RED/GREEN if lint changes;
4. `python -m pytest -q` or the repository's complete accepted Python test command;
5. `python scripts/check_namespace_isolation.py`;
6. `python scripts/check_baseline_consistency.py`;
7. Python compile/self-tests used by the current validation workflow;
8. relevant plugin validation/build/tests/evaluation/production audit only if the diff or repository validation contract requires them; otherwise explicitly record why plugin code is unaffected;
9. whitespace/diff checks;
10. final `rg --pcre2 "check cogentnexus(?!-openclaw)"` inventory showing only classified historical evidence, or zero current occurrences.

No test may access or mutate the live workspace. Use temporary fixtures.

## Commit and publication structure

Implementation commit:

- change only the bounded production/test/current-documentation/lint paths;
- commit message: `fix: align canonical CogentNexus-OpenClaw check help`;
- do not include coordination `ACTIVE.md`, `STATUS.md`, task/review files, live artifacts, caches, package archives, or unrelated changes.

After the implementation commit, publish exactly one report-only commit at:

`docs/operations/coordination/reports/CNX-20260824-051-align-canonical-check-help.md`

Report commit message must begin:

`report: CNX-20260824-051 align canonical check help`

The report must include:

- fetched start HEAD;
- root-cause confirmation;
- complete pre/post invalid-command inventory and classification;
- exact RED and GREEN commands/results;
- implementation changed paths and commit SHA;
- full validation commands/results;
- side-effect accounting;
- remaining uncertainty;
- one exact result token.

Before publication, prove the report commit changes exactly the one report path relative to the implementation commit. Also prove the full Task 051 compare contains only the reviewed implementation paths plus the one report.

## Results

Return exactly one:

- `PASS_CANONICAL_CHECK_HELP_ALIGNED`
- `BLOCKED_SOURCE_OR_DUPLICATE_FENCE`
- `BLOCKED_ROOT_CAUSE_DRIFT`
- `BLOCKED_TDD_RED_NOT_REPRODUCED`
- `BLOCKED_CANONICAL_HELP_TEST`
- `BLOCKED_NAMESPACE_LINT_REGRESSION`
- `BLOCKED_FULL_VALIDATION`
- `BLOCKED_DIFF_SCOPE`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

A PASS requires a genuine observed RED for the stale help, GREEN after the minimal fix, canonical mapping preserved, generic component still rejected, full validation passing, and no live side effect.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- source/duplicate fence;
- invalid-command inventory;
- canonical-help RED;
- minimal production GREEN;
- namespace-lint RED/GREEN;
- full validation;
- implementation publication;
- report publication or blocker.

Progress updates are not pause points.

## Prohibited

No live workspace access or mutation; no installer/clean reinstall/migration; no installed-file edit; no OpenClaw config/plugin command; no Gateway/Ollama/scheduler/controller/lifecycle action; no reset/uninstall; no Procmon/Task 027/038 access; no primary-repository mutation; no HermesAgent/Ecosystem/staged-capability-loop action; no merge/tag/Release/archive; no unrelated refactor; no compatibility alias for generic `cogentnexus`.
