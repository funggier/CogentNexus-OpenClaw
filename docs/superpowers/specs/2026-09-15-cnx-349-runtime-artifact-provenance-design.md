# CNX-349 — Runtime Artifact & Effective Hook Provenance Design

**Goal:** Determine whether the OpenClaw process that exhibited CNX-344 loaded the expected CogentNexus artifact/module and whether its Dashboard execution path reaches `before_agent_run`, using read-only evidence only.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub is authoritative; local-only state is not evidence.
- Parent baseline: CNX-348 `5d02a044007ece94b66d1845ecbdf7d686678498`
- No v0.9.5 history mutation.

## Why this follows CNX-348

CNX-348 established that the repository-shaped registration path loads `v091-release-entry`, reaches exactly one `before_agent_run` registration at priority `2000`, retains it in a simulated effective registry, and invokes it successfully. That still does not prove what the already-running OpenClaw process loaded or whether the real Dashboard path reaches the hook.

## Target boundary

```text
GitHub source
  -> build/dist artifact
  -> installed plugin artifact
  -> running OpenClaw process
  -> loaded module identity
  -> actual plugin registration metadata
  -> effective hook registry
  -> Dashboard execution path
  -> before_agent_run invocation
```

## Candidate classifications

- **D:** running OpenClaw loaded a stale/different artifact or module.
- **E:** the Dashboard execution path bypasses `before_agent_run`.
- **Unresolved:** available read-only evidence cannot distinguish D/E.

## Investigation principles

1. Start from GitHub branch/commit and verify exact remote HEAD.
2. Inspect existing repository diagnostics and OpenClaw-compatible runtime introspection already present in the codebase.
3. Prefer existing read-only process/plugin metadata over introducing new runtime behavior.
4. Compare exact source/build/install identities where possible using paths, hashes, module URLs, package metadata, or already-exposed fingerprints.
5. Do not install, rebuild in-place, restart, mutate runtime configuration, or alter database state.
6. Do not send a semantic Dashboard request or modify UI state in this phase.
7. If the real running process cannot be inspected from the authorized environment, document that limitation rather than fabricating D/E evidence.

## Required evidence

The final GitHub report must include:

- remote branch and exact HEAD SHA;
- parent CNX-348 lineage;
- exact changed paths;
- exact commands and fresh test results;
- source/dist/install/runtime module identity observations;
- any existing OpenClaw plugin registration diagnostics found;
- evidence for or against D;
- evidence for or against E without live semantic/UI interaction;
- explicit unresolved state when D/E cannot be distinguished;
- confirmation that production source did not change;
- confirmation that no install/restart/provider/runtime/config/database/UI/semantic mutation occurred.

## TDD rule

This task is diagnosis only. No production repair is allowed without a reproducible RED test that identifies the boundary. A diagnostic harness may include a controlled negative test, but a synthetic negative control is not evidence that the live OpenClaw process is broken.

## Acceptance

CNX-349 may only produce one of two outcomes:

1. **D/E evidence established:** identify the first broken runtime boundary and stop for a separate repair task.
2. **D/E unresolved:** remain `BLOCKED` and recommend the next read-only evidence boundary.
