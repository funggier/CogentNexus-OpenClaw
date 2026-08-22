# CogentNexus Current Operational State

**As of:** 2026-08-21  
**Core version:** 0.9.2  
**OpenClaw Bridge package:** 0.9.1 (unchanged payload)  
**Accepted Recovery Core:** `eadb89099637d24f96e265a500d66c577aa939a3`  
**Validated OpenClaw:** `2026.7.1-2`

## Classification

CogentNexus v0.9.2 is **operationally usable for general single-node managed use** on the validated Windows/OpenClaw/Ollama stack once release installation gates pass. The accepted v0.9.1 Recovery Core remains the authority for Ticket admission, Direct recovery, durable-result ownership, and delivery.

v0.9.2 adds provider-neutral local lifecycle support, durable selected-provider/transition state, LM Studio adapters, and read-only system pre-flight checks without rewriting the accepted Recovery Core.

LM Studio lifecycle support is implemented and repository-tested, but has not yet received the same target-machine live acceptance as Ollama. Treat that as a provider-specific acceptance boundary, not as a change to the Core recovery guarantees.

## Accepted capability boundary

| Capability | State |
| --- | --- |
| Ticket-first durable admission | Accepted |
| Fresh-install base + managed runtime DB bootstrap before MANAGED | Implemented / release-gated |
| DIRECT lane without forced workflow promotion | Accepted |
| Host-owned managed recovery authority | Accepted |
| Gateway/provider stop/restart recovery path (Ollama baseline) | Accepted |
| Original provider/model recovery provenance | Accepted |
| Native OpenClaw restart ownership fence | Accepted |
| Recursive recovery intake suppression | Accepted |
| Same-session duplicate Ticket suppression | Accepted |
| Transient SQLite BUSY authority-read tolerance | Accepted |
| Single recovery inference attempt in Test A v16 | Accepted |
| Response-ready immutability | Accepted |
| One durable direct result | Accepted |
| Delivery confirmation / exactly-once-ish CNX delivery | Accepted |
| PASSTHROUGH design / native OpenClaw compatibility mode | Implemented |
| MAINTENANCE deliberate-stop semantics | Implemented |
| Durable selected provider (`ollama` / `lmstudio`) | Implemented / release-gated |
| Interrupted provider-transition resume marker | Implemented / unit-tested |
| LM Studio discovery/start/stop/readiness adapter | Implemented / unit-tested; live acceptance pending |
| Provider-neutral Direct-stall lifecycle translation | Implemented / unit-tested; Ollama live Core remains accepted baseline |
| `cnx check system` aircraft-style pre-flight | Implemented / read-only invariant tested |
| Component checks under `cnx check ...` | Implemented |
| Real power-loss/cold-boot acceptance | Deferred |
| Newer OpenClaw version compatibility | Deferred |
| High-concurrency/long-soak hardening | Not fully accepted |
| Disk-full / DB corruption recovery | Not production-hardened |
| Exactly-once arbitrary external side effects | Requires adapter idempotency/verification |

## Provider state semantics

A successful `start --provider <name>` commits `selectedProvider` only after provider + Gateway verification. `start`/`restart` without a provider reuse the last successfully selected provider.

A provider switch writes `providerTransition` before lifecycle mutation. If the process or machine dies before selection commit, the next start resumes the transition target instead of silently falling back.

`stop`, `disable`, restart and reboot preserve the selected provider. `reset` returns to fresh provider-selection semantics; when both Ollama and LM Studio are installed, reset requires an explicit provider choice.

## System-check semantics

`cnx check ...` is observational only. It does not start/restart processes, mutate provider selection, repair runtime state, rewrite config, mutate the Ticket DB, or execute model inference.

`check system` reports `READY`, `READY_WITH_WARNINGS`, `NOT_READY`, or `INDETERMINATE` and uses stable exit codes 0/1/2/3.

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

v0.9.2 intentionally layers provider selection/preflight above this accepted behavior. It does not reopen the Ticket/result/delivery classifier.

## Operational interpretation

For ordinary conversation, research, coding assistance, file/tool work, and other reversible or verifiable tasks, this baseline can be used normally with CNX MANAGED mode after installation and `cnx check system` report an acceptable readiness state.

For irreversible external effects, do not infer exactly-once execution solely from a completed CNX Ticket. External systems should expose idempotency keys, receipts, read-after-write verification, or another durable reconciliation mechanism.

## Frozen-core rule

Do not modify the accepted Recovery Core merely for cleanup or refactoring. Change it only when new failure evidence, a compatibility requirement, or an explicit feature requirement justifies reopening the boundary.

## Deferred acceptance

LM Studio live acceptance, power-loss/cold-boot testing, and OpenClaw-version migration testing are intentionally deferred. Their absence is a known scope boundary, not evidence that the accepted Test A recovery path failed.
