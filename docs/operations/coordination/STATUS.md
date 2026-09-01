# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK222_STATIC_PAYLOAD_BYTE_GUARD_AND_CANDIDATE_REQUALIFICATION`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + isolated build/CI/Windows exact-first package evidence through Hermes  
**Active task:** `CNX-20260901-222`  
**Parent:** `CNX-20260901-221`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK221_TWO_STAGE_CARRYOVER_PROVEN__TASK222_STATIC_BYTE_GUARD_READY`

## Publication authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Accepted generated-output boundary

Task 219 established a genuine real-boundary LF/CRLF RED and a bounded generated-`dist` canonicalizer. The generated-output problem is considered solved at that boundary: 43 pre-fix generated differences reduced to zero after canonicalization, with byte-exact fingerprint semantics unchanged.

## Task 221 accepted boundary

Task-221 report disposition:

`PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN`

Independent review disposition:

`ACCEPT_PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN__FAIL_CLOSED_STATIC_BYTE_GUARD_REQUIRED`

Exact-first controls at `4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0` produced LF-only static package bytes and clean status under inherited/default `core.autocrlf=true`, explicit true, and explicit false.

The historical CRLF result reproduced only when a newer branch worktree was materialized first and Git then detached to the older target while the static blobs stayed unchanged across the attribute-policy transition. Therefore direct `core.autocrlf=true` is not the root cause; two-stage attribute/worktree state carry-over is.

The branch still contains the unaccepted `b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5` `-text` experiment, and the current package validator checks package membership but does not fail closed on static CRLF contamination.

## Active Task 222

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-222-static-payload-byte-guard-and-candidate-requalification.md`

Required outcome:

- genuine test-only RED proving static CRLF contamination currently passes package validation;
- RED committed separately;
- restore `.gitattributes` entries to `text eol=lf` by forward commit;
- minimal fail-closed static byte validation, with no tracked-file normalization side effect;
- contaminated input rejected before package identity/packing;
- generated `dist` canonicalizer remains generated-only;
- focused/full repository validation GREEN;
- one new exact candidate SHA;
- Validate + Windows Installer Pack Smoke + PS5.1 Acceptance Smoke GREEN on that exact SHA;
- new package-proof artifact recorded;
- fresh Windows exact-first checkout of the same candidate under inherited Git policy remains LF-only/clean;
- Windows payload path set and all 192 bytes match CI exactly, fingerprint equal;
- report and stop for independent review.

Only after Task 222 PASS + independent review may a later task resume Windows installer requalification using the Task-215 direct Scheduled Task topology.

## Runtime / Discord boundary

`0 Discord Sends`.

No installer/install-over, lifecycle action, live OpenClaw plugin/config mutation, Gateway restart, live SQLite/ownership/transaction write, provider/model substitution, Release/tag mutation, or force push is authorized.
