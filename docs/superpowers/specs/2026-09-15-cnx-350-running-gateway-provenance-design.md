# CNX-350 — Running Gateway Process Provenance Design

## Status

**DESIGN APPROVED BY HUMAN OPERATOR — read-only diagnosis only; no production behavior change is authorized.**

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub branch: `cnx-350-running-gateway-provenance`
- Parent/baseline: `b1ecee8a552821872bb4e815c7ba35bd0418e541` (CNX-349)
- GitHub remote is authoritative; local-only state is not evidence.

## Problem

CNX-349 established that the installed extension is loaded according to `openclaw plugins list --json`, but the authorized probes could not bind the extension to a specific running OpenClaw gateway PID, could not expose the process-scoped loaded module identity, and could not expose the live effective hook registry. Therefore stale/different runtime artifact loading (D) and Dashboard hook bypass (E) remain unresolved.

## Objective

Obtain the smallest trustworthy, read-only evidence from the actual running OpenClaw gateway process that can establish:

1. the gateway PID;
2. the exact loaded CogentNexus module path/URL where observable;
3. the loaded artifact SHA-256 where observable;
4. plugin registration metadata and hook registration state where observable; and
5. the effective `before_agent_run` registry or an equivalent process-scoped registration diagnostic.

The design must distinguish runtime evidence from static repository/source evidence.

## Boundary model

```text
GitHub source
  -> build/dist artifact
  -> installed extension
  -> running OpenClaw gateway PID
  -> loaded module identity
  -> plugin registration metadata
  -> effective hook registry
  -> Dashboard execution boundary
```

## Investigation principles

### 1. Process-scoped proof

An artifact/path observed on disk is not proof of what a running process loaded. A plugin inventory entry is not proof of a dynamic hook registry. Every runtime claim must be tied to a real process, explicit OpenClaw runtime diagnostic, or exact OS/process evidence.

### 2. Read-only first

Use existing OpenClaw diagnostics, process inspection, module metadata, command output, file hashes, and repository tooling before writing new instrumentation.

### 3. No semantic traffic

Do not send or replay a Dashboard request. CNX-350 must remain diagnostic.

### 4. No repair

Even if D or E is established, stop at diagnosis. A production repair requires a separate task and its own RED regression test.

## Evidence classes

### D — stale/different runtime artifact

D is proven only when exact evidence demonstrates a mismatch between the GitHub-intended/build/install identity and the artifact/module actually used by the running gateway process.

Acceptable evidence includes an exact module URL/path plus SHA-256, a process-scoped module filename with an exact content fingerprint, or an equivalent authoritative runtime identity.

### E — Dashboard bypass

E is proven only when static/read-only execution-path evidence establishes that the real Dashboard/webchat request path can reach provider execution without invoking `before_agent_run`.

No live semantic request is allowed in CNX-350. A code path or runtime diagnostic must establish the bypass.

### UNRESOLVED

If neither D nor E can be proven, remain `BLOCKED` and identify the exact missing runtime observation.

## Required evidence chain

The final report must show, separately:

```text
SOURCE
  exact GitHub revision and source identity

INSTALL
  exact installed extension path/version/fingerprint

PROCESS
  exact gateway PID and process identity

MODULE
  exact loaded module identity if exposed

REGISTRATION
  registration invocation/metadata if exposed

HOOK
  effective hook registry / before_agent_run visibility if exposed

PATH
  Dashboard execution path evidence if available
```

Never collapse these into one claim such as “plugin is loaded”.

## Hard fences

- No production code changes.
- No install/reinstall.
- No OpenClaw restart.
- No provider routing change.
- No runtime/config/database mutation.
- No UI interaction.
- No semantic Dashboard request.
- No CNX-344 replay/resend.
- No change to `durableAdmissionEligible`.
- No timeout-authority change.
- No second admission owner.
- No v0.9.5 tag/history mutation.
- No force-push/history rewrite.
- No self-acceptance.

## Acceptance criteria

CNX-350 is successful only when one of these is supported by GitHub-verifiable evidence:

- **D proven** — exact running-process artifact/module mismatch established;
- **E proven** — exact execution-path bypass established; or
- **UNRESOLVED** — the environment still does not expose the required runtime boundary, with a precise next probe documented.

No production repair is part of CNX-350.
