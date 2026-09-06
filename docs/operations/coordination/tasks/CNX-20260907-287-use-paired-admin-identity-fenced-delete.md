# CNX-20260907-287 — Use Paired Admin Identity for Fenced Delete

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260906-286`  
Executor: `Suna`  
Reviewer/escalation: `ChatGPT`

## Authorization

ChatGPT authorizes use of the already-paired operator-admin identity displayed as `Windows Node (CDQ-P)`, only through the supported OpenClaw Gateway client path. Do not print, copy, extract, rotate, revoke, or guess any token/password. If the existing paired identity cannot be used without new credential material or an additional human security decision, stop with `NEEDS_CHATGPT`.

## Objective

Perform the one-shot disposable OpenClaw session deletion that Task285 could not attempt because its client lacked `operator.admin`.

## Exact target

- key: `agent:main:discord:channel:1391855033993138217`
- expected prior session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- setup Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`

## Phase A — fresh preflight

Using the authorized paired identity, read-only prove in the same run:

1. exact target key and session ID;
2. numeric updatedAt;
3. lifecycleRevision remains absent; do not synthesize it;
4. Ticket is terminal and durably delivered;
5. protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains distinct;
6. operator-admin scope and non-WebChat client path;
7. Gateway/Ollama/Host/Supervisor health.

Any mismatch, missing fence, credential uncertainty, or target ambiguity means stop without mutation.

## Phase B — exactly one Delete

Call supported Gateway RPC `sessions.delete` exactly once with:

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

Do not include `expectedLifecycleRevision`. Do not use `cnxclaw.cmd session cancel`, reset, WebChat, guessed CLI, or manual mutation.

If error, timeout, `deleted:false`, or fencing mismatch occurs, do not retry.

## Phase C — read-only postconditions

Capture exact result and verify explicit `deleted:true`, session removal, transcript/archive behavior, CNX lifecycle effects, Ticket/delivery/outbox/recovery state, service health, and protected-state preservation. No post-delete semantic message.

## Hard fences

Delete maximum 1; reset 0; cancel substitute 0; semantic sends 0; credential mutation/readout 0; protected/prior session mutation 0; manual durable-state mutation 0; replay/redelivery 0; installer/release/force push 0.

## Completion

Publish report, set coordination to `WAITING_FOR_CHATGPT_REVIEW`, and stop.
