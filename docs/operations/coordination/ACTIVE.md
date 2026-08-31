# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK188_RELEASE_PUBLICATION__TASK197_CREDENTIALED_EXACT_CANDIDATE_PUBLICATION`
Current disposition: `TASK196_REVIEWED_FAIL__TASK197_READY__TASK198_QUEUED`
Task ID: `CNX-20260831-188`
Active publication subtask: `CNX-20260831-197`
Queued Discord investigation: `CNX-20260831-198`
Failed publication subtask: `CNX-20260831-196`
Completed repair subtask: `CNX-20260831-195`
Updated: 2026-08-31 ICT
Executor: Hermes
Coordinator / final reviewer: ChatGPT

## Current default branch / workflow identity

`main = c70552801ddbb9dc0a49c9cfc64368b9f4820f07`

## Frozen v0.9.3 release target

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Do not retarget the release merely to avoid the GitHub authorization boundary.

## Task 196 result

Release workflow run `33406148890` validated and staged the exact candidate assets, then failed during GitHub Release creation with `HTTP 403: Resource not accessible by integration`. No tag or Release exists.

The refined root cause is the GitHub authorization edge created because the frozen target differs from the current default branch in `.github/workflows/release.yml`; the Actions `GITHUB_TOKEN` cannot provide the workflow-write authority required for that target.

## Active task

[`tasks/CNX-20260831-197-v093-exact-candidate-credentialed-release-publication.md`](tasks/CNX-20260831-197-v093-exact-candidate-credentialed-release-publication.md)

Hermes must use a sufficiently authorized user/GitHub-App credential, download the exact retained artifact from run `33406148890`, verify it locally, and make exactly one Release creation attempt targeting `26ce64a624255278a3a0266ad38746e0e6ed2e31`. No rebuild and no workflow redispatch are authorized.

## Queued Discord defect

[`tasks/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md`](tasks/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md)

Task 196 proved divergent Discord session behavior plus an incomplete durable-delivery evidence path. Task 198 is queued for systematic diagnosis after publication; root cause is not yet claimed.

## User-directed lifecycle boundary

Release first. Do not reset/uninstall/reinstall before publication. Clean removal and fresh installation/reset testing remains deferred until after release.

## Hard fence

No candidate retarget, no archive rebuild, no Release workflow redispatch, no automatic retry after publication failure, no product/runtime/plugin/installer/provider/package mutation, no reset/uninstall/reinstall, and no force push.
