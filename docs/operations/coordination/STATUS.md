# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK188_RELEASE_PUBLICATION__TASK194_DISPATCH_AND_VERIFY`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository + Actions  
**Active umbrella task:** `CNX-20260831-188`  
**Active publication subtask:** `CNX-20260831-194`  
**Disposition:** `WAITING_AUTHENTICATED_RELEASE_WORKFLOW_DISPATCH`

## Merge result

PR #26 is merged.

Exact authoritative merged `main` SHA:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

This SHA is frozen as the v0.9.3 publication candidate.

## Prior acceptance chain

- Task 191 repository repair: accepted;
- Task 192 real-Windows NO_REPLY repair requalification: `PASS`;
- Task 193 Recovery Reality CI contract repair: `PASS`;
- final PR head before merge: `66fdba1c6dc2ee0997c5764bc56a52f543741bdc`;
- all final-head release gates passed, including Validate, PS5.1 Acceptance, Windows Installer Pack, Recovery Reality, Recovery V2/V3, Gateway Convergence, Partial Repair, and Live Runner.

Accepted product/payload identities remain:

- repaired product candidate: `050ab53f4b593ab538143084d6bbdbf7e1672e34`;
- installable plugin payload-v2: `b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93` / `186` files.

Current provider boundary:

- managed runtime/operator provider: Ollama only;
- installer: provider-neutral.

## Active Task 194

Task:

[`tasks/CNX-20260831-194-v093-release-workflow-dispatch-and-publication-verification.md`](tasks/CNX-20260831-194-v093-release-workflow-dispatch-and-publication-verification.md)

Required exact dispatch after fresh authority checks:

- workflow: `.github/workflows/release.yml`
- ref: `main`
- `version=0.9.3`
- `candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31`

Dispatch exactly once. Then verify workflow terminal success, tag target, GitHub Release state, exact release asset set, archive integrity, and independent SHA-256 checksums.

## Hard fence

No force push, no source/runtime/plugin/test/installer/provider change, no main commit before publication, no release candidate retargeting, no manual release outside the approved Release workflow, and no duplicate dispatch/release/tag are authorized.
