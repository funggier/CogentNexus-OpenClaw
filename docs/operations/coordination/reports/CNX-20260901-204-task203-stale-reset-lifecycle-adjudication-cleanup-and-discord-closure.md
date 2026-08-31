# CNX-20260901-204 — Task 203 Stale Reset Lifecycle Adjudication, Cleanup, Managed Recovery, and Discord Closure

- **Task:** `CNX-20260901-204`
- **Parent:** `CNX-20260901-203`
- **Fresh authority SHA:** `4fd2ce526fe18167e4612c6c092800b2bcc81acc`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Frozen candidate:** `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- **Expected installed fingerprint:** `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`
- **Evidence root:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx204-reset-adjudication-20260901T`
- **Final disposition:** `FAIL_DISCORD_SEMANTIC_DELIVERY`

## Executive result

Task 204 completed the authorized stale-reset cleanup and one managed recovery transition. Managed convergence passed. The single human Discord Send was then consumed, but the operator subsequently identified that the visible room was the previously failing room rather than the task-designated healthy acceptance surface. The durable snapshot contains no matching nonce, Ticket, model call, or delivery delta.

The one-shot Send budget is consumed and cannot be replayed in another room under this task. A second room/message would violate the explicit hard fence and would invalidate the one-shot acceptance ledger. No second Send was performed.

This report records the user-visible room correction as a semantic acceptance failure; it does not claim a product root cause from the absence of a durable nonce record.

## Authority and scope

Fresh GitHub synchronization confirmed `ACTIVE.md` and `STATUS.md` identified Task 204 as `READY_FOR_HERMES`. The published v0.9.3 target remained immutable at:

```text
26ce64a624255278a3a0266ad38746e0e6ed2e31
```

Task 204 authorized only:

1. read-only reset-tree adjudication;
2. identity-fenced cleanup of child `17360` and parent `9840` only;
3. one installed `cnxclaw.cmd enable` invocation;
4. one human Discord Send only after managed convergence;
5. read-only durable correlation and final health.

No installer replay, reset replay, broad process kill, provider/model substitution, manual config/SQLite mutation, source/test/workflow edit, Release/tag mutation, or force push occurred.

## Phase A/B — stale reset adjudication

The reset tree was revalidated with exact PID, parent, executable, command line, and creation-time identity. Two samples were captured at:

```text
sample-1: 2026-08-31T18:35:36.406772+00:00
sample-2: 2026-08-31T18:36:12.698253+00:00
interval: 36.291481 seconds
```

The same logical reset invocation was present at both samples:

```text
PID 9840
PPID 10724 (parent no longer existed at final revalidation)
Executable: C:\\Users\\CDQ-P\\AppData\\Local\\CogentNexus-OpenClaw\\runtime\\python\\Scripts\\python.exe
Command: host_control_v092.py --root C:\\Users\\CDQ-P\\.openclaw\\workspace\\.cogentnexus-openclaw reset --provider ollama
Creation: 1788186963.6185184

PID 17360
PPID 9840
Executable: C:\\Users\\CDQ-P\\AppData\\Roaming\\uv\\python\\cpython-3.11-windows-x86_64-none\\python.exe
Command: host_control_v092.py --root C:\\Users\\CDQ-P\\.openclaw\\workspace\\.cogentnexus-openclaw reset --provider ollama
Creation: 1788186963.6370635
```

Creation-time proximity was approximately 19 ms and argv was identical, supporting one launcher-to-underlying-Python reset invocation rather than two independent resets. The tree also contained only console infrastructure PID `22140`.

Across the two samples:

```text
PID 9840: running, 1 thread, 57 handles, CPU 0.0/0.0, unchanged
PID 17360: running, 1 thread, 135 handles, CPU 0.046875/0.0625, unchanged
PID 22140: running conhost, unchanged
controller.json: size 565, hash 0433b9e1499816fbcb242a63a9f678c648ced432eed682705c5b8ca567554eed, unchanged
ownership.json: size 804, hash 081961df81f9bced0e4e72cf0bb4144e518e741ea9c010b4d7674404a1f247b6, unchanged
SQLite: size 204800, hash 2fdad8a81983a1c8c7452d1c65d6743f2d22cc7318d4d707d0544826804c903e, unchanged
```

No input was sent to the reset process. No reset prompt was answered. No second lifecycle process was found against the state root. The cleanup gate passed. The reset process's exact internal wait location remains unproven.

## Phase C — identity-fenced cleanup

The permitted cleanup sequence was executed exactly once:

```text
1. terminate PID 17360 after identity revalidation
2. wait boundedly
3. revalidate PID 9840 identity
4. terminate PID 9840
```

Results:

```text
child 17360: exit 0
parent 9840: exit 0
parent 10724: not targeted
conhost 22140: not targeted directly; absent after tree cleanup
```

Post-cleanup scan proved PIDs `17360`, `9840`, `22140`, and `10724` absent. No broad process-name kill or tree-by-name kill was used.

## Phase D — coherent pre-enable gate

Read-only pre-enable probes passed:

```text
installed fingerprint: f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
ownership verify: exit 0 / PASS
Host: passthrough
startup/plugin: disabled baseline
Gateway: healthy/listening
Ollama: selected/reachable/healthy/ready
delivery: READY, pending outbox 0
recovery: READY, active incident false, attempts 0
SQLite integrity: ok
lifecycle residue against state root: none
```

Durable baseline before enable/send:

```text
tickets: 10
ticket_events: 79
cnx_direct_model_call: 10
cnx_direct_recovery: 0
cnx_assistant_delivery: 7
ticket_outbox: 0
cnx_sessions: 19
```

## Phase E — one managed recovery transition

The installed launcher was invoked exactly once through a root-only polling wrapper. No descendant-wait semantics or installer replay was used.

```text
argv: cmd.exe /d /c C:\\Users\\CDQ-P\\.openclaw\\workspace\\cnxclaw.cmd enable
root PID: 8828
started: 2026-08-31T18:37:40.838747+00:00
ended: 2026-08-31T18:41:08.764566+00:00
duration: 207.922 seconds
exit code: 0
stdout bytes: 74810
stderr bytes: 0
enable invocation count: 1 / 1
```

Managed convergence read-back passed:

```text
Host mode: managed
desired Gateway: running
desired provider: running
selected provider: ollama
startup policy: enabled
startup adapter: installed=true, State=Ready, Enabled=true, LastTaskResult=0
plugin cogentnexus-openclaw: version 0.9.3, enabled=true, status=loaded
plugin diagnostics: none
Gateway: healthy, connectivity probe ok, listening 127.0.0.1:18789
Ollama: installed/reachable/healthy/ready
Delivery: READY, pending terminal deliveries 0
Recovery: READY, active incident false, recovery attempts 0
SQLite integrity: ok
Installed fingerprint: exact expected candidate
```

The post-enable durable counts remained the baseline counts listed above. No semantic activity occurred during enable.

## Phase F — human Discord Send boundary

After managed convergence, Hermes generated one nonce:

```text
CNX204-20260831T184201Z-db4a02
```

The operator was instructed to send exactly once:

```text
ตอบกลับข้อความนี้เพียงว่า CNX204-20260831T184201Z-db4a02
```

The operator replied `ส่งแล้ว`, so the human Send boundary was recorded as consumed:

```text
human Discord Send: 1 / 1
Hermes/bot/API/injection: 0
retry: 0
regenerate: 0
second message: 0
second room: 0
```

Afterward the operator corrected the room identity, stating that the visible room was the previously failing room and not the intended healthy acceptance surface. The desktop window metadata at inspection showed:

```text
Discord window title: #คุยกัน | Lobby 404 - Discord
```

The room/session identity was therefore not accepted as the task-designated healthy acceptance room. This is a semantic acceptance-boundary failure, not proof that the product failed in the intended room.

Per the task's one-shot fence, the operator's correction did not authorize another message or another room. No additional Send, Enter, retry, regenerate, API send, or injection was performed.

## Phase G — durable correlation

Immediate read-only durable inspection was captured at:

```text
2026-08-31T18:43:49.882594+00:00
```

A final read-only inspection after the room correction was captured at:

```text
2026-08-31T18:44:33.011040+00:00
```

Both inspections showed no occurrence of the nonce in any searched text/prompt/result/content/message/request/run/session field and no new durable rows.

Final counts:

```text
tickets: 10
ticket_events: 79
cnx_direct_model_call: 10
cnx_direct_recovery: 0
cnx_assistant_delivery: 7
ticket_outbox: 0
cnx_sessions: 19
SQLite integrity: ok
```

Correlated nonce matches:

```text
none
```

Therefore the required chain was not proven:

```text
1 human Send -> 1 Ticket -> 1 Direct model call -> response_ready ->
1 native visible Discord result -> delivery_confirmed -> completed
```

Specifically:

```text
Ticket for nonce: NOT FOUND
model call for nonce: NOT FOUND
delivery for nonce: NOT FOUND
recovery for nonce: NOT FOUND
outbox residue for nonce: NOT FOUND
```

The absence is preserved as evidence. It is not relabeled as a proven `before_agent_run` product failure because the Send was made in a room the operator later identified as the known failing room and the exact durable binding is absent.

## Phase H — final state

The managed runtime remained healthy after the failed semantic acceptance boundary:

```text
Host: managed
startup adapter: enabled/Ready
plugin: enabled/loaded
Gateway: healthy
Ollama: ready
delivery: READY, outbox 0
recovery: READY, no active incident
SQLite integrity: ok
installed fingerprint: exact candidate
stale reset PIDs: absent
```

No later semantic action was attempted.

## Acceptance matrix

| Criterion | Result | Evidence |
|---|---|---|
| exact stale reset identity | PASS | PID/creation/argv/lineage |
| reset stale/no-progress gate | PASS | two unchanged samples |
| exact child cleanup | PASS | PID 17360 exit 0, absent |
| exact parent cleanup | PASS | PID 9840 exit 0, absent |
| no broad kill | PASS | only 17360 and 9840 targeted |
| pre-enable health | PASS | exact fingerprint/ownership/health |
| one enable | PASS | PID 8828, exit 0, 1/1 |
| managed Host | PASS | mode managed |
| startup/plugin convergence | PASS | Ready/enabled/loaded |
| Gateway/Ollama | PASS | healthy/ready |
| delivery/recovery/SQLite | PASS | READY/zero pending/ok |
| human Send budget | CONSUMED | 1/1 |
| correct healthy acceptance room | FAIL | operator identified room as previously failing |
| nonce durable correlation | FAIL / NOT FOUND | no nonce/Ticket/model/delivery delta |
| retry/second room | 0 | correctly not performed |

## Issue register

### I-01 — Historical reset tree

- **Observed:** old `9840 -> 17360` reset invocation remained alive.
- **Product effect:** blocked pre-enable gate.
- **Action:** exact authorized child/parent cleanup only.
- **Result:** residue removed; no root cause claimed.

### I-02 — Human Send room mismatch

- **Observed:** after `ส่งแล้ว`, operator stated the visible room was the previously failing room rather than the designated healthy acceptance room.
- **Product effect:** one-shot semantic acceptance is invalid/unfulfilled for Task 204.
- **Action:** no retry or second room, per hard fence.
- **Remaining consequence:** intended healthy-room Discord requalification remains unproven.

### I-03 — No durable nonce binding

- **Observed:** exact nonce search returned no matches; all durable counts stayed at baseline.
- **Classification:** NOT FOUND / NOT PROVEN, not a claimed root cause.
- **Action:** read-only inspection only.
- **Remaining consequence:** Ticket/model/delivery chain cannot be assigned to this Send.

### I-04 — UI/window identity uncertainty

- **Observed:** Discord window title was `#คุยกัน | Lobby 404 - Discord`; the operator later identified it as the failed room.
- **Classification:** semantic surface mismatch confirmed by operator statement; numeric internal session mapping not inferred.
- **Action:** no UI correction or second Send.

### I-05 — Separate harness/probe considerations

- **Observed:** previous Task-202 collector issues and broad process scans included shell self-matches.
- **Classification:** harness evidence only; no effect on enable result or semantic ledger.
- **Action:** final nonce query used direct read-only SQLite mode and preserved its own output.

## Mutation ledger

```text
stale reset child termination (17360): 1 authorized
stale reset parent termination (9840): 1 authorized
installer/install-over replay: 0
reset replay/input injection: 0
cnxclaw enable: 1 authorized
additional enable: 0
Gateway/provider lifecycle outside enable: 0
manual config/SQLite/provider mutation: 0
broad process kill: 0
source/test/workflow edit: 0
Release/tag/asset mutation: 0
human Discord Send: 1 / 1 consumed
Hermes/bot/API/injected send: 0
retry/regenerate/second message/second room: 0
force push: 0
```

## Final disposition

```text
FAIL_DISCORD_SEMANTIC_DELIVERY
```

Cleanup and managed convergence passed. The one human Send was consumed in the room later identified by the operator as the previously failing room; the nonce produced no durable Ticket/model/delivery correlation. The acceptance cannot be retried or moved to another room under Task 204. Further Discord qualification requires a new task with a new semantic budget and explicit room/session preparation.

## Evidence manifest

```text
cnx204-capture-reset.py
sample-1.json
sample-2.json
cleanup-start.txt
child-exit.txt
parent-exit.txt
cleanup-post.json
gate-*.stdout
gate-*.stderr
gate-*.exit
enable-rootpoll.py
enable.meta.json
enable.stdout
enable.stderr
post-*.stdout
post-*.stderr
post-*.exit
discord-initial.json
discord-final-readonly.json
```

No credentials, tokens, passwords, or connection strings were recorded.
