# CogentNexus-OpenClaw Current Operational State

**Release line:** v0.9.3  
**Core version:** 0.9.3  
**OpenClaw Bridge package:** 0.9.3  
**Validated OpenClaw:** `2026.7.1-2 (0790d9f)`  
**Managed provider:** **Ollama only**  
**Accepted Recovery Core:** `eadb89099637d24f96e265a500d66c577aa939a3`  
**Frozen accepted v0.9.3 product candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`  
**Accepted active facade SHA-256:** `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`  
**Accepted plugin fingerprint:** `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`  
**Latest published release:** v0.9.2  
**v0.9.3 publication state:** `BLOCKED — documentation-bearing product/payload requalification required`

## Classification

CogentNexus-OpenClaw v0.9.3 has completed the bounded real-Windows acceptance sequence for the exact frozen product candidate above. The accepted sequence covers install-over/provenance, reset/fresh-state behavior, uninstall with preservation of external OpenClaw/Ollama/user data, fresh reinstall/post-install health, and a final Dashboard semantic/durable-delivery turn.

Task 187 then performed the release-documentation audit. It found stale current-facing text inside documentation that is itself part of the installed/product artifact:

- `plugins/cogentnexus-openclaw/README.md` is declared in `package.json.files` and therefore contributes directly to the accepted plugin payload-v2 fingerprint;
- `skills/cogentnexus-openclaw/SKILL.md` and skill references are copied as part of the installed skill tree and participate in the runtime instruction surface;
- at least `skills/cogentnexus-openclaw/references/architecture.md` still identifies the architecture as current v0.9.1 rather than the v0.9.3 accepted state.

Correcting these files is necessary for full current-documentation convergence, but doing so changes the accepted artifact identity. Task 187 therefore cannot publish v0.9.3 while claiming that the previous Windows acceptance still applies to the corrected payload.

## Accepted lifecycle/semantic evidence

The exact frozen candidate passed:

1. **Task 182** — repaired-candidate Windows install-over reacceptance;
2. **Task 183** — reset/fresh-state reacceptance;
3. **Task 184** — uninstall/external-preservation acceptance;
4. **Task 185** — fresh reinstall/post-uninstall reacceptance;
5. **Task 186** — final post-lifecycle Dashboard semantic/durable-delivery acceptance.

Task 186 proved:

```text
1 human Send
-> 1 Ticket
-> 1 session/run
-> 1 Ollama model call
-> 1 durable assistant delivery
-> 1 logical Dashboard assistant result
```

with no duplicate semantic work, retry, direct recovery, or outbox residue.

## Current capability boundary

| Capability | v0.9.3 state |
| --- | --- |
| Ticket-first durable admission | Accepted |
| DIRECT lane without forced workflow promotion | Accepted |
| Host-owned managed recovery authority | Accepted |
| Gateway/Ollama lifecycle and recovery path | Accepted for the frozen candidate |
| Managed provider | **Ollama only** |
| Validated OpenClaw | `2026.7.1-2 (0790d9f)` |
| Original provider/model recovery provenance | Accepted |
| Native OpenClaw restart ownership fence | Accepted |
| Recursive recovery intake suppression | Accepted |
| Same-session duplicate Ticket suppression | Accepted |
| Transient SQLite BUSY authority-read tolerance | Accepted |
| Response-ready immutability | Accepted |
| Durable direct result and delivery confirmation | Accepted |
| PASSTHROUGH / native OpenClaw compatibility mode | Accepted through lifecycle sequence |
| MAINTENANCE deliberate-stop semantics | Accepted through lifecycle sequence |
| `reset` explicit-`y` fresh-state reconstruction | Accepted |
| `uninstall` explicit-`y` ownership-safe external preservation | Accepted |
| Fresh reinstall after uninstall | Accepted |
| Final Dashboard durable-delivery semantic path | Accepted |
| Public v0.9.3 GitHub Release | **Blocked pending corrected artifact requalification** |
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

## Artifact identity boundary

Acceptance evidence is exact-artifact evidence, not a floating branch promise.

For the accepted candidate:

```text
source candidate: f6392da3e4112ce441526d5ef19925c90a872b0b
facade SHA-256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
```

Safe repository documentation outside the installed/product payload may move after that candidate while preserving runtime identity. In contrast, changing plugin package README bytes changes the plugin fingerprint, and changing the installed skill tree changes the product instruction surface. Those changes require a new exact candidate and changed-surface requalification before release publication.

## Required next step

Create a narrowly scoped documentation-payload repair/requalification task that:

1. corrects stale current-facing text in plugin/skill product documentation without changing executable/runtime/test/workflow/dependency behavior;
2. proves executable/runtime source bytes remain unchanged from `f6392da3...`;
3. records the new plugin payload fingerprint and installed skill-tree identity;
4. reruns repository/package/release validation for the exact new candidate;
5. performs the bounded Windows requalification needed for the changed artifact surface, including exact install-over/provenance and a final semantic/durable-delivery check if the runtime instruction surface changed;
6. returns to exact-SHA PR/merge/release publication only after that new candidate is accepted.

## Historical boundary

v0.9.2 is a frozen historical release. Historical release notes and acceptance evidence may preserve LM Studio and older provider-neutral behavior when that is what actually occurred.

The frozen v0.9.3 Windows evidence must also remain historical evidence for its exact accepted artifact. It must not be silently reassigned to a corrected payload with different bytes.
