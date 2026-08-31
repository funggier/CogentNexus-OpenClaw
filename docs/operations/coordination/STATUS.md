# Coordination Channel Status

**State:** `IN_PROGRESS`  
**Execution mode:** `TASK198_DISCORD_SESSION_CORRELATION_AND_DURABLE_DELIVERY_INVESTIGATION`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository + Actions; bounded Hermes Windows/Discord evidence only when explicitly handed off  
**Active task:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `V093_PUBLISHED__TASK198_SOURCE_INVESTIGATION_ACTIVE`

## Public v0.9.3 authority

Task 197 is reviewed and accepted `PASS`.

- tag: `v0.9.3`
- tag target: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Release: public, non-draft, non-prerelease
- required assets: exactly three
- public asset digests independently verified against the retained validated artifact and `SHA256SUMS.txt`

No additional v0.9.3 publication action is required or authorized.

## Task 198 objective

Diagnose the Discord session/run-correlation and durable-delivery inconsistency observed in Task 196 before making any repair.

Live evidence to explain:

1. Discord session `agent:main:discord:channel:1531201432861282405` was blocked before the agent ran with missing correlation/delivery-observer prerequisites.
2. Discord session `agent:main:discord:channel:1531199905673252946` completed one Ticket/model-call lifecycle and produced a user-visible Discord response.
3. The successful session still showed a `missing-run-correlation` observer skip.
4. That completed Ticket had no `cnx_assistant_delivery` row, so the exact channel-specific durable-delivery contract must be traced before deciding whether table absence is defective.

## Method

Systematic debugging first, then TDD:

- read and trace existing hook/data-flow contracts;
- compare working and failing session paths;
- identify the minimum violated invariant;
- form one root-cause hypothesis;
- write and run a focused failing regression test;
- only then apply the minimum production fix;
- re-run focused/full validation;
- request one bounded Hermes reality test only if repository evidence requires live confirmation.

## Lifecycle boundary

The release-first gate is complete. Destructive clean uninstall/reset/fresh reinstall remains deferred during Task 198 source/evidence investigation; it may resume after the Discord defect is resolved or explicitly separated by a later coordination task.

## Hard fence

No force push, no republish/retarget of v0.9.3, no production mutation before root cause + RED, no test weakening, no provider substitution, no state deletion/reset/uninstall/reinstall to manufacture a passing Discord result, and no unbounded/repeated human-send testing.
