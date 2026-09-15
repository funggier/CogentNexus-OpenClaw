# CNX-20260915-363 — Runtime identity reconciliation

Status: `READY_FOR_HERMES`
Parent: `CNX-20260915-362`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Explain the live Host controller regression without normalizing or manually editing runtime state. Do not open Dashboard, send prompts, reinstall, run lifecycle mutation, change provider routing/auth, modify hooks/main/tag, or force-push.

## Exact identity transition

```text
CNX-361 accepted:
schemaVersion=2
cnxMode=active
desiredGateway=running
generation=103

        ↓

CNX-362 observed:
schemaVersion=1
mode=passthrough
desiredGateway=running
generation=1
```

The installed plugin artifact/module identity remains the CNX-361 candidate identity. The investigation must therefore treat this as a runtime-state reconciliation boundary, not as a Dashboard/OpenAI defect.

## Alternatives to distinguish

Do not assume the writer. Trace evidence for:

A. controller overwritten by installer
B. controller reset during host initialization
C. migration/compatibility logic writing a legacy schema
D. startup/enable/disable lifecycle transition
E. stale/alternate workspace or state root
F. recovery/restore/quarantine copying an old controller
G. another process/service writing the controller
H. runtime reading a different controller than the one CNX-361 activation wrote

## Required investigation

1. Read CNX-361 and CNX-362 reports and bind claims to the exact remote HEAD.
2. Trace every code path that can write `host/controller.json`, including `save_state`, `transition_mode`, `default_state`, `migrate_v094_state`, `cnxMode`, `mode`, and `generation`. Classify each writer as read-only, initialization, migration, lifecycle transition, recovery, installer, or service/supervisor.
3. Prove the installer/Host workspace, stateRoot, controllerPath, applicationData, launcher, and runtime-authority chain. Do not infer equality from filenames.
4. Inspect canonical v0.9.5 state and the exact path that could produce schema 1 / passthrough / generation 1.
5. Compare available timestamps and provenance: CNX-361 activation, controller `updatedAt`, installer stages, Gateway/service/supervisor starts, and CNX-362 preflight.
6. State exactly one primary hypothesis and test it with the smallest offline/replayable evidence. Do not implement a repair unless the defect is proven.

## Outcome

Publish `CNX-20260915-363-runtime-identity-reconciliation-report.md` as `ROOT_CAUSE_PROVEN` only if the writer and event are established. Otherwise publish `BLOCKED`. Do not manually restore `cnxMode=active` or generation 103. Do not send a Dashboard handoff from CNX-363.
