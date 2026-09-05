# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SINGLE_HERMES_EXECUTOR__TASK269_HOST_ACTIONABLE_DURABLE_WORK_HINT_REPAIR`
Current disposition: `TASK268_CHATGPT_ACCEPTED_CAUSAL_PROOF__TASK269_OPEN`
Task ID: `CNX-20260906-269`
Parent task: `CNX-20260905-268`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-06 ICT — ChatGPT accepted Task268 causal proof and opened bounded source repair

Assigned executor: `Hermes`
Review owner after report: `ChatGPT`
Handoff from: `ChatGPT`
Next execution actor after review: `Hermes` if a bounded successor is opened
Coordination protocol: `docs/operations/coordination/HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
Delayed recheck policy: `docs/operations/coordination/DELAYED_RECHECK_QUEUE.md`

## ChatGPT Task268 review

Review:

`docs/operations/coordination/reviews/CNX-20260906-268-chatgpt-causal-root-review.md`

Verdict:

`ACCEPT_CAUSAL_PROOF__SOURCE_ACTIONABILITY_REPAIR_REQUIRED`

Accepted causal evidence:

- APPSTARTING aligned with 6/6 natural `PT1M` supervisor waves;
- each run lasted roughly 8.0–8.3 seconds;
- no APPSTARTING off-cycle;
- foreground app was substantially unchanged;
- Gateway/Ollama PIDs stayed stable.

Narrowed source defect:

`host_v091.py::durable_work_hint()` treats stored nonterminal/direct-recovery state as actionable more broadly than the plugin Direct-recovery due contract. The stale target Ticket/recovery is not eligible under the 15-minute owner-session liveness fence, but it still forces the Host into heavy reconciliation every minute.

## Active Task269

Task:

`docs/operations/coordination/tasks/CNX-20260906-269-host-actionable-durable-work-hint-repair.md`

Objective:

Make Host durable-work hints represent actually actionable work while preserving hard-hang recovery and the one-minute supervisor cadence. Use TDD and keep the old stale Ticket/recovery untouched.

## Hard fences

Task269 is source/test/docs/CI only.

```text
installer/install-over/uninstall/reset           = 0
Gateway/provider/service lifecycle mutation      = 0
live OpenClaw session delete/reset                = 0
live Discord/Dashboard/API semantic send         = 0
manual live Ticket/session/SQLite mutation       = 0
recovery replay/redelivery/disposition            = 0
Scheduled Task enable/disable/create/delete/run   = 0
stop/kill/restart unrelated live processes        = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains read-only evidence; owner intent is unproven.

## Completion

Hermes publishes:

`docs/operations/coordination/reports/CNX-20260906-269-host-actionable-durable-work-hint-repair.md`

Then set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation.
