# CNX-20260901-204 Review — Stale Reset Cleanup / Managed Recovery / Discord Room Mismatch

Disposition: `ACCEPT_FAIL_DISCORD_SEMANTIC_DELIVERY__CORRECT_ROOM_REQUALIFICATION_REQUIRED`

## Accepted Task-204 result

Task 204 correctly completed the stale historical reset adjudication and identity-fenced cleanup, then restored the already-installed repaired candidate to a healthy MANAGED runtime with exactly one `cnxclaw.cmd enable` invocation.

Accepted successful boundaries:

- historical reset tree `9840 -> 17360` was revalidated as stale/no-progress and removed without broad process termination;
- installed repaired fingerprint remained `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`;
- ownership verify passed;
- enable invocation count was exactly `1 / 1` and exited `0`;
- Host converged to `managed`;
- startup adapter became installed/enabled/Ready;
- plugin became enabled/loaded;
- Gateway and Ollama were healthy;
- delivery/recovery were READY with outbox `0`;
- SQLite integrity was `ok`;
- stale reset processes were absent after cleanup.

## Discord result classification

The Task-204 human Send was made in a room that the operator later identified as the wrong / previously failing Discord room. The intended acceptance surface was not exercised.

The consumed nonce `CNX204-20260831T184201Z-db4a02` produced:

- no matching Ticket;
- no matching direct model call;
- no matching delivery;
- no recovery row;
- no outbox residue;
- no durable count delta.

Therefore Task 204's final `FAIL_DISCORD_SEMANTIC_DELIVERY` is accepted as an **acceptance-surface mismatch**, not as proof that the repaired product fails in the intended healthy room.

A second Send was correctly not attempted under Task 204 because its one-shot budget had already been consumed.

## Current runtime authority

Task-204 final read-only state is accepted as the starting point for the successor:

- Host: managed;
- startup: enabled/Ready;
- plugin: enabled/loaded;
- Gateway: healthy;
- Ollama: ready;
- delivery: READY / outbox 0;
- recovery: READY / no active incident;
- SQLite integrity: ok;
- installed repaired fingerprint: exact;
- lifecycle residue: absent.

No reset, installer, install-over, additional enable, provider/model change, source change, or Release mutation is needed before the successor Discord-only qualification unless fresh read-only preflight proves drift.

## Frozen authorities

- repaired product candidate: `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- installed repaired fingerprint: `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`
- published `v0.9.3` target: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- intended Discord owner session: `agent:main:discord:channel:1531199905673252946`
- intended numeric channel ID: `1531199905673252946`

## Successor authorization

The user's explicit instruction after Task 204 is to repeat the Discord qualification because the previous Send was made in the wrong room.

A successor task may grant a **new independent human Send budget of exactly `1 / 1`** for the correct room only. This is not a retry within Task 204; it is a new acceptance attempt with a new nonce and explicit room-identity gate.

Before generating the nonce, Hermes must prove the active/selected Discord acceptance surface corresponds to numeric channel/session identity `1531199905673252946`. A room name or window title alone is insufficient.

If exact room identity cannot be established, stop without consuming the new Send budget.

No lifecycle mutation is authorized in the successor unless fresh read-only health has materially drifted; in that case stop for review rather than forcing convergence.
