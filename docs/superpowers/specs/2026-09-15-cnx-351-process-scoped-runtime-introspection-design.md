# CNX-351 — Process-Scoped Runtime Introspection Boundary Design

## Status

**DESIGN APPROVED BY HUMAN OPERATOR — read-only diagnosis only; no production behavior change is authorized.**

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub branch: `cnx-351-process-scoped-runtime-introspection`
- Parent/baseline: `f0426865160e6a4e2fdef35de397a648fc5a314f` (CNX-350 finalization)
- GitHub remote is authoritative; local-only state is not evidence.

## Problem

CNX-350 established the real OpenClaw Gateway PID (`17080`) and the installed CogentNexus extension path/fingerprint, but could not bind that installed artifact to the JavaScript module actually loaded by the running process. The effective dynamic hook registry and process-scoped `before_agent_run` handler are also not externally observable through the current read-only surfaces. D and E therefore remain unresolved.

## Objective

Determine whether the repository already has, or can safely expose through **read-only diagnostic means**, a process-scoped runtime introspection boundary that can identify:

1. the active OpenClaw Gateway PID;
2. the loaded CogentNexus module path/URL;
3. the loaded artifact fingerprint;
4. plugin registration state;
5. effective `before_agent_run` registry/handler ownership; and
6. the distinction between static plugin inventory and the live dynamic hook registry.

CNX-351 must not alter runtime semantics. If the environment cannot observe the boundary, the task must document the exact observability gap rather than invent a new runtime path or perform live traffic.

## Boundary model

```text
GitHub source
  -> installed extension
  -> running Gateway PID
  -> loaded JS module
  -> registration call
  -> effective hook registry
  -> before_agent_run handler
```

## Design principles

### Process-scoped proof

A file on disk, plugin inventory row, or repository source hash is not proof of what the running Gateway has loaded. Runtime claims must be tied to the actual process or an authoritative process-scoped diagnostic.

### Read-only diagnostics first

Prefer existing OpenClaw commands, existing plugin diagnostics, OS process inspection, and read-only runtime metadata. Only add instrumentation when there is no existing safe observation surface.

### No semantic traffic

No Dashboard/UI request, replay, resend, provider call, or user-facing semantic message is permitted.

### No repair

Even if a definitive mismatch or bypass is found, stop at diagnosis. Production repair requires a new task with its own reproducible RED regression test.

## Investigation requirements

### 1. Existing mechanism inventory

Search the repository and current OpenClaw tooling for runtime introspection, plugin registration, hook registry, loaded module, process, gateway diagnostics, and fingerprints.

Do not assume command names or undocumented APIs. Only use mechanisms verified in the repository or in the current environment.

### 2. Process binding

Use the already-running Gateway identified in CNX-350 where possible. The diagnostic must establish process identity without restarting or mutating it.

### 3. Module binding

Determine whether Node/Windows/OpenClaw exposes a way to bind PID `17080` (or the currently verified Gateway PID) to the loaded CogentNexus JavaScript module. Acceptable evidence includes an exact module path/URL and content fingerprint obtained from a process-scoped source.

If no such surface exists, record the limitation explicitly.

### 4. Registration binding

Determine whether registration metadata can be observed from the live runtime, including `before_agent_run` registration, priority, owner, handler identity, and effective registry visibility.

Do not infer dynamic state from `openclaw plugins list --json` alone.

### 5. Test-only diagnostic adapter

If repository tooling can safely exercise an existing read-only introspection boundary, create a focused test-only diagnostic adapter. It must not change production behavior or expose a fabricated runtime state.

### 6. Classification

Use only:

- **D proven** — exact process-scoped evidence shows stale/different runtime artifact/module.
- **E proven** — exact static/read-only evidence shows Dashboard/WebChat can bypass `before_agent_run`.
- **UNRESOLVED** — required process-scoped observation remains unavailable.

## TDD / evidence contract

CNX-351 is evidence-only.

- A genuine RED may identify a missing diagnostic boundary, but it is not a production defect reproduction by itself.
- No production fix is authorized in this task.
- No production behavior may be changed merely to make the diagnostic test pass.

## Hard fences

- No production code changes that alter runtime semantics.
- No install/reinstall.
- No OpenClaw restart.
- No provider routing change.
- No runtime/config/database mutation.
- No UI interaction.
- No semantic Dashboard request.
- No CNX-344 replay/resend.
- No `durableAdmissionEligible` change.
- No timeout-authority change.
- No second admission owner.
- No v0.9.5 tag/history mutation.
- No force-push/history rewrite.
- No self-acceptance.

## Required final evidence

The GitHub report must contain:

1. remote branch and final HEAD;
2. parent baseline/lineage;
3. exact changed files;
4. exact commands and fresh results;
5. actual Gateway PID;
6. process-scoped module identity, if observable;
7. artifact fingerprint, if observable;
8. registration/hook evidence, if observable;
9. D/E/UNRESOLVED classification;
10. production-change declaration;
11. hard-fence declaration; and
12. smallest next probe if unresolved.

## Acceptance

CNX-351 is complete only when the above evidence is present on GitHub and independently reviewable. Absence of observability is an acceptable terminal result, but it must be demonstrated rather than guessed.