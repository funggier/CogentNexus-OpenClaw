# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX399_GLOBAL_LOADER_INVOCATION_CACHE_PROVENANCE`
Execution mode: `GLOBAL_LOADER_INVOCATION_CACHE_PROVENANCE`
Task ID: `CNX-20260917-399`
Parent: `CNX-20260917-398`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-398-global-origin-only-pre-api-eligibility-ab-replay-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-399-global-loader-invocation-cache-provenance.md`

## Current position

CNX-398 is reviewed and accepted as `GLOBAL_ORIGIN_ONLY_PRE_API_DIAGNOSTICALLY_BLOCKED`. Exact OpenClaw source confirms `config` and `global` share the same non-bundled conversation-hook policy branch, but the supported loader API does not permit the exact origin-only runtime A/B without dependency patching or production global-discovery mutation. No synthetic A/B result was claimed.

The remaining causal question is whether repeated Gateway loader invocations, loader-local/plugin-load caches, registry snapshots, prewarm/refresh lifecycles, or retained activation state can explain why the running process lacks `before_agent_run` despite the expected production config/artifact inputs.

## Current authorization

CNX-399 is READY for Hermes execution.

Trace exact loader invocation entry points and cache/lifecycle state in installed OpenClaw `2026.7.1-2 (0790d9f)`. Determine whether plugin discovery, normalized config, plugin load state, or registry state can be reused/retained across loader invocations and whether that mechanism can affect the missing hook registration path.

Use read-only production evidence plus safe disposable exact-module probes where possible. Synthetic results are mechanism evidence only.

No production mutation is authorized.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No environment mutation.
- No Scheduled Task mutation.
- No production global extension installation/mutation.
- No production artifact replacement/deploy.
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
- No historical edits to CNX-360 through CNX-398.
- Do not create or start CNX-400 yourself.

## Closeout

After report publication, set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`, verify local/remote equality and a clean worktree, then stop. Do not create/start CNX-400.