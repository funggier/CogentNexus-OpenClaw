# Active Coordination

Status: `IN_PROGRESS`
State: `CNX446_DASHBOARD_DIRECT_TERMINAL_BOUNDARY_RED_PENDING`
Task: `CNX-20260925-446-dashboard-direct-terminal-final-boundary.md`
Assigned executor: `ChatGPT`
Review owner: `ChatGPT independent final verification`
Human final authority: `Operator`
Working branch: `cnx-446-dashboard-direct-terminal-final-boundary`
Target release line: `v0.9.8`

## Current objective

Repair the live OpenClaw 2026.9.5 Dashboard Direct completion-boundary defect in which a non-terminal assistant progress/commentary write can be staged as the durable result and close the Ticket before the exact run finishes.

## Production trigger

Session `6090e8c3-88fc-420d-8ee8-1f498b9146f6`, run `63bb6787-a016-426b-9ba0-d84ac15ff555`, Ticket `CNXT-f191f552-305a-4950-a77c-1dfd3444d253` proved:

- Ticket-first admission and Direct routing were correct;
- a progress message was incorrectly marked durable/delivered/completed;
- the exact run continued tool execution for about 110 seconds afterward;
- true terminal OpenAI/Codex mirrored output carried `__openclaw.runTerminal=true`, while the progress message did not;
- native Ollama terminal messages do not expose that field, so the repair must remain provider-neutral.

## Immediate execution order

1. Add a RED production-topology regression.
2. Fence mirrored fallback staging on exact terminal/run authority.
3. Preserve existing `before_agent_finalize` and native Ollama/legacy behavior.
4. Run focused then full plugin validation.
5. Commit/push exact repair candidate.
6. Run exact-SHA CI.
7. Deploy/install-over only after local/CI GREEN.
8. Perform a fresh live Dashboard progress -> tools -> terminal acceptance.
9. Update the CNX-446 report and coordination state.
10. Publish v0.9.8 only after all release gates are GREEN.

## Baseline authority

v0.9.7 remains the immutable published baseline. CNX-444 remains historical GREEN evidence and is not modified.
