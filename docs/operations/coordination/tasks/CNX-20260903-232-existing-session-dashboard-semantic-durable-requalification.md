# CNX-20260903-232 — Existing-Session Dashboard Semantic/Durable Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-03 ICT
Parent: `CNX-20260903-231`
Repair parent: `CNX-20260902-226`
Installer-requalification parent: `CNX-20260902-230`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Complete the Dashboard-origin semantic/durable acceptance that Task 231 did not actually execute.

Task 231 consumed **zero** Dashboard semantic submissions. Its stop was caused by an incorrect executor-side assumption that a Discord-associated Dashboard session was ineligible. Current authority explicitly rejects that assumption.

Use the existing Dashboard session associated with Discord channel `1531199905673252946` directly and prove:

```text
one Dashboard-origin human submission
-> one Ticket lineage
-> one OpenClaw session/run lineage
-> one Ollama/model-call lineage
-> one durable semantic/result lineage
-> one logical Dashboard assistant result
-> zero Discord replies attributable to this Dashboard-origin turn
```

## Parent review authority

Task-231 independent review:

`docs/operations/coordination/reviews/CNX-20260903-231-post-repair-managed-dashboard-semantic-durable-requalification-review.md`

Accepted review verdict:

`REJECT_PRODUCT_FAILURE_CLASSIFICATION__ACCEPT_FAIL_CLOSED_PRESERVATION__SEMANTIC_BUDGET_UNCONSUMED__EXISTING_SESSION_REEXECUTION_AUTHORIZED`

Accepted repaired source:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Exact Dashboard session authority

The following Dashboard session is **eligible and intended** for this task even though its session key is Discord-associated and it contains existing conversation history:

```text
http://127.0.0.1:18789/chat?session=agent%3Amain%3Adiscord%3Achannel%3A1531199905673252946
```

Equivalent session key:

```text
agent:main:discord:channel:1531199905673252946
```

### Hard interpretation rule

Existing Discord association or prior conversation history is **not** a reason to create a new session.

`New session` must not be clicked during Task 232.

Do not spend retry budget trying to create a fresh/empty Dashboard session.

## Exact semantic submission

Use exactly this Dashboard-origin human message once, with **no `@Ce` prefix and no added text**:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

Dashboard semantic submission budget:

`1 maximum`

Task-231 report states this exact message was left as an unsent draft. Fresh UI evidence wins:

- if the exact draft is still present, **do not retype, append, prepend, or alter it**; use that exact draft;
- if the composer is empty, enter the exact message once;
- if the composer contains materially different text, do not Send; fail closed as `BLOCKED_DASHBOARD_COMPOSER_DRIFT` and report the observed text/state.

## One-shot Send boundary

The Dashboard `Send message` control may be activated at most **once**.

Immediately when the single Send activation is issued, or if a new semantic lineage is observed before the UI activation can be conclusively observed, set:

`SEMANTIC_RETRY_GATE=CLOSED`

Once closed, the gate cannot reopen during Task 232.

A delayed UI update, observer timeout, ambiguous click acknowledgement, slow Ollama response, or missing immediate evidence is **never** permission to click Send again.

## Routing invariant

Normal behavior for this environment is:

```text
Dashboard-origin turn -> Dashboard result
Discord-origin turn   -> Discord result
```

Therefore Task 232 requires:

```text
Dashboard-origin human submission: 1
logical Dashboard assistant result: 1
product/runtime Discord replies attributable to Task-232 Dashboard turn: 0
operator Discord/API Sends: 0
```

Discord channel `1531199905673252946` is read-only negative-control evidence only.

A conclusively attributable Discord reply from this Dashboard-origin turn is failure:

`FAIL_UNEXPECTED_DISCORD_CROSS_SURFACE_DELIVERY`

## Retry policy

The user's bounded tooling-retry policy remains active only for **read-only evidence collection and harmless UI observation before Send**.

Authorized:

- up to 2 additional attempts per logical read-only probe/observation;
- only when the failure is tooling/transport/query/evidence-collection related;
- each retry must change a material method or address the observed failure;
- record every retry in the attempt ledger.

Not retryable:

- Dashboard Send activation;
- semantic submission;
- Ticket creation;
- model invocation;
- durable result generation;
- Dashboard response generation;
- Discord/product semantic effect;
- lifecycle mutation.

Required final retry classification:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

## Hard fences

Authorized:

- fresh GitHub/Actions/source/coordination reads;
- read-only controller/startup/Supervisor/Gateway/Ollama/plugin/ownership checks;
- read-only Delivery/Recovery and SQLite inspection;
- read-only process/log/session/run/Ticket/event/outbox/recovery evidence collection;
- read-only Dashboard and Discord observation;
- use of the existing eligible Dashboard session above;
- exactly one Dashboard Send activation for the exact authorized message;
- passive observation after Send;
- bounded read-only tooling retries;
- coordination report publication.

Not authorized:

- clicking `New session`;
- second Dashboard Send activation;
- second Dashboard semantic submission;
- Discord-origin test message;
- direct operator Discord/API Send;
- manual Ticket/event/outbox/recovery/SQLite writes;
- manual recovery replay/resend;
- `cnxclaw` enable/disable/start/stop/restart/reset/uninstall;
- Gateway restart;
- installer execution;
- OpenClaw plugin install/enable/disable/uninstall;
- provider/model substitution;
- process termination;
- stale Task-223 transaction/inventory/backup cleanup/finalization/edit/move/delete;
- product/source/test/workflow edits;
- Release/tag/asset mutation;
- force push/history rewrite.

## Phase A — fresh repository authority

Before UI semantic activity:

1. fetch fresh branch HEAD;
2. verify Task 232 is active and `READY_FOR_HERMES`;
3. verify accepted repair `9a8510f...` remains an ancestor;
4. compare accepted repair -> HEAD and require no unexpected product/source/test/workflow drift;
5. verify public `v0.9.3` unchanged;
6. verify Task-231 report-head CI remains successful;
7. verify no newer coordination authority supersedes Task 232.

Unexpected drift:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase B — fresh managed-runtime preflight

Capture read-only evidence for:

```text
controller mode + generation
startup policy / startup adapter / LastTaskResult
Supervisor/doctor health
AGENTS managed-policy state
plugin id/version/path/enabled/status/fingerprint
live repaired namespace_ownership.py identity
ownership manifest verification
Gateway health
provider and selected Ollama model health
Delivery readiness + pending ticket_outbox
Recovery readiness + emittable recovery state
SQLite integrity + counts/max IDs
relevant nonterminal Tickets/session/run/model residue
relevant product processes
historical Task-223 evidence identities
```

Require coherent managed state, exact plugin fingerprint, Delivery READY with pending=0, Recovery READY, and SQLite integrity `ok`.

Material drift:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase C — no-lineage / contamination gate

Prove before Send:

- Task-231 created no semantic lineage;
- no competing nonterminal acceptance Ticket/session/run exists;
- no pending outbox entry can emit into the Dashboard session;
- no emittable recovery state can create a competing Dashboard result;
- Dashboard session key remains the intended `agent:main:discord:channel:1531199905673252946`.

Do not manually clean conflicts.

Failure:

`BLOCKED_DELIVERY_HAZARD`

## Phase D — establish exact pre-turn baselines

Persist read-only baselines for at least:

- SQLite integrity;
- Ticket count/status/max/newest identity;
- Ticket-event count/max identity;
- relevant Evidence/Decision/PluginLane fields and maxima;
- `ticket_outbox` count/pending identities;
- recovery state;
- OpenClaw session/run baseline for the intended Dashboard session;
- model/Ollama call/log baseline;
- Dashboard user/assistant visible history baseline;
- Discord channel observable baseline as negative control.

Existing history is expected and must not be treated as contamination merely because it exists. Correlate by pre/post IDs and timestamps.

## Phase E — verify composer and submit once

Freshly inspect the current Dashboard composer.

Allowed cases:

### Case 1 — exact Task-231 draft remains

If composer text equals exactly:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

then do not modify it.

### Case 2 — composer empty

Enter exactly the authorized message once, then verify exact text before Send.

### Case 3 — unexpected composer contents

Do not Send. Stop:

`BLOCKED_DASHBOARD_COMPOSER_DRIFT`

### Send

Activate `Send message` exactly once.

Immediately record:

`SEMANTIC_RETRY_GATE=CLOSED`

No second Send under any circumstance.

## Phase F — passive semantic lineage observation

After the one Send, observe passively/read-only until terminal/settled or until a reasonable bounded observation horizon is exhausted.

Prove exactly one attributable:

```text
new Ticket lineage
new OpenClaw session/run lineage
new Ollama/model-call lineage
new durable semantic/result lineage
new logical Dashboard assistant result
```

Also prove:

```text
Dashboard human submissions: 1
Discord replies attributable to this Dashboard turn: 0
operator Discord/API Sends: 0
semantic resubmissions: 0
recovery replay/resend: 0
```

Do not infer cardinality from UI alone when stronger durable IDs/events exist.

## Phase G — payload/provenance proof

Inspect durable semantic provenance and prove the current-schema equivalent of:

```text
source = openclaw
payload_source = channel_payload
payload_author_kind = human
subject derived from exact user message
body derived conservatively from distinct body candidate or no-body fallback
```

No `@Ce` prefix may appear unless the underlying system itself stores unrelated channel metadata in a field explicitly not treated as human semantic content. Human semantic subject/body/notes must reflect the exact Dashboard text without invented control tokens.

Failure:

- missing durable trace: `FAIL_DURABLE_SEMANTIC_TRACE`
- bad human provenance/semantic extraction: `FAIL_PAYLOAD_PROVENANCE`

## Phase H — Ollama lineage proof

Prove the attributable turn used configured Ollama provider/model and no fallback/provider substitution occurred.

Require exactly one attributable model-call lineage when the evidence surface exposes exact cardinality.

Failure:

`FAIL_OLLAMA_LINEAGE`

## Phase I — Dashboard result / Discord negative-control proof

Require exactly one logical Dashboard assistant result attributable to the one Dashboard-origin turn.

Failure cases:

- zero Dashboard result: `FAIL_DASHBOARD_NO_RESULT`
- more than one logical Dashboard result for same lineage: `FAIL_DASHBOARD_DUPLICATE_RESULT`
- attributable Discord product reply: `FAIL_UNEXPECTED_DISCORD_CROSS_SURFACE_DELIVERY`

Discord negative control must remain observation-only.

## Phase J — post-turn health

After settled evidence, require:

```text
controller coherent managed state
startup adapter healthy
Supervisor/doctor healthy
Gateway healthy
provider remains Ollama
Delivery READY
pending ticket_outbox returns to 0
Recovery READY
SQLite integrity_check=ok
no unexpected duplicate/nonterminal Ticket/run/outbox/recovery residue
```

Record actual generation; do not force parent value 38.

Failure:

`FAIL_POST_TURN_HEALTH`

## Phase K — preservation proof

Reverify:

- plugin fingerprint exact;
- live Task-226 repair identity exact;
- ownership manifest coherent;
- public `v0.9.3` unchanged;
- historical Task-223 transaction/inventory/backup unchanged.

No historical-evidence cleanup.

## Required semantic/mutation ledger

Report exact counts for:

```text
Dashboard Send activations
Dashboard human submissions
new Ticket lineages attributable to Task 232
new OpenClaw session/run lineages
new Ollama/model calls
new durable semantic/result lineages
new logical Dashboard assistant results
product/runtime Discord replies attributable to Task-232 Dashboard turn
direct operator Discord/API Sends
semantic retries/resubmissions
recovery replays/resends
manual Ticket/outbox/recovery/SQLite writes
manual lifecycle/Gateway actions
process terminations
provider/model substitutions
stale-evidence mutations
installer/plugin/rollover actions
Release/tag/asset mutations
product/source/test/workflow edits
```

Expected PASS shape:

```text
Dashboard Send activations: 1
Dashboard human submissions: 1
new Ticket lineage: 1
new session/run lineage: 1
new Ollama/model-call lineage: 1
new durable semantic/result lineage: 1
new logical Dashboard assistant result: 1
Discord replies attributable to Dashboard turn: 0
direct operator Discord/API Sends: 0
semantic retries/resubmissions: 0
recovery replay/resend: 0
manual product/data/lifecycle mutations: 0
```

## Allowed final dispositions

Use one primary disposition:

- `PASS_EXISTING_SESSION_DASHBOARD_SEMANTIC_DURABLE_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_DELIVERY_HAZARD`
- `BLOCKED_DASHBOARD_COMPOSER_DRIFT`
- `FAIL_DASHBOARD_TURN`
- `FAIL_DURABLE_SEMANTIC_TRACE`
- `FAIL_PAYLOAD_PROVENANCE`
- `FAIL_OLLAMA_LINEAGE`
- `FAIL_DASHBOARD_NO_RESULT`
- `FAIL_DASHBOARD_DUPLICATE_RESULT`
- `FAIL_UNEXPECTED_DISCORD_CROSS_SURFACE_DELIVERY`
- `FAIL_POST_TURN_HEALTH`
- `BLOCKED_EVIDENCE`

## Stop boundary

Publish:

`docs/operations/coordination/reports/CNX-20260903-232-existing-session-dashboard-semantic-durable-requalification.md`

Then stop for independent ChatGPT review.

Even after PASS, do not automatically:

- begin Discord-origin semantic acceptance;
- clean historical Task-223 evidence;
- run installer/reset/uninstall/reinstall;
- mutate public Release/tag/assets;
- edit product/source/test/workflow files;
- begin another semantic turn.