# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_LIVE_TIMEOUT_AUTHORITY_PROVENANCE_DIAGNOSTIC`
Execution mode: `READ_ONLY_RUNTIME_DIAGNOSTIC`
Task ID: `CNX-341`
Parent: `CNX-340F`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Known failing session: `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5`
Active branch: `agent/v0.9.6-live-timeout-authority-diagnostic`

## Objective

Determine why the real runtime direct-model-call lease produced `timeoutMs=900000` during CNX-340F despite the CNX-340A timeout-authority repair and the reported repaired artifact SHA. Identify the exact runtime timeout source/path that caused 900s so the next repair can be selected without guessing.

## Hard fences

- Read-only diagnostic by default.
- No new Dashboard session.
- No `New session` click.
- No semantic request.
- No additional live model call.
- No retry, resend, recovery, fallback, or manual dispatch.
- No provider/model/config/timeout/controller/database mutation.
- No installation or Gateway restart in this task.
- No production code or test changes.
- No change to `v0.9.5` or published history.
- No force push/history rewrite.
- If evidence is unavailable or contradictory, report `BLOCKED`; do not guess.

## Required investigation

1. Establish the exact plugin artifact actually loaded by the running Gateway, including installed path, exact SHA-256, version/provenance, and whether the loaded file contains the repaired resolver and handler call site.

2. Establish what can be proven about the running Gateway process/load boundary without restarting it: process identity/start time if available, plugin load evidence, artifact modification/install time if available, and the limits of any timestamp-based inference.

3. Determine the timeout values visible at the model-call resolver boundary using existing diagnostic facilities or an isolated non-production harness. Capture, where observable:
   - `event.timeoutMs`
   - `event.timeoutSeconds`
   - `ctx.timeoutMs`
   - `ctx.timeoutSeconds`
   - `api.config.agents.defaults.timeoutSeconds`
   - `api.config.models.providers.ollama.timeoutSeconds`
   - plugin/runtime config timeout fields used by the resolver
   - final resolver result

4. Reconcile the known CNX-340F live `timeoutMs=900000` with those observations and classify the narrowest proven cause:
   - `ROOT_CAUSE_PROVEN — STALE_RUNTIME_ARTIFACT`
   - `ROOT_CAUSE_PROVEN — RUNTIME_LOAD_BOUNDARY`
   - `ROOT_CAUSE_PROVEN — LIVE_TIMEOUT_INPUT_OVERRIDE`
   - `ROOT_CAUSE_PROVEN — RUNTIME_CONFIG_SHAPE`
   - `ROOT_CAUSE_PROVEN — OTHER_RUNTIME_AUTHORITY`
   - `ROOT_CAUSE_NOT_PROVEN — EVIDENCE_INSUFFICIENT`

Do not classify the runtime as stale merely because the local repository branch differs from the task branch.

## PASS

PASS only if the diagnostic identifies a concrete, evidence-backed cause for `900000` sufficient to choose the next repair/requalification action without guessing.

## BLOCKED

BLOCKED if the runtime cannot expose enough evidence to distinguish the plausible causes safely. State the minimum next evidence needed.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260914-341-live-timeout-authority-provenance-diagnostic-report.md`

The report must distinguish proven facts from hypotheses and include exact artifact hashes, runtime/load evidence, timeout input values, resolver outcome, and recommendation for the next successor task.

Stop for independent ChatGPT review. Do not self-accept CNX-341.
