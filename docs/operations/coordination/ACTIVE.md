# Active Coordination Task

Status: `WAITING_FOR_CHATGPT_REVIEW`
State: `CNX398_GLOBAL_ORIGIN_ONLY_PRE_API_ELIGIBILITY`
Execution mode: `GLOBAL_ORIGIN_ONLY_PRE_API_ELIGIBILITY`
Task ID: `CNX-20260917-398`
Parent: `CNX-20260917-397`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260917-397-global-candidate-pre-api-eligibility-and-manifest-provenance-trace-report.md`
Task specification: `docs/operations/coordination/tasks/CNX-20260917-398-global-origin-only-pre-api-eligibility-ab-replay.md`

## Current position

CNX-397 is reviewed and accepted as `GLOBAL_CANDIDATE_PRODUCTION_CORRELATION_INCONCLUSIVE`. Exact OpenClaw source identifies the complete pre-API gate sequence and shows that global candidates can diverge through candidate data such as root/manifest association, scope filtering, duplicate precedence, enablement, and registration planning. Read-only production evidence is internally consistent but does not prove which historical gate, if any, blocked the running Gateway.

CNX-398 isolates candidate `origin` as the single variable in an exact disposable A/B replay. The purpose is to determine whether `origin=config` versus `origin=global` itself changes any pre-API eligibility, registration-plan, normalized-entry, or hook-policy outcome when all other candidate/config inputs are held constant.

## Current authorization

CNX-398 is READY for Hermes execution.

Use the exact installed OpenClaw `2026.7.1-2 (0790d9f)` module graph. Build a disposable isolated A/B fixture with identical plugin/root/manifest/config/ID/enablement/plan inputs and only candidate origin changed between `config` and `global`, where internal APIs permit. Capture the exact pre-API and hook-registration outcomes.

Synthetic results are mechanism evidence only. Do not use them as historical production proof.

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
- No historical edits to CNX-360 through CNX-397.
- Do not create or start CNX-399 yourself.

## Closeout

After report publication, set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not create/start CNX-399.