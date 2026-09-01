# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK222_STATIC_PAYLOAD_BYTE_GUARD_AND_CANDIDATE_REQUALIFICATION`
Current disposition: `TASK221_ACCEPTED__TWO_STAGE_CARRYOVER_PROVEN__FAIL_CLOSED_STATIC_BYTE_GUARD_REQUIRED`
Task ID: `CNX-20260901-222`
Parent task: `CNX-20260901-221`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / repository engineer + authenticated Windows verifier
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted generated-output repair

Task 219 genuine RED and bounded generated-output repair remain accepted evidence:

- LF/CRLF real plugin build: 188 generated files each;
- pre-fix differing generated files: 43;
- bounded `dist` canonicalizer lineage: `9af329b4de7c02fda35b467d84e76bb0f0bb0944`;
- post-repair `dist` differences: 0;
- fingerprint algorithm unchanged.

## Task-221 accepted result

Report:

`reports/CNX-20260901-221-task220-exact-first-checkout-control-adjudication.md`

Review:

`reviews/CNX-20260901-221-task220-exact-first-checkout-control-adjudication-review.md`

Accepted disposition:

`ACCEPT_PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN__FAIL_CLOSED_STATIC_BYTE_GUARD_REQUIRED`

Accepted facts:

- exact `4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0` static Git objects are LF-only;
- exact-first materialization yields LF-only static bytes under inherited/default `core.autocrlf=true`, explicit true, and explicit false;
- the historical CRLF mismatch is reproduced only by two-stage materialization: newer branch working tree first, then detach to older target whose static blobs are unchanged but attributes differ;
- direct `core.autocrlf=true` alone is not the root cause;
- current branch still carries the unaccepted `b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5` `-text` experiment;
- merely relying on checkout discipline is insufficient as a fail-closed package provenance control.

## Active Task 222

Hermes must execute:

`tasks/CNX-20260901-222-static-payload-byte-guard-and-candidate-requalification.md`

Required flow:

1. fresh authority/product-drift check;
2. test-only RED proving current package validation accepts deliberately CRLF-contaminated static package bytes;
3. commit RED separately;
4. restore the four `.gitattributes` entries to `text eol=lf` by forward commit, preserving history;
5. minimally make package validation reject CRLF/noncanonical bytes in the four static package identity files without rewriting them;
6. prove contaminated two-stage-style input fails closed before package identity/packing;
7. full repository/build/plugin validation;
8. establish one exact final candidate SHA;
9. authoritative CI on that exact SHA and retain its new package proof;
10. fresh Windows exact-first materialization of that same candidate, build/validate, then require 192-file path equality, zero byte differences, exact CI/Windows fingerprint equality, and clean tracked status;
11. report and stop.

Task 222 is repository/package provenance only. A PASS does not itself authorize installer execution; independent review is required first.

## Runtime / Discord boundary

Task 222 authorizes `0 Discord Sends`.

No installer/install-over, lifecycle action, live OpenClaw plugin/config mutation, Gateway restart, live SQLite/ownership/transaction mutation, provider/model substitution, Release/tag mutation, or force push is authorized.
