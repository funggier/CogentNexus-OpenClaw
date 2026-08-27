# CogentNexus-OpenClaw Direction Decision Log

This file records decisions that materially change project direction, scope, safety rules, or architecture.

A decision may be revised later. When that happens, preserve the old entry and add a new decision explaining why the direction changed.

---

## D-012 — Explicit OpenClaw security exception with continuing development

**Date:** 2026-08-28  
**State:** Active / explicit operator exception

### Decision

For the v0.9.3 stabilization line, retain OpenClaw `2026.7.1-2` as the validated operational baseline and explicitly accept the known upstream high-severity dependency findings in the published OpenClaw dependency graph for the purpose of completing bounded real-Windows acceptance.

This exception does **not** claim that the upstream findings are remediated. In particular, the accepted risk includes the known OpenClaw `2026.7.1-2` shrinkwrap findings involving `brace-expansion` (`GHSA-mh99-v99m-4gvg`) and `fast-uri` (`GHSA-v2hh-gcrm-f6hx`). CogentNexus production-dependency validation continues to require `npm audit --omit=dev` to pass; the exception exists because the full development/install graph reaches OpenClaw's externally published pinned dependency graph.

The operator does **not** require the v0.9.3 development branch or version line to stop moving after acceptance. Development may continue normally.

### Acceptance snapshot rule

Continuing development does not permit ambiguous live evidence.

Before a real-Windows acceptance execution, select one exact acceptance snapshot and record:

- the exact CogentNexus source commit tested;
- version metadata;
- payload-v2 fingerprint and file count;
- archive SHA256 used for installation when applicable;
- OpenClaw baseline `2026.7.1-2`;
- commands, exit codes, and durable evidence paths.

For acceptance purposes, the exact commit/artifact snapshot is treated as immutable evidence even though the branch and v0.9.3 development line may continue to advance afterward. No permanent branch stop, release tag, or version freeze is implied.

Acceptance evidence applies only to the exact snapshot/artifact that produced it. A later source or package-affecting change requires qualification of that newer snapshot before it can inherit the acceptance claim.

### Phase K interpretation

The Phase K exact-candidate requirement remains a provenance gate, not a requirement to halt ongoing development.

Phase K is satisfied by identifying and proving the exact acceptance snapshot before live-machine work. The branch may subsequently advance, but the tested snapshot remains identifiable by commit and artifact hashes. Release publication remains separately gated.

### Authorized live scope

After the selected snapshot has fresh repository/package proof, a bounded real-Windows acceptance task may perform the lifecycle work required by D-010, including clean uninstall, fresh reinstall from the exact candidate artifact/consumer path, install-over where required, reset confirmation testing, Gateway/provider lifecycle and recovery tests, durable Ticket/Workflow/Delivery verification, and the final Dashboard durable-delivery acceptance scenario.

The task must preserve externally owned OpenClaw and Ollama installations/data unless a separately proven CogentNexus-owned artifact is explicitly in scope. Exact-PID and recovery safety invariants remain in force.

### Boundaries that remain unchanged

This exception does not authorize:

- rebaselining OpenClaw away from `2026.7.1-2`;
- silently patching or overriding OpenClaw's foundational dependency graph;
- claiming the accepted upstream vulnerabilities are fixed;
- rewriting the frozen v0.9.2 historical baseline;
- force push;
- merge, tag, or GitHub Release publication.

Release publication remains a separate explicit human action under D-011.

### Why

The CogentNexus repository stabilization gates through Phase J are green, while the remaining high-severity findings originate from the externally published OpenClaw stable baseline rather than from CogentNexus choosing an older top-level dependency graph. Rebaselining to a different OpenClaw runtime would introduce a separate host-compatibility qualification problem.

The operator chose to preserve the already-qualified OpenClaw baseline, explicitly accept the known upstream risk, complete real-Windows behavioral acceptance against an exact proven snapshot, and continue development afterward rather than treating acceptance as a permanent stop on the v0.9.3 development line.

### Follow-up

Continue monitoring the OpenClaw stable channel for authoritative remediation. A future supported stable fix can be evaluated as a separate OpenClaw rebaseline/compatibility task rather than silently altering this v0.9.3 acceptance baseline.

---

## D-011 — Release publication requires an explicit exact-candidate human action

**Date:** 2026-08-28  
**State:** Active

### Decision

GitHub Release publication is a separate manual action and must not be reachable merely because a development, tag, or `release/v*` branch is pushed.

The release workflow uses explicit `workflow_dispatch` inputs for the requested version and exact candidate SHA. It must fail closed unless the checked-out candidate SHA and release metadata agree with those inputs.

Candidate validation/build executes with read-only repository contents permission and without persisted checkout credentials. The separate publish job receives write permission only after the validated release proof artifact is produced.

### Required fences

- validate candidate SHA shape before checkout;
- checkout and verify the exact requested candidate SHA;
- require requested version, `VERSION`, package version, manifest version, lock version, and release notes to agree;
- preserve a duplicate-release fence using `gh release view` before `gh release create`;
- publish assets only from the previously validated package job;
- target the exact requested candidate SHA;
- never treat branch push CI/package proof as authorization to publish.

### Why

The previous release workflow accepted both tag pushes and `release/v*` branch pushes, so ordinary branch activity could reach `gh release create`. That collapsed candidate preparation and public publication into the same automation boundary.

### Safety consequence

Repository stabilization may inspect and test the release workflow but must not dispatch it. Merge, tag, and release publication remain explicit human-controlled decisions after the exact candidate and required acceptance evidence are reviewed.

---

## D-010 — v1.0.0 requires real-Windows lifecycle acceptance

**Date:** 2026-08-22  
**State:** Active

### Decision

Target the current Ollama-only development line for a `v1.0.0` release only after the complete real-Windows consumer lifecycle is proven with reviewable evidence.

The lifecycle gate includes:

- install the exact candidate from the real release/consumer path;
- install over an existing CogentNexus-OpenClaw deployment and verify safe convergence;
- exercise the documented `cnxclaw reset` confirmation path and verify its outcome;
- cleanly uninstall CogentNexus-OpenClaw after explicit confirmation;
- verify CogentNexus-OpenClaw-owned tasks, package/plugin state, launchers, and managed artifacts are removed or intentionally documented;
- preserve external OpenClaw and Ollama installations and user data unless a task explicitly proves CogentNexus-OpenClaw ownership and authorizes removal;
- reinstall the exact candidate from the real release/consumer path after uninstall;
- prove post-reinstall MANAGED/Ollama state, healthy Gateway and Ollama listeners, and recovery verdict `READY`;
- retain exact artifact version, source commit, SHA256, commands, exit codes, and evidence paths;
- require all applicable CI and process-recovery gates to be green for the exact release candidate.

### Why

The human operator requested a complete install on the real machine, an uninstall/reinstall proof, and promotion to version 1 when the product is genuinely complete. A successful one-time developer-path install is not sufficient release evidence.

### Safety boundary

Lifecycle tasks must remain exact and reversible. They may not touch the frozen v0.9.2 release, reintroduce LM Studio, uninstall external dependencies, use process-tree kills, conceal skipped checks, or repeat side effects after a matching completed report exists.

### Release consequence

Passing the current process-recovery plan is necessary but not sufficient for `v1.0.0`. After all lifecycle evidence and CI gates are accepted, prepare the PR and release candidate for final human review. Do not merge, tag, or publish the release automatically from the coordination loop.

---

## D-009 — Optional automatic Codex watch mode

**Date:** 2026-08-22  
**State:** Active

### Decision

Allow an optional continuous coordination mode using a Codex Scheduled task that polls the durable GitHub coordination branch at a minute-based cadence.

Automatic execution is authorized only when `ACTIVE.md` contains both `Status: READY_FOR_CODEX` and `Execution mode: AUTO`.

### Why

The human operator should not need to relay `ต่อ` after every ChatGPT-Codex handoff. GitHub already provides the durable task pointer, immutable execution specification, report state, and duplicate-execution fence.

### Safety boundary

Watch mode does not grant open-ended autonomy. Codex must still re-synchronize on every poll, read the exact task, satisfy every precondition, preserve unrelated work, avoid duplicate side effects, publish a matching report, and stop that run.

Codex may not invent the next task. ChatGPT remains responsible for tasks/reviews and the human remains final authority.

### Operational consequence

Near-immediate pickup means a one-minute Scheduled-task cadence, not a zero-latency webhook. Local execution requires the Windows machine to remain powered on and the ChatGPT desktop app to remain running.

Manual `ต่อ` remains a fallback. `หยุดเฝ้า` pauses/disables the Scheduled task without changing CogentNexus-OpenClaw runtime state.

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

A real Gateway hard-crash test showed that the replacement OpenClaw Gateway listener returned successfully while `cnxclaw check recovery` still reported `READY_WITH_WARNINGS` because a maintenance/recovery marker remained active.

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

Existing LM Studio installations are not uninstalled or modified merely because CogentNexus-OpenClaw no longer manages them.

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
