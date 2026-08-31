# CogentNexus-OpenClaw Current Operational State

**Release line:** v0.9.3  
**Core version:** 0.9.3  
**OpenClaw Bridge package:** 0.9.3  
**Validated OpenClaw:** `2026.7.1-2 (0790d9f)`  
**Managed provider:** **Ollama only**  
**Accepted Recovery Core:** `eadb89099637d24f96e265a500d66c577aa939a3`  
**Previously accepted implementation candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`  
**Accepted active facade SHA-256:** `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`  
**Task-188 package payload-v2 identity:** `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / `184` files  
**Task-188 installed skill-tree identity:** `a1e873ba404205507a1623961b49f1b1a0689f9f`  
**Executable scripts tree:** `3d9d323ba19443d46e970b87cef52ce878da274f` — unchanged from the accepted implementation baseline

## Classification

CogentNexus-OpenClaw v0.9.3 completed the bounded real-Windows acceptance sequence on implementation candidate `f6392da3...`. The accepted sequence covers install-over/provenance, reset/fresh-state behavior, uninstall with preservation of external OpenClaw/Ollama/user data, fresh reinstall/post-install health, and a final Dashboard semantic/durable-delivery turn.

Task 187 then correctly stopped the initial publication path because some stale current-facing documentation was itself part of the npm package and installed skill surface. Task 188 corrected that documentation-only product surface:

- `plugins/cogentnexus-openclaw/README.md` now reflects the completed v0.9.3 stabilization lineage;
- `skills/cogentnexus-openclaw/SKILL.md` now reflects the completed v0.9.3 stabilization lineage;
- `skills/cogentnexus-openclaw/references/architecture.md` now identifies the current architecture as v0.9.3;
- `skills/cogentnexus-openclaw/references/scheduler-adapters.md` now identifies current managed installations as v0.9.3.

Those changes created the package/skill identities recorded above while leaving executable/runtime scripts byte-identical. The corrected artifact therefore requires proportional changed-surface requalification before publication, not a silent transfer of the old exact-artifact acceptance and not an automatic replay of every destructive lifecycle test.

## Accepted lifecycle/semantic evidence

The implementation baseline passed:

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

## Task-188 changed-surface identity

Task 188 changes documentation/instruction bytes only. Proven current identities include:

```text
package payload-v2: 408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b
package file count: 184
installed skill tree: a1e873ba404205507a1623961b49f1b1a0689f9f
executable scripts tree: 3d9d323ba19443d46e970b87cef52ce878da274f
facade Git blob: 879083d6186589d4b2774b8fd87fa93692dd2dfc
```

The package payload identity changed because the package README changed. The skill-tree identity changed because installed skill documentation changed. The scripts tree and facade source blob did not change.

## Capability boundary

| Capability | v0.9.3 state |
| --- | --- |
| Ticket-first durable admission | Accepted on implementation baseline; executable surface unchanged |
| DIRECT lane without forced workflow promotion | Accepted; executable surface unchanged |
| Host-owned managed recovery authority | Accepted; executable surface unchanged |
| Gateway/Ollama lifecycle and recovery path | Accepted; executable surface unchanged |
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
| `reset` explicit-`y` fresh-state reconstruction | Accepted on implementation baseline |
| `uninstall` explicit-`y` ownership-safe external preservation | Accepted on implementation baseline |
| Fresh reinstall after uninstall | Accepted on implementation baseline |
| Final Dashboard durable-delivery semantic path | Accepted on implementation baseline; Task 188 requires one proportional confirmation turn because installed instruction bytes changed |
| Public v0.9.3 GitHub Release | Determined only by GitHub Releases/tag and exact release-workflow evidence |
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

## Requalification and publication boundary

Acceptance evidence is exact-artifact evidence, not a floating branch promise. Task 188 uses proportional requalification because the changed product surface is documentation/instruction-bearing while executable/runtime bytes are proven unchanged.

The required changed-surface proof is:

1. exact-candidate repository/package CI;
2. one supported Windows install-over of the corrected artifact;
3. installed package/skill documentation identity and facade/runtime provenance checks;
4. MANAGED + Ollama + Gateway + delivery/recovery + SQLite health;
5. one bounded Dashboard semantic/durable-delivery turn;
6. repeat reset/uninstall/fresh-reinstall only if evidence demonstrates a concrete lifecycle reason.

After those gates pass, publication proceeds through a current PR to `main`, exact merged-SHA freeze, `.github/workflows/release.yml`, and post-release tag/asset/checksum verification. GitHub Releases/tags remain authoritative for public availability.

## Historical boundary

v0.9.2 is a frozen historical release. Historical release notes and acceptance evidence may preserve LM Studio and older provider-neutral behavior when that is what actually occurred.

The `f6392da3...` Windows evidence also remains immutable exact-artifact history. Task 188 carries forward unchanged-surface claims only through explicit byte-identity proof and independently qualifies the documentation-bearing surface that changed.
