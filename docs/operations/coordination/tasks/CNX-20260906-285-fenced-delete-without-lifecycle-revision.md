# CNX-20260906-285 — Fenced Delete Without Optional Lifecycle Revision

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-284`  
Resumes acceptance context: `CNX-20260906-272`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authorization

Task284 correctly stopped before mutation because the exact installed OpenClaw session entry has no `lifecycleRevision`. This task authorizes exactly one supported Gateway `sessions.delete` attempt using only fencing fields actually present in the fresh runtime entry. It does not authorize inventing, omitting, or fabricating a lifecycle revision value.

The source contract makes `expectedLifecycleRevision` optional and independently supports `expectedSessionId` and `expectedSessionUpdatedAt`. The latter two must be supplied from the same fresh preflight snapshot.

## Exact target

- key: `agent:main:discord:channel:1391855033993138217`
- expected prior session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- setup Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`

## Phase A — mandatory fresh preflight

Prove again, in the same run:

1. exact key and current session ID match the disposable target;
2. current session entry has a numeric updatedAt;
3. lifecycleRevision is absent or unavailable; do not synthesize one;
4. CNX generation/Ticket is terminal and durably delivered;
5. protected Ticket/session remains distinct and untouched;
6. operator-admin Gateway client and non-WebChat path are available;
7. Gateway/Ollama/Host/Supervisor health is good;
8. no ambiguity or concurrent lifecycle change exists.

Any mismatch or uncertainty means stop without mutation.

## Phase B — exactly one Delete

Invoke the supported Gateway RPC once with:

```json
{
  "key": "<fresh exact key>",
  "agentId": "main",
  "deleteTranscript": true,
  "expectedSessionId": "<fresh exact session ID>",
  "expectedSessionUpdatedAt": "<fresh exact numeric updatedAt>",
  "emitLifecycleHooks": true,
  "archivedOnly": false
}
```

Do not send `expectedLifecycleRevision` because the installed session entry has no such field. Do not use `cnxclaw.cmd session cancel`, reset, WebChat, guessed CLI, or manual mutation.

If the RPC returns any error, `deleted:false`, mismatch, permission rejection, or timeout, do not retry.

## Phase C — read-only postconditions

Capture exact RPC result and verify:

- explicit `deleted:true`;
- old OpenClaw session no longer appears under the key;
- transcript/archive behavior;
- CNX lifecycle/deletion/revocation/generation effects;
- Ticket, event, delivery, outbox, and recovery state;
- Gateway/Ollama/Host/Supervisor health;
- protected old Ticket/session unchanged.

No post-delete semantic message is authorized.

## Hard fences

- Delete attempts: maximum 1;
- reset: 0;
- cancel substitute/retry: 0;
- semantic sends: 0;
- protected or prior sacrificial session mutation: 0;
- manual SQLite/Ticket/session/transcript/config mutation: 0;
- replay/redelivery/disposition: 0;
- installer/uninstall/release/force push: 0.

## Completion

Publish an evidence report and set coordination to `WAITING_FOR_CHATGPT_REVIEW`. Stop after the one attempt or any preflight/error boundary.
