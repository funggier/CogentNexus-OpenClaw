# CNX-20260917-391 — Isolated Production-Config Hook Registration Trace

## Purpose

Resolve the CNX-390 diagnostic boundary by replaying the relevant production plugin configuration through the **real OpenClaw `2026.7.1-2` loader at the loader/API boundary**, while using only a disposable isolated process and disposable instrumentation.

CNX-390 established that:

- the production-shaped plugin entry can be loaded and activated by the real OpenClaw CLI;
- the exact effective CogentNexus artifact is the same artifact used in the prior isolated traces;
- the supported CLI inventory reports `hookCount=0`;
- the supported CLI does not expose `register(api)`, `api.on("before_agent_run")`, the host `registerTypedHook` decision, typed-hook inventory, or `hasHooks`.

CNX-381 established in a disposable instrumented run that the exact real loader/API path can expose `api.on("before_agent_run")` calls and the native non-bundled policy diagnostic when the effective hook policy is not true.

The remaining high-value question is therefore:

> With the **relevant production plugin-entry configuration**, does the exact real loader/API path invoke `before_agent_run` registration and does the host `registerTypedHook` gate accept or reject it?

This task is strictly an isolated reproduction. It must not be presented as direct observation of production memory or as a production root-cause proof.

## Parent

`CNX-20260917-390`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from authoritative branch HEAD and re-read:

- `ACTIVE.md`
- `STATUS.md`
- this task
- CNX-390 report
- CNX-389 report
- CNX-388 report
- CNX-387 report
- CNX-385 report
- CNX-382 report
- CNX-381 report
- CNX-380 report

Record authoritative starting HEAD in the report.

Known baseline:

- OpenClaw `2026.7.1-2 (0790d9f)`
- exact effective artifact SHA:
  `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- production config SHA observed by CNX-388/389:
  `19d7e6acf53ce370dc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`
- production hook policy value:
  `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`

## Objective

Construct a disposable isolated config from the relevant production plugin entry and execute the real installed OpenClaw loader/plugin lifecycle **without using the production Gateway**.

Instrument only a disposable copy/process enough to observe the registration boundary:

`register(api)`
→ `api.on("before_agent_run")`
→ host `registerTypedHook`
→ policy decision
→ final typed-hook registry / `hasHooks`

The decisive output must distinguish:

- hook registration accepted by host policy;
- hook registration rejected by host policy;
- registration path not reached;
- or diagnostic boundary still blocked.

## Required investigation

### 1. Re-correlate exact installed baseline

Verify read-only:

- OpenClaw version;
- exact installed module hashes relevant to loader/registry;
- exact effective CogentNexus artifact hash.

Do not assume hashes from predecessor reports without re-checking.

### 2. Extract production-shaped plugin entry

Read only:

`C:\Users\CDQ-P\.openclaw\openclaw.json`

Use the relevant:

`plugins.entries.cogentnexus-openclaw`

Preserve only fields demonstrated by installed source to affect plugin activation, normalized entry, `pluginConfig`, `hookPolicy`, registration mode, or `preInferenceAdmission`.

Do not copy secrets unnecessarily.

If secret-bearing fields are omitted, report only the field category and reason for omission; never print values.

### 3. Build disposable isolated fixture

Use a temporary config/state/workspace outside the production state directory.

The production config must not be modified.

The production Gateway must not be contacted.

### 4. Use real loader/API path

Do not replace the loader or registry with a synthetic model.

Use the installed OpenClaw `loadOpenClawPlugins` / equivalent real plugin-load path already proven in CNX-381.

Use the exact effective CogentNexus artifact.

### 5. Disposable instrumentation

Instrumentation may be applied only to a disposable copy of the plugin artifact or an isolated API delegate.

Observe, as applicable:

- `register(api)` entry;
- the exact `api.on("before_agent_run")` call(s);
- return value / throw status;
- host `registerTypedHook` path;
- policy input if safely observable;
- exact native policy diagnostic;
- final typed-hook inventory;
- `hasHooks("before_agent_run")`;
- other typed hooks accepted in the same run.

Do not instrument or attach to the production process.

### 6. Control comparison

Where practical, run a minimal pair in isolated space:

A. production-shaped entry with `hooks.allowConversationAccess=true`;

B. same fixture with the hook policy removed/false, using a disposable copy only.

The control run exists to establish that the observed instrumentation distinguishes accept from reject. Do not alter production state to create the control.

### 7. Compare with CNX-381 / CNX-385 / CNX-390

Explicitly explain:

- CNX-381: exact isolated policy-rejection path;
- CNX-385: known-good true-policy fixture;
- CNX-390: production-shaped CLI replay where supported inventory did not expose the gate;
- CNX-391: loader-level instrumented result.

Do not relabel isolated evidence as production memory evidence.

## Interpretation rules

- If true-policy production-shaped fixture reaches `registerTypedHook` and is accepted, classify the isolated replay as accepted; this still does not prove production in-memory acceptance.
- If true-policy production-shaped fixture reaches `registerTypedHook` and is rejected, classify the isolated replay as rejected and document the exact policy path; this narrows the mechanism substantially but still does not prove production memory.
- If the host boundary remains unobservable even with disposable instrumentation, classify diagnostically blocked.
- Absence of a warning without observing the gate is not proof of acceptance.
- `hookCount=0` without registration-boundary evidence is not proof of rejection.
- Do not claim registry composition loss unless `before_agent_run` is directly observed entering the host registry before disappearing.
- Do not claim Dashboard Ticket-first semantic success.

## Runtime restrictions

Production is strictly read-only and must remain untouched.

Forbidden:

- production Gateway restart/reload;
- production config mutation;
- environment mutation;
- Scheduled Task mutation;
- production artifact replacement/deploy;
- production dependency patch;
- production source repair;
- production debugger/inspector attachment;
- production semantic/model/provider/Dashboard request;
- retries against production;
- permanent instrumentation.

Disposable temporary instrumentation is allowed only outside production and must not be committed unless a narrowly scoped regression is explicitly required to preserve a proven mechanism.

## Required classification

Use exactly one:

`PRODUCTION_CONFIG_REPLAY_ACCEPTS_HOOK_POLICY`

`PRODUCTION_CONFIG_REPLAY_REJECTS_HOOK_POLICY`

`PRODUCTION_CONFIG_REPLAY_INCONCLUSIVE`

`PRODUCTION_CONFIG_REPLAY_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-391-isolated-production-config-hook-registration-trace-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- production config fixture provenance;
- secret categories omitted, if any;
- isolated PID/runtime if available;
- `register(api)` evidence;
- `api.on("before_agent_run")` evidence;
- host `registerTypedHook` evidence;
- policy input/decision evidence if observable;
- native diagnostic if emitted;
- final typed-hook inventory and `hasHooks` if observable;
- control comparison, if run;
- comparison with CNX-381, CNX-385, CNX-390;
- direct evidence versus inference;
- exact remaining production uncertainty;
- semantic request count = `0`;
- production mutation count = `0`;
- hard-fence compliance.

## Closeout

After publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- stop;
- do not create/start CNX-392;
- do not modify historical CNX-360 through CNX-390;
- do not modify `main`, tags, or releases.
