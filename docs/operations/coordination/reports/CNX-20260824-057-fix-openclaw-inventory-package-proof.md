# CNX-20260824-057 — Fix OpenClaw Inventory Package Proof

Status: **PASS**

Result: `PASS_OPENCLAW_INVENTORY_SCHEMA_COMPAT_FIXED`

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-recovery-reality-tests`

Reviewed start HEAD: `884c84f269203338eeb144f7db715afe8eee8a51`

Remote implementation HEAD: `f379e5c5d8dddb144cb0d1991b645b16055e1303`

## Accepted blocker and root cause

Task 056 safely stopped before recovery plan creation because the supported OpenClaw 2026.7.1-2 plugin-list record omitted optional `packageName`, while Task 055 `_active_registered_plugin()` required that field unconditionally.

The behavior was checked against OpenClaw source commit `b8d6e799a31d469f60277427472b87036b1f9be7`:

- `src/cli/plugins-list-command.ts` serializes `PluginRecord` into `plugins list --json`;
- `src/plugins/registry-types.ts` declares `PluginRecord.packageName` optional.

Therefore the defect was the recovery primitive's interface assumption, not a reason to transform inventory or relax active-root ownership.

## TDD evidence

Before production changes, a regression record removed `packageName` while retaining the supported canonical registration fields. The exact RED result was:

`RuntimeError: OpenClaw active canonical registration package/version is unproven`

The existing focused baseline was `15 passed`. After the narrow implementation:

- the new regression passed;
- the focused rollover suite passed `17 passed`;
- present exact package identity uses `inventory` evidence;
- absent optional package identity uses `payload-package-json` evidence;
- present null or foreign package identity remains rejected;
- all prior root, ambiguity, wrapper, inventory-drift, atomic-move, rollback, and CLI-round-trip tests remain green.

## Implementation

The implementation changes only `_active_registered_plugin()`:

1. an observed inventory version must still equal v0.9.3;
2. if `packageName` is present, it must exactly equal `openclaw-plugin-cogentnexus-openclaw`;
3. if absent, no package identity is inferred from the plugin ID;
4. the bound `rootDir` must still be inside OpenClaw state and `_plugin_payload()` must prove exact plugin ID/version plus package name/version from the payload manifests;
5. normalized `activeRegistration` records the exact package and `packageNameEvidence` source;
6. raw full-inventory and normalized-registration SHA-256 bindings remain unchanged in purpose and are rechecked at apply.

No plan schema, installer, resolver, wrapper proof, tree hashing, backup/move, apply, rollback, or lifecycle behavior changed.

## Changed paths

Implementation commit `f379e5c5d8dddb144cb0d1991b645b16055e1303` changes exactly:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `tests/test_plugin_generation_rollover.py`.

Preceding coordination commits add the Task 056 review, Task 057 specification, and current coordination pointers. Operational machine details were intentionally omitted from the successor review/status publication.

## Local verification

- full Python suite: `275 passed, 1 skipped, 4 subtests passed`;
- namespace isolation: PASS;
- v0.9.3 baseline consistency: PASS;
- workspace-singleton validation: PASS;
- Python compile: PASS;
- POSIX installer syntax: PASS;
- `git diff --check`: PASS;
- local/remote implementation trees: byte-identical.

The single local skip is the Windows-only runtime test on the Linux work host; Windows CI executed the platform coverage successfully.

## Exact-head GitHub verification

Every workflow associated with implementation HEAD `f379e5c5d8dddb144cb0d1991b645b16055e1303` completed successfully:

- Validate `32748714805`;
- Windows Installer Pack Smoke `32748714747`;
- PS5.1 Acceptance Smoke `32748714957`;
- PS5.1 Live Runner Smoke `32748714938`;
- PS5.1 Partial Repair Smoke `32748714791`;
- PS5.1 v0.9.3 Gateway Convergence Smoke `32748714744`;
- PS5.1 v0.9.3 Ollama Recovery V2 Smoke `32748714751`;
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke `32748714818`;
- PS5.1 v0.9.3 Ollama Recovery Reality Smoke `32748714862`.

Validate passed package dry-run plus Ubuntu, macOS, and Windows jobs on Python 3.11 and 3.14.

## Safety and remaining work

- live inventory captures: **0**;
- recovery plan/apply invocations: **0**;
- installer/plugin/lifecycle actions: **0**;
- Gateway/Ollama/model/process/scheduler/supervisor actions: **0**;
- primary-repository, retained-evidence, Procmon, or excluded-system actions: **0**.

The repository compatibility defect is fixed and proved. A new Task 058 must independently repeat plan-only preflight and plan generation; no recovery apply or MANAGED enable is authorized by this result.
