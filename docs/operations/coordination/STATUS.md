# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK198_DISCORD_INVESTIGATION__TASK199_EXISTING_EVIDENCE_CAPTURE`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository + read-only Windows/OpenClaw evidence through Hermes  
**Active parent:** `CNX-20260831-198`  
**Active subtask:** `CNX-20260831-199`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `V093_PUBLISHED__WAITING_EXISTING_DISCORD_FAILURE_EVIDENCE`

## Publication

v0.9.3 publication is complete and accepted. No further publication action is authorized.

- tag: `v0.9.3`
- target: `26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Task 198 source-trace status

Established from the exact published candidate:

- native non-Dashboard Direct delivery may terminal through `message_sent`/`confirmDirectDelivery` without a `cnx_assistant_delivery` row;
- Dashboard verified delivery intentionally does not stage non-Dashboard Direct tickets;
- `missing-run-correlation` and `missing-append-before-deliver` in that Dashboard observer are diagnostic return paths, not exceptions;
- OpenClaw's `before_agent_run` hook class is fail-closed on handler exceptions;
- the exact exception that blocked the old Discord session is not present in the coordination report and must be recovered from existing logs/state before source repair.

## Task 199

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260831-199-task198-existing-discord-hook-failure-evidence-capture.md`

This is read-only evidence collection. No user/Discord Send is required or authorized.

Required result:

- exact Session-A before-agent exception if retained;
- Session-A Ticket/run/session-generation mapping;
- Session-B native delivery correlation mapping;
- A/B comparison;
- hypotheses confirmed/rejected/unresolved.

After the Task 199 report, ChatGPT resumes root-cause analysis and TDD. Production source must remain untouched until a focused RED regression test reproduces the proven invariant violation.

## Hard fence

No new Discord messages, no restart/reset/uninstall/reinstall/install-over, no provider/model/config/state/source mutation during Task 199, no republish/retarget, no test weakening, and no force push.
