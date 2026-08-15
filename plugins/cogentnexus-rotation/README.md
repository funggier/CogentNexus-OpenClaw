# CogentNexus OpenClaw Bridge

The package ID remains `cogentnexus-rotation` for compatibility, but in v0.8 the plugin is documented as the **CogentNexus OpenClaw Bridge**.

It connects OpenClaw to the external CogentNexus Host/Ticket/workflow runtime. The bridge is not the durability authority by itself; durable authority lives in persisted Host, Ticket, workflow, lease, generation, and outbox state.

## Responsibilities

- commit eligible owner messages to the SQLite Ticket store before inference when `ticketFirst` is enabled;
- bind requests/workflows to trusted owner session identity;
- route obvious durable requests before conversational inference when pre-inference admission qualifies them;
- dispatch and recover Ticket-backed durable workflows;
- preserve request-hash/idempotency boundaries;
- fence duplicate starts by lease/generation/run identity;
- bridge verified context-rotation handoffs when explicitly enabled;
- deliver terminal Ticket/workflow outbox results to the bound owner;
- expose optional knowledge/research tools without making them execution authority.

## What the bridge must not do

- force every message into a durable workflow;
- make a greeting pay STAGED workflow overhead;
- treat model prose as authoritative completion evidence;
- silently repeat external side effects after interruption;
- resurrect cancelled Tickets/sessions;
- make native OpenClaw unusable when CogentNexus is disabled.

## Ticket-first continuity

With managed defaults:

```text
owner message
   -> Ticket commit
   -> lane selection
      DIRECT / LOOKUP / ACTION / STAGED
   -> execution
   -> terminal/outbox state
   -> owner delivery
```

Ticket creation is intentionally lightweight. A DIRECT message may remain an ordinary conversational turn after its Ticket is committed.

If a direct turn is left accepted when Gateway failure is confirmed, the external Host Controller may promote that Ticket to durable recovery after runtime health returns.

## Managed defaults

`cnx enable` configures conservative defaults suitable for local models and low-resource machines:

- `ticketFirst = true`
- `preInferenceAdmission = true`
- `autoWorkflowCompletion = true`
- `enforcedMode = true`
- `autoResume = true`
- `ticketDispatchLimit = 1`
- `ticketMaximumRunning = 1`
- bounded attempts and short deterministic recovery/dispatch/outbox polls

These settings preserve one inference lane by default. Parallelism should increase only from measured need.

## Pre-inference durable admission

`preInferenceAdmission` is distinct from Ticket-first intake.

- Ticket-first records eligible owner messages for continuity.
- Pre-inference admission blocks duplicate conversational execution only when deterministic classification says the request already belongs in durable execution.

Configuration:

- `preInferenceAdmission`
- `admissionMinimumScore`
- `durableWorkerModel`

The bridge excludes internal continuation/subagent turns from owner admission and retains idempotent workflow identity.

## Durable workflow execution

Normal durable work runs through the deterministic CogentNexus controller and configured worker provider. Executors produce candidates; validators/controller evidence determine PASS.

Temporary clean-session TaskFlow/Codex rotation remains opt-in through `autoRotate`. It should not be enabled merely to make ordinary work more complex.

## Cancellation

Host-level commands can cancel a single Ticket or all non-terminal Tickets for an owner session. Cancellation is terminal and must fence later recovery.

For workflow-level cancellation, the deterministic workflow controller records cancellation evidence and terminal completion delivery.

## Experience / lesson store

The optional SQLite Experience/Lesson store remains additive. Verified lessons may be retrieved as data; they are not executable policy and do not override user intent, authorization, controller state, or deterministic gates.

Disable with:

```text
knowledgeEnabled = false
```

without disabling Ticket continuity.

## External research

External research storage is optional and bounded by query/source/size/time/freshness/corroboration budgets. Stored pages remain external observations and never become verified lessons automatically.

Network access still requires an explicit provider/capability adapter.

Disable with:

```text
externalResearchEnabled = false
```

without affecting local Ticket/workflow continuity.

## PASSTHROUGH

When `cnx disable` enters PASSTHROUGH:

- CogentNexus startup ownership is disabled;
- the managed workspace policy block is removed;
- this plugin is disabled;
- native OpenClaw is restarted/started;
- durable CogentNexus state is preserved.

Native OpenClaw must remain usable in this mode.

## Build and validate

```bash
npm ci
npm test
npm run evaluation
npm audit --omit=dev
npm run plugin:validate
```

A Gateway restart is required after plugin installation/configuration changes.

## Compatibility

The technical peer dependency is intentionally broader than the current tested baseline. CogentNexus release/compatibility documentation defines the OpenClaw versions exercised end-to-end for a given release.
