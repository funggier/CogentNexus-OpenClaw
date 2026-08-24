# Review — CNX-20260824-056 Recover Live Plugin Generation

Decision: `ACCEPT`

Disposition: `ACCEPT_BLOCKER_OPENCLAW_OPTIONAL_PACKAGE_NAME`

Reviewed report:

`docs/operations/coordination/reports/CNX-20260824-056-recover-live-plugin-generation.md`

Report commit:

`884c84f269203338eeb144f7db715afe8eee8a51`

Report result:

`BLOCKED_RECOVERY_PLAN_UNSAFE`

## Publication and safety fence

The report commit is a direct child of the Task 056 coordination HEAD and adds exactly the matching report path. Phase A performed zero live mutations and did not create or apply a recovery plan.

## Accepted findings

- The supported OpenClaw 2026.7.1-2 plugin-list record omitted optional `packageName` while retaining the fields needed to bind the active record to an exact root and version.
- Task 055 `_active_registered_plugin()` required `packageName` unconditionally, so plan generation failed before any plan file or mutation.
- Task 056 correctly refused to transform the supported inventory or manufacture missing plan evidence.

## Source confirmation

At inspected OpenClaw source commit `b8d6e799a31d469f60277427472b87036b1f9be7`, `plugins list --json` serializes `PluginRecord` directly and `PluginRecord.packageName` is optional. Therefore the failure is a repository compatibility defect in the recovery primitive, not live-state drift.

## Decision

Accept the safe blocker. Do not authorize Phase B or reuse Task 056: it has a terminal blocker report and no plan SHA-256.

The narrow successor must add a schema-compatible regression fixture and allow an absent optional inventory `packageName` only when the bound exact payload manifests prove the expected ID/package/version. A present but wrong/null `packageName`, wrong/missing version, foreign root, or any existing ownership/boundary/tree/inventory contradiction must continue to fail closed.
