# CNX-20260827-094 — Repair Complete Installable Plugin Payload Fingerprint

Result: `PASS_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION_REPAIRED`

## Scope and live fence

This task was executed source/test-only. No live install-over, uninstall, reset, cleanup, plugin-generation mutation, controller/startup/Supervisor/AGENTS/config/runtime/SQLite edit, provider/model/timeout change, semantic message, direct Ollama/provider probe, restart, merge, tag, or release was performed.

The Task-092 semantic artifacts remain retired evidence and were not repaired or reused.

## Phase A — defect reproduction

- Coordination branch was fetched/reset before work.
- Execution HEAD before source edits: `41ba7815dd87b7ebda1b0a4e89b97ff9325c9272`
- Task-093 implementation/report and independent disposition were present in ancestry.
- The candidate plugin was built and validated using the production package contract.
- The old `_plugin_payload()` helper was reproduced as blind to a non-`ticket-store.js` shipped runtime file: changing only `dist/v091-dashboard-verified-delivery.js` left the old fingerprint unchanged.
- Read-only live comparison showed the installed legacy payload was distinguishable from the candidate under v2: live candidate root accepted by the new contract had v2 fingerprint `6d40f856313f6c295a51956d130cd977337a3dd8ac64fd51ed6db20f568b40cb`, while the final candidate fingerprint is recorded below. No live file was changed.

## Gate R — mandatory RED

Regression tests were added against the real production `namespace_ownership.py` helper and valid package-shaped fixtures.

Before production changes, the focused RED run produced:

```text
2 failed, 27 deselected
```

Both failures were the intended attestation blind spot:

- changing only `dist/v091-dashboard-verified-delivery.js` did not change the legacy fingerprint;
- renaming that shipped runtime path did not change the legacy fingerprint.

The failures were assertions on equal fingerprints, not fixture identity or package parsing errors.

## Gate F — canonical v2 implementation

`skills/cogentnexus-openclaw/scripts/namespace_ownership.py` now provides one canonical package-owned payload enumerator and fingerprint implementation.

The implementation:

- treats `package.json.files` as the package ownership contract;
- always includes `package.json`;
- recursively enumerates every regular file selected by literal file/directory entries;
- uses normalized relative POSIX paths;
- includes a versioned `cogentnexus-openclaw-plugin-payload-v2` domain separator;
- frames each path and exact file bytes with NUL delimiters;
- excludes absolute roots from the digest;
- rejects absolute paths, traversal, empty/dot path components, unsupported patterns, missing declared entries, symlinks and non-regular payloads;
- preserves strict manifest/package id and exact version checks;
- returns the existing 64-hex fingerprint shape and feeds existing classifier/lifecycle consumers.

The Task-093 Dashboard source fix was preserved unchanged.

## GREEN and regression evidence

The focused RED tests became GREEN after the minimal production implementation:

```text
73 passed, 1 skipped
```

This included complete-payload runtime content/path changes, root relocation invariance, source/cache exclusion, unsafe/missing/unsupported package paths and symlink rejection.

The existing classifier/lifecycle and rollover tests passed with the package-shaped fixtures:

```text
14 passed
```

Full Python suite after the final fixture and helper updates:

```text
381 passed, 3 skipped, 4 subtests passed
```

The three skips are existing platform-conditional tests.

`python -m py_compile skills/cogentnexus-openclaw/scripts/namespace_ownership.py`: pass.

Baseline consistency:

```text
CogentNexus-OpenClaw v0.9.3 baseline consistency: PASS (Bridge v0.9.3)
```

## npm package-set equivalence

The canonical enumerator produced exactly `176` files.

Actual `npm pack --dry-run --json --ignore-scripts` path sets were compared programmatically against the canonical set:

- Node 24.18.0 / npm 11.16.0: `176` packed, `176` canonical, missing `[]`, extra `[]`.
- Node 22.23.2 / npm 12.0.2: `176` packed, `176` canonical, missing `[]`, extra `[]`.

The npm 12 object-shaped JSON output was parsed using its actual supported shape. No tarball container bytes were used as the fingerprint authority.

## Node/plugin verification

Node 24.18.0 / npm 11.16.0:

- clean `npm ci --ignore-scripts`: exit `0`;
- full plugin suite: `49 files`, `257 tests passed`;
- `npm run plugin:validate`: exit `0`;
- TypeScript build: pass;
- schema verification: pass;
- ticket DB bootstrap: pass;
- package-content verification: pass, `176` packed files.

Node 22.23.2 / npm 12.0.2 isolated execution path:

- clean `npm ci --ignore-scripts`: exit `0`;
- full plugin suite: `49 files`, `257 tests passed`;
- `npm run plugin:validate`: exit `0`;
- TypeScript build: pass;
- schema verification: pass;
- ticket DB bootstrap: pass;
- package-content verification: pass, `176` packed files.

Task-093 Dashboard verified-delivery tests remained green in both plugin runs.

`git diff --check`: pass.

## Final fingerprint and attestation consequence

Final Task-093+094 candidate v2 plugin fingerprint after the final build:

```text
df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4
```

Canonical file count: `176`.

Read-only installed candidate comparison:

```text
installed legacy payload v2: 6d40f856313f6c295a51956d130cd977337a3dd8ac64fd51ed6db20f568b40cb
Task-093+094 candidate v2:   df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4
```

They differ. Therefore the future supported install classifier cannot treat the pre-Task-093 live payload as exact when given this candidate fingerprint.

## Publication fence

Source/tests implementation commit was pushed first:

```text
3313930064123867ad760908a77b498f3bad029a
```

This report is the only intended file in the report-only publication commit.

The next allowed successor gate is independent acceptance of:

```text
PASS_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION_REPAIRED
```

Only that acceptance may authorize the next one-shot supported live install-over. This task itself authorized zero live mutation and zero semantic sends.
