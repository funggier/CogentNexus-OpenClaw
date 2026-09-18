# CNX-20260918-404 — Production Loader Cache and Active-Registry Correlation Diagnosis

## Purpose

Continue from the accepted CNX-403 discovery-root review.

CNX-403 materially narrows the duplicate-root hypothesis:
- one directly observed manifest-selected CogentNexus production root;
- no directly observed second same-ID production candidate;
- corrected selected artifact remains `v091-release-entry.js` / SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`;
- duplicate precedence is source-proven as a mechanism but not observed in PID 27372.

CNX-401 remains separately relevant:
- exact OpenClaw source proves active-registry replacement;
- cache-hit restoration can activate a retained registry without fresh `register(api)`;
- activation swaps the complete registry object and does not merge `typedHooks`;
- production occurrence remains unproven.

This task diagnoses whether existing production read-only observability can correlate PID 27372 with loader cache decisions, active-registry activation/replacement, or registry lifecycle markers. It is diagnosis only and production is strictly read-only.

## Parent

CNX-20260918-403

## Branch

cnx-357-openai-dashboard-ticket-first-requalification-v2

## Executor / Reviewer

Executor: Hermes
Reviewer: ChatGPT
Human final authority: Operator

## Starting authority

Begin from the authoritative branch HEAD and re-read:
- ACTIVE.md
- STATUS.md
- this task
- CNX-403 report
- CNX-401 report
- CNX-400 report
- CNX-399 report
- CNX-398 through CNX-391 reports as needed for exact runtime semantics.

Record exact authoritative starting HEAD from GitHub and verify it before investigation.

Known expected starting HEAD after CNX-403 publication:
`2f9c3b584476b9f8de581d4df0c4d7dbec474404`

## Objective

Determine whether production PID 27372 exposes any existing, non-invasive evidence that can distinguish:

1. loader cache hit;
2. loader cache miss;
3. active-registry compatibility/scope short circuit;
4. new-registry activation;
5. cached-registry activation;
6. registry replacement/retirement;
7. repeated loader lifecycle calls.

The objective is production correlation, not source-mechanism re-proof.

## Required investigation

### 1. Exact source observability map

Using exact OpenClaw 2026.7.1-2 (0790d9f) installed modules, inspect the already-established loader/runtime paths and identify every existing log, diagnostic, metric, trace, or supported status output around:

- `loadOpenClawPlugins`
- cache-key construction
- cache hit/miss decision
- cached registry restore
- `activatePluginRegistry`
- `setActivePluginRegistry`
- active-registry compatibility reuse
- `ensurePluginRegistryLoaded`
- registry retirement/clear
- plugin register/API hook registration

Record module hashes and exact line mappings for any relevant built-in observability.

Do not add instrumentation.

### 2. Production log correlation

Read the production OpenClaw log only.

Correlate:
- PID 27372 startup;
- config load;
- discovery activity;
- both known CogentNexus `hook-registered` events;
- server listening/ready;
- later discovery/prewarm-labelled activity;
- any loader/cache/registry/activation messages before, between, or after those events.

Search the relevant runtime window first. Expand only when exact source-defined marker terms justify it.

For every candidate marker record timestamp and exact message. Do not treat timestamp proximity as identity proof.

### 3. Supported diagnostic surfaces

Use only already-supported read-only diagnostics that do not restart/reload or trigger a production semantic request.

Determine whether any existing command/output can expose:
- loader invocation count or identifier;
- cache hit/miss;
- cache key/fingerprint;
- active registry identity/version/key;
- activation/replacement;
- typed-hook registry count/name;
- `createApi` reachability;
- plugin registration outcome.

A negative result is useful evidence when the inspected command/source surface is explicitly documented by exact source.

Do not run a diagnostic that intentionally forces a fresh production plugin load or registration.

### 4. Process/environment provenance

Read-only inspection may correlate PID 27372 with:
- executable/command line;
- relevant existing environment selectors;
- runtime version;
- current log path;
- current supported plugin/status projection.

Do not modify environment, Scheduled Task, config, or process state.

Do not inspect arbitrary unrelated process memory or private object state.

### 5. Correlate with CNX-401 mechanism

Answer whether the production evidence can distinguish any of these sequences:

```
register(api) -> registry A -> activate A
                         -> later cache/registry event -> activate B
```

or:

```
cache hit -> activate retained B -> no register(api)
```

or:

```
active-registry short circuit -> no loader/register
```

Do not claim that any sequence occurred unless a production-local observation identifies it.

### 6. Production artifact identity

Use only the corrected production identity:

- `v091-release-entry.js`
- SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Keep `v091-dashboard-verified-delivery.js` / `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98` as an alternate unselected artifact unless direct evidence proves otherwise.

### 7. Optional isolated mechanism probe

Do not patch or monkey-patch OpenClaw and do not touch production.

An isolated probe is optional only when the public surface can demonstrate an already-existing diagnostic marker without instrumentation. Do not manufacture production identities or claim a fixture as production evidence.

## Required conclusion

Answer directly:

- Does the installed OpenClaw build emit any built-in cache/registry lifecycle evidence that can be correlated to PID 27372?
- Is a production cache hit, cache miss, active-registry reuse, or registry replacement directly observed?
- Can either known `hook-registered` event be correlated to a specific registry identity or activation?
- Is the final production missing `before_agent_run` state causally attributable to registry replacement/cache restoration from available evidence?
- What exact production-local evidence remains unavailable?
- Does this materially narrow the remaining explanation compared with CNX-401/CNX-403?

## Required classification

Choose exactly one:

`PRODUCTION_REGISTRY_CACHE_CORRELATION_PROVEN`
`PRODUCTION_REGISTRY_ACTIVATION_CORRELATION_PROVEN`
`PRODUCTION_REGISTRY_CACHE_OBSERVABILITY_NEGATIVE`
`PRODUCTION_REGISTRY_CACHE_CORRELATION_INCONCLUSIVE`
`PRODUCTION_REGISTRY_CACHE_DIAGNOSTICALLY_BLOCKED`

Use:
- `CORRELATION_PROVEN` only for direct PID-correlated production evidence of the relevant cache/registry event;
- `ACTIVATION_CORRELATION_PROVEN` only for direct production evidence of registry activation/replacement and its ordering;
- `OBSERVABILITY_NEGATIVE` only when exact source plus supported surfaces establish that the relevant markers/state are not exposed;
- `INCONCLUSIVE` when some read-only evidence exists but cannot establish causal identity;
- `DIAGNOSTICALLY_BLOCKED` only when the required evidence cannot be obtained under the explicit fences and no stronger negative conclusion is justified.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No environment mutation.
- No Scheduled Task mutation.
- No production global extension installation/mutation.
- No production artifact replacement/deploy/rename/copy-over.
- No OpenClaw dependency patch.
- No CogentNexus source repair.
- No debugger/inspector attachment.
- No semantic/model/provider/Dashboard request.
- No TicketStore/admission/routing/auth changes.
- No production retry.
- No speculative workaround.
- No permanent instrumentation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-403.
- Do not create or start CNX-405 yourself.

Required counts:
- Semantic/model/provider/Dashboard requests: 0
- Production mutations: 0

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260918-404-production-loader-cache-registry-correlation-report.md`

Include:
- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- exact source observability map;
- production log evidence with timestamps;
- supported diagnostic outputs and negative findings;
- PID/process provenance;
- cache/registry correlation result;
- relation to CNX-401 and CNX-403;
- direct evidence versus inference;
- missing `before_agent_run` impact;
- counts and hard-fence compliance.

## Closeout

After report publication:
- set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`;
- verify local HEAD equals remote HEAD;
- verify clean worktree;
- stop;
- do not create/start CNX-405;
- do not modify main, tags, or releases.
