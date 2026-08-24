# CNX-20260824-042 — CogentNexus-OpenClaw Namespace Isolation Report

Status: SUCCESS
Result: `PASS_OPENCLAW_NAMESPACE_ISOLATED`
Implementation commit: `d0a692331b2e9f29fc9b318fcd7beac5d5acf4bb`
Branch: `agent/v0.9.3-recovery-reality-tests`

## What was actually changed

Implemented the intentional v0.9.3 namespace/API/installation-layout break in one isolated full clone. No live installation or runtime was touched.

Canonical rename map:

- product/display: `CogentNexus` -> `CogentNexus-OpenClaw` on current surfaces;
- CLI: `cnx.cmd` / `cnx` / `cnx.py` / `cnx_v093.py` -> `cnxclaw.cmd` / `cnxclaw` / `cnxclaw.py` / `cnxclaw_v093.py`;
- skill: `skills/cogentnexus` -> `skills/cogentnexus-openclaw`, with frontmatter `CogentNexus-OpenClaw`;
- state: `.cogent` -> `.cogentnexus-openclaw`;
- plugin: `cogentnexus-rotation` -> `cogentnexus-openclaw` and npm package `openclaw-plugin-cogentnexus-openclaw`;
- plugin display/config: `CogentNexus-OpenClaw Bridge`, `cogentNexusOpenClawRoot`;
- tools: generic `cogent_*` registrations -> the five required `cnxclaw_*` registrations;
- environment/durable prefix: `CNX_` -> `CNXCLAW_` on current operational surfaces;
- policy/supervisors: `AGENTS.cogentnexus-openclaw.md`, `CogentNexus-OpenClaw-Supervisor`, `cogentnexus-openclaw-supervisor`, and `ai.cogentnexus.openclaw.supervisor`;
- release archives: `cogentnexus-openclaw-v<version>` and release title `CogentNexus-OpenClaw v<version>`.

Added `ownership.json` under the new state root. Install/upgrade, repair, clean reinstall, reset, and uninstall now verify `productId`, display name, workspace, state root, plugin ID, paths, version, task/service identities, timestamp, and migration source before claiming or mutating owned state.

Legacy install-over now inventories without mutation, requires multiple independent identities, rejects mixed/corrupt/foreign state, invokes the installed legacy launcher exactly once for MANAGED/MAINTENANCE handoff, creates a versioned variant-scoped backup, stages and validates the new layout, creates the ownership manifest before MANAGED enable, and removes legacy artifacts only after new-namespace validation. Interrupted migration writes an exact recovery report and requests PASSTHROUGH.

Added deterministic ownership/coexistence tests with byte-identical HermesAgent sentinels, legacy PASSTHROUGH/MANAGED/MAINTENANCE cases, corrupt/ambiguous/mixed rejection, canonical fresh layout, install ordering, interruption-report, reset/uninstall ownership gates, release naming, and permanent-alias absence.

Added `scripts/check_namespace_isolation.py` to validation, release packaging, and local release publication gates. Historical coordination evidence and release notes before v0.9.3 are excluded. The reviewed migration-literal allowlist is limited to:

- `scripts/install.ps1`;
- `scripts/install.sh`;
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `tests/test_namespace_ownership.py`;
- `tests/test_namespace_install_contract.py`;
- `docs/releases/v0.9.3.md`.

Root, plugin manifest/package/lock versions are `0.9.3`. Added `docs/releases/v0.9.3.md`, including “กำหนดชื่อเรียกและ namespace ของแต่ละส่วนให้ชัดเจน”.

## Commands and exit codes

- `git fetch origin agent/v0.9.3-recovery-reality-tests` — exit `0` (before isolated clone creation).
- `python scripts/check_namespace_isolation.py` — exit `0`; PASS.
- `python scripts/check_baseline_consistency.py` — exit `0`; v0.9.3 baseline PASS.
- `python skills/cogentnexus-openclaw/scripts/validate.py --workspace-singleton` — exit `0`; PASS.
- `python -m compileall -q skills/cogentnexus-openclaw/scripts scripts tests` — exit `0`.
- `python -m pytest -q` — exit `0`; `208 passed, 1 skipped, 4 subtests passed`.
- `python skills/cogentnexus-openclaw/scripts/cogent.py self-test` — exit `0`.
- `python skills/cogentnexus-openclaw/scripts/runtime.py self-test` — exit `0`.
- `python skills/cogentnexus-openclaw/scripts/workflow.py self-test` — exit `0`.
- PowerShell parser validation for install, clean-reinstall, publish-release, and repair scripts — exit `0`.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/repair-v092-partial-windows.ps1 -SyntaxOnly` — exit `0`.
- `npm ci` in `plugins/cogentnexus-openclaw` — exit `0`.
- `npm run plugin:validate` — exit `0`; build, schema, ticket DB bootstrap, and package contents PASS.
- `npm test` — exit `0`; `49` files and `237` tests passed.
- `npm run evaluation` — exit `0`; all integrity/interruption/retry/deduplication/retrieval/provenance/latency gates passed.
- `npm audit --omit=dev` — exit `0`; `0 vulnerabilities`.
- `git diff --check` — exit `0` after normalizing the portable CMD template.
- `git diff --cached --check` — exit `0` before the final implementation commit.

The first attempted `python -m pytest -q` from the plugin directory returned exit `5` because that directory contains no Python tests; the full suite was then run from repository root and passed. A POSIX `bash -n scripts/install.sh` attempt could not start because this Windows environment has no `/bin/bash`; POSIX ordering/layout is covered by repository contract tests, while Windows PowerShell syntax and package assertions passed.

## Proof accounting

Proved:

- required canonical names and v0.9.3 metadata;
- new-only fresh layout and no permanent generic repository alias;
- fail-closed ownership verification for destructive/current lifecycle paths;
- multi-identity legacy proof and rejection of mixed, corrupt, unknown, or foreign ownership;
- legacy PASSTHROUGH, MANAGED, and MAINTENANCE planning, one handoff call in installer source, staged ordering, backup, and interrupted-migration report;
- reset/uninstall owned-path boundaries do not include HermesAgent sentinels;
- sibling HermesAgent files remain byte-identical in deterministic simulations;
- CI/release archive/title/package naming;
- Python and plugin behavior remained green after the rename.

Skipped by task safety gate:

- live install, install-over, reset, uninstall, gateway/plugin registration, scheduled task/service mutation, and OpenClaw/Ollama start/stop/restart;
- real GitHub tag, Release, or archive publication.

Not proved in this repository-only task:

- a destructive end-to-end migration on the operator's live machine;
- POSIX shell execution on this Windows host without Bash.

These are environment/runtime acceptance matters, not evidence of a repository implementation failure. The task explicitly prohibited live destructive acceptance.

## Problems and evidence

No acceptance blocker remains. During implementation, stale test imports and v0.9.2 version assertions failed after the intentional rename; they were updated and the full suite passed. Initial all-dependency npm audit output listed development-tree advisories, while the required production audit completed with zero vulnerabilities.

Blocker type: `NONE`.

Safest narrow remediation if later live migration acceptance fails: preserve the generated versioned migration backup and `migration-report.json`, keep native OpenClaw/PASSTHROUGH, and issue a separate diagnostic task scoped only to the failing migration boundary. Do not broaden cleanup or infer ownership from names.

Recommended method: review this implementation/report, then gate any live migration acceptance as a separate explicit task.

Human decision required: NO.

## Side-effect and duplicate-execution accounting

- Work occurred only in isolated full clone `C:\Users\CDQ-P\AppData\Local\Temp\cnx042-clone-20260823T235612Z`.
- No live OpenClaw configuration, installation, plugin, Gateway, Ollama, scheduler/service, retained Procmon evidence, or operator workspace was mutated.
- Local validation created ignored `node_modules` content in the isolated clone and installed `pytest` into the available Python environment because it was initially absent.
- No tag or GitHub Release was created.
- No matching Task 042 report existed before execution.
- No consequential side effect was repeated.
