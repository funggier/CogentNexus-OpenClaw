# CNX-20260827-084 — Repair Same-Version Rollover Attestation and Pending Recovery

Result: `PASS_ATTESTED_SAME_VERSION_ROLLOVER_AND_PENDING_RECOVERY_REPAIRED`

## Scope and live fence

Task 084 was source/test-only. No live installer, install-over, uninstall, reset, cleanup, plugin-generation deletion/rename, controller/startup/Supervisor/AGENTS/ownership/config/runtime mutation, SQLite/Ticket/session mutation, Dashboard/WebChat message, CLI semantic run, direct Ollama probe, provider/model/timeout change, restart, reboot, merge, tag or release was performed.

Evidence directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue-20260826T214558Z`

Execution checkout:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue-20260826T214558Z\clone`

## Lineage and commits

Execution HEAD before implementation:

`e7acf12e354db056abb8ec39e6157fe0028e34c7`

Accepted Task-083 blocker report and review were present in the fetched coordination history. The accepted prior source was:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

Implementation commit:

`0847a260d6f689f364bb096bd7857bb1dd4d58e1`

Implementation scope is exactly:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
- `scripts/install.ps1`
- `tests/test_plugin_generation_rollover.py`

No file under `plugins/cogentnexus-openclaw/**` changed. `git diff --check` and Python compilation passed.

## Phase A — live/source fingerprint proof

Read-only evidence: `a02-fingerprint-proof.txt` and `a05-live-preservation.txt`.

Production fingerprint primitive is `_plugin_payload()` and the new CLI/API surface is:

```text
namespace_ownership.py plugin-fingerprint --plugin-root <path> --version 0.9.3
```

It requires the exact product/package/version and the existing four-file payload contract, then returns normalized root, version and SHA-256 fingerprint.

Observed values:

| payload | fingerprint |
|---|---|
| accepted source candidate `df412ed...` | `8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360` |
| live Task-083 newer generation `g-7257c4555ca8ad21` | `8fd911e3b8f6326c8907b7d92c11028d931df203dcaafdb59cc1e6d0a3b56360` |
| live manifest-owned prior generation `g-5593cbcfff5b35d5` | `7e9189f81eeda728a35a0722f69cfd4a3b48e0fac36fde8d846a188072577332` |

The newer live replacement is source-exact and the prior generation differs, satisfying the prerequisite for an attested recovery path.

## Gate R — RED evidence

Before implementation, the new focused tests were run against the predecessor source:

`17 passed, 5 failed`

Expected failures:

- `build_plugin_rollover_plan()` had no expected-replacement attestation argument;
- `classify_install()` had no inventory/attestation interface;
- rollover plan CLI rejected `--expected-replacement-fingerprint`;
- the legitimate changed same-version source-attested payload could not be authorized;
- Task-083 pending topology had no explicit classification path.

The existing negative changed-payload test remained green, proving the predecessor did reject the changed same-version replacement. The RED tests also covered wrong attestation and no-attestation ambiguity.

## Gate A — source attestation contract

Added `plugin_fingerprint()` and the `plugin-fingerprint` CLI command. It reuses `_plugin_payload()` and rejects incomplete, wrong-id, wrong-package or wrong-version payloads.

Extended rollover plan construction with:

- `expectedReplacementFingerprint`
- `replacementAuthorization`

Changed same-version behavior:

- equal retired/replacement fingerprints retain the existing equivalent-generation path;
- changed fingerprints require a valid 64-hex expected source fingerprint;
- replacement fingerprint must equal expected source fingerprint exactly;
- wrong or absent attestation fails before retirement;
- plan/apply bind and re-prove the expected fingerprint.

`rollover-apply` re-proves the attested replacement immediately before atomic retirement through the same `_exact_rollover_state()` path. Existing manifest, inventory, wrapper, project-tree, plan-hash, PASSTHROUGH and rollback fences remain intact.

## Gate P — pending and idempotent classification

`classify-install` now accepts optional:

```text
--plugin-inventory-json <path>
--expected-replacement-fingerprint <sha256>
```

Without both inputs, generic ambiguous resolution remains fail-closed.

With explicit attestation:

- exact two-generation Task-083 topology returns `mode=upgrade`, `pendingRollover=true`, `pluginAlreadyExact=false`, old manifest path, new active path and expected fingerprint;
- wrong/missing attestation fails closed;
- exact single manifest-owned source-matching generation returns `pluginAlreadyExact=true` and skips redundant generation creation;
- fresh installs without a product registration retain the existing fresh classification behavior.

Generic `resolve_installed_plugin()` remains strict and still rejects two candidates as ambiguous.

## Gate I — installer orchestration

`scripts/install.ps1` now:

1. performs candidate-only `npm ci` and `npm run plugin:validate` before source fingerprint derivation;
2. derives expected fingerprint from the source plugin candidate, not live inventory;
3. captures OpenClaw plugin inventory read-only before classification;
4. passes inventory and source fingerprint to the explicit classifier;
5. skips npm pack/plugin install when `pendingRollover=true` or `pluginAlreadyExact=true`;
6. passes expected source fingerprint into rollover planning;
7. preserves existing normal changed-payload npm-pack/install flow for ordinary upgrades;
8. preserves temporary inventory cleanup without losing the classification exit code;
9. continues existing owned-runtime, launcher, ownership, AGENTS and MANAGED restoration after successful rollover.

The pending recovery path therefore completes the already-installed source-exact replacement before any new plugin install and does not create a third semantic generation.

## Gate C — deterministic fixture

The production-facing fixture uses:

- manifest-owned old v0.9.3 generation;
- active disabled new v0.9.3 generation;
- different old/new fingerprints;
- expected source fingerprint equal to the new generation;
- exactly two valid managed npm wrappers;
- PASSTHROUGH controller.

Verified flow:

1. generic resolver remains ambiguous;
2. unattested classification remains ambiguous;
3. attested classification returns pending rollover;
4. attested plan/apply succeeds;
5. old project moves to the exact backup boundary;
6. manifest binds the new generation;
7. unique resolution returns the new generation;
8. source and installed fingerprints match;
9. no third generation is created by the fixture.

## GREEN and security matrix

Focused rollover/namespace/installer/recovery/npm-pack tests:

`90 passed`

Full Python suite:

`368 passed, 2 skipped, 4 subtests passed`

Negative and atomicity coverage remains green, including:

- no-attestation changed payload rejection;
- wrong-attestation rejection before retirement;
- foreign/shared wrapper rejection;
- active old-root rejection;
- outside-state rejection;
- three-candidate rejection;
- non-PASSTHROUGH rejection;
- inventory drift rejection;
- manifest drift rejection;
- payload/tree drift rejection;
- atomic rename failure preservation;
- final verification rollback;
- unrelated project preservation;
- exact plan hash enforcement.

## Toolchain and validation verification

### Node 24 / npm 11

- clean `npm ci`: passed
- full plugin test suite: `49 files, 257 tests passed`
- `npm run plugin:validate`: passed
- package contents: `176` files
- mixed-plugin validation: passed
- Ticket DB bootstrap: passed

### Node 22 / npm 12

- clean `npm ci`: passed
- full plugin test suite: `49 files, 257 tests passed`
- `npm run plugin:validate`: passed
- package contents: `176` files
- mixed-plugin validation: passed
- Ticket DB bootstrap: passed

### Other checks

- PowerShell 5.1 installer syntax: `PS51_INSTALL_SYNTAX_PASS`
- `python -m py_compile`: passed
- baseline consistency: `PASS (Bridge v0.9.3)`
- `git diff --check`: passed
- plugin payload diff: zero

## Read-only live preservation

Final evidence: `a05-live-preservation.txt`.

After all source/test work:

- controller remained `passthrough`, generation `13`;
- ownership manifest SHA-256 remained `3428c74b9f51389de7a1934630102896bae90c060b2b65e51fd2dbc1380b3bed`;
- AGENTS markers remained `0/0`;
- OpenClaw registration remained on `g-7257c4555ca8ad21`, disabled;
- both Task-083 generations remained present;
- old/new fingerprints remained `7e9189f8...` / `8fd911e3...`;
- Gateway/Ollama/SQLite state was not mutated by Task 084;
- no semantic/provider activity was generated.

The live partial installation was not normalized, deleted, or manually repaired.

## Mutation accounting

- live installer/install-over: `0`
- live uninstall/reset/cleanup: `0`
- live plugin generation mutation: `0`
- live controller/startup/Supervisor/AGENTS/ownership/config/runtime mutation: `0`
- live SQLite/Ticket/session mutation: `0`
- semantic/user messages: `0`
- Dashboard/WebChat sends: `0`
- CLI semantic runs: `0`
- direct Ollama/provider probes: `0`
- provider/model/timeout changes: `0`
- restart/reboot: `0`

## Final disposition

`PASS_ATTESTED_SAME_VERSION_ROLLOVER_AND_PENDING_RECOVERY_REPAIRED`

Only the next separately authorized live recovery task may mutate the current Task-083 two-generation partial installation. That successor must use this exact accepted source, re-prove the live fingerprints, perform one supported installer invocation, complete the attested pending rollover without manual deletion or a third generation, restore MANAGED/startup/Supervisor/AGENTS, prove parity/health, observe five natural no-flash ticks, and prove Dashboard/WebChat owner-surface readiness without sending a semantic prompt.
