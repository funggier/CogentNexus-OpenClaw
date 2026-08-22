# CogentNexus Direction Decision Log

This file records decisions that materially change project direction, scope, safety rules, or architecture.

A decision may be revised later. When that happens, preserve the old entry and add a new decision explaining why the direction changed.

---

## D-008 — Codex execution is signal-driven from durable GitHub state

**Date:** 2026-08-22  
**State:** Active

### Decision

Keep substantive project conversation in ChatGPT and reduce the human handoff to Codex to minimal trigger signals.

After Codex accepts the standing bootstrap in `docs/operations/coordination/CODEX_BOOTSTRAP.md`, the normal execution trigger is:

```text
ต่อ
```

On each trigger, Codex must synchronize and re-read the current GitHub coordination state rather than depending on copied task text or stale conversation memory.

### Why

The human operator should remain the final authority without becoming a manual message bus between ChatGPT and Codex. GitHub already carries the durable task specification, exact source expectations, evidence contract, and execution report.

### Safety boundary

A human trigger authorizes Codex to evaluate the current active task; it does not bypass task-specific safety gates.

Codex must not repeat completed disruptive effects merely because `ต่อ` is sent again. If a matching completed report exists or the active state is awaiting ChatGPT review, Codex reports that state and stops.

### Consequence

The normal coordination loop is:

```text
Human talks with ChatGPT
  -> ChatGPT publishes READY_FOR_CODEX task
  -> Human sends Codex: ต่อ
  -> Codex syncs, executes, pushes report, stops
  -> Human returns to ChatGPT / asks to continue
  -> ChatGPT reviews GitHub report and publishes next task
  -> repeat
```

This is a controlled handshake, not autonomous background execution. ChatGPT and Codex communicate through durable repository state while the human supplies the execution pulse.

---

## D-007 — GitHub is the durable ChatGPT-Codex coordination surface

**Date:** 2026-08-22  
**State:** Active

### Decision

Use `docs/operations/coordination/` as the durable handoff surface between ChatGPT, Codex, and the human operator when ChatGPT is responsible for task design/review and Codex performs local-machine execution.

### Why

ChatGPT and Codex may have different tool surfaces and may run in different sessions. Relying on copied chat text makes task intent, source provenance, execution results, and evidence easy to lose or distort.

GitHub already provides shared durable state, exact commits, reviewable history, and a common repository context for both sides.

### Ownership rule

To reduce write conflicts:

- ChatGPT owns `ACTIVE.md`, `tasks/`, and `reviews/`;
- Codex owns `reports/`;
- the human operator remains final authority and may intervene anywhere.

Task specifications are not rewritten by the executor merely to report progress. Execution state and evidence belong in the matching report.

### Consequence

A task may now flow as:

```text
Human intent
  -> ChatGPT task file
  -> ACTIVE.md
  -> Codex local execution
  -> Codex report + evidence references
  -> ChatGPT review
  -> next task / close
```

Coordination files are not technical acceptance by themselves. Code, tests, durable evidence, and release gates remain authoritative for proven capability.

---

## D-006 — Operations documentation is a living layer

**Date:** 2026-08-22  
**State:** Active

### Decision

Maintain `docs/operations/` as a changeable working-memory layer for project status, roadmap, work history, and direction decisions.

### Why

The project now contains several different kinds of truth:

- frozen release behavior;
- accepted technical boundaries;
- active development hypotheses;
- live Windows evidence;
- short-term experiments;
- long-term architectural intent.

Putting all of these into one static `CURRENT_STATE` or README causes either stale documentation or premature claims.

### Consequence

Operations docs may change frequently and may lead the latest accepted release documentation during development. Durable evidence and accepted release gates remain authoritative for claims that a capability is proven.

---

## D-005 — Separate process recovery from durable-state convergence

**Date:** 2026-08-22  
**State:** Active

### Decision

Do not equate “listener returned” with “recovery completed.”

Process health and durable recovery-state convergence must be observed separately.

### Why

A real Gateway hard-crash test showed that the replacement OpenClaw Gateway listener returned successfully while `cnx check recovery` still reported `READY_WITH_WARNINGS` because a maintenance/recovery marker remained active.

### Consequence

A dedicated Gateway Convergence diagnostic now observes whether durable state returns to `READY` without an operator command. Runtime code should not be modified until this diagnostic distinguishes test timing from a genuine state-machine completion bug.

---

## D-004 — Recovery test harnesses may kill exact validated PIDs only

**Date:** 2026-08-22  
**State:** Active / safety invariant

### Decision

Disruptive Recovery Reality tests must never use process-tree kill as a normal injection mechanism.

### Required gates

Before a target process may be force-killed:

- resolve it from the intended listener;
- validate executable/process name;
- validate command line/role identity;
- reject the harness PID;
- reject harness ancestors;
- reject protected interactive/system process classes;
- persist active-operation/target evidence;
- kill only the exact validated PID.

### Why

An early harness terminated abruptly and unrelated interactive processes were lost before the intended recovery scenario even started.

### Consequence

PowerShell, cmd, conhost, Firefox, Explorer, Windows Terminal/OpenConsole, the harness, and harness ancestors are explicit protected targets in current harnesses.

---

## D-003 — v0.9.3 is Ollama-only

**Date:** 2026-08-22  
**State:** Active

### Decision

Starting with v0.9.3, the managed local provider surface is Ollama only.

### Why

Maintaining LM Studio in parallel increased lifecycle, adapter, timeout, ownership, and testing complexity during the phase where recovery semantics themselves still need real-machine proof. The intended deployment also favored Ollama's memory/operational characteristics.

### Consequence

v0.9.3 operator paths should not select, start, stop, probe, advertise, or test LM Studio.

Existing LM Studio installations are not uninstalled or modified merely because CogentNexus no longer manages them.

v0.9.2 remains historically unchanged.

---

## D-002 — Recovery authority is event/evidence driven, not timer driven

**State:** Active architectural invariant

### Decision

Elapsed time, cooldown windows, or arbitrary retry timers must not become the authority that decides whether a failure is real or whether recovery is allowed.

### Why

A slow but healthy model call can be silent for a long time, while an actual provider/Gateway failure may be detectable immediately from stronger evidence.

### Consequence

Timeouts in test harnesses are observation/safety fuses. Durable incidents, explicit failure evidence, stable-success evidence, verified operator transitions, and ownership/generation fences define recovery authority.

---

## D-001 — v0.9.2 is a frozen Golden Baseline

**Date:** 2026-08-22  
**State:** Active

### Decision

Do not rewrite the released v0.9.2 tag or patch it merely to simplify current v0.9.3 development.

### Why

v0.9.2 completed acceptance and release publication and provides a known rollback/reference boundary.

### Consequence

v0.9.3 work occurs on its own development branch/PR and may layer compatibility/migration behavior without changing the historical release.
