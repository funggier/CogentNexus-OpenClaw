# CNX-20260906-284 — Bounded Disposable OpenClaw Session Delete

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-283`  
Resumes acceptance context: `CNX-20260906-272`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authorization

This task authorizes exactly one supported OpenClaw Gateway `sessions.delete` attempt against the disposable target below, only after the same-run fresh preflight proves every fence. It does not authorize deletion of any other session.

## Exact target

- session key: `agent:main:discord:channel:1391855033993138217`
- previously observed session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- setup Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`

## Phase A — mandatory fresh read-only preflight

Before mutation, prove:

1. exact current OpenClaw session key and session ID still match the target;
2. exact current CNX lifecycle generation, lifecycle revision, and updatedAt;
3. setup Ticket is terminal and durably delivered;
4. protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and its owner session remain distinct and untouched;
5. Gateway/Ollama/Host/Supervisor health;
6. authenticated Gateway client has `operator.admin` and is not WebChat;
7. no ambiguity or concurrent lifecycle change is present.

If any check fails, stop without mutation and publish BLOCKED evidence.

## Phase B — exactly one Delete

Invoke the supported Gateway RPC `sessions.delete` exactly once with values taken from the same fresh snapshot:

```json
{
  "key": "agent:main:discord:channel:1391855033993138217",
  "agentId": "main",
  "deleteTranscript": true,
  "expectedSessionId": "<fresh exact session ID>",
  "expectedLifecycleRevision": "<fresh exact revision>",
  "expectedSessionUpdatedAt": "<fresh exact numeric updatedAt>",
  "emitLifecycleHooks": true,
  "archivedOnly": false
}
```

The request must use the supported Control UI/operator-admin-capable Gateway path. Do not use `cnxclaw.cmd session cancel`, WebChat, guessed CLI commands, or manual file/SQLite edits.

If the RPC returns an error, `deleted:false`, fencing mismatch, permission rejection, or timeout, do not retry. Capture the exact result and stop.

## Phase C — read-only postcondition capture

Capture:

- exact RPC result; PASS requires explicit `deleted:true`;
- OpenClaw session inventory and transcript/archive result;
- CNX lifecycle state, generation/revision/session identity;
- setup Ticket, event history, delivery, outbox, and recovery rows;
- Gateway/Ollama/Host/Supervisor health;
- protected old Ticket/session unchanged;
- no semantic message or post-delete workaround.

## Hard fences

- Delete attempts: exactly 1 maximum;
- reset attempts: 0;
- Hermes semantic sends: 0;
- protected Ticket/session mutation: 0;
- prior sacrificial session mutation: 0;
- manual SQLite/Ticket/session/transcript/config mutation: 0;
- replay/redelivery/disposition: 0;
- installer/install-over/uninstall: 0;
- release/tag/default-branch promotion: 0;
- force push/history rewrite: 0.

## Completion

Publish a complete evidence report under `docs/operations/coordination/reports/`, then set coordination to `WAITING_FOR_CHATGPT_REVIEW` and stop. Do not send a post-delete semantic message in this task.
