# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_ONLY_TDD`
Current authorization: `CNX-20260828-106_NPM12_INSTALLER_CONTRACT_REGRESSION_REPAIR_NO_LIVE_MUTATION`
Task ID: `CNX-20260828-106`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-106-npm12-installer-contract-regression-repair.md`](tasks/CNX-20260828-106-npm12-installer-contract-regression-repair.md)

Task 106 is a source-only follow-up to the failed Task 105 real-Windows install-over attempt.

## Accepted Task-105 finding

Task 105 safely stopped after install-over failed in the OpenClaw `npm-pack:` metadata path on npm `12.0.2`.

The live machine remains intentionally preserved as:

- CogentNexus-OpenClaw mode: `PASSTHROUGH`;
- generation: `25`;
- Gateway: healthy;
- Ollama: healthy;
- SQLite: healthy;
- later destructive Task-105 phases: not executed;
- Dashboard semantic Send: not executed.

No live action is authorized by Task 106.

## Accepted source repair ancestry

- RED contract commit: `e0b6173d2ed888303bae3e31fd023b24e201c167`
- minimal installer fix: `c676c50cb19378541a8223263a609fb7d18ed5a8`
- npm12 production-shaped regression: `5e41c0c3a8b9da920571b828c9a863f5591af86b`

Windows Installer Pack Smoke run `33148715184` on `5e41c0c3...` is SUCCESS, including npm `12.0.2`, keyed-object pack metadata resolution, npm12-safe local archive invocation, and archive inspection.

PS5.1 Acceptance Smoke run `33148715168` on `5e41c0c3...` is SUCCESS.

Validate run `33148715162` reaches pytest but fails only three stale test assertions that still require the superseded executable `npm-pack:` invocation. Observed result: `3 failed, 390 passed, 30 skipped, 4 subtests passed`.

## Task-106 source scope

Hermes/Codex must make the smallest test-only repair to:

- `tests/test_fresh_transaction_failure_coverage.py`
- `tests/test_namespace_install_contract.py`
- `tests/test_npm_pack_installer_boundary.py`

The tests must require the current Windows local `.tgz` invocation while preserving existing ordering, rollback-inverse, rollover, artifact-resolution, and cleanup invariants.

Do not modify production source or the npm12 smoke workflow. If the focused tests require a production change, publish `BLOCKED` instead of widening scope.

## Hard fence

Task 106 does **not** authorize:

- live install/install-over/uninstall/reset/cleanup;
- runtime enable/disable/start/stop/restart;
- OpenClaw Gateway, Supervisor, or Ollama restart/change;
- npm/Node/OpenClaw/Ollama version change on the user's machine;
- live SQLite/config/session/runtime mutation;
- Dashboard semantic Send;
- credentials/token/password access or re-entry;
- reboot;
- production-source redesign;
- merge/tag/GitHub Release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-106-npm12-installer-contract-regression-repair.md`

After the report is pushed, stop for independent ChatGPT review. Do not invent or start the next live task.