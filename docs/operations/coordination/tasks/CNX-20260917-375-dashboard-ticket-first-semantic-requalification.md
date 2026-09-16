# CNX-20260917-375 — Dashboard Ticket-first Semantic Requalification

## Purpose

Verify end-to-end whether the CNX-374 registry-wiring repair restores the Dashboard `before_agent_run` path and therefore restores Ticket-first admission before model inference.

This task follows CNX-374, which proved and repaired the host conversation-hook registration gate. CNX-374 intentionally did not perform semantic Dashboard traffic; CNX-375 is the separately authorized semantic requalification step.

## Preconditions

- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260916-374`
- Base report: `docs/operations/coordination/reports/CNX-20260916-374-plugin-hook-registration-registry-wiring-report.md`
- Runtime must use the repaired `cogentnexus-openclaw` artifact whose definition exposes `hooks.allowConversationAccess=true`.
- Existing authoritative live configuration must retain `ticketFirst=true`, `preInferenceAdmission=true`, and `enforcedMode=true`.
- Do not normalize or rewrite controller/config state merely to satisfy the task.

## Exact authorization

Hermes is authorized to issue **exactly one** controlled Dashboard semantic request through the existing Dashboard path.

Use a deterministic request whose only semantic purpose is to create a traceable admission attempt. A response-content contract is not required; the decisive evidence is the runtime admission/hook/Ticket lifecycle.

Recommended request text:

`CNX-375 controlled semantic requalification request: reply exactly CNX375-SEMANTIC-ACK.`

Do not issue the request more than once. If the request is duplicated by an external mechanism, record the duplication and stop rather than retrying.

## Evidence to capture

Capture before/after runtime identity sufficiently to prove the request used the repaired process/artifact.

For the single request, capture the strongest supported evidence available for:

1. `session.started`
2. `context.compiled`
3. `prompt.submitted`
4. `before_agent_run` / `admission.trace.*` evidence, including eligibility and Ticket decision
5. Ticket acceptance/persistence/routing evidence, including Ticket ID if generated
6. explicit pre-inference block evidence
7. `model.completed` or equivalent inference evidence, only to determine whether inference occurred
8. `session.ended`

Record counts for Dashboard semantic requests, provider/model requests, retries, configuration mutation, and Gateway restart/reload.

The desired positive lifecycle is that the request reaches `before_agent_run`, is recognized as Ticket-first eligible, creates/accepts a Ticket, routes/persists it, and is blocked before ordinary model inference.

A model response without Ticket-first evidence is **not** success; it is a remaining bypass and must be reported as such.

## Runtime activation

A Gateway restart is authorized only when necessary to ensure the already-built CNX-374 artifact is loaded. No source change is authorized merely to make the request pass.

If runtime evidence shows the repaired artifact is not active, stop and report the activation discrepancy instead of performing an unrelated repair.

## Source repair boundary

No new production source repair is authorized by default.

If the single semantic request exposes a new concrete defect, Hermes must stop before changing production behavior unless the defect falls directly within the previously authorized CNX-374 repair boundary and a minimal deterministic correction is justified by evidence. Do not redesign TicketStore, admission policy, Dashboard routing, provider selection, or hook architecture inside this task.

Any repair actually performed must include:

- the exact causal evidence;
- the smallest changed surface;
- focused regression coverage;
- verification of the affected tests/build;
- a fresh report distinguishing pre-existing CNX-374 evidence from new CNX-375 evidence.

## Hard fences

- Exactly one controlled Dashboard semantic request.
- No repeated Dashboard traffic.
- No provider/auth/routing/model changes.
- No provider-selection or model-selection experiments.
- No Dashboard UI/provider-layer changes.
- No TicketStore redesign.
- No admission-policy redesign.
- No controller normalization.
- No speculative source patch.
- No broad refactor.
- No historical edits to CNX-360 through CNX-374.
- No release/tag/main changes.
- No force-push/history rewrite.
- No unrelated configuration/runtime mutation.

## Completion contract

Publish:

`docs/operations/coordination/reports/CNX-20260917-375-dashboard-ticket-first-semantic-requalification-report.md`

Then update `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`, include the final classification and evidence summary, and stop.

Do not create or start CNX-376.

## Possible classifications

- `REQUALIFIED / TICKET_FIRST_RESTORED`
  - `before_agent_run` is observed on the Dashboard path;
  - Ticket-first decision is accepted/persisted/routed;
  - pre-inference block is evidenced;
  - no ordinary model inference occurs for the controlled request.

- `FAIL / TICKET_FIRST_STILL_BYPASSED`
  - the request reaches model execution without the expected Ticket-first lifecycle.

- `INCONCLUSIVE`
  - runtime evidence is insufficient or contradictory to establish the lifecycle.

- `ACTIVATION_MISMATCH`
  - the repaired artifact cannot be proven to be the artifact serving the request.

Any classification must be evidence-backed and must not be inferred from the model's textual response alone.
