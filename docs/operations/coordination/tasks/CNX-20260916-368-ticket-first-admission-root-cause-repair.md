# CNX-368 — Ticket-first admission root-cause investigation and repair

Status: `READY_FOR_HERMES`
Classification: `ROOT-CAUSE INVESTIGATION + REPAIR`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Parent evidence: `docs/operations/coordination/reports/CNX-20260916-367-openai-dashboard-ticket-first-semantic-requalification-report.md`

## Objective

Determine and repair the single root cause of the proven Dashboard Ticket-first bypass. The exact CNX-367 execution is the forensic anchor:

- Session: `agent:main:dashboard:83027933-3a42-4877-a79a-167caaa396a5`
- Run: `c3e88413-5199-4d0c-bfec-deb33e86928e`
- traceId: `7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`
- Provider/model/API: `openai` / `gpt-5.6-luna` / `openai-chatgpt-responses`
- First divergence: `prompt.submitted` → `model.completed`, with no `before_agent_run`, admission trace, Ticket, lifecycle, or Ticket-linked evidence.

This task is not authorized to rediscover the defect through another semantic request.

## A. Root-cause tracing

Trace backward from `prompt.submitted → model.completed` and determine exactly why the active OpenAI Dashboard path does not invoke the expected `before_agent_run` / Ticket-first admission boundary. Investigate, without assuming historical hypotheses:

- plugin registration;
- effective runtime hook registration;
- event dispatch;
- OpenClaw runtime integration;
- session/source eligibility;
- whether the active installed entry actually registers the hook;
- whether the hook is registered in the same Gateway process that handled CNX-367;
- compatibility or entrypoint boundaries bypassing the CogentNexus handler; and
- whether the direct OpenAI execution is outside the plugin hook path.

Stop at and document the first proven broken component boundary.

## B. Evidence preservation

Use the exact CNX-367 identifiers above as the forensic anchor. Preserve existing evidence. Do not generate another Dashboard/model request merely to rediscover the same defect. Do not mutate runtime state during diagnosis.

## C. Instrumentation first

If the failing boundary is not observable, add minimal diagnostic instrumentation before changing behavior. Instrumentation must be diagnostic only, must not log prompts, credentials, or tokens, must use safe correlated identifiers, and must prove the first failing boundary.

## D. TDD production repair

Before any production behavior change:

1. Create a focused failing regression test reproducing the missing Ticket-first admission boundary.
2. Verify and retain RED evidence.
3. Implement the smallest root-cause repair.
4. Verify GREEN.
5. Run the relevant full test/build suites.

Use one root cause and one minimal repair. No opportunistic refactor.

## Hard fences

Until root cause is proven: no production behavior change, runtime repair, reinstall, controller edit, Dashboard/model request, second semantic test, provider/auth/routing change, release/tag change, or force-push/history rewrite. Do not edit historical CNX-360 through CNX-367 task/report files.

If root cause cannot be proven, classify `UNRESOLVED/BLOCKED` and publish the evidence. If proven but unsafe to repair/test, stop with explicit diagnosis. If repaired and verified, do not run live semantic requalification in CNX-368; that needs separate authorization.

## Deliverables

Publish a report under `docs/operations/coordination/reports/` containing exact starting HEAD, CNX-367 anchor, root-cause hypothesis and evidence, proven divergence boundary, RED/GREEN evidence if repaired, changed files, runtime mutation count, Dashboard/model request count, final disposition, and the next authorization boundary.

## Stop gate

After publishing the report and verifying it from the GitHub remote at the exact final SHA, stop. No live semantic requalification is authorized by this task.
