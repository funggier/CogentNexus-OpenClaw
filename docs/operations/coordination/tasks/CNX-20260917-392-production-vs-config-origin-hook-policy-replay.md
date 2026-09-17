# CNX-20260917-392 — Production-vs-Config-Origin Hook-Policy Replay

## Purpose

Resolve the next concrete isolated discrepancy identified after CNX-391.

CNX-391 established in a disposable exact OpenClaw `2026.7.1-2` lifecycle that the relevant production plugin-entry configuration with `hooks.allowConversationAccess=true` can reach the real host registration path and produce `before_agent_run` entries in the final typed-hook registry. A false-policy control rejects the targeted hook while retaining other typed hooks.

Production, however, still reports a different plugin inventory projection:

- production: `origin=global`, `status=loaded`, `hookCount=0`;
- CNX-390 isolated config replay: `origin=config`, `status=loaded`, `activated=true`, `hookCount=0`;
- CNX-391 isolated instrumented replay: true policy accepted `before_agent_run` through the real loader/API path.

This creates a concrete remaining question that has not yet been isolated:

> Does the OpenClaw discovery/activation origin (`global` versus `config`), or an associated registration-mode difference, change the `hookPolicy` path or registration behavior for the same production plugin-entry configuration?

The task must first establish from installed OpenClaw source whether `origin` / `registrationMode` is causally relevant to `createApi(... hookPolicy ...)` or typed-hook registration. Only then should it run a minimal isolated A/B replay that preserves the exact production plugin configuration and artifact.

This is an isolated reproduction task only. It is not production-memory observation and must not be presented as direct production root-cause proof.

## Parent

`CNX-20260917-391`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from authoritative branch HEAD and re-read:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`
- this task
- CNX-391 report
- CNX-390 report
- CNX-389 report
- CNX-388 report
- CNX-387 report
- CNX-385 report
- CNX-382 report
- CNX-381 report
- CNX-380 report

Record the authoritative starting HEAD in the report.

Known baseline from predecessors:

- OpenClaw `2026.7.1-2 (0790d9f)`
- exact effective CogentNexus artifact SHA:
  `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- production config SHA:
  `19d7e6acf53ce370dc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`
- production plugin entry has `enabled=true` and `hooks.allowConversationAccess=true`
- production inventory has reported `origin=global`, `hookCount=0`
- CNX-391 true-policy isolated replay accepted `before_agent_run`

## Objective

Determine whether the production `origin=global` activation path is materially different from the CNX-391 `origin=config` isolated path in a way that can explain the `before_agent_run` discrepancy.

The investigation must separate:

1. metadata-only origin labeling;
2. registration-mode differences;
3. actual differences in `entry`, `hookPolicy`, or host typed-hook behavior.

## Required investigation

### 1. Re-correlate exact artifacts/modules

Read-only re-check:

- OpenClaw version;
- loader/registry/runtime/hook-runner module hashes;
- effective CogentNexus artifact hash.

Do not patch installed modules.

### 2. Static source trace: origin and registration mode

Inspect the exact installed OpenClaw `2026.7.1-2` source and answer:

- Where is plugin `origin` assigned (`global`, `config`, etc.)?
- Is `origin` only inventory metadata, or does it affect loader control flow?
- Where is `registrationMode` derived?
- Does `registrationMode` differ by origin?
- Does `registrationMode` affect `createApi(...)` arguments?
- Does it affect `hookPolicy` source or `registerTypedHook` policy selection?
- Does any global-plugin path skip or alter `entry?.hooks`?
- Does any config-origin path use a different registry or API construction path?

Record exact file/function/line evidence where available.

Do not infer causality merely because two fields differ.

### 3. Reproduce production-shaped config in two isolated activation modes

Build disposable isolated runs using the same:

- production plugin entry;
- exact effective artifact;
- exact OpenClaw version/modules;
- relevant config fields;
- `hooks.allowConversationAccess=true`.

Run the closest safe equivalents of:

A. `origin=config` — the existing CNX-391/CNX-390 style config-origin load.

B. `origin=global` — a disposable global/discovered extension activation path that reproduces the real loader's global-origin classification without modifying the production installation.

Do not create a persistent installation side effect. Do not modify the real global extension or production `.openclaw` tree.

If an exact global-origin reproduction cannot be constructed safely, stop before inventing a substitute and classify diagnostically blocked/inconclusive according to evidence.

### 4. Instrument the exact host boundary

Disposable instrumentation only.

Observe in both A and B, where technically exposed:

- plugin record `origin`;
- `registrationMode`;
- `entry?.hooks` at `createApi` boundary if safely observable;
- `hookPolicy` value/shape if safely observable;
- `register(api)` entry;
- `api.on("before_agent_run")` calls;
- host policy acceptance/rejection;
- exact native diagnostic;
- final typed-hook inventory;
- `hasHooks("before_agent_run")` if exposed.

Do not instrument production.

### 5. Control requirement

The comparison must hold the production plugin configuration constant. The primary variable should be loader activation origin/registration mode.

Do not change `allowConversationAccess` between A and B unless a separate control is required to validate instrumentation; any such control must be disposable and clearly separated.

### 6. Compare against CNX-381 / CNX-390 / CNX-391

Explain:

- CNX-381: exact policy rejection under false/absent effective policy;
- CNX-390: production-shaped config loaded through config-origin CLI path but diagnostic boundary blocked;
- CNX-391: production-shaped config accepted through config-origin instrumented loader/API path;
- CNX-392: whether global-origin activation changes the registration boundary for the same true policy.

## Interpretation rules

- If source shows `origin` is metadata-only and A/B behavior is identical, origin is eliminated as a causal explanation.
- If global-origin changes `registrationMode` and the mode changes the `hookPolicy` source or registration behavior, document the exact mechanism and classify accordingly.
- If global-origin cannot be reproduced safely, do not fabricate it; use the blocked/inconclusive classification.
- A production inventory label `origin=global` by itself does not prove a different hook-policy path.
- Isolated acceptance does not prove production memory acceptance.
- Absence of a diagnostic is not proof of acceptance unless the registration/storage boundary is directly observed.
- `hookCount=0` without boundary evidence is not proof of rejection.
- Do not claim registry-composition loss unless accepted host insertion is directly observed before disappearance.
- Do not claim Dashboard Ticket-first semantic success.

## Runtime restrictions

Production is strictly read-only.

Forbidden:

- production Gateway restart/reload;
- production configuration mutation;
- environment mutation;
- Scheduled Task mutation;
- production artifact replacement/deploy;
- production dependency patch;
- production source repair;
- debugger/inspector attachment to production;
- production semantic/model/provider/Dashboard request;
- production retry;
- persistent installation of a test copy into the production extension tree;
- permanent instrumentation.

Disposable isolated temporary files/copies are authorized only outside production state. Do not commit disposable instrumentation.

## Required classification

Use exactly one:

`PRODUCTION_ORIGIN_DIFFERENCE_CAUSALLY_REPRODUCED`

`PRODUCTION_ORIGIN_DIFFERENCE_ELIMINATED`

`PRODUCTION_ORIGIN_REPLAY_INCONCLUSIVE`

`PRODUCTION_ORIGIN_REPLAY_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-392-production-vs-config-origin-hook-policy-replay-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- production-vs-config origin evidence;
- exact source trace for origin/registrationMode;
- isolated A/B fixture provenance;
- isolated process/runtime information;
- `entry` / `hookPolicy` evidence if observable;
- `register(api)` / `api.on` evidence;
- host policy decision/diagnostic evidence;
- final typed-hook inventories;
- whether origin changes behavior causally;
- comparison with CNX-381 / CNX-390 / CNX-391;
- direct evidence versus inference;
- remaining production uncertainty;
- semantic/model/provider/Dashboard request count = `0`;
- production mutation count = `0`;
- hard-fence compliance.

## Closeout

After publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- stop;
- do not create/start CNX-393;
- do not modify historical CNX-360 through CNX-391;
- do not modify `main`, tags, or releases.
