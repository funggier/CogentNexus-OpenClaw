# CNX-20260830-150 — Runtime Lifecycle Stop/Start/Restart/Disable/Enable Acceptance Review

## Disposition

**ACCEPT**

Task 150 is accepted as the real-Windows runtime lifecycle acceptance for the frozen v0.9.3 candidate.

## Evidence reviewed

- Task report: `docs/operations/coordination/reports/CNX-20260830-150-runtime-lifecycle-stop-start-restart-disable-enable-acceptance.md`
- Report commit: `b285257a411a7242a79abafde4f6053e92354985`
- Accepted production implementation: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Accepted installed plugin fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`
- Accepted installed ownership-helper SHA-256: `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`

The publication commit adds only the matching Task-150 report. No production source, configuration, lifecycle code, or coordination authority was changed by the executor report publication.

## Review findings

The authorized sequence was executed exactly once per lifecycle command, in the required order:

`stop → start → restart → disable → enable`

Observed postconditions match the source contract:

- `stop`: controller entered `maintenance`, desired Gateway/provider became `stopped/stopped`, Gateway and Ollama were verified stopped;
- `start`: controller returned to `managed`, Gateway and Ollama became healthy through product-owned lifecycle;
- `restart`: Gateway PID changed `21316 → 17464`, proving a real process boundary, then health returned;
- `disable`: controller entered `passthrough`, CNX plugin became disabled, native OpenClaw Gateway remained healthy;
- `enable`: controller returned to `managed`, CNX plugin became enabled/loaded, Gateway/Ollama/recovery/delivery returned healthy.

The initial STOP verifier incorrectly classified expected intentional-maintenance `READY_WITH_WARNINGS` probes as lifecycle failure. This does not invalidate the run because no lifecycle command was repeated and no mutation was used to repair state. The executor corrected only the read-only assertion against the already-consumed STOP evidence, proved the STOP contract, then continued. The no-retry fence remained intact.

Across the complete sequence:

- accepted plugin/ownership provenance remained unchanged;
- SQLite integrity remained `ok`;
- semantic table counts remained zero;
- pending outbox remained zero;
- no manual OpenClaw/Ollama/process lifecycle was used outside the product command;
- Dashboard semantic Sends remained zero.

## Plan position

The Full Stabilization and Final Acceptance Plan orders live acceptance as:

`M clean uninstall → N fresh install → O install-over/reset/uninstall/reinstall lifecycle → P final Dashboard semantic/durable-delivery proof → Q final acceptance matrix`.

Task 150 closes the remaining Phase-O normal runtime transition evidence. There is no separate reboot/crash gate required by this plan between Phase O and Phase P.

## Successor

Open one narrowly bounded Phase-P task for the final Firefox Dashboard semantic/durable-delivery acceptance.

It must be single-attempt and must preserve the repaired Task-138 invariant: the visible final response is not sufficient. PASS requires durable final capture, exactly one `cnx_assistant_delivery` direct-result row, native delivery confirmation, Ticket `completed`, and no duplicate inference or delivery.

No release/tag/merge is authorized by this review.