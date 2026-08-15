# CogentNexus v0.8 Baseline

This document is the canonical architecture and terminology baseline for CogentNexus v0.8+.

Historical release notes describe how the project evolved. If older documentation conflicts with this baseline, this baseline governs current design language and intended behavior.

## 1. Purpose

CogentNexus exists to preserve user intent and accepted work across failures while using only as much execution machinery as the request actually needs.

The system is built around one core continuity rule:

> Once an eligible user message is durably accepted, it must not silently disappear. It must eventually become delivered/completed, cancelled, or explicitly failed with evidence.

This is a **continuity guarantee**, not a requirement to run every request through a heavy workflow.

## 2. Layer model

```text
User / Channel
      |
      v
+---------------------------+
| CogentNexus Host          |
| continuity + lifecycle    |
+-------------+-------------+
              |
              v
+---------------------------+
| OpenClaw                  |
| channel/session/tool host |
+-------------+-------------+
              |
              v
+---------------------------+
| Admission / lane policy   |
| DIRECT/LOOKUP/ACTION/...  |
+-------------+-------------+
              |
       +------+------+
       |             |
       v             v
 lightweight      STAGED
 execution        durable workflow
                     |
                     v
             validator / reviewer
                     |
                     v
                  delivery
```

### 2.1 CogentNexus Host Controller

Runs outside model inference and must remain useful even when OpenClaw or the provider is unavailable.

Responsibilities:

- persist desired runtime state;
- support Ticket-first durable acceptance;
- supervise health without model inference;
- distinguish unplanned failure from intentional stop;
- start/stop/restart managed runtime components;
- recover eligible non-terminal work;
- cancel Tickets/sessions and fence cancelled work from resurrection;
- preserve state across process death and machine reboot.

The Host does **not** decide that every request needs STAGED execution.

### 2.2 OpenClaw bridge

The `cogentnexus-rotation` plugin is the OpenClaw integration bridge. The historical plugin ID is retained for compatibility, even though its responsibility is now broader than context rotation.

Responsibilities include:

- Ticket-first intake inside the OpenClaw request boundary;
- owner/session binding;
- durable admission for requests that already qualify for durable execution;
- Ticket dispatch/recovery/outbox integration;
- context handoff and completion delivery.

The plugin is a managed component, not the durability authority. Durable authority lives in persisted Host/Ticket/workflow state.

### 2.3 Request lane policy

Admission chooses the lightest reliable lane **before heavy workflow modules are loaded**:

- **DIRECT** — greetings, conversation, explanation, advice, brainstorming, short drafting, simple questions from current context.
- **LOOKUP** — focused read-only retrieval using the minimum necessary sources/tools.
- **ACTION** — bounded reversible execution with proportionate verification.
- **STAGED** — multi-step, consequential, interruption-prone, dependency-heavy, externally mutating, repeatedly failing, or independently reviewed work.

Escalation is based on observed complexity/risk, not on the mere presence of CogentNexus.

### 2.4 Durable workflow runtime

Activated only when work needs durable decomposition/recovery/verification.

Responsibilities:

- stable unit contracts and dependency graph;
- checkpointed controller state;
- bounded execution/repair;
- deterministic validation;
- reviewer policy where semantic review is required;
- artifact hashes and integration gates;
- terminal evidence and owner delivery.

## 3. Authority order

Current design uses this conceptual priority order:

1. system/platform safety and authorization constraints;
2. explicit user intent and requested outcome;
3. durable continuity state already committed by Host/Ticket infrastructure;
4. request-lane admission;
5. durable workflow controller when STAGED is selected;
6. executor/tool/reviewer outputs within bounded authority;
7. deterministic evidence before consequential completion claims.

No AI prose is authoritative merely because it says an action succeeded.

## 4. Operating modes

### MANAGED

CogentNexus owns continuity and managed lifecycle behavior.

Typical state:

```text
mode = managed
desiredGateway = running
desiredProvider = running
```

The supervisor may reconcile an unplanned failure and resume eligible committed work.

### PASSTHROUGH

CogentNexus relinquishes OpenClaw interception/background ownership.

`cnx disable` means:

- persist PASSTHROUGH mode;
- disable CogentNexus background startup ownership;
- remove the managed workspace policy block;
- disable the CogentNexus OpenClaw plugin;
- keep durable CogentNexus state;
- restart/start OpenClaw natively so it remains usable.

PASSTHROUGH is not an uninstall.

### MAINTENANCE

Intentional stopped state.

`cnx stop` means:

- persist MAINTENANCE mode;
- set desired managed runtime to stopped;
- stop managed runtime/provider according to policy;
- prevent the supervisor from fighting the operator's deliberate stop.

`cnx start` returns to MANAGED and reconciles runtime health.

## 5. Ticket-first semantics

A Ticket is a lightweight durable record that the system accepted a user message. It is not itself a plan or reasoning trace.

Conceptually:

```text
receive message
   -> commit Ticket
   -> choose lane
   -> execute
   -> commit response/terminal state
   -> deliver
```

Ticket-first intake should store only durable facts needed for continuity, such as message/session identity, timestamps, status, leases, attempts, workflow binding, and terminal delivery state.

Do not store private chain-of-thought.

## 6. Interruption and recovery

Recovery must distinguish slow work from dead/stale work using observable evidence such as:

- Gateway/provider health;
- worker PID/lease state;
- heartbeat and generation;
- Ticket/workflow status;
- response/outbox state;
- deterministic checkpoints.

Important rules:

- do not rerun completed work;
- do not rerun external side effects blindly;
- if response content is already durably ready, retry delivery rather than inference;
- cancelled work is terminal and must not be resurrected;
- stale worker generations cannot regain authority;
- periodic supervision performs no model inference.

## 7. Session cancellation

Cancelling or deleting a managed session must revoke unfinished work associated with the affected session scope.

Cancellation should be represented durably before cleanup so detached workers cannot recreate abandoned work later.

Terminal cancellation may be garbage-collected later, but recovery must always observe the cancellation/tombstone first.

## 8. Reboot / power-loss model

The design assumes that committed durable state on persistent storage survives ordinary process/machine interruption.

After reboot, the Host supervisor can:

1. read persisted operating/desired state;
2. reconcile Gateway/provider health;
3. identify stale leases/controllers;
4. resume eligible non-terminal Tickets/workflows from committed evidence;
5. retry pending delivery without recomputing completed output.

This architecture does not claim protection against storage corruption, disk loss, or messages that never reached the durable acceptance boundary.

## 9. Startup policy vs operating mode

These are separate concepts:

- **Operating mode** answers: who owns OpenClaw continuity/lifecycle now? (`managed`, `passthrough`, `maintenance`)
- **Startup policy** answers: should the CogentNexus supervisor be automatically launched by the operating system?

Changing startup policy must not silently change operating mode. Changing operating mode may reconcile startup ownership as part of an explicit `enable`/`disable` operation.

## 10. Resource policy

For local models and constrained hardware:

- default to one inference lane;
- keep DIRECT context/tool surface small;
- load references lazily;
- prefer durable external state over giant always-live context;
- increase parallelism/context only from measured need.

The intended equation is:

```text
small active context + durable external state = long-running capability
```

## 11. Compatibility principle

OpenClaw must remain usable without CogentNexus.

CogentNexus must retain control state without depending on a live OpenClaw inference process.

When combined, CogentNexus enhances continuity and verification without becoming a required dependency for native OpenClaw operation.

## 12. Current naming

Use these names consistently in current documentation:

- **CogentNexus Host Controller** — external deterministic control/lifecycle layer.
- **CogentNexus OpenClaw Bridge** — plugin integration role; plugin ID remains `cogentnexus-rotation` for compatibility.
- **Ticket-first continuity** — durable acceptance before inference.
- **Request lane** — DIRECT / LOOKUP / ACTION / STAGED.
- **Durable workflow runtime** — heavy checkpointed/verified machinery used only when needed.
- **MANAGED / PASSTHROUGH / MAINTENANCE** — host ownership modes.

Avoid describing CogentNexus as a mandatory heavy cognitive runtime for every request.
