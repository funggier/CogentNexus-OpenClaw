# CNX-20260910-315 — v0.9.5 Session Handoff Checkpoint v2

## Purpose

This checkpoint supersedes the older Task315 handoff snapshot for session continuation. It records the repository state verified from the current branch, what is actually complete, the current verification blocker, and the exact remaining v0.9.5 work.

This document is a resume aid, not an authority over newer source or Actions evidence. On every resume, fresh-fetch the current branch HEAD, `ACTIVE.md`, `STATUS.md`, Task315, PR #29, and current GitHub Actions. Newer repository/Actions evidence wins over this checkpoint.

## Repository position

- Repository: `funggier/CogentNexus-OpenClaw`
- Working branch: `agent/v0.9.5-architecture-repair`
- Base public release: `v0.9.4`
- Base SHA: `40352b3c8b6b9c98c1dfdead5d197f976976bc9f`
- Current branch HEAD: `84541bc1bd3a7bc1b66038c4c19eaa2290697508`
- HEAD message: `docs(v0.9.5): record CI timeout hardening evidence`
- PR: #29, `v0.9.5 architecture repair — verification candidate`
- PR state: open, Draft
- No v0.9.5 release/tag has been created.

## Coordination position

- Task: `CNX-20260909-315`
- State: `IN_PROGRESS`
- Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
- Current phase: end of Plan 1 (provider/runtime/command repair), before Plan 1 completion gate.
- Plan 2 (delivery/session identity), Plan 3 (idle/single-wake), and Plan 4 (migration/matrix/release) are not yet cleared to start until their dependency gates are satisfied.

Important: the older `ACTIVE.md` / `STATUS.md` next-step text may still say to write RED Host-state migration tests. Those migration tests and the provider-neutral Host foundations are already implemented. Treat current source, this checkpoint, and current Actions as newer evidence.

## Approved v0.9.5 architectural invariant

While CogentNexus-OpenClaw is enabled:

OpenClaw owns:

- provider selection;
- model selection;
- authentication/credentials;
- provider routing and failover.

CogentNexus-OpenClaw owns:

- Ticket admission;
- workflow ownership;
- context/compaction continuity;
- inference-attempt evidence;
- recovery authority;
- durable delivery identity/state;
- session ownership/generation fences.

Ollama is an optional local adapter, not a global provider-routing authority.

Provider/model identity is inference-attempt provenance, not Host lifecycle authority.

Provider/model changes must not:

- disable CNX;
- change CNX Host mode;
- increment CNX generation;
- force a Gateway restart as a side effect of provider selection;
- mutate AGENTS.md policy;
- enable/disable the plugin;
- transfer Ticket/workflow ownership;
- invalidate CNX recovery or durable delivery capability.

Cloud, unknown, and future providers must retain CNX capabilities.

## Completed work

### 1. Architecture and subsystem contracts

The v0.9.5 design/spec and four-plan execution structure exist and establish the dependency order:

1. provider/runtime/command repair;
2. delivery/session identity repair;
3. supervisor idle/single-wake repair;
4. migration/matrix/release.

The shared interface contract also defines the intended `HostStateV095`, `InferenceAttempt`, `DeliveryAttempt`, session-generation, local-adapter, and Supervisor wake vocabularies.

### 2. Canonical Host state

`skills/cogentnexus-openclaw/scripts/host_state_v095.py` now owns the v0.9.5 Host-state shape:

```text
schemaVersion=2
cnxMode=active|disabled|maintenance
desiredGateway=running|stopped
providerOwnership=openclaw
managedLocalAdapters={ollama:auto|disabled}
generation=<integer>
updatedAt=<ISO timestamp>
```

No canonical selected/desired provider field remains as execution authority.

Migration coverage exists for managed, maintenance, and passthrough/plugin-enabled or disabled states. A mixed legacy/canonical normalization bug was found and fixed so stale canonical `cnxMode` cannot override authoritative legacy `mode` during migration.

### 3. Compatibility façade strategy

The proven v0.9.4 Host payload was preserved behind compatibility façades:

- `host.py` / `host_legacy_v094.py`
- `host_v091.py` / `host_v091_legacy_v094.py`
- `host_provider_v092.py` / `host_provider_v092_legacy_v094.py`

This reduces blast radius while moving v0.9.5 authority to explicit seams.

### 4. Provider-neutral Host/runtime behavior

Current v0.9.2 Host façade no longer treats provider selection as lifecycle authority. Lifecycle start/stop calls strip legacy provider flags before delegation. Supervisor provider state is diagnostic/compatibility information only. The legacy open-circuit reader refuses to guess among multiple provider incidents.

### 5. Host activation authority

`host_authority_v091.py` no longer injects provider selection into normal lifecycle activation. Existing quiescence lease and rollback protections are preserved.

### 6. Exact Direct model-call evidence and terminal semantics

`plugins/cogentnexus-openclaw/src/v091-direct-model-call-lease.ts` records exact:

- `runId`;
- `callId`;
- provider/model provenance;
- start/deadline/end;
- outcome;
- `errorCategory`;
- `failureKind`.

Hook flow is:

```text
model_call_started
    -> model_call_ended
    -> agent_end(false)
    -> recordDirectRunTerminalFailure()
    -> exact errored call becomes terminal_error evidence
```

`model_call_ended(error)` alone remains evidence only. This preserves failover safety: an errored call followed by a successful failover and successful `agent_end` must not create recovery.

### 7. Exact Host terminal-error claim/classification

`host_provider_v092.py` claims only an exact eligible Ticket/run/call with bounded recovery attempts. Provider/model fields are provenance only, so unknown/future providers are eligible.

Quiesced classification reuses Direct delivery/session fences. Durable response/delivery/workflow/terminal evidence suppresses duplicate inference recovery. Genuine failures produce Host-authorized Direct recovery with `recoveryAuthority=terminal-model-call-error`.

### 8. Provider-neutral terminal recovery lifecycle

Current recovery path is:

```text
exact Host claim
 -> lifecycle prepare
 -> Gateway stop
 -> exact quiesced classification
 -> Gateway start
 -> Gateway health verification
```

The lifecycle itself does not select, probe, start, or stop a provider.

Failure-path hardening exists for prepare failure, stop/partial-stop restoration, classification failure after stop, Gateway start failure with restore retry, and unhealthy Gateway after start. Recovery failures are surfaced; they are not converted into fake inference success.

### 9. Supervisor terminal-error consumption

Supervisor now attempts the exact terminal model-call claim before falling back to legacy stall recovery. The exact recovery lifecycle is called only from that exact claim path.

The production logic and dedicated tests cover the important fences: no latest-run inference, no provider process authority, and no timer-only replacement of exact terminal evidence.

### 10. Provider-mode capability gating repaired

The v0.9.5 provider-independent capability repair removes the old passthrough capability kill-switch behavior.

The repair prevents `providerMode=passthrough` from suppressing core service registration, auto-resume/workflow completion, core recovery fences, durable delivery, Direct model-call lease, dashboard delivery, and related capability surfaces.

Provider mode remains compatibility metadata; Host authorization remains the activation boundary; OpenClaw remains provider/auth/routing owner.

### 11. CI timeout harness hardening

The old Windows Python 3.14 plugin timeout in `src/evaluation.test.ts` was isolated as a test-harness timeout rather than a production failure and the test timeout was increased from 30s to 240s.

This does not prove the entire validation matrix is green; fresh current-head Actions evidence is still required.

## Current exact verification blocker

The latest Validate run associated with the current PR merge candidate is still `FAILURE`.

The important failure is now a Python test wiring defect, not the previous Phase 6 assertion/timeout:

```text
V095ProviderNeutralSupervisorTests.test_consumes_exact_terminal_model_error_claim_before_legacy_stall_recovery

AttributeError:
module 'host_provider_v092' has no attribute 'authority'
```

The test currently patches `hp.authority.supervisor_quiescence`, but the actual namespace is under the embedded legacy module (`hp.stall.authority.supervisor_quiescence`). Another test in the same file already uses that correct namespace pattern.

Therefore the current blocker is narrow and should be fixed with a minimal RED->GREEN test correction, followed by fresh focused tests and GitHub Actions.

The latest run also established that the plugin suite reached the Python test step quickly and failed at this single test; the failure is not evidence that the Supervisor implementation itself is semantically broken.

## CLI architecture gap — explicit and mandatory

The CLI is **not yet aligned with the approved v0.9.5 architecture**.

Current `skills/cogentnexus-openclaw/scripts/cnxclaw.py` still contains the older global provider-routing model, including logic equivalent to:

```text
cnxclaw start --provider ollama
cnxclaw restart --provider lmstudio
resolve_target()
begin_transition()
commit_provider()
openclaw_route.begin()
openclaw_route.commit()
provider.probe()
```

That is incompatible with the v0.9.5 ownership rule when those commands are treated as CNX lifecycle commands, because it allows `cnxclaw` to act as a second provider-routing authority.

### Required v0.9.5 CLI contract

The intended command ownership is:

```text
CNX lifecycle
  cnxclaw start
  cnxclaw stop
  cnxclaw restart
  cnxclaw status
        |
        +--> CogentNexus / Gateway lifecycle only

Local adapter lifecycle
  cnxclaw local ollama start
  cnxclaw local ollama stop
  cnxclaw local ollama restart
  cnxclaw local ollama status
  cnxclaw local ollama check
        |
        +--> Ollama process / local adapter only

Provider/model routing
  OpenClaw Web Chat / native OpenClaw selector
        |
        +--> provider/model/auth/routing owned by OpenClaw
```

### CLI invariants

1. `cnxclaw start|stop|restart|status` must not select a provider or model.
2. `cnxclaw local ollama ...` may manage Ollama but must not write OpenClaw provider/model/auth route configuration.
3. Normal OpenClaw provider/model selection must remain possible while CNX is enabled.
4. Provider/model switching must not increment CNX generation or force CNX lifecycle transitions.
5. `cnxclaw cloud` must not become a second provider-routing framework.
6. Legacy `--provider` may survive only as an explicit compatibility/deprecation surface; it must not regain route or capability authority.
7. Unknown/future OpenClaw providers must work without requiring CNX CLI provider registration.
8. CLI status/check commands may report provider metadata/diagnostics, but reporting is not authority.

### Required CLI implementation direction

Before Plan 1 can be declared complete:

- isolate local-provider operations into an explicit local-adapter namespace;
- remove provider-selection and route-commit behavior from normal CNX lifecycle commands;
- retain read-only provider diagnostics where useful;
- add RED tests proving lifecycle commands do not call provider selection/routing functions;
- add RED tests proving local Ollama commands cannot mutate OpenClaw route configuration;
- add compatibility tests for any retained legacy `--provider` input to ensure it is deprecated/neutralized rather than authoritative;
- then run the provider-switch matrix through the native OpenClaw route boundary.

This CLI gap is part of Plan 1 and must be closed before Plan 2 begins.

## Remaining work by execution order

### Plan 1 — Provider/runtime/command repair

Current state: **implementation largely complete, completion gate not yet green**.

Remaining:

1. Fix the current Supervisor test namespace defect (`hp.authority` -> correct embedded namespace).
2. Run focused Supervisor/lifecycle/provider-capability tests.
3. Run fresh full Validate and required Windows smoke workflows.
4. Complete the CLI ownership split described above.
5. Add/execute provider-switch matrix proving:
   - Ollama -> Cloud;
   - Cloud -> Ollama;
   - Cloud -> unknown/future provider metadata;
   - no CNX mode/generation/plugin/policy mutation;
   - local adapter lifecycle remains local-only.
6. Update coordination docs once Plan 1 is actually green.

### Plan 2 — Delivery/session identity repair

Not yet started as the canonical v0.9.5 implementation.

Create/implement:

```text
v095-inference-attempt.ts
v095-delivery-core.ts
v095-delivery-webchat.ts
v095-delivery-discord.ts
v095-session-generation.ts
```

Core requirement:

```text
Ticket
 -> stable Session
 -> stable SessionGeneration
 -> one InferenceAttempt per model call
 -> one or more exact DeliveryAttempt records for delivery
```

Provider/model are inference provenance, not identity.

Do not weaken existing v0.9.4 Discord exact-run / owner-generation fences.

### Plan 3 — Idle / single-wake repair

Not yet started as the canonical implementation.

Create the single wake authority and exact dispatch contract so one Supervisor decides which actionable authority gets serviced. Preserve Task312 stale-pending-delivery wake repair. Do not introduce another recurring poller without explicit contract amendment and tests.

### Plan 4 — Migration / matrix / release

Not started.

Only after Plans 1-3 are green:

- converge all version surfaces to 0.9.5;
- validate v0.9.4 -> v0.9.5 migration;
- run provider-switch matrix;
- run Windows lifecycle acceptance;
- run idle/quiescence matrix;
- run full Actions on exact candidate SHA;
- verify package/release artifacts;
- then create/tag/publicly release v0.9.5.

## Safety fences that must remain intact

- no latest-run inference;
- exact Ticket/run/call identity;
- exact Discord delivery identity;
- no runId-less settlement;
- session owner/generation fencing;
- durable response/delivery evidence wins over inference recovery;
- terminal Ticket fences;
- config single-writer/quiescence protection;
- stale pending-delivery wake repair;
- timer-only destructive recovery suppression;
- bounded Host recovery attempts;
- fail-closed ambiguous delivery handling;
- provider-neutral CNX recovery lifecycle;
- no provider lifecycle authority in CNX Supervisor;
- no provider/model/auth route mutation by normal CNX lifecycle commands;
- no force push;
- no release/tag before exact candidate gates pass.

## Current recommended continuation

```text
1. Fix Supervisor test namespace defect.
2. Focused tests -> GREEN.
3. Fresh full Actions -> GREEN.
4. Finish CLI ownership split + tests.
5. Provider-switch matrix.
6. Declare Plan 1 green.
7. Start Plan 2: InferenceAttempt -> Delivery Core -> surface adapters -> Session Generation.
8. Start Plan 3: single wake / idle.
9. Start Plan 4: migration -> exact candidate -> release.
```

## Resume prompt

> ทำ CogentNexus-OpenClaw ต่อจาก `CNX-20260910-315-session-handoff-checkpoint-v2.md` ครับ
>
> Repo: `funggier/CogentNexus-OpenClaw`
> Branch: `agent/v0.9.5-architecture-repair`
>
> ให้ fresh-fetch current HEAD, `ACTIVE.md`, `STATUS.md`, Task315, PR #29 และ current GitHub Actions ก่อนทุกครั้ง โดยยึด source/Actions ล่าสุดเป็น authoritative
>
> จุดปัจจุบันคือ HEAD `84541bc1bd3a7bc1b66038c4c19eaa2290697508` และ Plan 1 อยู่ปลายทางแต่ยังไม่ผ่าน gate
>
> Blocker ปัจจุบันของ CI คือ test namespace ใน `tests/test_v095_provider_neutral_supervisor.py`: `hp.authority.supervisor_quiescence` ต้องใช้ namespace ที่มีอยู่จริง (`hp.stall.authority.supervisor_quiescence`)
>
> หลังจาก CI ผ่าน ให้ปิด CLI architecture gap ให้ตรง contract ใน checkpoint นี้: `cnxclaw start|stop|restart|status` เป็น CNX/Gateway lifecycle เท่านั้น, `cnxclaw local ollama ...` จัดการ Ollama เท่านั้น, ส่วน provider/model/auth/routing ให้ OpenClaw native selector เป็นเจ้าของ
>
> จากนั้นทำ provider-switch matrix ให้ผ่าน แล้วจึงเริ่ม Plan 2 canonical InferenceAttempt / DeliveryAttempt / SessionGeneration, ต่อ Plan 3 single-wake/idle, และสุดท้าย Plan 4 migration/release
>
> ห้าม release/tag v0.9.5 ก่อน Plans 1-3 และ exact candidate/Windows/provider-switch/idle/CI gates ผ่านครบ
