# CNX-20260917-399 — Global Loader Invocation and Cache Provenance Trace

## Purpose

Resolve the next causal boundary after CNX-398 without repeating the blocked origin A/B experiment.

CNX-396 proved that `origin=config` and `origin=global` enter the same normalized configuration producer and common downstream hook-policy path. CNX-397 identified the pre-API eligibility gates that can prevent a global candidate from reaching `createApi`. CNX-398 then showed that the exact paired runtime experiment cannot be injected through the supported loader API without patching OpenClaw or touching the production global-discovery/install state, so no synthetic origin A/B result was claimed.

The remaining question is whether the production Gateway's observed behavior can be explained or narrowed by **loader invocation lifetime, cache reuse, registry snapshot reuse, or repeated discovery/load cycles** before or during plugin registration. The source already shows repeated discovery/prewarm activity in the known production chronology, while supported inventory remains a separate persisted/derived projection. This task must determine whether loader-local state can persist, be reused, refreshed, or bypassed across those lifecycles in a way that could explain the missing `before_agent_run` registration.

This is a diagnosis task only. It must not turn into a production requalification attempt.

## Parent

`CNX-20260917-398`

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
- CNX-398 report
- CNX-397 report
- CNX-396 report
- CNX-395 report
- CNX-394 report
- CNX-393 report
- CNX-392 report
- CNX-391 report

Record the exact authoritative starting HEAD actually verified from GitHub.

Known expected starting HEAD after CNX-398 closeout:

`7323eb46c0c84377464994d76c3edc11eb190f46`

Do not assume this remains current; verify it first.

## Objective

Trace the exact installed OpenClaw `2026.7.1-2 (0790d9f)` loader lifecycle for any state that can survive or influence multiple plugin-load invocations.

Determine whether any of the following can cause the running Gateway to use stale, partial, prior, or independently constructed plugin state instead of rebuilding the candidate/normalized/registry path expected by the current configuration:

- loader-local caches;
- plugin load caches;
- registry snapshots or retained registries;
- discovery caches;
- manifest maps retained across invocations;
- normalized config reuse;
- activation-source config snapshots;
- candidate list reuse;
- installed-index-derived plugin records feeding loader decisions;
- duplicate load suppression;
- prewarm/re-discovery paths;
- lifecycle-specific short circuits;
- separate load invocations that use different config/profile/context inputs.

The key causal chain is:

`Gateway lifecycle`
→ `plugin load invocation`
→ `cache/load context`
→ `discovery/candidate construction`
→ `normalized config`
→ `manifest/plugin ID`
→ `registry composition`
→ `register(api)`

Identify exactly where state is created, keyed, reused, invalidated, or bypassed.

## Required investigation

### 1. Trace loader invocation entry points

Inspect the exact installed OpenClaw source and identify all relevant callers of the plugin loader used by the Gateway lifecycle.

For each call site, record:

- function and line range;
- lifecycle/stage (startup, prewarm, refresh, status, other);
- config/context object passed;
- discovery inputs passed;
- whether a fresh loader context is constructed;
- whether a cache key or singleton is involved;
- whether the result is retained for later reuse.

Do not infer call relationships from function names alone; trace actual source references.

### 2. Trace every relevant cache/context structure

Starting from known `resolvePluginLoadCacheContext` and the loader entry identified by CNX-396/397, trace all structures that can outlive one candidate loop iteration or one loader invocation.

For every such structure, determine:

- creator;
- key/identity;
- lifetime;
- invalidation condition;
- whether it contains candidates, normalized config, manifests, plugin records, or registry state;
- whether it is shared between startup and prewarm/refresh;
- whether it is process-global, invocation-local, or persisted.

Special attention:

- WeakMap/Map caches;
- memoized discovery;
- cached normalized config;
- cached activation-source config;
- registry snapshots;
- plugin load result caches;
- installed-plugin index reads.

### 3. Explain repeated production discovery chronology

Using read-only production logs already available, correlate the known events around:

- process creation;
- configuration loading;
- first discovery;
- plugin registration event(s);
- server listening/readiness;
- second discovery/prewarm event(s);
- repeated plugin-side `hook-registered` events.

Do not claim causal linkage merely because timestamps are close.

The goal is to determine whether source supports the possibility of multiple loader invocations and whether those invocations are documented by source as sharing or replacing cache/registry state.

### 4. Determine whether production can expose safe provenance

Use only supported/read-only production evidence to look for:

- loader lifecycle counters already emitted by OpenClaw;
- cache refresh timestamps;
- plugin activation/reload metadata;
- registry snapshot metadata;
- startup/prewarm diagnostics;
- persisted records that explicitly identify their producing lifecycle.

Do not add instrumentation to production.

If supported telemetry cannot expose loader-local cache state, state exactly what remains unobservable.

### 5. Disposable isolated replay where APIs permit

A disposable isolated probe is allowed only when it can use the exact installed OpenClaw module graph without patching dependencies and without touching production installation/global extension state.

Prefer a minimal probe that invokes two loader lifecycles or two relevant entry points sequentially with identical inputs and observes whether:

- a cache is reused;
- a new normalized object is created;
- a registry is reused or replaced;
- candidate discovery repeats;
- hook registration is repeated or suppressed;
- config changes are visible to the second invocation.

This is mechanism evidence only.

Do not fabricate a production-global lifecycle by relocating or mutating the production extension tree.

If the public/internal API surface does not safely permit the probe, classify the limitation rather than substituting synthetic semantics.

### 6. Installed index versus live loader state

Continue the distinction established by CNX-394/CNX-395:

- installed-index records are persisted/derived projections;
- live typed-hook registry state is process-local;
- a persisted record must not be treated as proof of a particular loader invocation.

Determine whether any source path actually feeds an installed-index record back into the live plugin loader or whether the index is only a separate inventory/projection input.

### 7. Boundary conclusion

The report must answer:

1. Can multiple Gateway loader invocations share or reuse plugin load state?
2. Can a loader invocation reuse stale normalized config or candidate/manifest state?
3. Can registry composition be retained while plugin registration is skipped on a later invocation?
4. Can production logs/index data safely distinguish those cases?
5. Does this boundary materially narrow the remaining missing-hook explanation?

Do not claim which mechanism happened in production unless direct evidence supports it.

## Required classification

Use exactly one:

`LOADER_INVOCATION_CACHE_REUSE_PROVEN`

`LOADER_INVOCATION_CACHE_REUSE_DISPROVEN`

`LOADER_INVOCATION_CACHE_EFFECT_INCONCLUSIVE`

`LOADER_INVOCATION_CACHE_DIAGNOSTICALLY_BLOCKED`

Use `PROVEN` only when exact source and/or exact isolated lifecycle evidence demonstrates a concrete reusable state that can affect this plugin-registration path.

Use `DISPROVEN` only when the relevant state is proven invocation-local/new on each relevant load path and no surviving cache can affect this boundary.

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
- historical edits to CNX-360 through CNX-398;
- creation/start of CNX-400.

Temporary disposable isolated files are allowed only outside production state and must be removed after use.

Required counts:

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-399-global-loader-invocation-cache-provenance-report.md`

Include:

- authoritative starting and final HEAD;
- exact OpenClaw/artifact/module hashes;
- loader invocation entry points and line mappings;
- cache/context structures, identity, lifetime, and invalidation;
- repeated production chronology correlation;
- installed-index/live-loader separation;
- isolated lifecycle probe, if safely possible;
- direct evidence versus inference;
- exact remaining production observability gap;
- effect on the missing `before_agent_run` registration explanation;
- required counts;
- hard-fence compliance.

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- verify local HEAD equals remote HEAD;
- verify clean worktree;
- stop;
- do not create/start CNX-400;
- do not modify historical CNX-360 through CNX-398;
- do not modify `main`, tags, or releases.
