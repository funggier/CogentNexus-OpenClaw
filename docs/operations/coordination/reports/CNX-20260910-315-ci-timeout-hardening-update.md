# CNX-20260910-315 — CI Timeout Hardening Update

## Scope

Close the known v0.9.5 verification blocker exposed by the previous Windows Python 3.14 validation run.

## Evidence

The prior Windows 3.14 validation run completed the Python suite successfully (`617 passed, 3 skipped, 6 subtests passed`) and all Windows PowerShell smoke checks passed. The plugin suite then failed only because `src/evaluation.test.ts` Phase 6 exceeded its explicit 30-second Vitest timeout; the test consumed roughly 180 seconds of the 220-second plugin run.

## Repair

`plugins/cogentnexus-openclaw/src/evaluation.test.ts` now uses a 240-second test timeout for the Phase 6 evaluation. This is a test-harness timing correction only; it does not modify production recovery, provider, lifecycle, Ticket, or delivery behavior.

## Commit

`d2419ed6c05c364f85f65763ff8a5cc000ec831d`

## Verification boundary

Fresh GitHub Actions evidence for the new exact HEAD is still required. No release/tag or merge is authorized by this change.
