# CNX-20260903-231 — Post-Repair Managed Semantic Durable-Delivery Requalification

Status: `READY_FOR_HERMES`
Date: 2026-09-03 ICT
Parent: `CNX-20260902-230`
Repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Run exactly **one human Dashboard semantic turn** on the now-repaired managed runtime and prove the proportional acceptance lineage required by Task 188 / Task 223:

```text
one human Dashboard submission
-> one Ticket
-> one session/run
-> one Ollama model call
-> one durable delivery
-> one logical Dashboard assistant result
```

The turn must have no semantic retry, no recovery duplicate, no second user submission, no provider substitution, and no manually manufactured delivery.

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

## Exact semantic submission

Use exactly this human Dashboard message once:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

Dashboard human submission budget:

`1 maximum`

As soon as the submission is accepted by the Dashboard/runtime or any new semantic lineage is observed:

`SEMANTIC_RETRY_GATE=CLOSED`

The gate cannot reopen during Task 231.

A failed observer/tool command is never permission to send the Dashboard message again.

# Retry policy for Task 231

The user's bounded tooling-retry policy remains active for read-only observation only.

Authorized read-only retries:

- up to 2 additional attempts per logical observation/probe;
- only when the failure is clearly tooling/transport/query/evidence-collection related;
- each retry must change a material method/hypothesis or address the observed failure;
- record each attempt in the report.

Not retryable:

- Dashboard human submission;
- model invocation;
- Ticket creation;
- durable delivery;
- Discord/product semantic effect;
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
- read-only Dashboard/channel/Discord observation where available;
- exactly one human Dashboard submission containing the exact message above;
- passive observation of the product-generated semantic response/durable delivery;
- bounded read-only tooling retries under the policy above;
- coordination report publication.

Not authorized:

- a second Dashboard submission;
- manually replaying/resending/retrying the semantic request;
- direct operator Discord/API Send to manufacture or repair delivery;
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

## Discord/effect budget

Direct operator Discord/API Sends:

`0`

Product/runtime semantic delivery budget for the **single Task-231 test lineage**:

`exactly 1 logical delivery/effect maximum`

Do not issue a direct API Send to satisfy this requirement. The observable effect must be produced by normal CogentNexus/OpenClaw runtime behavior from the one human Dashboard turn.

If the runtime produces zero expected delivery/effect, fail closed. If it produces more than one logical delivery/effect for the same lineage, classify as duplicate delivery and fail closed.

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

## Phase C — delivery/recovery hazard gate

Before the semantic turn, prove there is no pending/emittable state that could contaminate exactly-once acceptance:

```text
Delivery READY
pending outbox = 0
Recovery READY
no emittable unresolved recovery for the acceptance channel/lineage
no existing nonterminal duplicate acceptance Ticket/session/run attributable to this task
```

If any old work can emit into the same observable channel or confound the lineage, do not clean it manually and do not submit the message.

Stop:

`BLOCKED_DELIVERY_HAZARD`

## Phase D — establish durable pre-turn baselines

Persist external read-only evidence with at least:

- SQLite `PRAGMA integrity_check`;
- Ticket count/status distribution and max/newest Ticket identity;
- Ticket-event count/max identity;
- Evidence/Decision trace counts/max identities where applicable;
- outbox/delivery counts + pending identities;
- recovery ledger/state baseline;
- PluginLane/Event baseline including source/provenance fields;
- OpenClaw session/run baseline for the target Dashboard context;
- Ollama/model-call/log baseline sufficient to distinguish one new call if available;
- Dashboard assistant-message baseline;
- Discord/channel observable baseline where available.

Do not mutate counters/rows to simplify comparison.

## Phase E — submit exactly one human Dashboard turn

Submit exactly once:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

Record the earliest reliable submission/acceptance timestamp and any request/message identity exposed by the UI/runtime.

Immediately set/report:

`SEMANTIC_RETRY_GATE=CLOSED`

From this point onward no second semantic submission is permitted for any reason.

If the single submission itself cannot be proven to have entered the runtime and no new semantic lineage appears, stop after bounded observation:

`FAIL_DASHBOARD_TURN`

Do not resubmit.

## Phase F — observe one semantic lineage

Using passive/read-only observation, correlate the one user turn to exactly one new lineage.

Prove as available:

```text
one new Ticket
one OpenClaw session/run lineage
one model/Ollama call lineage
one durable result/delivery lineage
one logical Dashboard assistant result
```

Use timestamps, IDs, correlation keys, Ticket IDs, run/session IDs, durable event IDs, request/model logs and delivery/outbox IDs as available.

No inference from terminal status alone is sufficient when stronger durable evidence exists.

If multiple independent semantic lineages are created from the single human turn, fail closed and report them.

## Phase G — durable semantic trace proof

Require one new durable Task/Evidence/Decision trace for the human turn and inspect exact rows/events.

At minimum prove the accepted human semantic provenance contract where the current schema exposes it:

```text
Ticket durable status = open at creation/semantic ingestion boundary
PluginLane/Event source = openclaw
payload_source = channel_payload
payload_author_kind = human
subject derives from the exact user message
body derives from the distinct body candidate when available, otherwise conservative no-body fallback
```

Also prove no channel metadata/control tokens were incorrectly persisted into human semantic notes/subject/body/decision fields.

If provenance fields/schema names differ in current source, document the exact equivalent fields and prove the same semantic property rather than inventing names.

Failure:

- semantic/durable lineage missing: `FAIL_DURABLE_SEMANTIC_TRACE`
- payload origin/author/subject/body semantics wrong: `FAIL_PAYLOAD_PROVENANCE`

## Phase H — Ollama-only model proof

Prove the new acceptance lineage used the configured Ollama provider/model and did not fall back/substitute another provider.

Prefer direct run/model-call/log correlation for exactly one model request for the lineage when the evidence surface exposes it.

If exact one-call cardinality cannot be proven despite otherwise successful response, classify conservatively:

`FAIL_OLLAMA_LINEAGE`

Do not trigger another semantic turn to improve evidence.

## Phase I — exactly-once durable delivery / Discord effect

For the same lineage, prove exactly one logical product/runtime delivery/effect into the intended observable Dashboard/Discord delivery surface according to the current integration contract.

Required properties:

- one durable delivery lineage/record;
- one observable logical assistant result;
- no duplicate delivery for the same semantic lineage;
- no recovery replay/resend;
- no second Dashboard user submission;
- direct operator Discord/API Sends = 0.

If zero expected product delivery/effect:

`FAIL_DISCORD_NO_DELIVERY`

If more than one logical delivery/effect for the same lineage:

`FAIL_DISCORD_DUPLICATE_DELIVERY`

A tool/observer timeout does not authorize a resend.

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
new durable delivery lineages
new logical Dashboard assistant results
product/runtime Discord/delivery effects for Task-231 lineage
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
new durable delivery lineage: 1
new logical Dashboard assistant result: 1
product/runtime logical delivery/effect: 1
direct operator Discord/API Sends: 0
semantic retries/resubmissions: 0
recovery replay/resend: 0
manual product/data/lifecycle mutations: 0
```

## Allowed final dispositions

Use one primary disposition:

- `PASS_POST_REPAIR_MANAGED_SEMANTIC_DURABLE_DELIVERY_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_DELIVERY_HAZARD`
- `FAIL_DASHBOARD_TURN`
- `FAIL_DURABLE_SEMANTIC_TRACE`
- `FAIL_PAYLOAD_PROVENANCE`
- `FAIL_OLLAMA_LINEAGE`
- `FAIL_DISCORD_NO_DELIVERY`
- `FAIL_DISCORD_DUPLICATE_DELIVERY`
- `FAIL_POST_TURN_HEALTH`
- `BLOCKED_EVIDENCE`

## Stop boundary

Publish:

`docs/operations/coordination/reports/CNX-20260903-231-post-repair-managed-semantic-durable-delivery-requalification.md`

Then stop for independent ChatGPT review.

Even after PASS, do not automatically:

- clean historical Task-223 evidence;
- run installer/reset/uninstall/reinstall;
- mutate public Release/tag/assets;
- edit product/source/test/workflow files;
- begin another semantic acceptance turn.
