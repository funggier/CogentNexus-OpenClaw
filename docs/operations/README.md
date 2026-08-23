# CogentNexus Project Operations

This directory is the **living operational memory** of the CogentNexus project.

It records what has been completed, what is being investigated now, what is planned next, and which project decisions changed the direction of development.

## This documentation is intentionally changeable

The documents in this directory are **not immutable specifications, release contracts, or promises**.

They are expected to change when:

- new real-world evidence contradicts an assumption;
- a test reveals a better implementation boundary;
- priorities change;
- a new idea produces a better path to the same project intent;
- an experimental direction is abandoned;
- a short-term objective is completed and the next objective becomes active.

Changing these documents is normal project operation. The purpose is to preserve direction without freezing the project into an obsolete plan.

## Evidence outranks plans

When this directory conflicts with durable test evidence, accepted release documentation, or the actual implementation, **evidence wins** and these operations documents should be updated.

Use these documents as a navigation and planning layer. Use accepted release documentation, source code, test artifacts, and durable evidence as the authority for claims that a capability is proven.

In particular:

- `docs/CURRENT_STATE.md` describes the accepted/released capability boundary;
- this directory may describe development work that is newer than the current accepted release;
- a roadmap item is not considered complete merely because code exists;
- a recovery capability is not considered proven until its required evidence gate passes.

## Documents

| Document | Purpose |
| --- | --- |
| [STATUS.md](STATUS.md) | Current project position, active experiment, proven vs unproven boundaries |
| [ROADMAP.md](ROADMAP.md) | Short-, medium-, and long-term objectives and success criteria |
| [WORKLOG.md](WORKLOG.md) | Chronological record of meaningful development/recovery milestones |
| [DECISIONS.md](DECISIONS.md) | Important direction changes and why they were made |
| [coordination/](coordination/) | Durable GitHub handoff between ChatGPT, Codex, and the human operator |

## ChatGPT ↔ Codex coordination

When ChatGPT can design/review work through GitHub but cannot directly execute on the local Windows machine, and Codex can execute locally, use [`coordination/`](coordination/) as the shared handoff layer.

The normal loop is:

```text
Human intent
   ↓
ChatGPT task specification
   ↓
GitHub coordination task
   ↓
Codex local execution
   ↓
GitHub execution report + evidence references
   ↓
ChatGPT review
   ↓
next task / close
```

The active handoff is always pointed to by [`coordination/ACTIVE.md`](coordination/ACTIVE.md). Task, report, and review files use one stable Task ID so that intent, execution, evidence, and review remain traceable across separate agents and sessions.

## Update discipline

A useful update should answer at least one of these questions:

1. What changed?
2. What evidence caused the change?
3. What is now considered proven?
4. What remains unproven?
5. What is the next smallest meaningful objective?
6. Did the project direction or architecture change?

Prefer exact references when available: version, branch, PR, commit SHA, test name, evidence filename, or acceptance gate.

## Time horizons

The roadmap uses flexible horizons rather than fixed calendar promises:

- **Short term** — the current blocking proof or implementation sequence.
- **Medium term** — the next capability layer after the current blocker is closed.
- **Long term** — the architectural destination and system properties we want to preserve as the project evolves.

Items may move between horizons when evidence changes priorities.

## Core continuity direction

The current project direction can be summarized as:

```text
User intent
   ↓
Durable Ticket / work state
   ↓
Runtime execution
   ↓
process / provider / machine failure
   ↓
recover runtime
   ↓
read durable evidence
   ↓
resume only incomplete work
   ↓
deliver without duplicating completed effects
```

The runtime processes are replaceable. Durable intent, committed work state, evidence, and reconciliation are the continuity authority.

## Maintenance rule

Keep this directory concise enough to read at the start of a development session. Archive history in `WORKLOG.md` and `DECISIONS.md`; keep `STATUS.md` focused on **now** and `ROADMAP.md` focused on **next**.
