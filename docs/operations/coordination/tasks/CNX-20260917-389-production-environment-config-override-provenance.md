# CNX-20260917-389 — Production Environment Config-Override Provenance

## Purpose

Resolve the remaining CNX-386/CNX-388 possibility that a User- or Machine-level environment variable, or an equivalent profile/state selector outside the explicit launch command, altered the OpenClaw configuration source used by the production gateway.

CNX-388 materially correlated the production launch chain:

`Scheduled Task → gateway.vbs → gateway.cmd → Node gateway`

with `C:\Users\CDQ-P\.openclaw\openclaw.json`, and found no explicit `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, `--config`, or profile/state override in the Task/VBS/CMD/process command line. It did not, however, reconstruct every inherited environment source available to the scheduled-task process.

CNX-389 therefore performs a strictly read-only environment-provenance check. It must not claim historical in-memory configuration consumption or hook acceptance.

## Parent

`CNX-20260917-388`

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
- CNX-388 report
- CNX-387 report
- CNX-386 report
- CNX-385 report

Record the authoritative starting HEAD in the report.

Known production baseline from CNX-388 (re-correlate; do not assume unchanged):

- Gateway PID `27372`
- OpenClaw `2026.7.1-2 (0790d9f)`
- Gateway `127.0.0.1:18789`
- Expected config `C:\Users\CDQ-P\.openclaw\openclaw.json`
- Config SHA-256 `19d7e6acf53ce370dc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`
- `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`

## Objective

Determine whether a User-level or Machine-level environment setting, Windows task environment mechanism, or directly relevant profile/state selector could materially redirect OpenClaw configuration resolution away from `C:\Users\CDQ-P\.openclaw\openclaw.json` for the production gateway.

The decisive question is:

> Does any read-only evidence outside the explicit Task/VBS/CMD command line show a materially plausible inherited environment or selector that changes the OpenClaw config/state/profile source for PID `27372`?

## Required investigation

1. Re-correlate the live gateway process:
   - PID
   - process creation time
   - command line
   - OpenClaw version
   - endpoint

2. Inspect the Windows environment sources read-only:
   - User environment variables for `CDQ-P`
   - Machine environment variables
   - specifically search for:
     - `OPENCLAW_CONFIG_PATH`
     - `OPENCLAW_STATE_DIR`
     - `OPENCLAW_PROFILE`
     - any additional OpenClaw configuration/profile selector actually supported by the installed `2026.7.1-2` code

3. Inspect the Scheduled Task principal/logon context read-only:
   - principal/user
   - logon type
   - run level
   - whether the task execution context is `CDQ-P\\CDQ-P`
   - do not modify the task

4. Determine whether User/Machine environment values are inherited in a way that could affect the scheduled task's Node process. Use only read-only OS evidence available without attaching a debugger or mutating the task/process.

5. Re-run supported OpenClaw config-path diagnostics and record:
   - CLI config path
   - service config path
   - state/config root if exposed
   - profile if exposed

6. Compare environment-source evidence with the explicit launch chain already established by CNX-388:
   `Scheduled Task → gateway.vbs → gateway.cmd → node gateway`

7. Search directly relevant environment/config selectors in the installed OpenClaw `2026.7.1-2` source or supported local diagnostics where this can be done read-only. Do not patch or alter installed dependencies.

8. Keep evidence classes separate:
   - Windows User/Machine environment evidence;
   - Scheduled Task principal/context evidence;
   - process command evidence;
   - supported OpenClaw resolver evidence;
   - installed-source evidence;
   - inference.

9. Explicitly determine whether:
   - no relevant override is found;
   - a relevant override is found and materially identifies an alternate source;
   - the evidence is diagnostically insufficient.

10. Do not claim that the production gateway's historical in-memory `hookPolicy` contained `allowConversationAccess=true` merely because no override is found.

11. Do not reopen CNX-385 normalization unless a new fact directly contradicts it.

## Important interpretation rules

- Absence of an environment variable is stronger than absence of a launcher assignment, but still does not directly observe the already-running process environment.
- User/Machine environment inspection is provenance evidence, not direct proof of historical process memory.
- Scheduled Task principal evidence must be distinguished from Node process environment reconstruction.
- Supported resolver output remains a configuration-source observation, not proof of the historical in-memory config object.
- Do not infer hook acceptance from absence of the host warning or from plugin-side `hook-registered` events.
- Do not claim Dashboard Ticket-first semantic success.

## Runtime restrictions

Production is strictly read-only.

Forbidden:

- Gateway restart/reload
- production configuration mutation
- environment-variable mutation
- scheduled-task mutation
- installed dependency mutation
- OpenClaw dependency patch
- CogentNexus source repair
- artifact deployment/rebuild
- debugger/inspector attachment
- semantic/model/provider request
- Dashboard request
- TicketStore/admission/routing/auth changes
- retry or semantic probe
- permanent instrumentation

Read-only OS environment, scheduled-task, process, supported OpenClaw diagnostics, and source inspection are authorized.

## Required classification

Use exactly one:

`PRODUCTION_CONFIG_ENVIRONMENT_OVERRIDE_NOT_FOUND`

`PRODUCTION_CONFIG_ENVIRONMENT_OVERRIDE_FOUND`

`PRODUCTION_CONFIG_ENVIRONMENT_PROVENANCE_INCONCLUSIVE`

`PRODUCTION_CONFIG_ENVIRONMENT_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-389-production-environment-config-override-provenance-report.md`

Include:

- authoritative starting/final HEAD
- live PID/process creation time/command/version/endpoint
- Scheduled Task principal/logon context
- User/Machine relevant environment values and absence/presence
- supported config/state/profile diagnostics
- directly relevant OpenClaw source evidence for environment selectors
- comparison with CNX-388 launch-chain evidence
- explicit alternate-source assessment
- direct evidence versus inference
- relationship to CNX-385 / CNX-386 / CNX-387 / CNX-388
- whether the in-memory production hook-policy gap remains
- semantic request count = 0
- production mutation count = 0
- hard-fence compliance
- remaining uncertainty

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`
- stop
- do not create/start CNX-390
- do not modify historical CNX-360 through CNX-388
- do not modify `main`, tags, or releases
