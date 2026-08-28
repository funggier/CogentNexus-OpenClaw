# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued repository repair and use of Hermes/Codex when required; Task 106 is strictly source-only and preserves the live PASSTHROUGH state  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-106-npm12-installer-contract-regression-repair.md`](tasks/CNX-20260828-106-npm12-installer-contract-regression-repair.md)

Task ID:

`CNX-20260828-106`

## Why Task 106 exists

Task 105 real-Windows lifecycle acceptance failed during install-over after a safe MANAGED → PASSTHROUGH handoff. The exact OpenClaw error was the npm-pack metadata failure reproduced by the OpenClaw `2026.7.1-2` × npm `12.0.2` contract.

The accepted minimal repair changes Windows installation to pass the exact generated `.tgz` archive as a plain local path to OpenClaw, bypassing the incompatible `npm-pack:` metadata probe while retaining OpenClaw's archive extraction, plugin validation, security scan, dependency install, peer link, and managed plugin installation path.

## Current source evidence

Accepted ancestry:

- `e0b6173d2ed888303bae3e31fd023b24e201c167` — RED installer-path contract;
- `c676c50cb19378541a8223263a609fb7d18ed5a8` — minimal production fix;
- `5e41c0c3a8b9da920571b828c9a863f5591af86b` — npm12 production-shaped smoke regression.

Evidence on `5e41c0c3...`:

- Windows Installer Pack Smoke `33148715184`: SUCCESS, including npm `12.0.2`, keyed-object pack metadata, production resolver, local archive contract, and archive-content inspection;
- PS5.1 Acceptance Smoke `33148715168`: SUCCESS;
- Validate `33148715162`: package dry-run SUCCESS, but matrix pytest fails only three stale assertions that still hard-code the removed `npm-pack:` executable invocation;
- pytest observed: `3 failed, 390 passed, 30 skipped, 4 subtests passed`.

Task 106 is limited to correcting those stale test expectations without weakening their actual safety/order invariants.

## Preserved live state

The Windows machine remains intentionally untouched after Task 105 stopped:

- CogentNexus-OpenClaw: `PASSTHROUGH`, generation `25`;
- Gateway: healthy;
- Ollama: healthy;
- SQLite: healthy;
- reset/uninstall/fresh reinstall/recovery phases: not executed;
- Dashboard semantic Send: not executed.

Task 106 must not alter this state.

## Task-106 required output

Hermes/Codex must make the smallest test-only change to:

- `tests/test_fresh_transaction_failure_coverage.py`;
- `tests/test_namespace_install_contract.py`;
- `tests/test_npm_pack_installer_boundary.py`.

It must run focused pytest, full pytest, namespace isolation, and baseline consistency checks, then publish:

`docs/operations/coordination/reports/CNX-20260828-106-npm12-installer-contract-regression-repair.md`

The report must include exact implementation SHA, changed-file list, verification results, and explicit confirmation that production source/workflow and live runtime were not modified by Task 106.

## Hard fence

No live lifecycle action, runtime mutation, dependency/version change on the user's machine, Dashboard semantic Send, credential access/re-entry, production-source redesign, reboot, merge, tag, GitHub Release, or force push is authorized.

After the report is pushed, stop for independent ChatGPT review.