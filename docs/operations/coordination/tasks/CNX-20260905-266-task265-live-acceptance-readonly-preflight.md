# CNX-20260905-266 — Task265 Live Acceptance Read-Only Preflight

## Objective

Prepare the exact live acceptance packet for the Discord manual session Delete -> recreated session -> first-message path, without performing any live mutation.

## Authority

Task266 is read-only live inspection plus repository/docs evidence only.

Hermes may inspect:

- current installed CogentNexus/OpenClaw plugin root and fingerprint/version identity;
- current Gateway/process/plugin/runtime identity and health;
- current CogentNexus SQLite state read-only, including owner session row/generation/session_id and nonterminal Tickets/outbox/recovery associated with the target Discord session;
- current OpenClaw Discord session metadata read-only where supported;
- exact candidate/package identity for Task265 source candidate `ec1fdbb2ea036c6dcd1c375b8171868335d63fc8`;
- whether deployment is required before live acceptance;
- exact one-shot action sequence and rollback/stop conditions for the later live task.

## Required outputs

1. Prove current installed plugin fingerprint/source identity, or record that it cannot be proven.
2. Compare installed identity to Task265 candidate/package identity.
3. Identify the intended Discord session key/session ID without deleting or resetting it.
4. Read-only inspect whether deleting that session would abandon any nonterminal Ticket, pending outbox, assistant delivery, direct recovery, or workflow completion.
5. Produce an exact proposed live sequence for a later authorized task, including as applicable:
   - candidate install-over / process boundary if installed code is older;
   - post-deployment fingerprint and Gateway process proof;
   - one explicit manual session Delete;
   - one benign first Discord test message;
   - proof of new sessionId / fresh CNX generation;
   - proof old-generation work did not revive/rebind/redeliver;
   - delivery confirmation for the first new message.
6. State every live side effect that would require explicit authorization.

## Hard fences

```text
installer/install-over/uninstall/reset           = 0
Gateway/provider/service lifecycle mutation      = 0
live OpenClaw session delete/reset                = 0
live Discord/Dashboard/API semantic send         = 0
manual live Ticket/session/SQLite mutation       = 0
recovery replay/redelivery/disposition            = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

Read-only live inspection is authorized. If a read-only query would itself trigger mutation or semantic delivery, do not perform it.

## Validation/reporting

Publish:

`docs/operations/coordination/reports/CNX-20260905-266-task265-live-acceptance-readonly-preflight.md`

The report must include exact observed identities, current nonterminal-state risk, candidate-vs-installed comparison, proposed one-shot live acceptance ledger, and any blocker/uncertainty.

After publication set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` and stop mutation.
