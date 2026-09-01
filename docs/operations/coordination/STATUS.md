# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK219_REAL_BOUNDARY_RED_AND_DIST_CANONICALIZATION_REPAIR`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + isolated build/CI/Windows payload evidence through Hermes  
**Active task:** `CNX-20260901-219`  
**Parent:** `CNX-20260901-218`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK218_FAIL_RED_ACCEPTED__TASK219_REAL_BOUNDARY_REPAIR_READY`

## Publication authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 semantic repair base remains:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

## Task 218 reviewed boundary

Task-218 report disposition:

`FAIL_RED_NOT_REPRODUCED`

Independent review disposition:

`ACCEPT_FAIL_RED_NOT_REPRODUCED__CROSS_PLATFORM_EQUALITY_PROVEN__BOUNDARY_REPAIR_REQUIRED`

Task-218 experimental candidate:

`e2dede9a0cb16b8b9536a350e018bfbd7c95c39b`

Positive evidence retained:

```text
Validate: 33521283353 success
PS5.1 Acceptance Smoke: 33521283398 success
Windows Installer Pack Smoke: 33521283517 success
artifact: 9805795685
digest: sha256:241846ea60531ebd45f008cf52ff3ebf4689c6887076b5b9bd1f92863c43a5d5
payload files: 192
CI fingerprint: 18a9003b47347bd598e58bef54f453313df8032943f5436cb9ed9096fe4bea14
Windows fingerprint: 18a9003b47347bd598e58bef54f453313df8032943f5436cb9ed9096fe4bea14
```

That exact equality is accepted as evidence that canonicalization can solve the provenance mismatch. It is not enough to authorize installation because the genuine pre-fix RED was not reproduced.

Independent source review also found the experimental implementation broader than the proven boundary: it canonicalizes declared static package text as well as `dist`, and its `statSync`/read traversal does not independently prove fail-closed no-follow behavior for symlink/junction indirection.

## Active Task 219

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-219-task218-real-boundary-red-and-dist-canonicalization-repair.md`

Required flow:

- preserve Task-218 evidence/history; no reset/rebase/force push;
- forward-revert only the unaccepted Task-218 production/build effects so effective build is pre-fix;
- identify a real historical Task-217 differing `dist` path and trace it to the source/output mechanism;
- run full real-source LF-vs-CRLF build probes;
- refuse to fabricate RED if the mechanism is not reproduced;
- corrected RED must fail by exact generated-byte/fingerprint inequality, not harness error;
- minimal GREEN limited to generated `dist`, deterministic sorted traversal, no-follow `lstat`/indirection rejection;
- normal build must not dirty tracked files;
- full plugin/build/package validation and authoritative CI must pass;
- new exact candidate/package proof must be recorded;
- fresh Windows build of that exact SHA must match CI payload bytes/fingerprint exactly.

If Task 219 passes, a later task may resume Windows installer requalification using the new candidate and the direct Scheduled Task execution model qualified in Task 215.

## Runtime / Discord boundary

`0 Discord Sends`.

No installer/install-over, lifecycle action, live OpenClaw plugin/config mutation, Gateway restart, live ownership/staging/transaction/SQLite write, provider/model substitution, Release/tag mutation, or force push is authorized.
