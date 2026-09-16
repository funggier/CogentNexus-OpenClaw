# CNX-20260916-371 — Dashboard Runner Admission Boundary Diagnosis and Minimal Repair

## Task identity

- **Task ID:** CNX-20260916-371
- **Parent:** CNX-20260916-370
- **State:** `CNX371_DASHBOARD_RUNNER_ADMISSION_BOUNDARY_REPAIR`
- **Executor:** Hermes
- **Reviewer:** ChatGPT
- **Human final authority:** Operator
- **Branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Identify the exact OpenClaw Dashboard execution boundary that allows a live Dashboard request to proceed from `prompt.submitted` directly to `model.completed` without invoking the registered CogentNexus `before_agent_run` admission hook, then implement the smallest justified repair at that boundary.

CNX-370 proved the repaired plugin artifact was active but the live Dashboard request still bypassed Ticket-first admission. The target of this task is therefore the **host runner/invocation boundary**, not another schema-v2 authority or TicketStore repair unless new evidence proves otherwise.

## Phase 1 — Diagnosis first

Synchronize with remote and read:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`
- this task
- `docs/operations/coordination/reports/CNX-20260916-370-live-semantic-requalification-report.md`
- relevant CNX-352/CNX-077/CNX-264/CNX-265 reports and reviews

Then inspect the exact OpenClaw 2026.7.1-2 host/runtime code actually used by the Dashboard surface. Establish with code and, where needed, read-only runtime evidence:

1. Dashboard request entrypoint.
2. Runner/agent execution path selected by that entrypoint.
3. Where `before_agent_run` is dispatched for that runner, if at all.
4. Whether the Dashboard path uses a distinct embedded/app-server/other runner that bypasses the normal hook dispatcher.
5. The exact first divergence between expected hook invocation and the observed `prompt.submitted → model.completed` path.
6. Whether CogentNexus plugin registration is still present at the host boundary immediately before execution.

Do not infer the runner solely from session-key shape. Use exact source/runtime evidence.

## Phase 2 — Minimal repair

Only after Phase 1 proves the concrete host-boundary cause, implement the smallest repair that restores the intended lifecycle:

`Dashboard → before_agent_run → CogentNexus admission → Ticket acceptance → model execution`

Preferred repair principles:

- Prefer an existing supported OpenClaw hook/runner integration point over invasive changes.
- Do not duplicate admission logic in the Dashboard UI or provider layer.
- Preserve the existing `durableAdmissionEligible()` owner policy.
- Preserve schema-v2 authority repair from CNX-368.
- Preserve existing TicketStore idempotency/ordering semantics.
- Fail closed if the hook cannot be established.
- Do not introduce a second competing Ticket admission path.

## Testing requirements

Add or update focused regression coverage for the exact diagnosed boundary. The test must fail before the repair and pass after it, and must prove that the Dashboard-compatible runner invokes the admission hook before model execution.

Run the applicable plugin tests, full test suite, build, and validation required by repository convention.

## Live verification boundary

After source repair and deterministic validation, use only the supported runtime activation/reload mechanism needed to make the repaired artifact active. Record exact artifact identity and process transition.

Do **not** perform another semantic Dashboard request in CNX-371 unless this task reaches the verification gate and the evidence is insufficient without one bounded proof request. If a live semantic request becomes necessary, it must be exactly one minimum-necessary controlled request and must be separately recorded in the report. Prefer handing the repaired runtime to a later requalification task when source/runtime evidence is sufficient.

## Hard fences

- No provider/auth/routing changes.
- No model/provider substitution.
- No manual controller normalization.
- No unrelated Dashboard traffic.
- No historical edits to CNX-360 through CNX-370.
- No release/tag/main changes.
- No force-push or history rewrite.
- Do not change the semantic contract merely to make the test pass.
- Do not bypass the host boundary by implementing a separate Dashboard-only Ticket path unless source evidence proves that is the supported architecture.
- Do not perform broad refactors.
- Do not claim Ticket-first restoration without lifecycle-ordering evidence.

## Reporting

Publish:

`docs/operations/coordination/reports/CNX-20260916-371-dashboard-runner-admission-boundary-repair-report.md`

Report must include:

- diagnosis with exact host/runner path;
- source references and relevant code-path evidence;
- root cause classification;
- pre/post source hashes for changed files;
- focused regression result;
- full test/build/validation results;
- installed/effective artifact identity;
- runtime lifecycle mutation evidence if activation occurred;
- semantic proof request details only if one was actually needed;
- explicit statement of which hard fences were exercised;
- remaining uncertainty, if any;
- recommended next state.

After report publication, transition coordination to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not start CNX-372 or another semantic request yourself.
