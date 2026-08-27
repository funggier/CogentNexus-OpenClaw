# Coordination Channel Status

**State:** `AWAITING_OPERATOR_DESIGN_APPROVAL`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator remains authority for definitive repair through final authenticated fresh-session semantic acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted baseline

Accepted source/live lineage through Tasks 078/079/080, 082, 084/085/086, 089, 090 and 091 remains in force.

Task 090 live recovery remains accepted: MANAGED, one canonical loaded plugin, accepted parity, Gateway/Ollama/SQLite healthy and `NO_FLASH_MULTI_TICK_PROVEN`.

Task 091 owner-authenticated Dashboard/WebChat surface remains accepted without secret disclosure.

Task 092 remains an accepted semantic blocker: fresh-session creation, Ticket-before-provider ordering, one correlated Ollama inference and one visible nonce passed; durable payload staging did not. Its semantic artifacts remain retired.

Task 093 preserved candidate repair:

`a924157ecdedef1d4f166d5762529b0d59536fc9`

It separates process-global TicketStore patch lifetime from per-runtime `reply_dispatch` registration and remains the intended Dashboard durable-staging fix.

## Task 094 result and review

Implementation:

`3313930064123867ad760908a77b498f3bad029a`

Report:

`0902c3c50fb1a46adfa9b8df86495fa521d01719`

Reported result:

`PASS_COMPLETE_INSTALLABLE_PLUGIN_PAYLOAD_ATTESTATION_REPAIRED`

Independent decision:

`REWORK`

Disposition:

`REWORK_WINDOWS_REPARSE_POINT_INDIRECTION_NOT_REJECTED`

Review:

`docs/operations/coordination/reviews/CNX-20260827-094-repair-complete-installable-plugin-payload-fingerprint.md`

Publication fence is valid.

## Preserved Task-094 attestation work

The v2 algorithm materially closes the original four-file fingerprint blind spot:

- package-owned files come from `package.json.files`, plus `package.json`;
- all declared runtime directories are recursively enumerated;
- normalized relative paths and exact bytes are hashed under a versioned domain;
- absolute installation roots are excluded;
- current npm11/npm12 packed set was reported 176/176 exact;
- current pre-Task093 installed payload and Task093+094 candidate were reported distinct under v2.

This design remains preserved.

## Current blocker

Task 094 required rejection of `symlinks/reparse-style path indirection` but production currently checks only `os.path.islink(path)` during package enumeration.

On Windows, a directory junction/reparse point is a distinct indirection form and is not guaranteed to satisfy the symbolic-link check. Such a path can be traversed by directory APIs and would violate the package-owned attestation boundary.

The regression suite proves a symlink case but does not prove a real Windows junction/reparse case.

No live install-over is authorized until this Windows path-indirection boundary is closed.

## Pending Task 095 design

A narrow source-only correction is proposed:

- add one exact path-indirection check;
- reject symlinks and Windows reparse-point/junction entries before traversal;
- apply it to declared entries and every recursive child;
- leave fingerprint v2 framing/package contract unchanged;
- mandatory Windows junction/reparse RED then GREEN;
- rerun npm11/npm12 equivalence, classifier/action truth tables, rollover plan/apply security/atomicity, Task-089 installer boundary, Task-093 staging and full suites.

## Hard fence

Until explicit operator approval of this bounded design:

- no Task-095 source implementation;
- no live install/reset/repair or generation mutation;
- no semantic message/provider probe;
- no controller/startup/Supervisor/AGENTS/config/runtime/SQLite change;
- no Task-092 state rewrite.

## Successor logic

After operator approval, Task 095 may be published source-only. Only independent acceptance of that Windows reparse-point hardening may release a one-shot supported live install-over. Only after live parity/MANAGED health are accepted may one new final authenticated fresh-session semantic attempt be authorized.
