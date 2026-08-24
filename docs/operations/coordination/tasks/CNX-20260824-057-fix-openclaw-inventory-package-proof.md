# CNX-20260824-057 — Fix OpenClaw Inventory Package Proof

Status: `CHATGPT_EXECUTING`

Execution mode: `CHATGPT_REPOSITORY_ONLY`

Owner: ChatGPT

Executor: ChatGPT work environment

## Goal

Make the Task 055 recovery planner compatible with the supported OpenClaw 2026.7.1-2 plugin-inventory schema when optional `packageName` is absent, without weakening package identity, registration, path, wrapper, tree, inventory, PASSTHROUGH, ambiguity, or apply-time drift gates.

Repository code/tests/docs only. Do not access or mutate the live installation or retained evidence.

## Accepted root cause

OpenClaw `plugins list --json` serializes `PluginRecord`; at source commit `b8d6e799a31d469f60277427472b87036b1f9be7`, `PluginRecord.packageName` is optional. The live record omitted it but supplied exact canonical ID, version, root, source, origin, enabled, and status.

Task 055 tests always supplied `packageName`, while `_active_registered_plugin()` required it unconditionally before validating the exact active payload. That assumption blocks a valid supported inventory shape.

## Required design

1. Continue selecting exactly one record whose `id` is `cogentnexus-openclaw`.
2. Continue requiring an observed inventory version equal to `0.9.3`.
3. If the `packageName` key is present, require its value to equal `openclaw-plugin-cogentnexus-openclaw`; present null/empty/foreign values fail closed.
4. If the key is absent, do not infer package identity from the ID alone.
5. Resolve and boundary-check `rootDir`, then require `_plugin_payload()` to prove exact plugin ID/version and exact payload package name/version from the files at that bound root.
6. Normalize the plan's `activeRegistration.packageName` to the exact package and include evidence source `inventory` or `payload-package-json`.
7. Preserve the raw full inventory SHA-256 and normalized active-registration SHA-256 binding so apply must observe the same schema/content.
8. Do not change plan schema version, resolver ambiguity, wrapper proof, project-tree hashes, backup/move behavior, apply/rollback logic, installers, or lifecycle code.

## TDD contract

Before production code:

- add a regression test mirroring the live OpenClaw record without `packageName`/`packageVersion`;
- prove RED with `OpenClaw active canonical registration package/version is unproven`;
- assert the generated plan contains exact normalized package identity and `payload-package-json` evidence;
- preserve the existing exact-present package behavior with `inventory` evidence;
- prove a present null/foreign package remains rejected without moving either project;
- run the focused rollover suite and full repository suite after GREEN.

## Verification

Run at minimum:

- focused RED/GREEN rollover tests;
- full Python suite;
- namespace isolation and baseline consistency;
- Python compile check for `namespace_ownership.py`;
- POSIX shell syntax/static installer contracts;
- Windows wrapper/static tests available locally;
- `git diff --check` and exact changed-path fence;
- exact-head GitHub Actions before publishing the final report.

## Results

Return exactly one:

- `PASS_OPENCLAW_INVENTORY_SCHEMA_COMPAT_FIXED`
- `BLOCKED_PACKAGE_PROOF_WEAKENED`
- `BLOCKED_TEST_FAILURE`
- `BLOCKED_CI_FAILURE`
- `BLOCKED_UNRELATED_DRIFT`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260824-057-fix-openclaw-inventory-package-proof.md`

The report must include accepted Task 056 evidence, official schema confirmation, RED/GREEN evidence, exact production/test change, focused/full results, exact commits/paths, CI results, remaining uncertainty, live-action count `0`, and one exact result token.

The final report commit must change only the matching report path relative to the verified implementation HEAD.

## Hard fence

No live inventory capture, recovery plan/apply, installer, plugin/lifecycle action, generation move/delete, ownership rewrite, Gateway/Ollama/model/process/scheduler/supervisor action, primary-repository mutation, retained-evidence access, Procmon/Task 027/038 action, HermesAgent, Ecosystem, staged-capability-loop, merge, tag, release, or archive publication.

Report meaningful progress approximately every 3 minutes and at RED, GREEN, full verification, CI, and publication boundaries.
