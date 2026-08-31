# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK188_RELEASE_PUBLICATION__TASK196_SECOND_RELEASE_DISPATCH`
Current disposition: `TASK195_PASS__PR27_MERGED__AWAITING_HERMES_RELEASE`
Task ID: `CNX-20260831-188`
Active publication subtask: `CNX-20260831-196`
Completed repair subtask: `CNX-20260831-195`
Failed first publication subtask: `CNX-20260831-194`
Updated: 2026-08-31 ICT
Executor: Hermes
Coordinator / final reviewer: ChatGPT

## Workflow execution identity

Repaired authoritative `main` after PR #27 merge:

`c70552801ddbb9dc0a49c9cfc64368b9f4820f07`

PR #27 merged only the Task 195 release-workflow/test/coordination repair. The publish step is now repository-explicit.

## Frozen v0.9.3 release target

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

This remains the `candidate_sha` and tag target. Do not substitute the repaired workflow merge SHA.

## Active task

[`tasks/CNX-20260831-196-v093-second-release-dispatch-and-publication-verification.md`](tasks/CNX-20260831-196-v093-second-release-dispatch-and-publication-verification.md)

## Current objective

Hermes must fresh-check authority, dispatch `.github/workflows/release.yml` exactly once from repaired `main` using:

- `version=0.9.3`
- `candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31`

Then verify workflow success, exact tag target, Release metadata, all three assets, and independent SHA-256 equality before publishing the Task 196 report.

## User-directed lifecycle boundary

Do not run reset/uninstall/reinstall before release. The user explicitly chose to publish first and perform clean removal/fresh installation testing afterwards.

## Hard fence

No manual tag/release, no second dispatch retry, no product/runtime/plugin/installer/provider/package change, no candidate retargeting, no reset/uninstall/reinstall, and no force push.
