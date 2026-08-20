# CogentNexus Current Operational State

**As of:** 2026-08-20  
**Version:** 0.9.1  
**Accepted Recovery Core:** `eadb89099637d24f96e265a500d66c577aa939a3`  
**Validated OpenClaw:** `2026.7.1-2`

## Classification

CogentNexus v0.9.1 is **operationally usable for general single-node managed use** on the validated stack once the release installation gates below pass. The recovery core is acceptance-proven. The project does not claim universal production hardening across every hardware, storage, concurrency, power-loss, or future OpenClaw scenario.

Fresh installation explicitly materializes both the base Ticket SQLite schema and the registration-time managed-runtime tables before MANAGED activation. This is required because the v095 Direct Recovery lane fence is installed during plugin registration and must see both `tickets` and `cnx_direct_recovery` before the first Chat turn. Release validation reproduces that exact registration precondition rather than validating only lazy TicketStore schema creation.

## Accepted capability boundary

| Capability | State |
| --- | --- |
| Ticket-first durable admission | Accepted |
| Fresh-install base + managed runtime DB bootstrap before MANAGED | Implemented / release-gated |
| v095 registration fence on an empty fresh DB | Regression-tested |
| DIRECT lane without forced workflow promotion | Accepted |
| Host-owned managed recovery authority | Accepted |
| Gateway/provider stop/restart recovery path | Accepted |
| Original provider/model recovery provenance | Accepted |
| Native OpenClaw restart ownership fence | Accepted |
| Recursive recovery intake suppression | Accepted |
| Same-session duplicate Ticket suppression | Accepted |
| Transient SQLite BUSY authority-read tolerance | Accepted |
| Single recovery inference attempt in Test A v16 | Accepted |
| Response-ready immutability | Accepted |
| One durable direct result | Accepted |
| Delivery confirmation / exactly-once-ish CNX delivery | Accepted |
| Recovery-session/temp cleanup after accepted test | Accepted |
| PASSTHROUGH design / native OpenClaw compatibility mode | Implemented |
| MAINTENANCE deliberate-stop semantics | Implemented |
| Real power-loss/cold-boot acceptance | Deferred |
| Newer OpenClaw version compatibility | Deferred |
| High-concurrency/long-soak hardening | Not fully accepted |
| Disk-full / DB corruption recovery | Not production-hardened |
| Exactly-once arbitrary external side effects | Requires adapter idempotency/verification |

## Test A v16 evidence summary

The accepted live recovery scenario demonstrated:

1. one original durable Ticket for the exact user prompt;
2. `workflow_eligible=0` with no generic workflow promotion;
3. Host timeout authority committed before recovery;
4. recovery on the original `ollama/qwen3.5:9b` route;
5. one Direct Recovery attempt and no retry event;
6. no SQLite lock error escaping the authority watcher;
7. no recursive self-intake or same-session extra Ticket;
8. native restart suppression only for the exact durable CNX-owned continuation;
9. one `response_ready`, one `direct_result`, one confirmed delivery;
10. clean post-recovery session/temp state.

The isolated recovery-core validation reproduced the accepted distribution hashes and passed targeted v094 3/3, targeted v099 11/11, the full 49-file/237-test plugin suite, plugin build/validation, and evaluation. Subsequent clean-install release validation additionally gates empty-database schema bootstrap and v095 registration readiness.

## Operational interpretation

For ordinary conversation, research, coding assistance, file/tool work, and other reversible or verifiable tasks, this baseline can be used normally with CNX MANAGED mode after installation reports healthy plugin registration and Ticket-first smoke testing succeeds.

For irreversible external effects, do not infer exactly-once execution solely from a completed CNX Ticket. External systems should expose idempotency keys, receipts, read-after-write verification, or another durable reconciliation mechanism.

## Frozen-core rule

Do not modify the accepted R2/R5B4 recovery behavior merely for cleanup or refactoring. Change it only when new failure evidence, a compatibility requirement, or an explicit feature requirement justifies reopening the boundary.

## Deferred acceptance

Power-loss/cold-boot testing and OpenClaw-version migration testing are intentionally deferred. Their absence is a known scope boundary, not evidence that the accepted Test A recovery path failed.
