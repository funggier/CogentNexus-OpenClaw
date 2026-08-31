# Review — CNX-20260831-198 Discord Session Correlation and Durable Delivery Investigation

**Review disposition:** `ACCEPTED_REPOSITORY_REPAIR__WAITING_WINDOWS_DISCORD_REQUALIFICATION`

## Reviewed authority

Task report:

`docs/operations/coordination/reports/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md`

Frozen repaired product candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Published v0.9.3 remains separate and immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Review findings

1. Task 199 correctly stopped short of inventing an unavailable historical stack trace. The retained evidence cannot identify the exact writer that caused the old blocked Discord attempt.
2. Source tracing correctly separates Dashboard observer diagnostics from the actual fail-closed before-agent path.
3. The absence of `cnx_assistant_delivery` for a successful native Discord Direct reply is not treated as a defect without architectural evidence; Ticket-level native delivery confirmation is an accepted path.
4. A deterministic real-SQLite integration reproduction established the violated invariant: transient writer contention exceeding the base five-second busy timeout can escape `TicketStore.accept()` as `ERR_SQLITE_ERROR / errcode 5 / database is locked` inside `before_agent_run`.
5. The regression was observed RED before production mutation.
6. The repair retries exactly once only for the exact transient SQLite contention class. It does not swallow unrelated errors and persistent contention remains bounded/fail-closed.
7. Exact-head validation is GREEN across Ubuntu, macOS, Windows, package dry-run, Windows installer pack smoke, and PS5.1 serializer smoke.
8. The repaired production bytes require proportional Windows/Discord reality requalification before Task 198 can be closed PASS.

## Required next boundary

Open a separate bounded Hermes task that:

- installs over the existing Windows host from exact candidate `9f4eaa429b2540540e7d6f6c2af99067960e45fb`;
- proves the installed repaired product identity;
- preserves current managed Ollama/Gateway/SQLite health;
- performs exactly one genuine human Discord Send in a known healthy room;
- proves one Ticket, one model call, one native visible reply, one `delivery_confirmed`, one `completed`, no recovery/duplicate/outbox residue, and no `before_agent_run hook failed` for that send;
- does not require `cnx_assistant_delivery` for native Discord delivery;
- does not artificially create a production SQLite writer lock.

## Review conclusion

The repository repair is accepted.

Task 198 remains open only for proportional live requalification.

```text
ACCEPTED_REPOSITORY_REPAIR__WAITING_WINDOWS_DISCORD_REQUALIFICATION
```