# CNX-20260917-376 — Dashboard Hook Dispatch Boundary Diagnosis

## Purpose

Determine why the CNX-374 repaired `before_agent_run` hook does not produce any admission trace or Ticket-first lifecycle evidence on the Dashboard semantic path, despite the plugin definition now declaring `hooks.allowConversationAccess=true`.

## Parent

`CNX-20260917-375`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from the authoritative branch HEAD and re-read `ACTIVE.md`, `STATUS.md`, this task, and the CNX-375 report before any runtime action.

## Objective

Trace the actual runtime boundary:

`Dashboard/WebChat request`
→ `Gateway agent handler`
→ `embedded selection runner`
→ `hookRunner`
→ `before_agent_run`
→ `CogentNexus admission handler`

Determine exactly where the observed CNX-375 request diverges from the expected path.

### Required questions

1. Is the repaired `before_agent_run` handler actually present in the global/runner hook registry at runtime?
2. Does the Dashboard selection runner obtain that same registry/runner?
3. Does the Dashboard path invoke `hasHooks("before_agent_run")` and `runBeforeAgentRun(...)` for the request?
4. If the hook is invoked, what event/context reaches the CogentNexus handler?
5. If the hook is invoked and admission traces still do not appear, where does the handler return or fail before Ticket-first acceptance?
6. Is a different WebChat/Dashboard execution path bypassing the selected embedded runner hook dispatch?

## Evidence method

Use supported read-only diagnostics and static source inspection first.

Where process-local state is not directly exposed, use the narrowest supported runtime observation available. Do not add persistent instrumentation or mutate production runtime merely to obtain evidence unless a minimal instrumentation change is explicitly justified in the report.

Distinguish:

- hook registration
- hook registry membership
- runner attachment
- hook dispatch
- handler invocation
- admission decision
- Ticket persistence

Do not collapse these into one claim.

## Semantic traffic authority

**No Dashboard semantic request is authorized by default in CNX-376.**

The CNX-375 task already consumed its single semantic request. Do not send another semantic request unless a new explicit authorization is created after the dispatch boundary has been established.

## Repair authority

No source repair is authorized by default.

If and only if a concrete causal defect is proven, the report may recommend the smallest justified repair. Do not patch during diagnosis merely to probe a hypothesis.

## Hard fences

- No Dashboard semantic request by default.
- No repeated semantic traffic.
- No provider/auth/routing/model changes.
- No semantic contract changes.
- No Dashboard UI/provider-layer redesign.
- No TicketStore redesign.
- No admission redesign.
- No controller normalization.
- No speculative source patch.
- No unrelated runtime mutation.
- No release/tag/main changes.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-375.
- If the dispatch boundary remains unproven, stop and report the exact uncertainty.
- Do not start CNX-377 yourself.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-376-dashboard-hook-dispatch-boundary-diagnosis-report.md`

The report must contain:

- authoritative starting/final HEAD
- runtime identity if observed
- exact source files/line ranges examined
- hook registry lineage
- runner lineage
- evidence for registration vs dispatch vs invocation
- first proven divergence
- classification:
  - `DISPATCH_BOUNDARY_PROVEN`
  - `HANDLER_INVOCATION_PROVEN_BUT_ADMISSION_FAILS`
  - `INCONCLUSIVE`
- whether a repair is justified (normally no)
- hard-fence compliance

After publishing the report, set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop.
