# CNX-20260910-315 — v0.9.5 Session Handoff Checkpoint

## Purpose

This is the resume checkpoint for the current v0.9.5 architecture-repair session. It records what is complete, what is in progress, the exact repository/CI position, and the next work sequence.

This is a snapshot, not a substitute for fresh source/Actions inspection. On resume, fresh-fetch the branch HEAD, `ACTIVE.md`, `STATUS.md`, Task315, and current Actions. Newer repository/Actions evidence wins over this document.

## Repository position

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.5-architecture-repair`
- Base release: `v0.9.4`
- Base SHA: `40352b3c8b6b9c98c1dfdead5d197f976976bc9f`
- HEAD at checkpoint: `58f70efb6c036615924119fc32129f4619944b6e`
- HEAD message: `fix(v0.9.5): add provider-neutral terminal recovery lifecycle`
- Branch is 48 commits ahead of the v0.9.4 base.
- No v0.9.5 release/tag has been created.

## Coordination position

- Task: `CNX-20260909-315`
- State: `IN_PROGRESS`
- Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
- Current implementation phase: provider/runtime authority repair.
- The Host-state migration and provider-neutral recovery foundations are already implemented beyond the older `ACTIVE.md`/`STATUS.md` next-step text.

`ACTIVE.md` and `STATUS.md` should be refreshed at the next coordination update; do not interpret their stale "write RED migration tests" sentence as proof that those tests have not already been implemented.

## Approved architecture invariant

OpenClaw owns:

- provider selection;
- model selection;
- authentication/credentials;
- provider routing/failover.

CogentNexus-OpenClaw owns while active:

- Ticket admission;
- workflow ownership;
- context/compaction continuity;
- inference-attempt evidence;
- recovery authority;
- durable delivery identity/state;
- session ownership/generation fences.

Ollama is an optional local adapter, not a global provider-routing authority.

### Critical user-facing invariant

While CNX is enabled, the user must be able to change provider/model from normal OpenClaw Web Chat/native UI without:

- disabling CNX;
- changing CNX Host mode;
- incrementing CNX generation;
- forcing a Gateway restart;
- mutating AGENTS.md policy;
- enabling/disabling the plugin;
- losing Ticket/workflow/context/recovery/delivery capability.

Provider/model is inference-attempt provenance, not Host lifecycle authority.

## What has been completed

### 1. v0.9.5 architecture/specification

Committed design/spec material covers:

- provider/runtime/command separation;
- local-provider command contract;
- delivery/session identity;
- idle/quiescence/single-wake authority;
- migration/release matrix;
- shared interfaces and execution order.

Execution order is explicitly:

1. provider/runtime/command repair;
2. delivery/session identity repair;
3. supervisor idle/single-wake repair;
4. migration/matrix/release.

### 2. Canonical Host state

Added:

`skills/cogentnexus-openclaw/scripts/host_state_v095.py`

Canonical state:

```text
schemaVersion=2
cnxMode=active|disabled|maintenance
desiredGateway=running|stopped
providerOwnership=openclaw
managedLocalAdapters={ollama:auto|disabled}
generation=<integer>
updatedAt=<ISO timestamp>
```

There is no canonical `selectedProvider`/`desiredProvider` execution authority.

Migration is covered for:

- managed -> active;
- maintenance -> maintenance;
- passthrough + plugin disabled -> disabled;
- passthrough + plugin enabled -> active.

A real migration bug was found and fixed: when mixed legacy/canonical fields coexist, legacy `mode` must not be overridden by stale `cnxMode` during normalization.

### 3. Compatibility façades

The proven v0.9.4 Host payload was preserved behind façades rather than rewritten wholesale:

- `host.py` / `host_legacy_v094.py`
- `host_v091.py` / `host_v091_legacy_v094.py`
- `host_provider_v092.py` / `host_provider_v092_legacy_v094.py`

This keeps the old overlay/global behavior available while moving authority to v0.9.5 seams.

### 4. Provider-neutral Host/runtime behavior

The v0.9.2 Host façade now strips legacy `--provider` from lifecycle start/stop calls and delegates lifecycle without selecting a provider.

Supervisor provider state is diagnostic/compatibility information only; it no longer provides global provider process authority.

The legacy open-circuit reader is read-only and refuses to guess when multiple provider incidents exist.

### 5. Host activation authority

`host_authority_v091.py` was repaired so normal activation no longer passes a provider selection into lifecycle startup.

The existing quiescence lease and transactional activation/rollback boundary remain intact.

### 6. Exact OpenClaw model-call evidence

`plugins/cogentnexus-openclaw/src/v091-direct-model-call-lease.ts` now persists:

- exact `runId`;
- exact `callId`;
- provider/model provenance;
- start/deadline/end;
- outcome;
- `errorCategory`;
- `failureKind`.

Terminal semantics are deliberately failover-safe:

```text
model_call_ended(error)
        -> evidence only
agent_end(false)
        -> terminal run fence
exact errored call
        -> terminal_error
```

Therefore:

```text
call A error -> call B succeeds -> agent_end success
```

must not create model-error recovery.

A completed model call followed by `agent_end(false)` also must not be promoted into model-error recovery.

### 7. Exact Host terminal-error claim

`host_provider_v092.py` now claims only an exact eligible terminal model-call row:

- accepted Direct Ticket;
- exact Ticket/run/call;
- `terminal_error` + `outcome=error`;
- bounded recovery attempts;
- transactional claim.

Unknown/future providers can be claimed because provider/model values are provenance only.

### 8. Quiesced terminal-error classification

The Host classification path reuses existing Direct delivery/session fences.

Durable response/delivery/terminal/workflow evidence wins and suppresses duplicate inference recovery.

For a genuine failure it queues `cnx_direct_recovery`, records `recoveryAuthority=terminal-model-call-error`, and marks the exact model-call row Host-authorized/interrupted.

### 9. Provider-neutral recovery lifecycle — current HEAD

HEAD `58f70efb...` adds:

`recover_terminal_error_direct_model_call(root, claim)`

Current lifecycle:

```text
exact Host claim
 -> lifecycle prepare
 -> Gateway stop
 -> exact terminal-error classification
 -> Gateway start
 -> Gateway health verification
```

No provider is selected/probed/started/stopped by this function.

A `finally` restart safeguard exists, but partial-stop/start-failure semantics still require explicit failure-path tests.

## Current CI evidence

### Validate run

Run: `34383579174`

Head: `58f70efb6c036615924119fc32129f4619944b6e`

Overall: `FAILURE`.

Matrix:

- macOS 3.11: PASS
- macOS 3.14: PASS
- Ubuntu 3.11: PASS
- Ubuntu 3.14: PASS
- Windows 3.11: PASS
- Windows 3.14: FAIL
- package dry-run: PASS

Python on Windows 3.14:

`617 passed, 3 skipped, 6 subtests passed`

Windows 3.14 plugin suite:

- `62` test files passed;
- `304` tests passed;
- `1` test failed by timeout;
- failing test: `src/evaluation.test.ts` Phase 6 evaluation;
- Vitest timeout: `30000ms`;
- the Phase 6 test consumed roughly 180 seconds of the roughly 220-second plugin run.

This was a timeout, not an assertion failure. Do not call the full Validate run green until a newer run proves it.

### PS5.1 acceptance smoke

Run: `34383579210`

Result: PASS.

Windows 3.14 also passed namespace validation, baseline consistency, Python compilation, PowerShell syntax/acceptance checks, root-process exact exit-code checks, and all Python tests before the plugin test timeout.

## What is currently being worked on

The exact terminal-error recovery primitives are implemented, but the steady-state Supervisor does not yet fully consume them as the production recovery path.

### Immediate next work

1. Fresh-inspect current `agent_end(false)` wiring in `index.ts` and the model-call lease module.
2. Add a RED Supervisor integration test proving an exact terminal-error claim is consumed.
3. Minimal GREEN implementation: Supervisor calls the exact Host terminal recovery lifecycle.
4. Prove Supervisor does not:
   - use timer-only destructive recovery;
   - select/probe/start/stop a provider;
   - infer a latest run/Ticket;
   - cross session generations.
5. Add lifecycle failure/rollback tests.
6. Re-run focused tests and GitHub Actions.

## Remaining v0.9.5 work

### A. Supervisor terminal-error integration

Need exact claim consumption, duplicate prevention, bounded attempts, session/run fencing, and provider-neutral execution.

### B. Recovery lifecycle hardening

Test:

- prepare failure;
- stop failure/partial-stop behavior;
- classification failure;
- Gateway start failure;
- unhealthy Gateway after start;
- durable recovery remains auditable/recoverable;
- no duplicate authorization;
- attempt ceiling remains enforced.

If classification already committed recovery authorization and Gateway start then fails, do not fake-success or roll back into inference-completed state; leave durable recovery pending for reconciliation.

### C. Remove provider-mode capability gating

Inspect/repair `plugins/cogentnexus-openclaw/src/index.ts` and related provider-mode logic so Cloud/unknown providers do not lose:

- durable admission;
- compaction continuation;
- recovery;
- Ticket/workflow capability.

Provider-mode compatibility data may remain only if it is not capability authority.

### D. CLI contract

Target:

```text
cnxclaw start|stop|restart|status
    -> CNX/Gateway lifecycle

cnxclaw local ollama start|stop|restart|status|check
    -> local Ollama lifecycle only

OpenClaw Web Chat/native selector
    -> provider/model routing
```

Legacy `--provider` may remain only as a compatibility/deprecation alias that cannot mutate route authority.

`cnxclaw cloud` must not become a second provider-routing framework.

### E. InferenceAttempt identity

Finish the planned attempt ledger:

- stable Ticket;
- stable Session;
- stable Session Generation;
- one InferenceAttempt per model call;
- provider/model metadata per attempt;
- exact OpenClaw runId.

Provider/model switch must not increment CNX session generation.

### F. DeliveryAttempt identity

Finish the canonical delivery core:

- separate from inference attempt;
- exact Ticket/run/session-generation/surface identity;
- durable staging before transport;
- transport acknowledgement distinct from durable completion;
- no latest-run inference;
- ambiguous Discord receipts remain pending/recoverable;
- Dashboard and Discord adapters share one state machine.

Provider/model is not delivery identity.

### G. Session generation

Provider/model change and compaction do not advance generation.

Native delete/replace/rotate advances generation only according to actual lifecycle evidence.

Stale callbacks must never settle newer work.

### H. Idle / single wake

Consolidate recurring decisions under one Supervisor wake authority.

Keep the Task312 stale-pending-delivery wake repair.

Do not add another recurring poller without amending/testing the idle contract.

### I. Migration/release

After Plans 1-3 are green:

- converge all version surfaces to 0.9.5;
- validate v0.9.4 -> v0.9.5 migration;
- run provider-switch matrix;
- run Windows lifecycle acceptance;
- run idle/quiescence matrix;
- run full Actions on the exact candidate SHA;
- only then release/tag/publication.

## Safety fixes that must remain

- exact Discord delivery identity;
- no runId-less settlement;
- no latest-run inference;
- session owner/generation fencing;
- durable response/delivery evidence wins over inference recovery;
- terminal Ticket fences;
- config single-writer/quiescence protection;
- stale pending-delivery wake repair;
- timer-only destructive recovery suppression;
- Host recovery claim/finalization fences;
- exact runId/callId model evidence;
- OpenClaw failover-safe terminal error semantics.

## Hard fences

- No force push.
- No v0.9.5 release/tag yet.
- No live provider/model/auth route mutation during source repair.
- No manual SQLite/Ticket/session mutation.
- No latest-run/latest-Ticket guessing.
- No provider lifecycle authority in CNX Supervisor.
- No weakening ambiguous Discord receipt handling.
- No unrelated live-service/install/reset mutation.

## Resume procedure

1. Fresh-fetch branch HEAD.
2. Fresh-read `ACTIVE.md`, `STATUS.md`, Task315, this checkpoint.
3. Check current Actions for the exact HEAD.
4. Inspect `index.ts` + `v091-direct-model-call-lease.ts` before the next repair.
5. Start production changes with RED -> minimal fix -> GREEN.
6. Record exact commit SHA and CI evidence at every milestone.

## Suggested next-session prompt

> ทำ CogentNexus-OpenClaw ต่อจาก `CNX-20260910-315-session-handoff-checkpoint.md` ครับ
>
> Repo: `funggier/CogentNexus-OpenClaw`
> Branch: `agent/v0.9.5-architecture-repair`
>
> Fresh-fetch current GitHub HEAD, `ACTIVE.md`, `STATUS.md`, Task315 และ Actions ก่อนทำงาน และยึด GitHub source/Actions เป็น authoritative
>
> จุดล่าสุดคือ `58f70efb6c036615924119fc32129f4619944b6e`: Host state/provider-neutral façade และ exact terminal model-call evidence/claim/classification/lifecycle ทำแล้ว
>
> ขั้นต่อไปตรวจ `agent_end(false)` wiring แล้วทำ RED test สำหรับ Supervisor integration ของ terminal model-call recovery ก่อน แก้ production แบบ minimal ให้ GREEN โดยห้ามคืน global provider authority และห้าม timer-only guessing
>
> จากนั้นทำ lifecycle failure/rollback, provider-mode gating, CLI local Ollama namespace, delivery/session identity, single-wake/idle และ migration/release ตาม execution index
>
> ห้าม release/tag จน Plans 1-3 และ exact candidate/Windows/provider-switch/idle/CI gates ผ่านครบ
