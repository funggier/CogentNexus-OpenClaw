# Review — CNX-20260825-066 Clean Reinstall Owned Runtime Live Acceptance

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_FRESH_INSTALL_REPRODUCIBILITY_AND_PARTIAL_RECOVERY`

Reviewed report commit: `d6812dd90a6ca28557cf18b6008a88dbfe5fe926`
Reviewed Task 065 implementation source: `21686f70520c5e0263e8aea4d644d2c87324e872`

## Publication fence

Independent compare from coordination HEAD `53348b24542dfd1bdbdc302c03773d10c41886b5` to report HEAD `d6812dd90a6ca28557cf18b6008a88dbfe5fe926` is ahead by exactly one commit and adds only:

`docs/operations/coordination/reports/CNX-20260825-066-clean-reinstall-owned-runtime-live-acceptance.md`

No repository source mutation was published by Task 066.

## Accepted live evidence

Task 066 correctly recovered the interrupted executor phase before mutation, then completed preservation and supported clean uninstall. The old Hermes-bound PT1M supervisor task, launcher, installed skill, live state root, application-data root, plugin registration/config, and managed AGENTS block were removed by the supported uninstall while OpenClaw Gateway, Ollama model inventory, unrelated plugin/config state, and the accepted AGENTS baseline were preserved.

The old flash-producing Scheduled Task is therefore no longer registered. This is not yet final no-flash acceptance because CogentNexus has not been freshly installed and no new supervisor has been observed across natural ticks.

## Independently confirmed blocker D1 — lockfile reproducibility

The reviewed plugin lockfile contains:

- `node_modules/openclaw/node_modules/@types/retry` at `0.12.5`;
- `node_modules/openclaw/node_modules/p-retry` at `4.6.2` with exact dependency `"@types/retry": "0.12.0"`.

This confirms the reported npm 12 `npm ci` consistency failure is source-bound rather than a speculative environment issue. A previously permissive npm version is not an acceptable substitute for a reproducible lockfile.

## Independently confirmed blocker D2 — partial-install dead end

`namespace_ownership.py::classify_install()` treats any non-empty new-namespace inventory as upgrade and immediately calls `verify_manifest()`. Therefore a failed fresh install that has already created new-namespace state/skill artifacts but has not yet created `ownership.json` cannot be classified for retry. The supported uninstall path also requires ownership proof. The reported partial state is therefore a real recovery gap.

## Review decision

The Task 066 result `BLOCKED_FRESH_INSTALL_FAILURE` is accepted. The executor followed the mutation fence by stopping instead of manually deleting residue or fabricating ownership.

The machine must not be described as repaired or freshly installed. Current accepted live condition is:

- OpenClaw native Gateway healthy;
- Ollama healthy and model inventory preserved;
- no CogentNexus supervisor task;
- no CogentNexus launcher/plugin registration;
- partial failed-install residues remain at the two reported workspace roots;
- CogentNexus is not in MANAGED operation.

## Required successor

A source-only successor must first:

1. make the plugin lock reproducible under the supported/current npm toolchains without relying on a permissive npm version;
2. add a bounded, durable fresh-install transaction/recovery contract so a failure before `ownership.json` cannot dead-end future supported install/recovery;
3. add RED/GREEN executable tests for both defects and full canonical validation;
4. publish implementation and report separately.

Only after independent acceptance may a live successor remove the exact Task-066-created residue under a bounded proof, retry fresh install, verify owned runtime binding, observe at least three natural PT1M ticks, and complete MANAGED health acceptance.
