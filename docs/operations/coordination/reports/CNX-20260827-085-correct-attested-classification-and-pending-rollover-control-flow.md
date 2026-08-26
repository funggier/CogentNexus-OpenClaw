# CNX-20260827-085 — Correct Attested Classification and Pending-Rollover Control Flow

Result: `PASS_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW_REPAIRED`

## Scope and live fence

Task 085 was source/test-only. No live installer/install-over, uninstall, reset, cleanup, plugin-generation mutation, controller/startup/Supervisor/AGENTS/ownership/config/runtime/SQLite/session mutation, Dashboard/WebChat message, CLI semantic message, direct Ollama probe, provider/model/timeout change, restart, reboot, merge, tag or release was performed.

Evidence directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue-20260826T225937Z`

Execution HEAD before implementation:

`0f67bdbd9e23cf1ea2761630f3dc05d36cc637eb`

The exact Task-084 implementation/rework base was preserved:

`0847a260d6f689f364bb096bd7857bb1dd4d58e1`

## Task-084 rework findings reproduced — RED

The three independent review findings were reproduced against the Task-084 implementation before the Task-085 production changes:

### R1 — ordinary single-generation changed-source upgrade

A coherent single manifest-owned v0.9.3 generation with an old fingerprint and an explicit different candidate-source fingerprint was sent through the real attested classifier. The predecessor rejected it instead of returning normal upgrade:

```text
manifest-owned plugin does not match the expected source attestation
```

Required final result is `upgrade`, `pendingRollover=false`, `pluginAlreadyExact=false`.

### R2 — pending action truth table

The executable production-action test for:

```text
mode=upgrade, pendingRollover=true, pluginAlreadyExact=false, SkipPlugin=false
```

failed because the predecessor’s lifecycle gate skipped both package installation and rollover. Required actions are:

```text
installPlugin=false
rolloverPlugin=true
```

### R3 — equivalent old generations must not impersonate source

Two equivalent old/replacement generations with an explicit different expected source fingerprint were accepted by the predecessor. The predecessor only compared replacement and retired fingerprints and did not always enforce explicit source equality. Required behavior is fail-closed.

The RED run showed the three expected Task-085 failures while predecessor Task-084 tests remained green.

## Gate C — corrected classification truth table

`classify_install()` now accepts optional explicit inventory and expected source fingerprint inputs while preserving generic strict behavior.

### One manifest-owned candidate

When the only canonical candidate is manifest-owned:

- fingerprint equals expected source:
  - `mode=upgrade`
  - `pendingRollover=false`
  - `pluginAlreadyExact=true`
- fingerprint differs from expected source:
  - `mode=upgrade`
  - `pendingRollover=false`
  - `pluginAlreadyExact=false`
  - manifest path is returned
  - replacement path is deterministic `null` until OpenClaw installs the replacement

The changed old candidate is no longer rejected merely because it is not source-exact; it proceeds through ordinary install-over behavior.

### Two-candidate pending recovery

With explicit inventory and expected source fingerprint, the pending path returns `pendingRollover=true` only after all existing topology, ownership, registration, wrapper, version and PASSTHROUGH fences pass.

`_exact_rollover_state()` now always enforces:

```text
active replacement fingerprint == explicit expected source fingerprint
```

This applies even when active replacement and retired fingerprints happen to equal each other. Without explicit expected authority, equivalent historical rollover behavior remains compatible and changed replacements remain rejected.

Generic `resolve_installed_plugin()` remains ambiguous/fail-closed for two candidates.

## Gate A — production plugin lifecycle action truth table

Added the executable PowerShell 5.1-compatible production helper:

`scripts/resolve-plugin-lifecycle-actions.ps1`

It is invoked by `scripts/install.ps1` and returns the single lifecycle action decision:

| mode | pending | exact | install plugin | rollover |
|---|---:|---:|---:|---:|
| fresh | false | false | true | false |
| legacy | false | false | true | false |
| upgrade | false | false | true | true |
| upgrade | true | false | false | true |
| upgrade | false | true | false | false |
| any | SkipPlugin | any | false | false |

The helper rejects logically impossible `pending=true` and `exact=true`.

Direct PowerShell 5.1 execution verified all supported rows and the impossible combination.

## Gate I — installer control flow

`scripts/install.ps1` now consumes the production action resolver and separates package installation from rollover:

```text
if installPlugin:
    npm-pack / openclaw plugins install / disable replacement

if rolloverPlugin:
    rollover-plan / rollover-apply
```

Specific behavior:

- ordinary changed-source upgrade: install then attested rollover;
- pending recovery: skip npm pack and plugin install, perform attested rollover first;
- already-exact upgrade: skip npm pack, plugin install and rollover;
- fresh/legacy: preserve plugin creation without upgrade rollover;
- Ticket DB bootstrap remains a single idempotent non-SkipPlugin action before lifecycle gates;
- pending rollover completes before later unique plugin resolution and ownership publication;
- no third semantic generation is created by the pending path.

Candidate fingerprint derivation and read-only inventory capture remain before classification and before live mutation.

## Security and atomicity preservation

Task-084 protections remain intact and all existing tests pass:

- changed replacement without source attestation rejected;
- wrong expected fingerprint rejected;
- explicit expected source mismatch rejected even for equivalent old/new payloads;
- generic two-candidate resolution remains ambiguous;
- active old-root registration rejected for pending rollover;
- outside-state registration rejected;
- three candidates rejected;
- foreign/shared wrappers rejected;
- wrong id/package/version rejected;
- non-PASSTHROUGH rollover rejected;
- inventory, manifest and replacement tree drift rejected;
- unrelated projects preserved;
- atomic rename failure preserves old/new/manifest;
- final verification failure restores project and manifest;
- exact plan hash remains required.

## Verification

Focused Task-085/classification/installer/recovery/npm-pack suite:

`93 passed`

Expanded full Python suite:

`372 passed, 2 skipped, 4 subtests passed`

Baseline:

`CogentNexus-OpenClaw v0.9.3 baseline consistency: PASS (Bridge v0.9.3)`

Python compile:

`pass`

PowerShell 5.1 syntax:

`PS51_SYNTAX_PASS`

PowerShell action resolver:

All truth-table rows passed; impossible pending+exact row failed closed as required.

### Node 24 / npm 11

- clean `npm ci`: passed
- full plugin suite: `49 files, 257 tests passed`
- `npm run plugin:validate`: passed
- package contents: `176` files
- mixed-plugin validation: passed
- Ticket DB bootstrap: passed

### Node 22 / npm 12

- clean `npm ci`: passed
- full plugin suite: `49 files, 257 tests passed`
- `npm run plugin:validate`: passed
- package contents: `176` files
- mixed-plugin validation: passed
- Ticket DB bootstrap: passed

`git diff --check`: passed.

## Plugin payload preservation

No file under:

`plugins/cogentnexus-openclaw/**`

changed relative to the Task-084 base. Final working-tree inspection reported:

`plugin_payload_diff=zero`

Implementation changes were limited to:

- `scripts/install.ps1`
- `scripts/resolve-plugin-lifecycle-actions.ps1`
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
- `tests/test_plugin_generation_rollover.py`

## Read-only live preservation

Task-085 did not repeat live mutation or normalization. Preserved Task-084 evidence and final read-only state show:

- controller remains PASSTHROUGH, generation 13;
- ownership manifest remains bound to prior generation `g-5593cbcfff5b35d5`;
- newer generation `g-7257c4555ca8ad21` remains registered disabled;
- old fingerprint remains `7e9189f8...`;
- newer/source fingerprint remains `8fd911e3...`;
- startup remains disabled;
- Supervisor remains absent;
- AGENTS managed markers remain absent;
- Gateway remains healthy/dashboard reachable;
- Ollama remains healthy with accepted four-model inventory;
- SQLite remains valid with zero Tickets/outbox;
- no semantic/provider activity was generated.

## Mutation accounting

- live installer/install-over: `0`
- live uninstall/reset/cleanup: `0`
- live plugin-generation mutation: `0`
- controller/startup/Supervisor/AGENTS/ownership/config/runtime mutation: `0`
- SQLite/Ticket/session mutation: `0`
- semantic/user messages: `0`
- Dashboard/WebChat/CLI sends: `0`
- direct Ollama/provider probes: `0`
- provider/model/timeout changes: `0`
- restart/reboot: `0`

## Publication fence

Implementation commit:

`6b5c9d56a48d4affe67c2bb718898378edee6e8a`

The implementation worktree was clean after commit and contained no plugin payload changes.

Only this report will be published as the Task-085 report-only commit:

`docs/operations/coordination/reports/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md`

Final disposition:

`PASS_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW_REPAIRED`

Only a separately authorized live recovery task may now mutate the current Task-083 two-generation partial installation. That successor must use this exact source, re-prove the source/live fingerprint match, invoke the supported installer once, complete pending rollover without a third generation or manual cleanup, restore MANAGED/startup/Supervisor/AGENTS, prove parity and health, observe five natural no-flash ticks and prove Dashboard owner-surface readiness without sending a semantic message.
