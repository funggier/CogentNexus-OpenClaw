# CNX-20260903-231 — Post-Repair Managed Dashboard Semantic/Durable Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-03 ICT
Parent: `CNX-20260902-230`
Repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Run exactly **one human Dashboard semantic turn** on the repaired managed runtime and prove the Dashboard-origin acceptance lineage without inventing Discord routing semantics:

```text
one human Dashboard submission
-> one Ticket
-> one OpenClaw session/run lineage
-> one Ollama model-call lineage
-> one durable semantic/result lineage
-> one logical Dashboard assistant result
```

Observed normal OpenClaw behavior for this environment is now an explicit acceptance invariant:

- a message submitted from the Dashboard can operate on a session originally associated with Discord;
- the response to that Dashboard-origin message is shown in the Dashboard;
- the Dashboard-origin message is **not expected to produce a Discord reply**;
- a Discord-origin message is the separate ingress path that normally produces a Discord reply.

Therefore Task 231 must **not** require `Dashboard -> Discord` delivery. Requiring that would misclassify normal routing as failure.

A Discord-origin exactly-once acceptance turn is intentionally deferred to a successor task after Task 231 is independently accepted.

## Accepted parent authority

Task-230 report:

`docs/operations/coordination/reports/CNX-20260902-230-scheduler-identity-recovery-bounded-retry-installer-reentry.md`

Task-230 independent review:

`docs/operations/coordination/reviews/CNX-20260902-230-scheduler-identity-recovery-bounded-retry-installer-reentry-review.md`

Accepted review disposition:

`ACCEPT_PASS_ALREADY_EXACT_INSTALLER_REENTRY__MANAGED_CONVERGENCE_PROVEN__RETRY_POLICY_EFFECTIVE__REPORTING_GAP_NONBLOCKING`

Accepted repaired source:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task-230 accepted managed baseline:

```text
controller mode: managed
generation: 38
startup policy: enabled
startup adapter: installed / Ready / LastTaskResult=0
provider: ollama
Gateway: healthy
Delivery: READY, pending=0
Recovery: READY
SQLite integrity_check: ok
```

Fresh Windows evidence is authoritative; generation 38 is an accepted parent baseline, not a value to force.

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No public Release/tag/asset mutation is authorized.

## Exact Dashboard semantic submission

Use exactly this Dashboard human message once, with **no `@Ce` prefix and no other added text**:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

Dashboard human submission budget:

`1 maximum`

As soon as the submission is accepted by the Dashboard/runtime or any new semantic lineage is observed:

`SEMANTIC_RETRY_GATE=CLOSED`

The gate cannot reopen during Task 231.

A failed observer/tool command is never permission to submit the Dashboard message again.

## Dashboard / Discord routing invariant for this task

Task-231 acceptance requires:

```text
Dashboard-origin human submission: 1
logical Dashboard assistant result: 1
product/runtime Discord reply attributable to Task-231 Dashboard turn: 0
operator Discord/API Sends: 0
```

Discord channel `1531199905673252946` may be observed read-only as a negative-control surface if available, but no operator message may be sent there during Task 231.

A Discord message appearing for this Dashboard-origin turn is not required for PASS. If a new Discord product reply is conclusively attributable to this Dashboard-origin turn, record it as unexpected cross-surface routing and fail closed:

`FAIL_UNEXPECTED_DISCORD_CROSS_SURFACE_DELIVERY`

Absence of a Discord reply is the expected routing behavior and is **not** a failure.

# Retry policy for Task 231

The user's bounded tooling-retry policy remains active for read-only observation only.

Authorized read-only retries:

- up to 2 additional attempts per logical observation/probe;
- only when failure is clearly tooling/transport/query/evidence-collection related;
- each retry must change a material method/hypothesis or address the observed failure;
- record each attempt in the report.

Not retryable:

- Dashboard human submission;
- model invocation;
- Ticket creation;
- durable semantic/result creation;
- Dashboard response generation;
- Discord/product semantic effects;
- lifecycle mutation.

Required retry classification in the final report:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

The report must include an attempt ledger with logical operation, attempt number, method, result/error, whether product/semantic state could have changed, remaining budget and next rationale.

# Hard fences

Authorized:

- fresh GitHub/Actions/source/coordination reads;
- read-only Windows/runtime/controller/startup/Supervisor/Gateway/Ollama checks;
- read-only plugin/source/ownership provenance verification;
- read-only Delivery/Recovery inspection;
- read-only SQLite queries and integrity checks;
- read-only process/log/session/run/Ticket/event/outbox/recovery evidence collection;
- read-only Dashboard observation;
- read-only Discord/channel observation where available;
- exactly one human Dashboard submission containing the exact message above;
- passive observation of the normal Dashboard-origin response and durable semantic/result lineage;
- bounded read-only tooling retries under the policy above;
- coordination report publication.

Not authorized:

- a second Dashboard submission;
- any Discord-origin human test message;
- manually replaying/resending/retrying the semantic request;
- direct operator Discord/API Send;
- manual Ticket/event/outbox/recovery/SQLite writes;
- manual recovery execution;
- `cnxclaw` enable/disable/start/stop/restart/reset/uninstall;
- Gateway restart;
- OpenClaw plugin install/enable/disable/uninstall;
- installer execution;
- provider/model substitution;
- process termination;
- stale Task-223 transaction/inventory/backup cleanup/finalization/edit/move/delete;
- product/source/test/workflow edits;
- public Release/tag/asset mutation;
- force push/history rewrite.

# Required execution flow

## Phase A — fresh repository authority

Before semantic activity:

1. fetch fresh branch HEAD;
2. verify Task 231 is active and `READY_FOR_HERMES`;
3. verify accepted repair `9a8510f...` remains an ancestor;
4. compare accepted repair -> HEAD and require no unexpected product/source/test/workflow drift;
5. verify public `v0.9.3` tag remains unchanged;
6. verify Task-230 report-head CI remains successful;
7. verify no newer coordination authority supersedes Task 231.

Unexpected product drift:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase B — fresh managed-runtime preflight

Capture read-only preflight:

```text
controller mode + generation
startup policy / startup adapter state / LastTaskResult
Supervisor/doctor health
AGENTS managed-policy state
installed plugin id/version/path/source/enabled/status/fingerprint
live repaired namespace_ownership.py identity
ownership manifest verification
Gateway health
provider and exact selected model/Ollama health
Delivery readiness + pending outbox
Recovery readiness + emittable recovery state
SQLite integrity + durable counts/max IDs
relevant pending/nonterminal Tickets
relevant session/run/model-call residue
relevant product processes
historical Task-223 evidence identities
```

Require coherent managed state and exact plugin fingerprint `e3bcce04...`.

If a materially different live state is found, stop before submission:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase C — semantic/recovery hazard gate

Before the Dashboard turn, prove there is no pending/emittable state that could contaminate one-turn acceptance:

```text
Delivery READY
pending outbox = 0
Recovery READY
no emittable unresolved recovery that can create a competing Dashboard result
no existing nonterminal duplicate acceptance Ticket/session/run attributable to this task
```

If old work can confound the lineage, do not clean it manually and do not submit the message.

Stop:

`BLOCKED_DELIVERY_HAZARD`

## Phase D — establish pre-turn baselines

Persist external read-only evidence with at least:

- SQLite `PRAGMA integrity_check`;
- Ticket count/status distribution and max/newest Ticket identity;
- Ticket-event count/max identity;
- Evidence/Decision trace counts/max identities where applicable;
- outbox/durable result counts + pending identities;
- recovery ledger/state baseline;
- PluginLane/Event baseline including source/provenance fields;
- OpenClaw session/run baseline for the target Dashboard context;
- Ollama/model-call/log baseline sufficient to distinguish one new call if available;
- Dashboard assistant-message baseline;
- Discord channel `1531199905673252946` observable baseline where available, for negative-control only.

Do not mutate counters/rows to simplify comparison.

## Phase E — submit exactly one human Dashboard turn

Submit exactly once, without `@Ce`:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

Record the earliest reliable submission/acceptance timestamp and any request/message identity exposed by the UI/runtime.

Immediately set/report:

`SEMANTIC_RETRY_GATE=CLOSED`

From this point onward no second semantic submission is permitted for any reason.

If the single submission itself cannot be proven to have entered the runtime and no new semantic lineage appears, stop after bounded observation:

`FAIL_DASHBOARD_TURN`

Do not resubmit.

## Phase F — observe one Dashboard-origin semantic lineage

Using passive/read-only observation, correlate the one user turn to exactly one new lineage.

Prove as available:

```text
one new Ticket
one OpenClaw session/run lineage
one Ollama/model-call lineage
one durable semantic/result lineage
one logical Dashboard assistant result
zero Discord reply attributable to this Dashboard-origin turn
```

Use timestamps, IDs, correlation keys, Ticket IDs, run/session IDs, durable event IDs, request/model logs, response/delivery IDs, Dashboard evidence, and read-only Discord observation as available.

No inference from terminal status alone is sufficient when stronger durable evidence exists.

If multiple independent semantic lineages are created from the single Dashboard turn, fail closed and report them.

## Phase G — durable semantic trace proof

Require one new durable Task/Evidence/Decision trace for the Dashboard human turn and inspect exact rows/events.

At minimum prove the accepted human semantic provenance contract where the current schema exposes it:

```text
Ticket durable status = open at creation/semantic ingestion boundary
PluginLane/Event source = openclaw
payload_source = channel_payload
payload_author_kind = human
subject derives from the exact user message
body derives from the distinct body candidate when available, otherwise conservative no-body fallback
```

Also prove no UI/channel metadata/control tokens, including an invented `@Ce` prefix, were incorrectly persisted into human semantic notes/subject/body/decision fields.

If provenance fields/schema names differ in current source, document the exact equivalent fields and prove the same semantic property rather than inventing names.

Failure:

- semantic/durable lineage missing: `FAIL_DURABLE_SEMANTIC_TRACE`
- payload origin/author/subject/body semantics wrong: `FAIL_PAYLOAD_PROVENANCE`

## Phase H — Ollama-only model proof

Prove the new Dashboard-origin acceptance lineage used the configured Ollama provider/model and did not fall back/substitute another provider.

Prefer direct run/model-call/log correlation for exactly one model request for the lineage when the evidence surface exposes it.

If exact one-call cardinality cannot be proven despite otherwise successful response, classify conservatively:

`FAIL_OLLAMA_LINEAGE`

Do not trigger another semantic turn to improve evidence.

## Phase I — Dashboard response and cross-surface routing proof

For the same lineage, prove:

- exactly one logical Dashboard assistant result;
- no duplicate Dashboard assistant result for the same semantic lineage;
- no recovery replay/resend;
- no second Dashboard user submission;
- no operator Discord/API Send;
- no product/runtime Discord reply attributable to the Dashboard-origin turn.

If zero Dashboard assistant result:

`FAIL_DASHBOARD_NO_RESULT`

If more than one logical Dashboard result for the same lineage:

`FAIL_DASHBOARD_DUPLICATE_RESULT`

If a new Discord product reply is conclusively attributable to this Dashboard-origin turn:

`FAIL_UNEXPECTED_DISCORD_CROSS_SURFACE_DELIVERY`

A tool/observer timeout does not authorize a resubmission.

## Phase J — post-turn runtime health

After terminal/settled evidence, recheck:

```text
controller remains coherent managed state
startup adapter healthy
Supervisor/doctor healthy
Gateway healthy
provider remains Ollama
Delivery READY
pending outbox returns to 0
Recovery READY
SQLite integrity_check=ok
no new unexpected nonterminal duplicate Ticket/run/outbox/recovery residue
```

Generation may change only if current runtime semantics explain it; record actual value and do not force 38.

Failure:

`FAIL_POST_TURN_HEALTH`

## Phase K — provenance and historical-evidence preservation

Reverify:

- plugin fingerprint remains `e3bcce04...`;
- live Task-226 repair identity remains exact;
- ownership manifest remains coherent;
- public tag unchanged;
- historical Task-223 transaction/inventory/backup identities remain unchanged.

Do not clean historical evidence in Task 231.

## Required semantic/mutation ledger

Report exact counts for:

```text
Dashboard human submissions
new Ticket lineages attributable to Task 231
new OpenClaw session/run lineages
new Ollama/model calls
new durable semantic/result lineages
new logical Dashboard assistant results
product/runtime Discord replies attributable to Task-231 Dashboard turn
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
Dashboard human submissions: 1
new Ticket lineage: 1
new session/run lineage: 1
new Ollama/model-call lineage: 1
new durable semantic/result lineage: 1
new logical Dashboard assistant result: 1
product/runtime Discord replies attributable to Dashboard turn: 0
direct operator Discord/API Sends: 0
semantic retries/resubmissions: 0
recovery replay/resend: 0
manual product/data/lifecycle mutations: 0
```

## Allowed final dispositions

Use one primary disposition:

- `PASS_POST_REPAIR_MANAGED_DASHBOARD_SEMANTIC_DURABLE_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_DELIVERY_HAZARD`
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

`docs/operations/coordination/reports/CNX-20260903-231-post-repair-managed-semantic-durable-delivery-requalification.md`

Then stop for independent ChatGPT review.

Even after PASS, do not automatically:

- send the Discord-origin acceptance message;
- clean historical Task-223 evidence;
- run installer/reset/uninstall/reinstall;
- mutate public Release/tag/assets;
- edit product/source/test/workflow files;
- begin another semantic acceptance turn.

The successor, if Task 231 is accepted, should separately test **Discord-origin ingress -> Discord reply** with its own one-message, no-retry semantic budget.
