# Coordination Channel Status

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX397_GLOBAL_CANDIDATE_PRE_API_ELIGIBILITY`
Execution mode: `GLOBAL_CANDIDATE_PRE_API_ELIGIBILITY`
Task ID: `CNX-20260917-397`
Parent: `CNX-20260917-396`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-396-global-candidate-normalized-config-provenance-trace-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-397-global-candidate-pre-api-eligibility-and-manifest-provenance-trace.md`

## Current position

CNX-396 is reviewed and accepted as `GLOBAL_CONFIG_NORMALIZATION_DIAGNOSTICALLY_BLOCKED`. Exact OpenClaw source proves that `origin=config` and `origin=global` candidates enter the same normalized configuration producer and downstream `entry?.hooks → createApi({ hookPolicy })` path. Exact global-origin A/B replay remained diagnostically blocked because reproducing the real global discovery path would require production global installation-state mutation.

The remaining causal gap is therefore earlier in the global candidate lifecycle: manifest/root association, plugin-ID derivation, scoped filtering, duplicate-ID handling, enablement, registration-plan selection, and whether the global candidate actually reaches `normalized.entries[pluginId]` before `createApi`.

## Current authorization

CNX-397 is READY for Hermes execution.

Trace the exact global candidate pre-API lifecycle and correlate the production global extension root, manifest identity, and eligibility inputs using read-only evidence. Compare the global path with an equivalent config-origin path and identify any divergence that can prevent `createApi({ hookPolicy })`.

Use exact installed OpenClaw `2026.7.1-2` source tracing plus disposable isolated probes where internal APIs permit. Treat synthetic evidence as mechanism evidence only.

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
- No historical edits to CNX-360 through CNX-396.
- Do not create or start CNX-398 yourself.

## Closeout

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not create/start CNX-398.