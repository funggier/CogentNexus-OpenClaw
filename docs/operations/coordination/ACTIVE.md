# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK231_POST_REPAIR_MANAGED_DASHBOARD_SEMANTIC_DURABLE_REQUALIFICATION`
Current disposition: `TASK230_ACCEPTED_PASS__DASHBOARD_ORIGIN_ROUTING_SEMANTICS_CORRECTED`
Task ID: `CNX-20260903-231`
Parent task: `CNX-20260902-230`
Repair parent: `CNX-20260902-226`
Failure lineage: `CNX-20260902-223`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-03 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted source/runtime authority

Exact repaired source remains:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task-230 accepted review disposition:

`ACCEPT_PASS_ALREADY_EXACT_INSTALLER_REENTRY__MANAGED_CONVERGENCE_PROVEN__RETRY_POLICY_EFFECTIVE__REPORTING_GAP_NONBLOCKING`

Accepted parent live baseline after Task 230:

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

Fresh Task-231 evidence is authoritative; generation 38 is the parent baseline, not a value to force.

## Corrected Dashboard routing invariant

Task 231 must follow the actual OpenClaw behavior established for this environment:

```text
Dashboard-origin message -> Dashboard response
Discord-origin message   -> Discord response
```

A Dashboard message may use a session originally associated with Discord, but a Dashboard-origin turn is not expected to produce a Discord reply.

Therefore Task 231 must **not** require a Discord product delivery. Discord exactly-once delivery will be tested separately by a successor using Discord-origin ingress after Task 231 passes independent review.

Discord channel `1531199905673252946` is read-only negative-control evidence in Task 231. No operator message may be sent there.

## Active Task 231

Execute:

`tasks/CNX-20260903-231-post-repair-managed-semantic-durable-delivery-requalification.md`

Task 231 authorizes exactly one human Dashboard semantic submission, with no `@Ce` prefix:

`ช่วยสรุปงานที่ฉันควรโฟกัสวันนี้จาก context ล่าสุด และบอกเหตุผลสั้น ๆ`

Required acceptance lineage:

```text
one Dashboard human submission
-> one Ticket
-> one session/run
-> one Ollama call
-> one durable semantic/result lineage
-> one logical Dashboard assistant result
```

Expected cross-surface result:

```text
product/runtime Discord replies attributable to the Dashboard turn: 0
```

## Semantic retry boundary

Dashboard human submissions:

`1 maximum`

Once the submission is accepted or any new semantic lineage is observed:

`SEMANTIC_RETRY_GATE=CLOSED`

It cannot reopen during Task 231. Observer/tool failures are never permission to send the message again.

Read-only tooling/observer retries remain bounded to up to 2 additional evidence-driven attempts per logical observation and must be reported in an attempt ledger with an explicit retry-policy classification.

## Discord/effect boundary

Direct operator Discord/API Sends:

`0`

Discord-origin semantic test messages:

`0`

Unexpected product/runtime Discord reply attributable to the Task-231 Dashboard turn:

`FAIL_UNEXPECTED_DISCORD_CROSS_SURFACE_DELIVERY`

## Historical evidence boundary

Task-223 transaction, matching inventory, ownership manifest and backup remain immutable forensic evidence. No finalization, cleanup, edit, move, rename, delete, archive, replace or reuse is authorized.

## Other hard fences

Task 231 does not permit:

- second Dashboard submission or semantic retry;
- Discord-origin acceptance turn;
- installer/reset/uninstall/reinstall;
- manual Ticket/outbox/recovery/SQLite writes;
- manual cnxclaw/Gateway lifecycle repair;
- manual plugin actions;
- recovery replay/resend;
- provider/model substitution;
- process termination;
- stale-evidence cleanup/finalization;
- product/source/test/workflow edits;
- Release/tag/asset mutation;
- force push/history rewrite.

## Stop boundary

Hermes must publish:

`reports/CNX-20260903-231-post-repair-managed-semantic-durable-delivery-requalification.md`

Then stop for independent ChatGPT review before any Discord-origin semantic acceptance, stale-evidence cleanup, lifecycle mutation or publication action.
