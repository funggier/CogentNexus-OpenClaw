# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK188_RELEASE_PUBLICATION__TASK197_CREDENTIALED_EXACT_CANDIDATE_PUBLICATION`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository + Actions + bounded authenticated publication  
**Active umbrella task:** `CNX-20260831-188`  
**Active publication:** `CNX-20260831-197`  
**Queued Discord investigation:** `CNX-20260831-198`  
**Reviewed failed publication:** `CNX-20260831-196`  
**Disposition:** `AWAITING_HERMES_TASK197`

## Current authority

Current default branch / repaired workflow SHA:

`c70552801ddbb9dc0a49c9cfc64368b9f4820f07`

Frozen v0.9.3 release target:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-196 validated Actions artifact:

- run `33406148890`
- artifact ID `9763253683`
- name `release-assets-0.9.3-26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Task 196

Accepted as `FAIL_RELEASE_WORKFLOW`.

The package job passed. The publish job reached the GitHub Releases API but failed with `HTTP 403: Resource not accessible by integration`. No tag/Release/assets were published and no retry occurred.

The frozen target differs from current default `main` in `.github/workflows/release.yml`; creating a Release for that target requires workflow-write authority unavailable to the Actions `GITHUB_TOKEN` in this edge case.

## Task 197

Hermes is authorized to use a sufficiently privileged authenticated user/GitHub-App credential to publish the exact already-validated artifact once, while preserving tag target `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

No rebuild, workflow redispatch, candidate retarget, or automatic retry is authorized.

## Task 198

Discord/session evidence from Task 196 is recorded and queued for systematic investigation after publication. Current evidence proves session-to-session behavioral divergence and incomplete durable-delivery evidence, but not a root cause.

## Lifecycle boundary

Per user direction: release first. No reset/uninstall/reinstall until publication is complete.

## Hard fence

No force push, no product/runtime/plugin/installer/provider/package change under Task 197, no candidate retarget, no archive rebuild, no workflow redispatch, and no lifecycle mutation before release.
