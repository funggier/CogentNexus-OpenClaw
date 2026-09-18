# CNX-20260918-405 — Production Repeated Registration Lifecycle and Loader Caller Correlation

## Purpose

Continue from the accepted CNX-404 boundary.

CNX-404 establishes:
- exact OpenClaw 2026.7.1-2 source contains cache-hit restoration, active-registry reuse, scope short-circuit, and registry activation/replacement mechanisms;
- production PID 27372 has two plugin-side `hook-registered` events at `05:13:58.242` and `05:14:10.542`;
- no production telemetry correlates those events with loader invocation ID, cache hit/miss, cache key, registry identity, activation ordering, or host typed-hook acceptance;
- therefore cache/registry causality remains inconclusive.

CNX-403 established:
- one directly observed manifest-selected production CogentNexus root;
- no directly observed second same-ID production candidate;
- no concrete root/manifest/ID mismatch.

The next useful boundary is to determine whether the OpenClaw startup/runtime source itself explains why the same production Gateway can execute multiple plugin registration lifecycles around the observed timestamps, and which exact callers can invoke the loader or registry ensure paths in that period.

This task is diagnosis only. Production remains strictly read-only.

## Parent

CNX-20260918-404

## Branch

cnx-357-openai-dashboard-ticket-first-requalification-v2

## Executor / Reviewer

Executor: Hermes
Reviewer: ChatGPT
Human final authority: Operator

## Starting authority

Begin from authoritative GitHub HEAD and re-read:
- ACTIVE.md
- STATUS.md
- this task
- CNX-404 report
- CNX-403 report
- CNX-401 report
- CNX-400 report
- CNX-399 report

Record exact authoritative starting HEAD.

Expected current HEAD after CNX-404 review correction:
`988563fd5bb34623c00c5d4d2eba9b6f73e33168`

Verify; do not assume.

## Objective

Map the exact production-relevant OpenClaw caller/lifecycle chain that can lead to repeated CogentNexus `register(api)` execution or registry load/ensure activity.

Answer:

1. Which concrete Gateway/startup/runtime callers can reach `loadOpenClawPlugins`?
2. Which callers can reach `ensurePluginRegistryLoaded` or active-registry compatibility reuse?
3. Which caller/path corresponds, by source-defined log markers and chronology, to the first and second production `hook-registered` events?
4. Can the source explain multiple `register(api)` executions during one Gateway process without assuming duplicate filesystem roots?
5. Can any caller perform a second registry activation after the first registration?
6. Does the caller graph materially strengthen or weaken the CNX-401 cache/registry-replacement hypothesis?

Do not claim exact production caller identity unless the production log provides a direct marker sufficient to bind it.

## Required investigation

### 1. Exact source caller graph

Using exact OpenClaw 2026.7.1-2 (0790d9f) installed modules, trace call sites into:

- `loadOpenClawPlugins`
- `resolveRuntimePluginRegistry`
- `ensurePluginRegistryLoaded`
- `getCompatibleActivePluginRegistry`
- `activatePluginRegistry`
- `setActivePluginRegistry`

Include relevant:
- Gateway startup/plugin initialization
- server plugin loading
- runtime registry initialization
- middleware fallback/reload paths
- any startup prewarm/discovery callers actually present in exact source

Ignore unrelated CLI-only paths except where needed to explain why a diagnostic is not production evidence.

Record exact module hashes and line ranges.

### 2. Production chronology correlation

Read production logs only.

Use exact source-defined marker strings to correlate:
- PID 27372 creation
- config load
- first discovery
- first `hook-registered`
- server listening
- gateway ready
- second discovery/prewarm-labelled activity
- second `hook-registered`

Determine whether the source has caller-specific log markers around these timestamps.

Do not infer caller identity from timestamp adjacency alone.

### 3. Registration multiplicity

Trace whether one process can legitimately execute plugin `register(api)` more than once through:
- repeated loader invocation;
- multiple runtime scopes;
- gateway startup plus later runtime ensure;
- fallback/reload paths;
- cache miss followed by another miss;
- cache hit followed by activation;
- active-registry scope short circuit followed by a different scoped load.

Distinguish source-supported possibility from what was actually observed in PID 27372.

### 4. Registry activation lineage

Using exact source, identify every path that can call:
- `activatePluginRegistry`
- `setActivePluginRegistry`

Classify each as:
- fresh/new registry activation;
- cached registry activation;
- active-registry reuse without activation;
- cleanup/retirement.

Determine whether a caller can activate a different registry after a successful `register(api)` without another visible plugin-side registration event.

This is mechanism analysis unless production telemetry proves the actual path.

### 5. Production supported surfaces

Use only existing read-only diagnostics/status/log surfaces.

Do not:
- restart/reload;
- force plugin load;
- invoke production semantic execution;
- attach debugger;
- add instrumentation.

Record negative observability where exact source shows the relevant caller does not emit a usable production marker.

### 6. Artifact identity

Use only:
- `v091-release-entry.js`
- SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Keep the dashboard artifact:
- `v091-dashboard-verified-delivery.js`
- SHA-256 `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98`

as unselected/unproven.

## Required conclusion

Answer directly:

- Is there an exact source-defined caller graph capable of explaining repeated registration?
- Which lifecycle paths can cause fresh registration versus cached-registry activation?
- Can the two production `hook-registered` timestamps be bound to distinct lifecycle callers?
- Can one process produce both events without duplicate filesystem candidates?
- Can a later activation replace the registry after an earlier successful registration?
- Does this materially change the remaining missing-`before_agent_run` hypothesis?

Also list exact production-local evidence still unavailable.

## Required classification

Choose exactly one:

`PRODUCTION_REPEATED_REGISTRATION_CALLER_CORRELATED`
`PRODUCTION_REGISTRY_LIFECYCLE_PATH_MAPPED`
`PRODUCTION_REPEATED_REGISTRATION_PRODUCTION_UNRESOLVED`
`PRODUCTION_REPEATED_REGISTRATION_DIAGNOSTICALLY_BLOCKED`

Use:
- `CALLER_CORRELATED` only when production evidence directly binds at least one registration event to a concrete caller/lifecycle path;
- `LIFECYCLE_PATH_MAPPED` when exact source fully maps relevant paths but production caller identity remains unproven;
- `PRODUCTION_UNRESOLVED` when source mapping plus chronology still leaves the production sequence materially ambiguous;
- `DIAGNOSTICALLY_BLOCKED` only when required source/production evidence cannot be obtained under the fences.

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
- No historical edits to CNX-360 through CNX-404.
- Do not create or start CNX-406 yourself.

Required counts:
- Semantic/model/provider/Dashboard requests: 0
- Production mutations: 0

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260918-405-production-repeated-registration-caller-lifecycle-correlation-report.md`

Include:
- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- caller/lifecycle graph;
- exact source line mappings;
- production chronology and markers;
- registration multiplicity analysis;
- activation lineage;
- direct evidence versus inference;
- relation to CNX-401/403/404;
- remaining missing-`before_agent_run` evidence;
- counts and hard-fence compliance.

## Closeout

After report publication:
- set ACTIVE.md and STATUS.md to `WAITING_FOR_CHATGPT_REVIEW`;
- verify local HEAD equals remote HEAD;
- verify clean worktree;
- stop;
- do not create/start CNX-406;
- do not modify main, tags, or releases.
