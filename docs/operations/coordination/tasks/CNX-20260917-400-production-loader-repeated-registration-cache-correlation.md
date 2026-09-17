# CNX-20260917-400 — Production Loader Repeated-Registration and Cache Correlation

## Purpose

Resolve the next causal boundary after CNX-399 without introducing runtime instrumentation or changing production state.

CNX-399 proved a concrete process-global loader-registry cache mechanism:

`cache hit → restore cached registry/registration state → return before discovery/createApi/register(api)`

It also established that normalized config itself is reconstructed per load-context call, while active-registry scope checks can short-circuit a later loader invocation. However, CNX-399 could not prove that the current production Gateway experienced a cache hit, used a particular cache key, or restored the registry that lacks `before_agent_run`.

The known production chronology contains plugin-side `hook-registered` events at `05:13:58.242` and `05:14:10.542`. The next question is whether these events are emitted only from actual `api.on("before_agent_run")` registration calls on the plugin side, whether they therefore imply loader misses/re-registration rather than cache hits, and whether the surrounding startup/prewarm lifecycle can be correlated to cache or active-registry behavior using only existing source and read-only telemetry.

This task is diagnosis/correlation only. It is not a production requalification task.

## Parent

`CNX-20260917-399`

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

Known expected starting HEAD after CNX-399 publication:

`accde2e0ec701e881397c19222f85c95d48b75f4`

Do not assume it remains current; verify first.

## Objective

Correlate the already-observed production repeated `hook-registered` events with exact plugin source and exact OpenClaw loader/cache lifecycle.

Determine whether the events can be used to distinguish:

1. actual `register(api)`/`api.on("before_agent_run")` execution;
2. loader cache hit restoring prior registration state;
3. active-registry short-circuit;
4. repeated loader cache miss and re-registration;
5. separate plugin-side lifecycle logging unrelated to host typed-hook acceptance.

Then determine whether the cache mechanism from CNX-399 can still plausibly explain the missing hook in the current production process, and exactly what remains unobservable.

## Required investigation

### 1. Exact plugin-side event provenance

Trace the CogentNexus source that emits the production `hook-registered` event(s).

Establish:

- exact source file and line range;
- exact function containing the log/event;
- exact call path from `register(api)` to that event;
- whether the event is emitted only when `api.on("before_agent_run")` is called;
- whether it can be emitted during any other lifecycle without host registration;
- whether one event can occur without `register(api)` having executed.

Do not infer from event name alone.

### 2. Production timestamp correlation

Use only the existing production log and previously captured read-only evidence.

Correlate:

- process creation;
- configuration loading;
- first discovery;
- first `hook-registered` event;
- server listening;
- gateway ready;
- second discovery/prewarm-labelled activity;
- second `hook-registered` event.

Do not claim causality from proximity alone.

Determine whether the source shows these timestamps could correspond to distinct loader calls, and whether a cache hit would have suppressed the plugin-side event.

### 3. Exact cache-hit implications

From CNX-399 source, trace the precise cache-hit return point and prove whether a cache hit can execute any plugin code between:

`cache lookup`
→ `cache hit`
→ `restore retained state`
→ `return`

Specifically answer whether a cache hit can emit the CogentNexus `hook-registered` event.

Also trace the active-registry short-circuit and determine whether it can emit the event.

### 4. Registration-state restoration semantics

Trace what registration side effects are retained in the cached registry state and restored on cache hit.

Determine whether a cached registry missing `before_agent_run` can remain missing after restoration, and whether a later invocation can repair it only on a cache miss / active-registry replacement.

Do not assume restore semantics; use exact source.

### 5. Production cache causality narrowing

Using only existing production data, identify what can be concluded about cache involvement.

Strong evidence examples:

- an event proven to require `register(api)` means that particular event cannot come from a pure cache hit;
- explicit cache-disabled caller invocation proves that call site did not use loader cache;
- process creation bounds the lifetime of process-global cache state;
- startup event ordering proves or disproves some lifecycle sequences when combined with exact source call order.

Weak/inadequate evidence examples:

- `plugins list --json` hookCount/hookNames;
- installed-index timestamps;
- matching timestamps without source linkage;
- event names without source tracing.

Do not claim production cache hit/miss unless directly evidenced.

### 6. Safe disposable source-only probe

A disposable probe is optional and only allowed if the exact installed module graph can be invoked without dependency patching, production global-state mutation, debugger, or permanent instrumentation.

A probe that merely calls the public loader without observing cache/registration identity is not sufficient and should not be reported as probative.

If no exact probative probe exists, explicitly record why.

## Required boundary questions

Answer precisely:

1. Does `hook-registered` require actual plugin registration/API hook call?
2. Can either loader cache hit or active-registry short-circuit produce that event?
3. Do the two production `hook-registered` events therefore prove at least two actual registration paths, or could they come from another plugin lifecycle?
4. Does this materially weaken the hypothesis that a cache hit caused the observed missing `before_agent_run`?
5. Can cache reuse still explain a later silent invocation that did not re-register the hook?
6. What exact production evidence would still be required to prove cache hit/miss or registry identity?

Do not claim historical production causality without direct evidence.

## Required classification

Use exactly one:

`PRODUCTION_CACHE_CAUSALITY_NARROWED`

`PRODUCTION_CACHE_CAUSALITY_SUPPORTED`

`PRODUCTION_CACHE_CAUSALITY_INCONCLUSIVE`

`PRODUCTION_CACHE_CAUSALITY_DIAGNOSTICALLY_BLOCKED`

Use `SUPPORTED` only if existing production evidence plus exact source linkage supports a concrete cache contribution.

Use `NARROWED` when exact source disproves/weakens a specific cache explanation for observed events but cannot establish complete production cache state.

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
- historical edits to CNX-360 through CNX-399;
- creation/start of CNX-401.

Temporary disposable isolated files are allowed only outside production state and must be removed after use.

Required counts:

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-400-production-loader-repeated-registration-cache-correlation-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- exact `hook-registered` source provenance;
- cache-hit and active-registry short-circuit source mappings;
- timestamp correlation;
- registration-state restore semantics;
- direct evidence versus inference;
- exact remaining production observability gap;
- effect on the cache hypothesis for missing `before_agent_run`;
- counts and hard-fence compliance.

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- verify local HEAD equals remote HEAD;
- verify clean worktree;
- stop;
- do not create/start CNX-401;
- do not modify historical CNX-360 through CNX-399;
- do not modify `main`, tags, or releases.
