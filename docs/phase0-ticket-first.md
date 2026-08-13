# Phase 0: Ticket-first intake

Status: implemented as an opt-in prototype; disabled by default.

## Invariant

For an eligible owner command, the `before_agent_run` hook must commit the complete command and an `accepted` event to SQLite before inference is allowed to continue. If the transaction fails, the OpenClaw input gate fails closed and the model does not receive an unrecorded command.

## Integration evidence

- OpenClaw exposes `before_agent_run` as an input gate with `pass` and `block` outcomes.
- The installed runner applies a 15 second default timeout and fail-closed policy to this hook.
- CogentNexus already registers this hook at priority 2000 for deterministic durable admission.
- The Phase 0 ticket write is synchronous, local, transaction-bound, and occurs before classification or workflow compilation.

## Storage contract

- Database: `.cogent/runtime/cogentnexus.sqlite3` by default.
- SQLite: WAL mode, foreign keys enabled, 5 second busy timeout.
- `tickets` stores the full prompt, its SHA-256, trusted owner session, run identity, and state.
- `ticket_events` is append-only evidence of accepted commands.
- `(owner_session_key, run_id)` is hashed into a unique request key, making hook retries idempotent.

Initial state transitions are deliberately narrow:

`accepted -> planned -> running -> waiting|completed|failed|cancelled`

Phase 0.1 adds atomic claims, expiring leases, heartbeats, monotonically increasing fencing generations, completion commits, and a deterministic recovery scanner. The scanner makes expired `running` Tickets `waiting` and records `lease_expired`; it never calls an LLM. A new worker must claim the Ticket and receive a new token and generation before acting. An old worker cannot heartbeat or complete after reassignment.

The scanner is registered only when `ticketFirst` is enabled and defaults to a 15-second interval. Dispatching `waiting` Tickets into bounded executors and terminal outbox delivery remain later increments.

## Phase 0.2: bounded dispatch and terminal delivery

- Existing Phase 0 databases are upgraded in place through recorded schema migrations; accepted Tickets are preserved.
- The dispatcher selects only `accepted` or `waiting` Tickets, claims each atomically, and enforces a caller-supplied bound capped at 32.
- Every Ticket has a retry ceiling configured by `ticketMaximumAttempts` (default 3, maximum 20). Transient, timeout, validation, and capability failures may requeue below that ceiling. Authorization and permanent failures terminate immediately.
- A terminal completion or exhausted retry writes exactly one owner-bound outbox row in the same transaction as terminal state.
- Outbox delivery uses a deterministic OpenClaw schedule tag. Failed delivery remains pending with attempt/error evidence.
- `cogent_ticket_status` exposes queue counts, expired running leases, and pending outbox count directly from SQLite without inference.

The dispatcher is a contract in this increment: no generic Ticket executor is started automatically. Connecting Tickets to the existing verified workflow compiler is required before live activation.

## Phase 0.3: verified workflow bridge and resource admission

- With `ticketFirst` enabled, durable intake now returns a queued Ticket gate after the Ticket is committed and routed; the conversational model is not used to launch it.
- The opt-in Ticket service admits work before claim using observed free memory, free disk, and linked-running concurrency. Defaults are one running workflow and 512 MiB free memory/disk.
- An admitted Ticket is compiled through the existing bounded workflow compiler, started with the trusted Ticket owner, and linked under the current lease token and fencing generation.
- The service heartbeats non-terminal linked workflows and atomically commits terminal workflow evidence into the Ticket result and owner outbox.
- After a worker disappears, lease recovery requeues the Ticket; a restarted service reuses an existing active workflow by request fingerprint and links it under a newer fencing generation.
- Dispatch interval, bound, lease, resource thresholds, and maximum running workflows are configurable, but `ticketFirst` remains disabled by default.

## Verified prototype checks

- A committed ticket remains readable from a fresh database connection.
- A repeated hook invocation for the same owner/run returns the original Ticket.
- Known internal continuation messages are excluded from creating recursive Tickets.
- Invalid/corrupt storage raises an error; it cannot silently admit an unrecorded command.
- Only one worker can claim a Ticket, expired leases are recovered deterministically, and reassignment increments the fencing generation.
- A stale worker cannot heartbeat or complete after recovery; the current worker can renew and commit.
- Existing plugin tests, TypeScript compilation, and OpenClaw plugin validation remain green.

## Safety switch

Set plugin option `ticketFirst: true` only after build, unit, plugin validation, restart, and controlled kill/recovery tests pass. No active OpenClaw configuration is changed by this prototype.
