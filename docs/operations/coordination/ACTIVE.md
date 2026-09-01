# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK219_REAL_BOUNDARY_RED_AND_DIST_CANONICALIZATION_REPAIR`
Current disposition: `TASK218_FAIL_RED_ACCEPTED__CROSS_PLATFORM_EQUALITY_PROVEN__BOUNDARY_REPAIR_REQUIRED`
Task ID: `CNX-20260901-219`
Parent task: `CNX-20260901-218`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / repository engineer
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Semantic repair base

Task-207 semantic repair remains based at:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

## Task-218 accepted result

Report:

`reports/CNX-20260901-218-task217-cross-platform-payload-determinism-tdd-repair.md`

Independent review:

`reviews/CNX-20260901-218-task217-cross-platform-payload-determinism-tdd-repair-review.md`

Accepted disposition:

`ACCEPT_FAIL_RED_NOT_REPRODUCED__CROSS_PLATFORM_EQUALITY_PROVEN__BOUNDARY_REPAIR_REQUIRED`

Experimental Task-218 candidate:

`e2dede9a0cb16b8b9536a350e018bfbd7c95c39b`

Accepted experimental evidence:

```text
Validate 33521283353: success
PS5.1 Acceptance Smoke 33521283398: success
Windows Installer Pack Smoke 33521283517: success
package-proof artifact: 9805795685
artifact digest: sha256:241846ea60531ebd45f008cf52ff3ebf4689c6887076b5b9bd1f92863c43a5d5
payload files: 192
CI fingerprint: 18a9003b47347bd598e58bef54f453313df8032943f5436cb9ed9096fe4bea14
fresh Windows fingerprint: 18a9003b47347bd598e58bef54f453313df8032943f5436cb9ed9096fe4bea14
```

The equality is real, but this candidate is not installer-authorized because:

- the required genuine pre-fix RED was not reproduced;
- the final helper broadened canonicalization from generated `dist` to tracked/static package files;
- independent source review found no proven no-follow symlink/junction boundary despite the report claim.

## Active Task 219

Hermes must execute:

`tasks/CNX-20260901-219-task218-real-boundary-red-and-dist-canonicalization-repair.md`

Task 219 must:

1. forward-revert only the unaccepted Task-218 production/build changes to restore effective pre-fix build behavior without rewriting history;
2. trace at least one actual Task-217 differing `dist` file back to the real source/output mechanism;
3. run a whole-real-source LF-vs-CRLF build probe;
4. establish a genuine assertion RED caused by different generated installable bytes, not harness failure;
5. commit corrected RED separately;
6. implement minimal GREEN only at generated `dist`, with sorted no-follow traversal and indirection rejection;
7. prove normal build does not dirty tracked files;
8. run full validation and authoritative CI;
9. establish a new candidate/package proof;
10. fresh-build the exact new candidate on Windows and require zero payload-byte difference vs CI.

The byte-exact fingerprint algorithm must remain unchanged. Do not accept multiple fingerprints.

## Runtime / Discord boundary

Task 219 authorizes:

`0 Discord Sends`

No installer/install-over, lifecycle action, live plugin/config mutation, Gateway restart, live SQLite/ownership/transaction mutation, provider/model substitution, or Release/tag mutation is authorized.

Only repository TDD/build/package work, isolated evidence builds, CI, and read-only live preservation checks are allowed.
