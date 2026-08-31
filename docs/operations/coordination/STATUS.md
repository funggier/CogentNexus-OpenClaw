# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK188_RELEASE_PUBLICATION__TASK196_SECOND_RELEASE_DISPATCH`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository + Actions  
**Active umbrella task:** `CNX-20260831-188`  
**Active publication:** `CNX-20260831-196`  
**Completed repair:** `CNX-20260831-195`  
**Disposition:** `AWAITING_HERMES_SECOND_RELEASE_DISPATCH`

## Repair merge

PR #27 merged successfully.

Repaired workflow execution `main` SHA:

`c70552801ddbb9dc0a49c9cfc64368b9f4820f07`

## Frozen release target

v0.9.3 `candidate_sha` remains:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

The repaired main SHA is workflow execution identity only.

## Task 196

Hermes is authorized to perform exactly one second Release workflow dispatch from repaired `main` with:

- `version=0.9.3`
- `candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31`

After success, verify tag target, GitHub Release, required assets, and independent SHA-256 equality, then publish the Task 196 report and stop.

## Lifecycle boundary

No reset/uninstall/reinstall before release. Clean removal and fresh installation testing is deferred until after publication per user direction.

## Hard fence

No manual tag/release, no retry after a failed second dispatch, no candidate retargeting, no product/runtime/plugin/installer/provider/package mutation, no lifecycle reset/uninstall/reinstall, and no force push.
