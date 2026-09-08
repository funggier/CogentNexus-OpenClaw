# CNX-20260907-300 — Quiesce Supervisor and Requalify Enable

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-299`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Explicit human authorization

The human authorizes bounded quiescence of the CogentNexus Supervisor to prevent concurrent config writes while running `cnxclaw enable` one time. This does not authorize quiescing unrelated services, manual config edits, uninstall, reset, or repeated enable.

## Objective

Use the supported quiescence mechanism for the recurring CogentNexus Supervisor, run the tested `cnxclaw enable` exactly once, restore Supervisor operation, and requalify the live worker runtime alignment.

## Preconditions

Freshly verify:

- current remote HEAD and Task296 repair/tests;
- current host mode/config fingerprint and Supervisor state;
- target pending Ticket/session and protected state;
- Gateway/Ollama/Host health;
- exact supported quiescence/restore commands;
- no newer coordination state supersedes this task.

If the only available mechanism is an ad hoc unsupported Scheduled Task mutation, stop and request ChatGPT.

## Allowed bounded actions

1. Enter supported Supervisor quiescence for the enable transaction.
2. Confirm no competing CogentNexus config writer remains active.
3. Run canonical `cnxclaw enable` exactly once.
4. Restore Supervisor through its supported mechanism regardless of enable result.
5. Read-only verify managed mode, plugin/worker adoption, Gateway/Ollama/Host/Supervisor health, and pending delivery behavior.
6. Capture exact hashes, timestamps, exit codes, and rollback/restore results.

Natural existing-worker processing may continue only as an effect of successful requalification. Do not manually replay, redeliver, cancel, dispose, or settle the pending Ticket.

## Strict fences

- enable: maximum 1
- Supervisor quiescence: only CogentNexus Supervisor, bounded to transaction
- Supervisor restore: exactly once
- unrelated service/process mutation: 0
- uninstall/reset/install-over: 0
- semantic send: 0
- retry/replay/redelivery/disposition: 0
- manual config/Ticket/SQLite/session/transcript mutation: 0
- session create/delete: 0
- credential exposure/change: 0
- protected-state mutation: 0
- release/force push: 0

## Stop rules

Stop without retry if quiescence mechanism is unsupported/ambiguous, enable fails, restore fails, health degrades, worker does not adopt the tested repair, or delivery remains ambiguous. Do not infer success from Gateway health alone.

## Completion

Publish an evidence-rich report with quiescence, enable, restore, adoption, and delivery evidence. Set coordination to `WAITING_FOR_CHATGPT_REVIEW` and stop.
