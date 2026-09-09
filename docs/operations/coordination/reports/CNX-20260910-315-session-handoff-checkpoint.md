# CNX-20260910-315 — v0.9.5 Session Handoff Checkpoint

## Purpose

This checkpoint records the exact v0.9.5 implementation position so a later ChatGPT/Hermes session can resume without reconstructing the work from memory.

This is a coordination snapshot, not a substitute for fresh repository or Actions inspection. On resume, always fresh-fetch the current branch HEAD, `ACTIVE.md`, `STATUS.md`, the Task315 document, and current GitHub Actions state. If they differ from this checkpoint, the newer repository/Actions evidence wins.

## Repository / branch

- Repository: `funggier/CogentNexus-OpenClaw`
- Working branch: `agent/v0.9.5-architecture-repair`
- Base public release: `v0.9.4`
- Base SHA: `40352b3c8b6b9c98c1dfdead5d197f976976bc9f`
- Exact HEAD at this checkpoint: `58f70efb6c036615924119fc32129f4619944b6e`
- HEAD commit: `fix(v0.9.5): add provider-neutral terminal recovery lifecycle`
- Branch is 48 commits ahead of the v0.9.4 base at checkpoint creation.

## Coordination state

- Task: `CNX-20260909-315`
- State: `IN_PROGRESS`
- Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
- Current phase: v0.9.5 provider/runtime authority repair, with terminal model-call recovery now implemented through the Host layer but not yet fully integrated into the steady-state Supervisor.

### Important coordination note

`ACTIVE.md` and `STATUS.md` currently describe the next step as the original Host-state migration RED tests. Those tests and their production repair have already progressed substantially beyond that point. Treat their broad state as authoritative coordination metadata, but treat their stale "current next step" text as needing refresh on the next coordination update. This checkpoint records the actual implementation position at HEAD `58f70efb...`.

## Approved v0.9.5 invariant

OpenClaw owns:

- provider selection;
- model selection;
- authentication/credentials;
- provider routing and failover.

CogentNexus-OpenClaw owns while active:

- Ticket admission;
- workflow ownership;
- context/compaction continuity;
- inference-attempt evidence;
- recovery authority;
- delivery identity and durable delivery state;
- session ownership/generation fences.

Local Ollama is an optional local adapter. It must not become a global provider-selection authority.

The critical user-facing invariant is:

> While CogentNexus-OpenClaw is enabled, the user can change provider/model directly from normal OpenClaw Web Chat/native UI without disabling CNX, changing Host mode, incrementing CNX generation, forcing a Gateway restart, mutating AGENTS.md policy, or losing Ticket/workflow/context/recovery/delivery capability.

Provider/model identity belongs to each inference attempt. It is provenance, not Host lifecycle authority.

## What has been completed

### 1. Architecture and execution plans

Approved and committed v0.9.5 architecture/specification material exists for:

- provider/runtime authority separation;
- local-provider command contract;
- idle/quiescence/single-wake behavior;
- delivery/session identity repair;
- migration/release matrix;
- shared interface vocabulary and execution ordering.

The shared execution index requires this order:

1. provider/runtime/command repair;
2. delivery/session identity repair;
3. supervisor idle/single-wake repair;
4. migration/matrix/release.

Do not jump to release or use release work to mask an unfinished subsystem.

### 2. Canonical Host state authority

Added:

`skills/cogentnexus-openclaw/scripts/host_state_v095.py`

Canonical state is now conceptually:

```text
schemaVersion=2
cnxMode=active|disabled|maintenance
desiredGateway=running|stopped
providerOwnership=openclaw
managedLocalAdapters={ollama:auto|disabled}
generation=<integer>
updatedAt=<ISO timestamp>
```

There is no canonical `selectedProvider` or `desiredProvider` execution authority.

Migration behavior:

- v0.9.4 `managed` -> v0.9.5 `active`;
- v0.9.4 `maintenance` -> `maintenance`;
- v0.9.4 `passthrough + plugin disabled` -> `disabled`;
- v0.9.4 `passthrough + plugin enabled` -> `active`.

The state save path was TDD-corrected so legacy `mode` wins over stale canonical `cnxMode` when handling a mixed legacy state and persisted schema is normalized to v0.9.5.

### 3. Compatibility façade split

The old proven v0.9.4 Host payload was preserved behind compatibility façades rather than rewritten wholesale.

Relevant files include:

- `skills/cogentnexus-openclaw/scripts/host.py`
- `skills/cogentnexus-openclaw/scripts/host_legacy_v094.py`
- `skills/cogentnexus-openclaw/scripts/host_v091.py`
- `skills/cogentnexus-openclaw/scripts/host_v091_legacy_v094.py`
- `skills/cogentnexus-openclaw/scripts/host_provider_v092.py`
- `skills/cogentnexus-openclaw/scripts/host_provider_v092_legacy_v094.py`

This preserves dynamic legacy globals/overlays while allowing v0.9.5 authority seams to override provider-sensitive behavior safely.

### 4. Provider-neutral Host/runtime behavior

The v0.9.2 Host provider façade now strips legacy `--provider` from lifecycle start/stop calls and delegates lifecycle through the existing runtime without selecting a provider.

`restart_managed()` and `supervisor_tick()` were adapted so provider fields remain compatibility/diagnostic data only.

The steady-state Supervisor no longer uses `selectedProvider`, `desiredProvider`, adapter health, or local provider process state as global execution authority.

The legacy open-circuit reader is diagnostic-only and deliberately does not guess among multiple provider incidents.

### 5. Host enable authority repair

`host_authority_v091.py` was adapted so the Host activation path no longer passes a provider selection into lifecycle startup.

The durable Host activation linearization point remains the CNX managed/active authority transition, with the existing quiescence lease and rollback protections retained.

### 6. Direct model-call evidence layer

`plugins/cogentnexus-openclaw/src/v091-direct-model-call-lease.ts` now records exact OpenClaw model-call evidence:

- `runId`;
- `callId`;
- provider;
- model;
- start/deadline/end;
- outcome;
- `errorCategory`;
- `failureKind`.

New error metadata columns are additive and migration-safe.

A new terminal-run promotion boundary exists:

```text
model_call_ended(outcome=error)
        |
        v
agent_end(success=false)
        |
        v
exact row -> terminal_error
```

A model-call error alone is not treated as a terminal run failure.

This intentionally allows OpenClaw failover:

```text
call A -> error
call B -> completed
agent_end -> success
```

must not create Host model-error recovery.

Likewise, a completed model call followed by `agent_end(false)` must not be promoted into model recovery.

Only the exact errored call that remains eligible at terminal run failure may be promoted.

### 7. Exact Host terminal-error claim

`skills/cogentnexus-openclaw/scripts/host_provider_v092.py` now contains an exact terminal model-call claim path.

It requires:

- exact Ticket/run/call identity;
- accepted Direct Ticket;
- `terminal_error` + `outcome=error`;
- bounded recovery attempt count;
- transactional claim.

Provider/model values are provenance only. Unknown/future providers can be claimed without requiring a provider adapter.

### 8. Quiesced terminal-error classification

The Host classification path now reuses the established Direct delivery/session fences before authorizing inference recovery.

It holds rather than regenerates when durable response/delivery evidence or terminal Ticket/workflow fences already exist.

When recovery is genuinely needed, it queues `cnx_direct_recovery`, records the exact terminal model-call error as recovery authority, and marks the exact model-call row interrupted with Host authorization provenance.

It does not use timeout-event semantics for this path.

### 9. Provider-neutral terminal recovery lifecycle

Current HEAD `58f70efb6c036615924119fc32129f4619944b6e` adds:

`recover_terminal_error_direct_model_call(root, claim)`

The lifecycle is:

```text
Host claim
  -> lifecycle prepare
  -> Gateway stop
  -> exact terminal-error classification
  -> Gateway start
  -> Gateway health verification
```

The implementation never selects/probes/starts/stops a provider. Provider/model values remain provenance.

If the Gateway was stopped and normal start did not complete, the current implementation has a `finally` restart safeguard. This area still needs failure-path review for partial-stop and start-failure behavior before it is considered fully hardened.

## Current tests / CI evidence

### Exact current HEAD

GitHub branch currently resolves to:

`58f70efb6c036615924119fc32129f4619944b6e`

### GitHub Actions — Validate

Run:

`34383579174` (`Validate`)

Head SHA:

`58f70efb6c036615924119fc32129f4619944b6e`

Overall conclusion: `failure`.

The failure is isolated to the Windows 3.14 plugin test job. The important observed result was:

- Python test suite: `617 passed, 3 skipped, 6 subtests passed`;
- Windows 3.14 plugin suite: `62 passed` test files / `304 passed` tests, `1 failed`;
- failing test: `src/evaluation.test.ts` Phase 6 evaluation;
- failure: Vitest test timeout at `30000ms`;
- total plugin run duration was about 220 seconds, with the Phase 6 test consuming about 180 seconds;
- the failing test did not report an assertion failure; it timed out.

Other Validate matrix results on the same SHA:

- macOS 3.11: success;
- macOS 3.14: success;
- Ubuntu 3.11: success;
- Ubuntu 3.14: success;
- Windows 3.11: success;
- Windows 3.14: failure only at `npm test` due to the Phase 6 timeout.

Windows 3.14 also passed:

- namespace isolation;
- baseline consistency;
- Cogent validation;
- Cogent/runtime/workflow self-tests;
- Python compilation;
- Python test suite;
- benchmark validator;
- PowerShell syntax validation;
- PowerShell 5.1 acceptance serializer;
- exact numeric root-process exit self-test;
- argument round-trip self-test.

### Separate PS5.1 acceptance smoke

Run:

`34383579210`

Conclusion: `success`.

This is useful supporting evidence, but it does not replace the failed full Validate run.

## Current implementation gap

The terminal-error recovery primitives are now present, but the full production control path is not finished.

The next implementation boundary is Supervisor integration:

```text
OpenClaw agent_end(false)
        |
        v
exact terminal model-call evidence
        |
        v
Supervisor claims exact terminal error
        |
        v
Host provider-neutral recovery lifecycle
        |
        v
CNX Direct Recovery
```

The Supervisor must not fall back to timer-only guessing and must not resurrect global provider lifecycle authority.

## What is currently being worked on

The active work is the v0.9.5 provider/runtime/command repair line, currently at the point where exact terminal model-call recovery has been implemented through the Host but still needs steady-state orchestration and failure-path hardening.

The immediate engineering focus should be:

1. verify the exact current `agent_end(false)` wiring into the durable model-call evidence path;
2. add a RED Supervisor integration test showing that an exact terminal model-call claim is consumed by the Supervisor;
3. make the smallest GREEN change so Supervisor invokes the exact Host recovery lifecycle;
4. prove that no timer-only Direct recovery, provider probing, provider start/stop, or global provider selection is triggered;
5. add lifecycle rollback/failure-path tests;
6. rerun focused tests and then GitHub Actions.

## Remaining v0.9.5 work after the immediate recovery integration

### A. Supervisor terminal-error integration

Required:

- exact claim consumption;
- no duplicate claim;
- bounded recovery attempts;
- no provider lifecycle authority;
- no timer-only destructive recovery;
- no stale session/run cross-talk.

### B. Lifecycle failure/rollback hardening

Explicitly test:

- `prepare` failure;
- stop failure, including partial-stop semantics if observable;
- classification failure;
- Gateway start failure;
- Gateway unhealthy after start;
- exact recovery row remains auditable and recoverable;
- no duplicate recovery authorization;
- recovery attempt bound remains enforced.

If classification has already durably authorized CNX recovery and Gateway start subsequently fails, do not roll back the authorization into a fake successful inference state. Leave the durable recovery pending for Gateway reconciliation.

### C. Remove remaining provider capability gating from plugin integration

Inspect and repair `plugins/cogentnexus-openclaw/src/index.ts` and related provider-mode integration so Cloud/unknown providers do not lose:

- durable admission;
- compaction continuation;
- recovery;
- Ticket/workflow capability.

`providerMode` may survive only as compatibility/diagnostic state if necessary; it must not disable CNX capability while CNX is active.

### D. CLI command contract

Target operator model:

```text
cnxclaw start|stop|restart|status
    -> CogentNexus/Gateway lifecycle only

cnxclaw local ollama start|stop|restart|status|check
    -> local Ollama lifecycle only

OpenClaw Web Chat/native model selector
    -> provider/model routing
```

Legacy `--provider` may remain as a one-release compatibility/deprecation alias only if it cannot mutate OpenClaw route authority.

`cnxclaw cloud` must not be a second global provider-routing framework. If retained, it is migration compatibility only.

### E. Canonical inference-attempt identity

Introduce/finish the planned `InferenceAttempt` layer:

- stable Ticket identity;
- stable Session identity;
- stable Session Generation unless native delete/replace/rotate requires advancement;
- a new InferenceAttempt per model call;
- provider/model attached to the attempt;
- exact OpenClaw `runId` binding.

Provider changes must not create a new CNX session generation.

### F. Canonical delivery identity

Introduce/finish the planned `DeliveryAttempt` core:

- separate from InferenceAttempt;
- exact Ticket/run/session-generation/surface identity;
- no "latest run" inference;
- durable staging before transport;
- transport acknowledgement distinct from durable completion;
- ambiguous Discord receipts remain pending/recoverable;
- Dashboard and Discord adapters share the same core state machine.

Provider/model is not part of DeliveryAttempt identity.

### G. Session-generation hardening

Required invariant:

- provider change: no generation increment;
- model change: no generation increment;
- compaction: no generation increment;
- Gateway restart: no generation increment unless actual session replacement semantics require it;
- native delete/replace/rotate: advance according to the actual session lifecycle contract.

Stale callbacks must not settle a newer generation.

### H. Supervisor idle / single-wake repair

Consolidate recurring decisions so Windows idle does not develop overlapping probes/timers and mouse-spinner/high-CPU behavior.

Keep the existing stale-pending-delivery wake repair from Task312.

No new recurring poller may be added unless the canonical Supervisor cannot own that condition and the idle contract is amended/tested.

### I. Migration and release

Only after Plans 1-3 are green:

- update version surfaces to `0.9.5`;
- update namespace/baseline expectations;
- prove v0.9.4 -> v0.9.5 migration;
- run exact provider-switch matrix;
- run Windows lifecycle acceptance;
- run idle/quiescence tests;
- run full GitHub Actions on the exact candidate SHA;
- only then perform release/tag/publication gates.

No v0.9.5 release/tag exists at this checkpoint.

## Important existing safety fixes that must not regress

Preserve all of the following unless an equal-or-stronger v0.9.5 contract replaces them:

- exact Discord delivery identity;
- no latest-run inference;
- no runId-less durable settlement;
- session owner/generation fencing;
- durable response-ready/delivery precedence over inference recovery;
- terminal Ticket fences;
- config mutation single-writer/quiescence protection;
- stale pending-delivery wake repair;
- timer-only destructive Direct recovery suppression;
- Host recovery claim/finalization fences;
- exact model-call run/call identity;
- OpenClaw failover-safe terminal error semantics.

## Hard fences at handoff

Until explicitly changed by the active task/authority:

- no force push;
- no release/tag/default-branch promotion;
- no live provider/model/auth route mutation;
- no manual SQLite/Ticket/session mutation;
- no destructive live recovery retry without exact evidence;
- no "latest run" or "latest Ticket" inference;
- no provider probing/start/stop from CNX Supervisor as global authority;
- no new recurring poller without the single-wake design/test;
- do not weaken ambiguous Discord receipt handling;
- do not mutate protected historical Tickets merely to make a test or acceptance state clean.

## Resume procedure for the next session

1. Fresh-fetch `agent/v0.9.5-architecture-repair` and record its exact HEAD.
2. Fresh-read `docs/operations/coordination/ACTIVE.md` and `STATUS.md`.
3. Fresh-read this checkpoint and `CNX-20260909-315-v095-provider-runtime-command-repair.md`.
4. Inspect current GitHub Actions for the exact HEAD; do not assume the failure above is still current if a newer SHA exists.
5. Inspect `plugins/cogentnexus-openclaw/src/v091-direct-model-call-lease.ts` and current plugin `index.ts` wiring before changing anything.
6. Start the next production change with a RED regression test.
7. Keep changes minimal and preserve all v0.9.4 safety fences.
8. After each meaningful repair, record exact commit SHA, tests, and CI result.

## Suggested next-session prompt

> ทำ CogentNexus-OpenClaw ต่อจาก handoff checkpoint นี้ครับ
>
> Repo: `funggier/CogentNexus-OpenClaw`
> Branch: `agent/v0.9.5-architecture-repair`
>
> อ่าน `docs/operations/coordination/reports/CNX-20260910-315-session-handoff-checkpoint.md` ก่อน แล้ว fresh-fetch GitHub current HEAD, `ACTIVE.md`, `STATUS.md`, Task315 และ GitHub Actions ทุกครั้ง
>
> GitHub repository/Actions เป็น authoritative source ถ้ามีอะไรใหม่กว่าข้อมูลใน handoff ให้ยึดข้อมูลใหม่
>
> ตอนนี้ v0.9.5 Host state/provider-neutral façade และ exact terminal model-call evidence/claim/classification/lifecycle ทำไปแล้วถึง `58f70efb6c036615924119fc32129f4619944b6e`
>
> ขั้นต่อไปให้ตรวจ exact `agent_end(false)` wiring แล้วทำ RED test สำหรับ Supervisor integration ของ terminal model-call recovery ก่อน จากนั้นแก้ production แบบ minimal ให้ GREEN โดยห้ามคืน global provider authority, ห้าม timer-only guessing และห้ามลด CNX capability เมื่อ OpenClaw ใช้ Cloud/unknown provider
>
> หลังจากนั้นทำ lifecycle failure/rollback tests, provider-mode gating, CLI local Ollama namespace, delivery/session identity, single-wake/idle และ migration/release ตาม execution index
>
> ห้าม release/tag จน Plans 1-3 และ exact candidate/Windows/provider-switch/idle/CI gates ผ่านครบ
