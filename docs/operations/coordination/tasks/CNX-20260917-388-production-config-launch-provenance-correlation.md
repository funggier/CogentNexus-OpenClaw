# CNX-20260917-388 — Production Config Launch Provenance Correlation

## Purpose

Resolve the remaining CNX-386 production-config provenance gap without restarting or instrumenting the live gateway.

CNX-385 proved that the normalized hook policy preserves `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true` through the host `hookPolicy` path.

CNX-386 proved that the current on-disk configuration contains the value and that supported config resolution points to that file, but could not prove the historical in-memory configuration actually used by the running gateway at plugin-registration time.

CNX-387 correlated the live gateway and registration log window but found no host-side `registerTypedHook` acceptance/rejection result.

This task therefore traces the strongest remaining non-invasive provenance chain:

`scheduled launch / gateway.cmd → process launch context → OpenClaw config path selection → config file metadata/content → gateway startup log`

The goal is not to infer an in-memory value that cannot be observed. The goal is to determine whether the production launch path materially corroborates the config file already observed, or whether an alternate profile/environment/path remains plausible.

## Parent

`CNX-20260917-387`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from the authoritative branch HEAD and re-read:

- `ACTIVE.md`
- `STATUS.md`
- this task
- CNX-387 report
- CNX-386 report
- CNX-385 report

Record the authoritative starting HEAD in the report.

Known production baseline from CNX-387 (re-correlate; do not assume unchanged):

- OpenClaw `2026.7.1-2`
- gateway endpoint `127.0.0.1:18789`
- effective CogentNexus artifact SHA:
  `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- reported gateway config path:
  `~\\.openclaw\\openclaw.json`

## Objective

Determine whether the live gateway's launch context and startup evidence materially corroborate that the expected OpenClaw config file was the configuration source selected at gateway startup.

The decisive question is:

> Is there read-only evidence tying the running gateway's actual launcher/environment and startup sequence to the same `~/.openclaw/openclaw.json` file that contains `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`, or does a materially plausible alternate config source/profile remain unresolved?

## Required investigation

1. Re-correlate the live gateway process:
   - PID
   - process creation time
   - command line
   - gateway endpoint
   - OpenClaw version

2. Inspect the actual launch chain read-only:
   - Windows Scheduled Task `\\OpenClaw Gateway` action/arguments if present
   - `C:\Users\CDQ-P\.openclaw\gateway.cmd`
   - any explicit `OPENCLAW_CONFIG_PATH` assignment in the launcher, task action, or other directly relevant launch configuration
   - any explicit `OPENCLAW_STATE_DIR` or profile/state selector that can alter config resolution

3. Determine whether the launch chain points to the same state/config directory reported by supported OpenClaw diagnostics.

4. Re-run supported read-only configuration-path diagnostics and record the exact resolved path.

5. Inspect the actual config file metadata read-only:
   - existence
   - last-write timestamp
   - SHA-256
   - relevant `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess` value

6. Correlate config-file timing to gateway process creation time. Record whether the observed file was already present and last-written before the current process started.

7. Correlate gateway startup logs for configuration-loading events:
   - startup timestamp
   - config path mention, if any
   - state/profile mention, if any
   - any diagnostic indicating an alternate config source

8. Search for evidence of multiple profiles/state directories or alternate config paths active on the machine that could plausibly have been used by the running gateway.

9. Keep the evidence classes separate:
   - launcher/task evidence;
   - process evidence;
   - supported OpenClaw resolver/CLI evidence;
   - config file metadata/content evidence;
   - startup log evidence;
   - inference.

10. Explicitly answer whether the provenance chain is:
   - materially correlated to the expected config file,
   - still ambiguous, or
   - diagnostically blocked.

11. Do not claim that the production gate received `allowConversationAccess=true` unless a direct host-side value is observed. Even a strong launch/config correlation does not by itself prove the historical in-memory `hookPolicy` argument.

12. Do not reopen CNX-385 normalization unless a new fact directly contradicts its evidence.

## Important interpretation rules

- A launcher pointing to `~/.openclaw/openclaw.json` is stronger provenance evidence, but is still distinct from observing the gateway's in-memory config object.
- A config file timestamp preceding process creation does not prove the process loaded that exact bytestring; it only removes one class of temporal mismatch.
- `openclaw gateway status` or resolver output is not by itself proof of the historical process environment.
- Absence of an alternate-path diagnostic is not proof that no alternate path existed.
- Do not infer hook registration acceptance from plugin-side `hook-registered` events.
- Do not claim Dashboard Ticket-first semantic success.

## Runtime restrictions

Production is strictly read-only.

Forbidden:

- Gateway restart/reload
- production configuration mutation
- installed dependency mutation
- OpenClaw dependency patch
- CogentNexus source repair
- artifact deployment/rebuild
- debugger/inspector attachment
- semantic/model/provider request
- Dashboard request
- TicketStore/admission/routing/auth changes
- any retry or second semantic probe

Read-only process, task, launcher, config metadata, supported diagnostics, and log inspection are authorized.

## Required classification

Use exactly one:

`PRODUCTION_CONFIG_LAUNCH_PROVENANCE_CORRELATED`

`PRODUCTION_CONFIG_LAUNCH_PROVENANCE_INCONCLUSIVE`

`PRODUCTION_CONFIG_LAUNCH_PROVENANCE_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-388-production-config-launch-provenance-correlation-report.md`

Include:

- authoritative starting/final HEAD
- live PID/process creation time/command/version/endpoint
- Scheduled Task evidence
- `gateway.cmd` evidence
- environment/profile/config-path evidence
- resolved config path
- config file SHA-256 and last-write time
- relevant `allowConversationAccess` value
- timestamp correlation between config file and process creation
- startup log configuration evidence
- alternate config/profile search result
- explicit distinction between direct evidence and inference
- relationship to CNX-385, CNX-386, and CNX-387
- whether the production in-memory hook-policy gap remains
- semantic request count = 0
- production mutation count = 0
- hard-fence compliance
- remaining uncertainty

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`
- stop
- do not create/start CNX-389
- do not modify historical CNX-360 through CNX-387
- do not modify `main`, tags, or releases
