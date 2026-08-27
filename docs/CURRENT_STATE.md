# CogentNexus-OpenClaw Current Operational State

**Development line:** v0.9.3  
**Core version:** 0.9.3  
**OpenClaw Bridge package:** 0.9.3  
**Validated OpenClaw:** `2026.7.1-2`  
**Managed provider:** **Ollama only**  
**Accepted Recovery Core:** `eadb89099637d24f96e265a500d66c577aa939a3`  
**Published historical release:** v0.9.2  
**v0.9.3 publication state:** development candidate; not yet a GitHub Release

## Classification

CogentNexus-OpenClaw v0.9.3 is the current development line. Its operator-facing managed provider surface is **Ollama only**. The accepted Recovery Core remains the historical technical checkpoint for Ticket admission, Direct recovery, durable-result ownership, and delivery behavior, while current v0.9.3 source, tests, packaging, and documentation are being stabilized as one candidate before real-machine acceptance.

The v0.9.2 provider-neutral Ollama/LM Studio implementation remains frozen historical evidence and compatibility code. It is not the current v0.9.3 managed-provider contract.

## Current capability boundary

| Capability | v0.9.3 state |
| --- | --- |
| Ticket-first durable admission | Accepted Recovery Core / current validation |
| DIRECT lane without forced workflow promotion | Accepted Recovery Core / current validation |
| Host-owned managed recovery authority | Accepted Recovery Core / current validation |
| Gateway/Ollama lifecycle and recovery path | Current managed contract |
| Managed provider | **Ollama only** |
| Validated OpenClaw | `2026.7.1-2` |
| Original provider/model recovery provenance | Accepted / current validation |
| Native OpenClaw restart ownership fence | Accepted / current validation |
| Recursive recovery intake suppression | Accepted / current validation |
| Same-session duplicate Ticket suppression | Accepted / current validation |
| Transient SQLite BUSY authority-read tolerance | Accepted / current validation |
| Response-ready immutability | Accepted / current validation |
| Durable direct result and delivery confirmation | Accepted / current validation |
| PASSTHROUGH / native OpenClaw compatibility mode | Implemented / repository-gated |
| MAINTENANCE deliberate-stop semantics | Implemented / repository-gated |
| Read-only `cnxclaw check ...` | Implemented / repository-gated |
| Real power-loss/cold-boot acceptance | Deferred |
| Newer OpenClaw compatibility | Deferred |
| High-concurrency/long-soak hardening | Not fully accepted |
| Disk-full / DB-corruption recovery | Not production-hardened |
| Exactly-once arbitrary external side effects | Requires adapter idempotency/verification |

## Provider state semantics

Current v0.9.3 lifecycle operations target Ollama. Explicit `--provider ollama` remains accepted, and provider-bearing lifecycle operations without an explicit provider are normalized to Ollama by the v0.9.3 facade.

Historical v0.9.2 selected-provider/transition state can remain relevant during migration and native restoration. That compatibility requirement does not re-open LM Studio as a current v0.9.3 managed provider.

## System-check semantics

`cnxclaw check ...` is observational only. It does not start/restart processes, mutate provider state, repair runtime state, rewrite OpenClaw configuration, mutate the Ticket DB, or execute model inference.

Current examples:

```powershell
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
```

`check system` reports `READY`, `READY_WITH_WARNINGS`, `NOT_READY`, or `INDETERMINATE` with stable exit codes 0/1/2/3.

## Accepted Recovery Core evidence

The accepted live Test A v16 checkpoint demonstrated:

1. one original durable Ticket for the exact user prompt;
2. no generic workflow promotion for the tested Direct path;
3. Host recovery authority committed before recovery;
4. recovery on the original Ollama/model route;
5. one Direct Recovery attempt and no competing native-restart inference;
6. no SQLite lock error escaping the authority watcher;
7. no recursive self-intake or same-session extra Ticket;
8. one response-ready boundary, one durable result, and confirmed delivery.

That checkpoint is historical technical evidence. It is not by itself the final v0.9.3 release acceptance.

## Repository stabilization boundary

Before the real Windows machine is touched, v0.9.3 must have coherent source/tests/docs/CI/package/release policy and a frozen exact candidate containing:

- exact commit SHA;
- version;
- plugin payload-v2 fingerprint;
- payload file count;
- archive SHA256;
- GitHub Actions evidence.

If source changes after freeze, the candidate identity changes and a new candidate cycle is required.

## Operational interpretation

Current repository work must not be interpreted as permission to mutate the live Windows CNXCLAW installation. Clean uninstall, fresh reinstall, install-over, reset, runtime acceptance, and the final Dashboard semantic/durable-delivery probe belong to the separate live acceptance phase after the repository candidate is frozen.

For irreversible external effects, do not infer exactly-once execution solely from a completed CNXCLAW Ticket. External systems should expose idempotency keys, receipts, read-after-write verification, or another durable reconciliation mechanism.

## Historical boundary

v0.9.2 is a frozen historical release. Historical release notes and acceptance evidence may preserve LM Studio and older provider-neutral behavior when that is what actually occurred. Living v0.9.3 operator documentation must not present those historical capabilities as current managed behavior.
