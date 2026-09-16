# CNX-20260916-370 — Live Semantic Requalification

## Task identity

- **Task ID:** CNX-20260916-370
- **Parent:** CNX-20260916-369
- **State:** `CNX370_LIVE_SEMANTIC_REQUALIFICATION`
- **Executor:** Hermes
- **Reviewer:** ChatGPT
- **Human final authority:** Operator
- **Branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Determine, with one controlled live semantic Dashboard request, whether the repaired runtime from CNX-368/CNX-369 restores the Dashboard Ticket-first admission path that CNX-367 proved was bypassed.

This task is **semantic requalification only**. It is not a source-repair task.

## Preconditions

1. Synchronize with the current remote branch before any action. GitHub state is authoritative.
2. Confirm the coordination gate authorizes this exact task.
3. Confirm the active runtime is the repaired artifact verified by CNX-369 before sending the semantic request.
4. Record the relevant runtime identity/artifact evidence before the request.

## Authorized live action

Perform **one minimum-necessary controlled Dashboard semantic request** against the already-activated runtime.

The request must be sufficient to exercise the Dashboard → Ticket-first admission path. Do not create a series of probes or retry CNX-367 verbatim unless the single controlled request is technically impossible to interpret and the task evidence explicitly requires one narrowly bounded follow-up.

## Required evidence

Capture enough fresh evidence to establish:

1. Dashboard request/session/run identity.
2. Request admission path.
3. Ticket creation/admission, including the relevant Ticket identity/state if exposed.
4. Whether `before_agent_run` is reached.
5. Ordering showing Ticket admission occurs before model execution.
6. Model/provider execution evidence only to the extent needed to establish the lifecycle ordering.
7. Comparison with CNX-367's failure signature (`prompt.submitted → model.completed` with no `before_agent_run` / Ticket-first admission evidence).
8. Relevant counters and any runtime lifecycle mutation.
9. Exact timestamps/IDs needed for independent review.

## Classification

- If the required lifecycle is proven, classify the result as a factual semantic requalification **PASS / RESTORED**.
- If the required lifecycle is not proven, classify it as **FAIL / NOT_REQUALIFIED** and stop.
- Do not infer success from model completion alone.

## Hard fences

- No source-code changes.
- No configuration redesign or controller normalization.
- No provider/auth/routing changes.
- No unrelated Dashboard/model traffic.
- No repeated CNX-367 reproduction.
- No historical edits to CNX-360 through CNX-369.
- No release/tag/main changes.
- No force-push or history rewrite.
- Do not perform repair work if the semantic requalification fails; publish the evidence and stop so a separate repair task can be framed.
- Any runtime lifecycle mutation, if genuinely required, must be explicitly recorded with exact before/after process identity and reason.

## Reporting

Publish:

`docs/operations/coordination/reports/CNX-20260916-370-live-semantic-requalification-report.md`

The report must contain the exact evidence, IDs, timestamps, artifact identity, lifecycle ordering, counters, classification, and hard-fence result.

After publishing the report, transition the durable coordination state to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not begin a follow-up repair task in the same execution.
