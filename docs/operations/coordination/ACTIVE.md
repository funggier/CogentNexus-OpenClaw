# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK188_RELEASE_PUBLICATION__TASK194_DISPATCH_AND_VERIFY`
Current disposition: `WAITING_AUTHENTICATED_RELEASE_WORKFLOW_DISPATCH`
Task ID: `CNX-20260831-188`
Active publication subtask: `CNX-20260831-194`
Completed repair: `CNX-20260831-191`
Accepted requalification: `CNX-20260831-192`
Completed CI contract repair: `CNX-20260831-193`
Updated: 2026-08-31 ICT
Executor: Hermes / authenticated GitHub operator
Coordinator / final reviewer: ChatGPT

## Authoritative release identity

PR #26 has been merged.

Exact merged `main` SHA:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

This is the only authorized `candidate_sha` for v0.9.3 publication.

Accepted real-Windows repaired product candidate:

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

Accepted installable plugin payload:

`b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93` / `186` files.

## Active subtask

[`tasks/CNX-20260831-194-v093-release-workflow-dispatch-and-publication-verification.md`](tasks/CNX-20260831-194-v093-release-workflow-dispatch-and-publication-verification.md)

Task 194 is `READY_FOR_HERMES` because the ChatGPT GitHub connector available in the coordinating session can merge/read Actions state but does not expose `workflow_dispatch`.

## Exact next action

After fresh authority checks, dispatch `.github/workflows/release.yml` exactly once with:

- ref: `main`
- `version=0.9.3`
- `candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31`

Then monitor the same run through terminal state and verify tag/release/assets/checksums as required by Task 194.

## Publication fence

Before dispatch, prove:

- `main` is still exactly `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- tag/release `v0.9.3` do not already exist;
- no v0.9.3 Release workflow run has already been dispatched.

If any authority has drifted, stop rather than retargeting.

## Hard fence

No force push, no product/runtime/plugin/test/installer/provider change, no commit to `main`, no manual release outside `release.yml`, no candidate retargeting, and no second Release dispatch are authorized.
