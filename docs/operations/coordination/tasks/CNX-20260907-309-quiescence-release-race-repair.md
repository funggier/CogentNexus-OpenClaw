# CNX-20260907-309 — Quiescence release replacement-race repair

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-308`
Executor: `Hermes`
Blocked candidate: `853650ce7f59687fbce172bd96543a38f288e47a`

## Authority

The Task308 report `BLOCKED_REVIEW_DEFECT__LEASE_RELEASE_REPLACEMENT_RACE` is published at remote commit `97b449b0690cc68974d368ca0251673e53e2495c`. This successor authorizes source-only TDD repair of the quiescence lease replacement race and exact-SHA source validation. It does not authorize any live installer, activation, Gateway/provider lifecycle, semantic send, replay, delivery disposition, database/session/Ticket mutation, version/tag/release change, or force push.

## Required procedure

1. Fresh-fetch and re-read `ACTIVE.md`, `STATUS.md`, this task, Task308 report, and exact source lineage. Require a clean tree and candidate `853650ce...` as the unmodified parent.
2. Add a deterministic production-shaped RED test proving that an old owner cannot unlink a replacement lease when stale reclamation/owner release interleave. Exercise the real `acquire`/`release` functions; do not mutate live state.
3. Run that test RED and retain the first failure. Fix only the owning quiescence primitive, using a cross-process-safe operation serialization/atomic ownership mechanism that keeps stale reclaim, acquire, owner/token validation, and unlink serialized. Preserve API shape, fail-closed mismatch behavior, crash/stale recovery, and no token plaintext in externally visible results.
4. Run focused quiescence tests, activation-safety tests, full Python suite, full plugin suite, build/schema/bootstrap/package validation, and production-only audit. Run independent security/logic review on the final source diff.
5. Commit test RED separately where practical, then minimal repair and any narrowly required fixture correction. Push without force. Bind all CI results to the exact new candidate SHA; do not reuse Task308 CI as acceptance for changed source.
6. Publish the matching Task309 report with exact RED/GREEN/review/CI evidence and stop. A separate successor must authorize fresh exact-candidate install and managed activation before release.

## Acceptance

- deterministic race RED observed before repair;
- minimal production repair GREEN with no regressions;
- independent review passed with empty security/logic blocker lists;
- exact-SHA CI terminal-successful for all required workflows;
- no live state, protected Ticket/session, semantic transport, or release metadata touched.

## Hard fences

No installer, `enable`, Gateway/provider restart, semantic send, replay/redelivery/disposition, session Delete/cancel, manual SQLite/Ticket/session/transcript/config mutation, release/tag/version mutation, force push, or reuse of the consumed Task308 installer/enable operations.

Report: `docs/operations/coordination/reports/CNX-20260907-309-quiescence-release-race-repair.md`
