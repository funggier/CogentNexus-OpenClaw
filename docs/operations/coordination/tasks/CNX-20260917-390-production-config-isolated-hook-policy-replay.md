# CNX-20260917-390 — Production Config Isolated Hook-Policy Replay

## Purpose

Resolve the remaining production hook-policy ambiguity by replaying the **relevant production plugin configuration** through the exact OpenClaw `2026.7.1-2` loader and the exact effective CogentNexus artifact in a disposable isolated process.

CNX-385 proved that normalized plugin configuration can preserve `hooks.allowConversationAccess=true` and that the host gate accepts the value in an exact isolated A/B/C fixture. CNX-388 materially correlated the production launch chain to `~/.openclaw/openclaw.json`. CNX-389 found no relevant User/Machine environment override. CNX-387 still found no production host-side acceptance/rejection result.

The remaining high-value question is therefore:

> When the exact production plugin-entry configuration is replayed through the exact installed OpenClaw loader and artifact in a disposable process, does `before_agent_run` reach the host gate with an accepted policy, or does the same configuration shape still produce the observed rejection?

This is an isolated reproduction task, not a production mutation or production root-cause claim.

## Parent

`CNX-20260917-389`

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
- CNX-389 report
- CNX-388 report
- CNX-387 report
- CNX-385 report
- CNX-382 report
- CNX-381 report
- CNX-380 report

Record the authoritative starting HEAD in the report.

Known artifact/module baseline:

- OpenClaw `2026.7.1-2`
- effective CogentNexus artifact SHA:
  `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- production endpoint `127.0.0.1:18789` is context only; do not connect to or mutate production

## Objective

Build a disposable isolated configuration fixture from the **relevant production plugin entry** currently stored in:

`C:\Users\CDQ-P\.openclaw\openclaw.json`

Then run the real OpenClaw loader and real effective CogentNexus artifact in an isolated process.

The replay must preserve the production values relevant to plugin registration, especially:

- plugin enabled state;
- `plugins.entries.cogentnexus-openclaw.config` relevant fields;
- `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess`;
- any plugin-entry fields the installed loader demonstrably consumes when constructing `hookPolicy` or deciding registration mode.

Do not copy or print secrets unnecessarily. If the production plugin entry contains credentials/tokens, omit secret-bearing fields unless the installed source proves they are required for the registration path. Record exactly which fields were omitted and why.

## Required investigation

1. Re-correlate the current live production artifact hash and OpenClaw version read-only.

2. Read the current production config file read-only and extract the relevant `plugins.entries.cogentnexus-openclaw` structure.

3. Inspect installed OpenClaw source as needed to determine which plugin-entry fields affect:
   - normalized entry;
   - `hookPolicy`;
   - plugin configuration validation;
   - registration mode;
   - non-bundled versus bundled hook policy.

4. Construct a disposable isolated config/workspace containing only the necessary relevant configuration. Do not mutate the production config.

5. Use the exact installed OpenClaw `2026.7.1-2` modules and the exact effective CogentNexus artifact SHA listed above.

6. Execute the real loader/plugin lifecycle in the disposable process.

7. Instrument only the disposable copy if necessary to observe:
   - `register(api)` entry;
   - `api.on("before_agent_run")` calls;
   - host policy diagnostic;
   - final typed-hook registry contents;
   - `hasHooks("before_agent_run")`.

8. Do not instrument or alter the production artifact/process.

9. Compare the replay result with CNX-381 and CNX-385:
   - Does production-shaped config cause `allowConversationAccess=true` to survive to the gate?
   - Does `before_agent_run` register successfully?
   - Does the host emit the policy rejection diagnostic?

10. Keep direct evidence and inference separate. In particular:
    - isolated success does not prove production in-memory equivalence;
    - isolated rejection with production-shaped config is stronger evidence of a configuration-shape/loader mechanism but still does not prove production memory;
    - do not relabel isolated evidence as production root cause.

11. Do not reopen launch provenance or User/Machine environment analysis unless a directly contradictory fact appears.

## Required comparison matrix

At minimum compare:

| Scenario | Config policy | Loader result | before_agent_run | Host diagnostic |
|---|---|---|---|---|
| CNX-385 known-good fixture | `true` | recorded from predecessor evidence | accepted/observable outcome | recorded |
| CNX-390 production-shaped fixture | exact production value | fresh observation | fresh observation | fresh observation |
| CNX-381 rejection fixture | effective false/absent policy | recorded from predecessor evidence | rejected | recorded |

Do not invent missing CNX-385 details; cite the exact prior report evidence used.

## Interpretation rules

- Do not claim the production process consumed the isolated fixture.
- Do not claim the isolated result is production proof.
- Do not claim Dashboard Ticket-first semantic success.
- Do not infer gate acceptance from absence of a warning alone.
- Do not infer registry composition failure if the hook never enters the final registry.
- Do not expose secrets in the report.

## Runtime restrictions

Production is strictly read-only.

Forbidden:

- production Gateway restart/reload;
- production config mutation;
- environment mutation;
- Scheduled Task mutation;
- dependency patch;
- CogentNexus source repair;
- production artifact replacement/deploy;
- debugger/inspector attachment to production;
- production semantic/model/provider/Dashboard request;
- production retry.

Disposable local instrumentation and temporary isolated files are authorized only for the isolated replay and must not be committed unless a focused regression is explicitly required to document a discovered mechanism.

## Required classification

Use exactly one:

`PRODUCTION_CONFIG_REPLAY_ACCEPTS_HOOK_POLICY`

`PRODUCTION_CONFIG_REPLAY_REJECTS_HOOK_POLICY`

`PRODUCTION_CONFIG_REPLAY_INCONCLUSIVE`

`PRODUCTION_CONFIG_REPLAY_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-390-production-config-isolated-hook-policy-replay-report.md`

Include:

- authoritative starting/final HEAD;
- production artifact/version baseline;
- relevant production config fields used and explicitly omitted secret fields;
- exact isolated config fixture provenance;
- exact loader/module identities and hashes;
- isolated PID/runtime;
- register/api.on/policy diagnostic evidence;
- final hook inventory and `hasHooks` result;
- comparison against CNX-381 and CNX-385;
- direct evidence versus inference;
- whether result narrows the remaining production in-memory gap;
- semantic request count = 0;
- production mutation count = 0;
- hard-fence compliance;
- remaining uncertainty.

## Closeout

After publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- stop;
- do not create/start CNX-391;
- do not modify historical CNX-360 through CNX-389;
- do not modify `main`, tags, or releases.
