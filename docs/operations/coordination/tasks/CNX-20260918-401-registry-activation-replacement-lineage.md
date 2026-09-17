# CNX-20260918-401 — Registry Activation and Replacement Lineage Trace

## Purpose

Resolve the next causal boundary after CNX-400 without repeating the already narrowed cache-hit explanation.

CNX-399 proved that OpenClaw has process-global plugin registry caches and active-registry reuse paths. A cache hit or compatible active-registry short circuit can skip `createApi` and `register(api)` for a later loader invocation.

CNX-400 then proved from the exact CogentNexus source that `hook-registered` is emitted from the plugin `register(api)` path after the `api.on(...)` call. Therefore a **pure OpenClaw cache hit / active-registry short circuit cannot itself generate that plugin-side event**. Production telemetry nevertheless cannot show which registry instance was active after repeated discovery/prewarm lifecycle events.

The remaining mechanism question is therefore:

> Can a later loader invocation, activation lifecycle, or cache restoration replace the active plugin registry after an earlier registration attempt, such that the registry visible to the running Gateway no longer contains the registration state established by the earlier invocation?

This is a diagnosis task only. No production mutation is authorized.

## Parent

`CNX-20260917-400`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from the authoritative branch HEAD and re-read:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`
- this task
- CNX-400 report
- CNX-399 report
- CNX-398 report
- CNX-397 report
- CNX-396 report
- CNX-395 report
- CNX-394 report
- CNX-393 report
- CNX-392 report
- CNX-391 report

Record the exact authoritative starting HEAD actually verified from GitHub.

## Objective

Trace exact installed OpenClaw `2026.7.1-2 (0790d9f)` source for all paths that create, activate, restore, replace, or retain the live plugin registry after `loadOpenClawPlugins`.

Determine whether the following sequence is mechanically possible:

`loader invocation A`
→ `register(api)` / attempted hook registration
→ `registry A activated`
→ later lifecycle or loader invocation B
→ `registry B created/restored`
→ `registry B activated/replaces active registry`
→ later Gateway behavior observes registry B instead of A

The key question is whether a registry replacement can erase or hide registration state established by an earlier invocation, including `before_agent_run`.

## Required investigation

### 1. Trace registry creation and activation

Inspect exact installed source for:

- registry constructor/creation sites;
- `activatePluginRegistry`;
- `setActivePluginRegistry` / `getActivePluginRegistry`;
- loader cache restore paths;
- loader miss paths that install a new registry;
- runtime-registry-loader activation paths;
- any registry cloning/copying/snapshotting.

For every site record:

- function + exact line range;
- source registry object identity/lifetime;
- when active registry pointer changes;
- whether replacement is unconditional or compatibility-scoped;
- whether prior registry remains reachable through cache/other state.

### 2. Trace what happens to hooks during replacement

Determine exactly whether registry activation/replacement:

- swaps the whole registry object;
- merges typed hooks;
- restores captured registration state;
- preserves handlers/providers/commands but not hooks;
- resets hook collections;
- rehydrates hooks from plugin registration;
- can produce a registry with zero `before_agent_run` after one with accepted hook state.

Do not assume object replacement means hook loss; prove the actual semantics.

### 3. Relate cache and active-registry paths

Trace the relationship between:

- cache hit restore;
- `activatePluginRegistry`;
- `getCompatibleActivePluginRegistry`;
- runtime scope short circuit;
- cache miss completion/activation.

Determine whether these paths can replace active registry in either direction:

`active → cached`
`cached → newly loaded`
`newly loaded → active`

and whether replacement can happen without `register(api)` during the replacing invocation.

### 4. Registration-state capture/restoration

Starting from the known cache capture area around `loader:2327-2339` and restore area around `loader:1509-1522`, trace the exact structure captured for registration state.

Determine whether typed hooks are part of that captured state or whether only commands/handlers/providers/memory/etc. are captured.

Then answer:

- Can a cache restore bring back an earlier missing-hook registry?
- Can it bring back an accepted-hook registry?
- Can a newly loaded registry supersede a cached registry?
- Can active-registry restoration bypass registration while changing which registry is visible to the Gateway?

### 5. Production chronology correlation — read only

Use the already-recorded production chronology:

- PID 27372 creation;
- config load;
- first discovery;
- first `hook-registered` event;
- server listening;
- Gateway ready;
- second discovery/prewarm-labelled phase;
- second `hook-registered` event.

Do not infer registry identity from timestamps alone.

Determine which source lifecycles are consistent with the chronology and exactly what remains unobservable.

### 6. Production observability boundary

Search only supported/read-only evidence for:

- active registry metadata;
- registry replacement/activation diagnostics;
- load invocation counters;
- cache hit/miss diagnostics;
- lifecycle IDs;
- registry snapshot identifiers;
- startup/prewarm loader diagnostics.

Do not add production instrumentation.

If none expose registry identity, state the exact gap.

### 7. Safe disposable probe

A probe is allowed only if exact installed APIs permit registry lifecycle observation without:

- dependency patching;
- monkey-patching OpenClaw;
- debugger/inspector;
- production installation/global state mutation.

A probe should preferably invoke two exact loader lifecycles in a disposable state and observe whether the active registry object is replaced/restored.

An uninstrumented loader call that cannot observe registry identity is not probative.

Synthetic fixtures are mechanism evidence only.

### 8. Boundary conclusion

Answer directly:

1. Can a later loader invocation replace the active registry?
2. Can registry replacement happen without a fresh `register(api)` in the replacing invocation?
3. Does replacement preserve typed-hook state or replace it?
4. Can cache restoration select a registry with different hook state?
5. Could the known repeated `hook-registered` events coexist with a later registry replacement that leaves the active registry without `before_agent_run`?
6. Which parts remain unobservable in production?
7. Does this materially narrow the remaining explanation for the missing host hook?

Do not claim that registry replacement happened in production without direct evidence.

## Required classification

Use exactly one:

`REGISTRY_REPLACEMENT_MECHANISM_PROVEN`

`REGISTRY_REPLACEMENT_MECHANISM_DISPROVEN`

`REGISTRY_REPLACEMENT_PRODUCTION_CORRELATION_INCONCLUSIVE`

`REGISTRY_REPLACEMENT_DIAGNOSTICALLY_BLOCKED`

Use `PROVEN` only when exact source proves a replacement mechanism capable of affecting this registration boundary.

Use `DISPROVEN` only when relevant activation paths are proven unable to replace/lose registry state at this boundary.

## Production and runtime hard fences

Production is strictly read-only.

Forbidden:

- Gateway restart/reload;
- production configuration mutation;
- environment mutation;
- Scheduled Task mutation;
- production global extension installation/mutation;
- artifact replacement/deploy;
- OpenClaw dependency patch;
- CogentNexus source repair;
- debugger/inspector attachment;
- semantic/model/provider/Dashboard request;
- TicketStore/admission/routing/auth changes;
- production retry;
- speculative workaround;
- permanent instrumentation;
- release/tag/main;
- force-push/history rewrite;
- historical edits to CNX-360 through CNX-400;
- creation/start of CNX-402.

Temporary disposable isolated files are allowed only outside production state and must be removed after use.

Required counts:

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260918-401-registry-activation-replacement-lineage-report.md`

Include:

- authoritative starting and final HEAD;
- exact OpenClaw/artifact/module hashes;
- registry creation/activation/replacement call graph and line mappings;
- hook-state preservation/replacement semantics;
- cache restore/active-registry relationship;
- production chronology correlation;
- production observability gap;
- isolated lifecycle probe, if safely possible;
- direct evidence versus inference;
- effect on the remaining missing `before_agent_run` explanation;
- counts and hard-fence compliance.

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- verify local HEAD equals remote HEAD;
- verify clean worktree;
- stop;
- do not create/start CNX-402;
- do not modify historical CNX-360 through CNX-400;
- do not modify `main`, tags, or releases.
