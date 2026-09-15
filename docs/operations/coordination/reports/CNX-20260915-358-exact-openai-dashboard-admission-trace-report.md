# CNX-20260915-358 — Exact OpenAI Dashboard Admission Trace Report

## Classification

**UNRESOLVED / BLOCKED**

The exact existing request is proven through supported OpenClaw records to have reached OpenAI / `gpt-5.6-luna` and returned `CNX357-DONE`. The exact Dashboard session is also present in the authoritative CogentNexus session table. However, the available read-only surfaces do not expose a `before_agent_run` dispatch/result or an admission-decision record for this run. No exact Ticket, Ticket event, Call, InferenceAttempt, AssistantDelivery, or outbox lineage exists for the request. Therefore the evidence cannot distinguish:

- `before_agent_run` never being dispatched;
- the hook being dispatched and returning before Ticket persistence;
- the hook being dispatched with a different effective configuration/runtime payload; or
- another runtime boundary bypassing the plugin.

Missing observability is not classified as a proven product defect.

## Identity

- Repository: `https://github.com/funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task starting SHA: `d75c9f4728aebae03aebfda8881afaafb1046382`
- Final SHA: recorded only after this report was committed and pushed; no self-referential pre-publication SHA is asserted here.
- Ancestry: task branch contains the CNX-357 report/task lineage and is descended from the repository's v0.9.5-era history; no `main`, tag, or history rewrite was performed.
- Reviewer: `ChatGPT`
- Human final authority: `Operator`

Exact existing request:

- Dashboard session key: `agent:main:dashboard:fffd7146-8d4b-4a1b-88dc-d9f249d98779`
- Runtime session ID: `4a027d34-4c87-4158-9afc-d08157942615`
- OpenClaw run ID: `b02dc7af-1a99-47eb-8526-c19297fffd90`
- Provider: `openai`
- Model: `gpt-5.6-luna`
- Model API: `openai-chatgpt-responses`
- Payload: `Reply exactly with CNX357-DONE.`
- Visible response: `CNX357-DONE`
- Dashboard displayed time: `Sep 15, 2026, 9:25 PM`
- Runtime prompt submitted: `2026-09-15T14:25:32.562Z` UTC (`Sep 15, 2026, 9:25:32 PM` Asia/Bangkok)
- Model completed/session ended: `2026-09-15T14:25:39.505Z` UTC (`9:25:39 PM` Asia/Bangkok)

## Runtime evidence

### OpenClaw identity and Gateway

Read-only `openclaw --version` returned:

```text
OpenClaw 2026.7.1-2 (0790d9f)
```

Read-only `openclaw status --json` returned:

- runtime version `2026.7.1-2`;
- Gateway mode `local`;
- Gateway URL `ws://127.0.0.1:18789`;
- `reachable: true`;
- Gateway service installed/loaded/managed by OpenClaw;
- Gateway runtime `running`, state `Ready`, last run result `0`;
- package root under the installed OpenClaw package path;
- no secret diagnostics exposed.

The status surface reported `missing scope: operator.read` for the optional self/operator field. That limitation is recorded, not inferred around.

### Exact session and run records

Supported local OpenClaw records were read without mutation:

`C:\Users\CDQ-P\.openclaw\agents\main\sessions\4a027d34-4c87-4158-9afc-d08157942615.jsonl`

The exact file contains:

1. Session ID `4a027d34-4c87-4158-9afc-d08157942615`.
2. One user message with exact payload and `sourceChannel: webchat`.
3. The message metadata has `senderIsOwner: true`.
4. One assistant message with text `CNX357-DONE`, provider `openai`, model `gpt-5.6-luna`, API `openai-chatgpt-responses`, and normal stop.

The corresponding trajectory:

`C:\Users\CDQ-P\.openclaw\agents\main\sessions\4a027d34-4c87-4158-9afc-d08157942615.trajectory.jsonl`

contains an exact sequence:

```text
session.started
  sessionKey=agent:main:dashboard:fffd7146-8d4b-4a1b-88dc-d9f249d98779
  sessionId=4a027d34-4c87-4158-9afc-d08157942615
  runId=b02dc7af-1a99-47eb-8526-c19297fffd90
  provider=openai
  modelId=gpt-5.6-luna
  ts=2026-09-15T14:25:32.540Z

context.compiled
prompt.submitted
  exact prompt
  ts=2026-09-15T14:25:32.562Z

model.completed
  timedOut=false
  aborted=false
  assistantTexts=[CNX357-DONE]
  ts=2026-09-15T14:25:39.505Z

session.ended
  status=success
  ts=2026-09-15T14:25:39.505Z
```

This proves the exact request reached the OpenAI runtime path and completed. It does not prove CogentNexus admission.

### CogentNexus loaded/enabled state and ownership metadata

Read-only installed configuration/status surfaces showed:

- plugin `cogentnexus-openclaw` enabled;
- `ticketFirst: true`;
- `preInferenceAdmission: true`;
- `autoWorkflowCompletion: true`;
- `enforcedMode: true`;
- `autoResume: true`;
- `providerMode: passthrough`;
- workspace `C:\Users\CDQ-P\.openclaw\workspace`;
- Host controller `cnxMode: active`;
- `providerOwnership: openclaw`;
- installed plugin package version `0.9.5` from the prior supported runtime inventory.

The current runtime ownership metadata therefore makes CogentNexus admission expected for an eligible owner message. The configuration itself is not evidence that the hook actually executed for this run.

## Source contract comparison

Installed source read-only inspection shows:

```ts
api.on("before_agent_run", ...)
```

is registered when `preInferenceAdmission !== false`.

The installed `durableAdmissionEligible` contract is:

```ts
if (!input.sessionKey || input.sessionKey.includes(":subagent:")) return false;
if (input.senderIsOwner !== false) return true;
return /^agent:[^:]+:dashboard:[^:]+$/u.test(input.sessionKey);
```

For the exact runtime values:

```text
sessionKey     = agent:main:dashboard:fffd7146-8d4b-4a1b-88dc-d9f249d98779
senderIsOwner  = true
```

that predicate would be eligible. Even if the event had carried `senderIsOwner=false`, the canonical Dashboard namespace would also be eligible under the current contract.

The source then evaluates:

```ts
if (config.ticketFirst === true && ticketIntakeEligible(event.prompt)) {
  acceptedTicket = ticketStore.accept(...)
}
```

`ticketIntakeEligible` excludes only internal context, delivery, continuation, workflow-result, resume, and prior-interruption markers. The exact prompt is not one of those exclusions. The source contract therefore provides no lawful eligibility reason for this exact prompt to bypass Ticket-first merely because it is short, direct, or from Dashboard.

The classifier would classify this short exact prompt as the direct lane, but the current source performs Ticket-first acceptance before the later durable-lane branch. Thus direct classification alone does not explain the absence of a Ticket.

## Durable evidence

Authoritative CogentNexus SQLite was opened read-only:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

Read-only integrity check:

```text
ok
```

The exact `cnx_sessions` row exists:

```text
session_key = agent:main:dashboard:fffd7146-8d4b-4a1b-88dc-d9f249d98779
state       = active
generation  = 0
session_id  = 4a027d34-4c87-4158-9afc-d08157942615
created_at  = 2026-09-15T14:24:54.330Z
updated_at  = 2026-09-15T14:24:54.330Z
```

Exact searches found no matching row/event for:

- `tickets` by the exact owner session key or exact prompt;
- `ticket_events` for an exact matching Ticket;
- `cnx_direct_model_call` for an exact matching Ticket/run;
- `cnx_inference_attempt` by the exact session key, runtime run ID, exact provider/model, or exact prompt lineage;
- `cnx_assistant_delivery` by the exact owner session key, run, or response text;
- `ticket_outbox` for an exact matching request.

The exact OpenClaw run ID `b02dc7af-1a99-47eb-8526-c19297fffd90` was not present as a durable Ticket/run lineage. No approximate timestamp-only correlation was used.

The session row is therefore a durable session identity record, not proof of Ticket admission.

## Backward trace and hypothesis results

```text
visible response                 PROVEN
  -> OpenAI provider invocation  PROVEN
  -> OpenClaw agent run          PROVEN (runId in trajectory)
  -> before_agent_run            NOT OBSERVED / NOT PROVEN
  -> CogentNexus handler         NOT OBSERVED / NOT PROVEN
  -> durableAdmissionEligible    NOT OBSERVED / NOT PROVEN
  -> Ticket-first branch         NOT OBSERVED / NOT PROVEN
  -> Ticket persistence         NOT FOUND
```

### Hypothesis A — `before_agent_run` never executed

Not proven. The exact run succeeded, but the retained trajectory has no hook-dispatch event and the Gateway/plugin logs expose no exact hook record. There is no stronger supported evidence establishing that the hook was expected to execute but did not.

### Hypothesis B — hook executed but Dashboard was judged ineligible

Not supported by the available inputs. The exact message metadata says `senderIsOwner=true`; the session is canonical Dashboard namespace; and the current source accepts both that owner bit and the canonical Dashboard fallback when the bit is false. The actual hook input/result is nevertheless not retained.

### Hypothesis C — eligible hook but Ticket-first branch not entered

Not proven. Current configuration and source contract say the exact prompt is Ticket-intake eligible and `ticketFirst` is true. No runtime decision record proves whether this branch was reached or whether persistence failed before a row/event became durable.

### Hypothesis D — Ticket created but durable correlation broken

Not supported by current exact searches. No exact Ticket, event, prompt hash, owner session key, run ID, provider/model row, or delivery lineage was found. A timestamp-only match was deliberately rejected.

### Hypothesis E — OpenAI bypassed CogentNexus entirely

Not proven. The OpenAI trajectory proves provider execution but cannot identify whether the preceding lifecycle hook ran.

## FIRST DIVERGENCE

```text
FIRST DIVERGENCE:
NOT PROVEN
```

The earliest unobserved boundary is `before_agent_run` dispatch/result. The first *missing expected durable artifact* is Ticket-first persistence, but the available evidence cannot establish whether that absence was caused by hook non-dispatch, hook failure, an unobserved runtime/config mismatch, or another boundary. The correct classification is therefore `UNRESOLVED / BLOCKED`, not `CURRENT_RED` and not `BOUNDARY_CLOSED`.

## Negative evidence

The following were searched/read but did not provide exact admission lineage:

- OpenClaw exact session JSONL: provider response present, no CogentNexus admission event.
- OpenClaw exact trajectory JSONL: lifecycle/model events present, no `before_agent_run` or plugin decision event.
- Gateway/OpenClaw logs around the request: no exact hook/admission record.
- CogentNexus runtime ledger: no exact request lineage.
- CogentNexus SQLite `tickets`, `ticket_events`, `cnx_direct_model_call`, `cnx_inference_attempt`, `cnx_assistant_delivery`, and `ticket_outbox`: no exact Ticket lineage.
- Exact payload search: no durable Ticket/event containing `Reply exactly with CNX357-DONE.`.
- Exact runtime run ID search: no durable Ticket/run/call/delivery lineage.
- Approximate timestamp-only matches: intentionally not treated as correlation.

The optional status self/operator diagnostic was unavailable because the supported status call reported `missing scope: operator.read`; no inference was made from that absence.

## Hard-fence accounting

- New semantic requests: `0`
- Retries: `0`
- CNX-344 replay: `0`
- Resend of `CNX357-DONE`: `0`
- Alternative test messages: `0`
- Provider/model configuration mutations: `0`
- Authentication/configuration mutations: `0`
- Provider installation/configuration: `0`
- Plugin enable/disable/reinstall: `0`
- Gateway lifecycle mutations: `0`
- OpenClaw source changes: `0`
- CogentNexus production source changes: `0`
- SQLite mutations: `0`
- Ticket record mutations: `0`
- Session record mutations: `0`
- Delivery-state mutations: `0`
- Credential extraction/display: `0`
- Changes to `main`: `0`
- Changes to tag `v0.9.5`: `0`
- Force-push/history rewrite: `0`

Only the required report file is changed on the task branch.

## Changed paths

Expected and authorized path only:

```text
docs/operations/coordination/reports/CNX-20260915-358-exact-openai-dashboard-admission-trace-report.md
```

No production source, OpenClaw source, provider code, configuration, database, session, or delivery file was modified.

## Repair boundary

No production repair, instrumentation, test, configuration change, provider change, or Gateway action was performed. Because `CURRENT_RED` was not proven, no successor repair is justified by this report. Further work would require an independently authorized observability or requalification task; it must not replay this request.

## Publication note

Final commit SHA, report blob, remote branch read-back, changed-path verification, and worktree state are intentionally recorded only after publication in the executor closeout, not prefilled into this report before the final commit exists.
