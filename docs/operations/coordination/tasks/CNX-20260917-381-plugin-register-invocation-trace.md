# CNX-20260917-381 — Plugin Register Invocation Trace

## Purpose

Determine whether the `cogentnexus-openclaw` plugin's real `register(api)` lifecycle is actually invoked in the exact OpenClaw `2026.7.1-2` isolated reproduction, and whether the `api` object used by the plugin exposes the same `api.on` / registry path assumed by CNX-376 through CNX-380.

This task moves the investigation one boundary earlier than registry composition:

`plugin load`
→ `plugin definition/register invocation`
→ `api object handed to register`
→ `api.on("before_agent_run")`
→ registry mutation

## Parent

`CNX-20260917-380`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: Hermes
Reviewer: ChatGPT
Human final authority: Operator

## Objective

Resolve whether the missing hook is caused by the plugin registration lifecycle itself rather than registry composition.

Specifically prove, using the exact installed OpenClaw module graph in a disposable isolated process:

1. the CogentNexus plugin definition is loaded;
2. its real `register(api)` function is invoked;
3. the exact `api` object received by `register` is identified;
4. `api.on("before_agent_run", ...)` is actually called;
5. the return value / side effects of `api.on` are recorded;
6. the host registry hook collection changes, if at all;
7. registration occurs before or after active registry/global-runner initialization.

## Required investigation

Use exact OpenClaw `2026.7.1-2` installation/module graph and the effective CogentNexus artifact where safely possible. Do not replace the lifecycle with a synthetic model.

Instrument only the disposable isolated process/environment.

Record:

- plugin definition identity;
- plugin `register` function entry/exit;
- `api` object identity token;
- `api.on` function identity/token;
- each `api.on("before_agent_run")` call;
- hook handler identity/token;
- registration return value;
- registry identity before and after registration;
- hook count before and after registration;
- active registry identity;
- global runner initialization timing;
- any errors, ignored returns, or conditional gates preventing registration.

Also inspect all compatibility/delegation layers between the exported plugin entry and `index.ts`, including the `v091-release-entry.ts` → legacy compatibility chain.

## Critical comparison

The task must explicitly distinguish these cases:

A. `register(api)` never invoked.
B. `register(api)` invoked, but the expected nested registration path is never reached.
C. `api.on()` invoked, but with a different/non-host API mechanism.
D. `api.on()` invoked and accepted, but registry hook count remains unchanged.
E. `api.on()` invoked and registry mutation succeeds; later boundary removes/excludes it.

Only E should send the investigation back toward composition lifecycle. A/B/C/D must be treated as registration-path findings.

## TDD

This is diagnosis-only. No production or repository repair is authorized.

A focused disposable trace assertion may be added and run locally, but temporary instrumentation must not be committed.

## Production boundary

Do not inspect by restarting or mutating the production Gateway.
Do not attach a debugger to production.
Do not send semantic traffic.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No production OpenClaw dependency patch.
- No CogentNexus source patch.
- No Dashboard semantic request.
- No model/provider request.
- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.
- No permanent instrumentation.
- No committed disposable harness/instrumentation.
- No speculative repair.
- No broad refactor.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-380.
- Do not start CNX-382 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-381-plugin-register-invocation-trace-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/plugin versions and hashes;
- isolated PID/environment identity;
- plugin definition/load evidence;
- real `register(api)` entry/exit evidence;
- API and `api.on` identity evidence;
- registration call/return evidence;
- hook counts before/after;
- lifecycle ordering relative to registry initialization;
- conclusion mapped explicitly to A/B/C/D/E above;
- whether composition remains the correct next boundary;
- production vs isolated evidence separation;
- remaining uncertainty;
- hard-fence compliance.

## Classification

Use exactly one:

- `PLUGIN_REGISTER_INVOCATION_PROVEN`
- `PLUGIN_REGISTER_PATH_FAILURE_PROVEN`
- `PLUGIN_REGISTRATION_ACCEPTED_REGISTRY_MUTATION_PROVEN`
- `PLUGIN_REGISTER_DIAGNOSTICALLY_UNRESOLVED`

Do not claim a production root cause unless the exact isolated lifecycle provides direct evidence and the report clearly separates isolated reproduction from production observation.

## Closeout

After report publication:

- update `ACTIVE.md`;
- update `STATUS.md`;
- set both to `WAITING_FOR_CHATGPT_REVIEW`;
- stop;
- do not start CNX-382.
