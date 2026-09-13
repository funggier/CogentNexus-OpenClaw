# CogentNexus-OpenClaw Current Operational State

**Current release:** `v0.9.5` — published and operationally validated  
**Main baseline:** `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`  
**Git tag:** `v0.9.5` → exact main merge SHA above  
**GitHub Release:** `CogentNexus-OpenClaw v0.9.5` — published, non-draft, non-prerelease  
**Validated OpenClaw:** `2026.7.1-2 (0790d9f)`  
**Managed provider:** **Ollama**  
**Cloud provider mode:** OpenClaw-owned **pass-through**

See [POST_RELEASE_BASELINE.md](POST_RELEASE_BASELINE.md) for the concise release baseline and evidence summary.

## Current classification

CogentNexus-OpenClaw v0.9.5 is the current published stable baseline. Final acceptance, exact-head release-gating validation, controlled actionable-wake validation, PR merge verification, immutable tag verification, and post-release exact-tag installation/runtime verification have completed.

The release was verified from a fresh detached checkout of `v0.9.5`. The checkout resolved to the exact merge SHA, reported repository and plugin version `0.9.5`, and executed the installer successfully. The installed plugin loaded in OpenClaw and matched the exact-tag `dist` tree by file count and tree fingerprint.

## Release identity

```text
main:     50be0b973c30fd8d1528aaac3497c0fc3b0b4d95
v0.9.5:   50be0b973c30fd8d1528aaac3497c0fc3b0b4d95
PR:       #38 — merged
release:  CogentNexus-OpenClaw v0.9.5
```

The merge commit has parent `6439dd963003856ee1b1f1f6f802fa2aa60d6612` and the accepted candidate `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`. GitHub verified the merge commit.

## Operational validation

The accepted runtime path demonstrated:

```text
human intent
-> durable Ticket admission
-> logical session/run ownership
-> model execution
-> durable result
-> delivery confirmation
-> settled state
```

Controlled actionable wake was verified with exactly one durable work item. Ticket/session/run identity, generation and ownership semantics were preserved, and the system returned to idle without duplicate owner activity.

The post-release baseline additionally verified:

- `main` and `v0.9.5` exact release identity;
- exact-tag detached installation;
- `VERSION` and plugin package version `0.9.5`;
- successful installer execution;
- plugin loaded at version `0.9.5`;
- Gateway healthy;
- Ollama installed/reachable/healthy/ready;
- Ticket store integrity;
- supervisor health;
- pending outbox `0`;
- source/installed `dist` tree identity;
- completed GitHub check-runs on the merge SHA with successful conclusions.

## Capability boundary

| Capability | Current v0.9.5 state |
| --- | --- |
| Ticket-first durable admission | Operationally validated |
| DIRECT lane without forced workflow promotion | Operationally validated |
| Host-owned managed recovery authority | Operationally validated |
| Gateway/Ollama lifecycle and recovery path | Operationally validated |
| Managed provider | **Ollama** |
| Cloud provider mode | **OpenClaw-owned pass-through** |
| Validated OpenClaw | `2026.7.1-2 (0790d9f)` |
| Original provider/model recovery provenance | Accepted |
| Native OpenClaw restart ownership fence | Accepted |
| Recursive recovery intake suppression | Accepted |
| Same-session duplicate Ticket suppression | Accepted |
| Transient SQLite BUSY authority-read tolerance | Accepted |
| Response-ready immutability | Accepted |
| Durable direct result and delivery confirmation | Accepted |
| Bare `NO_REPLY` durable/UI leakage fence | Accepted and requalified |
| Bounded same-run sentinel finalization handling | Implemented and requalified |
| PASSTHROUGH / native OpenClaw compatibility | Accepted |
| MAINTENANCE deliberate-stop semantics | Accepted |
| `reset` explicit-`y` fresh-state reconstruction | Accepted |
| `uninstall` ownership-safe external preservation | Accepted |
| Fresh reinstall after uninstall | Accepted |
| Public v0.9.5 GitHub Release | **Published** |
| Real abrupt power-loss/cold-boot acceptance | Deferred |
| Newer OpenClaw compatibility | Deferred |
| High-concurrency/long-soak hardening | Not fully accepted |
| Disk-full / DB-corruption recovery | Not production-hardened |
| Exactly-once arbitrary external side effects | Requires adapter idempotency/verification |

Operationally validated does not mean every future workload, provider, OpenClaw version, or failure mode is production-proven. The deferred boundaries above remain explicit.

## Provider semantics

v0.9.5 manages Ollama health, lifecycle, and recovery. Cloud routes remain OpenClaw-owned pass-through: OpenClaw owns authentication, routing/model selection, provider runtime, lifecycle, probing, and recovery. CogentNexus-OpenClaw preserves Ticket/session/generation continuity and durable delivery only; it does not read, copy, persist, refresh, or log Cloud credentials.

Historical LM Studio behavior belongs to the frozen historical provider layer and is not a current managed v0.9.5 provider contract.

## System-check semantics and known discrepancy

`cnxclaw check ...` is observational and does not own provider-state mutation or model inference.

The validated post-release host still exposes a narrow checker inconsistency: `cnxclaw.cmd check system` may exit `2` with a provider-selection diagnostic while the same environment reports an active managed runtime, selected Ollama model, healthy Gateway, and Ollama `ready: true`.

This is explicitly recorded as a **known checker anomaly**. It is not silently promoted to PASS and is not treated as evidence that the v0.9.5 runtime is inactive. It must be repaired only through a new development candidate and the normal validation/release process; the published v0.9.5 tag is not modified.

## Publication boundary

The public release is now complete:

1. accepted candidate `fc3f4bc0...`;
2. exact-head release-gating checks passed;
3. PR #38 merged;
4. `main` became `50be0b97...`;
5. immutable `v0.9.5` tag created at that exact merge SHA;
6. GitHub Release `v0.9.5` published;
7. exact-tag post-release installation/runtime verification completed.

Future source/documentation changes on `main` do not retroactively change the published `v0.9.5` tag or release contents.

Historical coordination reports remain immutable evidence and should not be rewritten merely to make their historical wording current.
