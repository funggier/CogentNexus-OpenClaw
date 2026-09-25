# Active Coordination

Status: `IN_PROGRESS`
State: `CNX446_LIVE_GREEN_INSTALLER_DEPENDENCY_LIFECYCLE_REPAIR_LOCAL_GREEN_COMMIT_PENDING`
Task: `CNX-20260925-446-dashboard-direct-terminal-final-boundary.md`
Assigned executor: `ChatGPT`
Review owner: `ChatGPT independent final verification`
Human final authority: `Operator`
Working branch: `cnx-446-dashboard-direct-terminal-final-boundary`
Target release line: `v0.9.8`

## Current objective

Close the OpenClaw 2026.9.5 Dashboard Direct terminal-final defect and qualify v0.9.8 without weakening native Ollama behavior or install-over recovery.

## Delivery repair state

The production Codex/App-Server defect is repaired and live-qualified:

- original exact implementation commit: `70a41c5d5465a898cc10cd23e5b415ffdf5695f2`;
- original exact-SHA GitHub Validate / PS5.1 Acceptance Smoke / Windows Installer Pack Smoke: GREEN;
- fresh Codex live run `cnx446-live-codex-b-send-v1`: GREEN;
- commentary and tool rows remained non-terminal;
- only the exact `runTerminal=true` final produced the durable Direct result;
- final text SHA-256 matched the Ticket payload exactly;
- exactly one durable result, delivery confirmation, and Ticket completion occurred.

Native OpenClaw/Ollama fallback is also live GREEN:

- run: `cnx446-ollama-live-a`;
- model: `ollama/qwen3.8:27b`;
- runtime: native `openclaw`;
- final: `CNX446_OLLAMA_NATIVE_OK`;
- native transcript exposed neither `mirrorOrigin` nor `runTerminal`, as expected;
- final SHA-256 matched the Ticket payload exactly;
- exactly one durable result, delivery confirmation, and completion occurred.

## Installer qualification finding

A real v0.9.8 candidate install-over exposed a separate OpenClaw 2026.9.5 lifecycle behavior: `openclaw plugins enable|disable` may persist the requested mutation and then fail to exit until the 180-second timeout.

The Host helper now handles only that ambiguous timeout case:

1. preserve the normal 180-second checked mutation path unchanged;
2. on `subprocess.TimeoutExpired` only, verify the canonical config boolean;
3. regenerate the official plugin registry with `plugins registry --refresh`;
4. require `plugins inspect --json` to report the exact requested enabled/status state with no diagnostics;
5. accept the timeout only when all three OpenClaw-owned authorities agree;
6. otherwise re-raise the original timeout and remain fail-closed.

No SQLite state is edited directly.

## Second real install-over finding

The first timeout-reconciliation commit `6f8c9ab25b52da8673fa9099cc2660063581d570` was pushed and all exact-SHA GitHub workflows were GREEN. A new real install-over from that exact SHA then stopped before classification/first install mutation because candidate preparation ran plain `npm ci`.

On this machine, npm resolved the plugin peer/dev dependency `openclaw@2026.7.1-2` and entered its `postinstall-bundled-plugins.mjs` lifecycle script. That child stopped making progress. The installer parent was terminated before the first install mutation, and the orphaned npm/node child tree was explicitly removed.

The candidate dependency install is now narrowed to `npm ci --ignore-scripts` in both installer preparation paths. This still installs the dependency graph required by TypeScript/plugin validation, while preventing peer/dev dependency lifecycle side effects from running during CNX candidate preparation. The CNX plugin itself has no required install lifecycle script; explicit `npm run plugin:validate` and `npm pack` remain authoritative build/package gates.

## Current validation

- plugin-mutation timeout reconciliation focused tests: 6/6 PASS;
- related Host / installer regression for that repair: 90/90 PASS;
- production OpenClaw parser probe: config=true, inspect=true;
- dependency-lifecycle RED: 1 passed / 1 failed before `--ignore-scripts`;
- dependency-lifecycle focused GREEN: 2/2 PASS;
- installer transaction/runtime/package regression after `--ignore-scripts`: 60/60 PASS;
- PowerShell parser for `scripts/install.ps1`: PASS;
- full Python after the second installer repair: 743 passed, 5 skipped, 38 subtests passed;
- `git diff --check`: PASS;
- prior Codex/App-Server and native Ollama live acceptance remain GREEN.

## Immediate next gates

1. commit and push the exact source SHA containing the dependency-lifecycle repair;
2. require exact-SHA GitHub Validate / PS5.1 Acceptance Smoke / Windows Installer Pack Smoke GREEN on that SHA;
3. perform a real install-over from that exact SHA;
4. prove installed/source parity, plugin loaded state, Gateway health, and runtime attestation;
5. rerun a fresh Codex progress -> tool -> terminal live acceptance on the installed candidate;
6. restore the v092 supervisor and re-prove stable runtime health;
7. only then prepare/publish v0.9.8.

## Baseline authority

v0.9.7 remains the immutable published baseline. Its tag/release is not moved or rewritten.
