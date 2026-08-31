# Active Coordination Task

Status: `IN_PROGRESS`
Execution mode: `TASK188_RELEASE_PUBLICATION__TASK195_RELEASE_WORKFLOW_REPAIR`
Current disposition: `TASK194_FAILED__TASK195_RED`
Task ID: `CNX-20260831-188`
Active repair subtask: `CNX-20260831-195`
Failed publication subtask: `CNX-20260831-194`
Updated: 2026-08-31 ICT
Executor: ChatGPT / GitHub repository + Actions
Coordinator / final reviewer: ChatGPT

## Frozen release target

Accepted v0.9.3 candidate SHA remains:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task 194 Release run `33399493141` was dispatched exactly once against that SHA. The package job passed; publish failed before creating a tag/release because GitHub CLI repository discovery required a local git repository.

## Active task

[`tasks/CNX-20260831-195-release-publish-repository-context-repair.md`](tasks/CNX-20260831-195-release-publish-repository-context-repair.md)

## Current objective

Use TDD:

`RED regression test -> minimal repository-explicit publish fix -> GREEN -> fresh repair PR -> merge -> freeze workflow main SHA -> separately authorize second Release dispatch`

## Hard fence

No product/runtime/plugin/installer/provider/package payload change, no manual tag/release, no candidate retargeting, no second Release dispatch before Task 195 is merged and reviewed, and no force push.
