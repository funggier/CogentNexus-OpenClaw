# CNX-20260831-198 — Discord Session Correlation and Durable Delivery Investigation

**Disposition:** `REQUALIFICATION_SCOPE_EXPANSION_REQUIRED`

## Scope and authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Coordination branch: `agent/v0.9.3-full-stabilization`
- Published v0.9.3 remains immutable at public tag target:
  `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Task 198 repaired branch candidate:
  `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- Task 199 read-only evidence report commit:
  `28e738e10b4977a56124eb4c9181ce5cbe7622b6`
- No v0.9.3 tag/Release/asset was republished, retargeted, or modified.
- No provider/model substitution, reset, uninstall, fresh reinstall, state deletion, or live Discord retry was used to obtain repository GREEN.

## Task 199 evidence review

Task 199 recovered the retained Windows/OpenClaw/SQLite evidence without sending any new Discord message.

The historical generic log line:

`before_agent_run hook failed; blocking request`

was retained, but the original handler exception/stack for that old blocked attempt was not recoverable from the remaining logs. Therefore this report does **not** claim which exact historical writer or lifecycle action owned the SQLite lock at that instant.

Task 199 also established that the durable Tickets attributable to both investigated Discord sessions eventually completed through the normal Direct lifecycle. Session A additionally had session deletion/generation churn, but that correlation alone is not sufficient to identify the historical exception owner.

## Delivery-contract findings

Source/test tracing rejected two misleading hypotheses from the Task 196 surface symptoms.

1. `missing-run-correlation` / `missing-append-before-deliver` are redacted diagnostic skip reasons emitted by the Dashboard verified-delivery observer. Those paths return without throwing and are not, by themselves, the cause of a Discord request being blocked.
2. A native non-Dashboard Direct reply is not required to create a `cnx_assistant_delivery` row. The base Ticket path can persist `response_ready`, receive native channel delivery confirmation through `message_sent`, invoke `confirmDirectDelivery(runId)`, and then persist `delivery_confirmed` plus `completed` directly on the Ticket.

Therefore the successful Discord Session-B shape with no `cnx_assistant_delivery` row is compatible with the native external-channel delivery contract.

## Root-cause invariant isolated

OpenClaw `2026.7.1-2 (0790d9f)` configures `before_agent_run` hook failures as fail-closed. Any uncaught exception in CogentNexus-OpenClaw Ticket-first admission can therefore reject a fresh human message before model inference.

The exact v0.9.3 source had this sequence inside Ticket-first admission:

`before_agent_run -> new TicketStore(...) -> TicketStore.accept(...)`

`TicketStore.open()` sets `PRAGMA busy_timeout=5000`. A deterministic integration reproduction showed that when another SQLite connection owns an `IMMEDIATE` writer transaction for slightly longer than five seconds, `TicketStore.accept()` throws:

```text
ERR_SQLITE_ERROR
errcode: 5
database is locked
```

That exception propagated out of the Ticket-first `before_agent_run` handler. OpenClaw then converted the handler exception into its fail-closed blocked-request behavior.

The proven violated invariant is therefore:

> A bounded transient SQLite writer-contention interval can escape Ticket-first admission as an uncaught `before_agent_run` exception and block fresh human Discord intent.

The repository evidence proves this defect mechanism. It does not prove which historical component held the writer lock during the original Task-196 blocked attempt.

## TDD RED

Regression test added:

`plugins/cogentnexus-openclaw/src/v198-discord-ticket-contention.test.ts`

RED commit:

`4df2e73d621ceed193a6fcbf27769fadd09291ea`

Validate run:

`33413191568`

Ubuntu job:

`99557484396`

The integration test uses:

- a real temporary SQLite database;
- a separate Node process holding `BEGIN IMMEDIATE` for 5.5 seconds;
- the real Ticket-first `before_agent_run` path;
- a Discord-shaped owner session;
- a fresh direct prompt and run identity.

Observed RED:

```text
promise rejected Error: database is locked instead of resolving
code: ERR_SQLITE_ERROR
errcode: 5
errstr: database is locked
```

Stack authority:

```text
TicketStore.open -> TicketStore.accept -> index.ts before_agent_run
```

At the RED commit, the plugin suite result was exactly:

- 275 passed
- 1 failed — the new contention regression

The existing suite therefore remained green while the new test reproduced the missing invariant.

## Minimal repair

Production module added:

`plugins/cogentnexus-openclaw/src/v198-ticket-admission-contention.ts`

Wiring change:

`plugins/cogentnexus-openclaw/src/ticket-dispatcher.ts`

Repair commits:

- `c59e15511409819bf62422c1c21a232bc60afcc5` — bounded contention retry implementation
- `9f4eaa429b2540540e7d6f6c2af99067960e45fb` — release-runtime wiring

The repair is deliberately narrow:

1. patch `TicketStore.accept()` once at runtime registration/module load;
2. retry exactly once only when all of these are true:
   - `code === ERR_SQLITE_ERROR`;
   - `errcode === 5`;
   - diagnostic text identifies `database is locked` or `database is busy`;
3. all other errors rethrow immediately;
4. a second contention failure rethrows normally;
5. each attempt retains the existing five-second SQLite busy timeout.

Persistent writer contention therefore remains bounded and fail-closed; the repair does not bypass Ticket-first durability and does not weaken authorization, delivery, recovery, provider, or lifecycle fences.

Exact diff from the Task-199 report commit to the repaired candidate is only:

1. `plugins/cogentnexus-openclaw/src/ticket-dispatcher.ts`
2. `plugins/cogentnexus-openclaw/src/v198-discord-ticket-contention.test.ts`
3. `plugins/cogentnexus-openclaw/src/v198-ticket-admission-contention.ts`

## GREEN verification

Exact repaired candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

### Validate

Run:

`33413832703`

Terminal result:

`completed / success`

Matrix completed successfully across:

- Ubuntu / Python 3.11
- Ubuntu / Python 3.14
- macOS / Python 3.11
- macOS / Python 3.14
- Windows / Python 3.11
- Windows / Python 3.14

Observed Ubuntu 3.11 evidence included:

- Python: `475 passed, 33 skipped, 4 subtests passed`
- plugin test files: `55 passed`
- plugin tests: `276 passed`
- new contention regression: PASS in approximately 5.56 seconds
- evaluation: PASS
- `npm audit --omit=dev`: 0 vulnerabilities
- plugin validation/package verification: PASS

Windows validation also completed successfully, including the Windows workflow self-test, PowerShell syntax checks, acceptance serializer smoke, exact root-process exit capture, npm tests/evaluation/audit, and plugin validation.

### Windows Installer Pack Smoke

Run:

`33413832709`

Terminal result:

`completed / success`

### PS5.1 Acceptance Smoke

Run:

`33413832777`

Serializer job:

`99559640385`

Terminal result:

`completed / success`

## Exact package proof

Validate artifact:

- artifact ID: `9766213750`
- name: `cogentnexus-openclaw-v0.9.3-package-proof-9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- artifact size: `5,410,395` bytes
- artifact ZIP digest:
  `f8190f9a1fe347be47c69fb9d9a6df2ade2edf8666fd25bfe57efff233f109d7`

Package identity:

- source commit: `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- package version: `0.9.3`
- payload file count: `190`
- payload-v2 fingerprint:
  `db5fbd96630ac3685c0588e3d5009dce68e0052bc03f8dab5fdb29577410b27d`

Archive digests:

- `cogentnexus-openclaw-v0.9.3.tar.gz`
  `379f0b4a7c12d4f350e0d3065dd25c7ab2bde80089adb16bfa64d6bbc673cdfb`
- `cogentnexus-openclaw-v0.9.3.zip`
  `07bcdc45810c86efb5535075e1e560f9477e65a1f72e5299d75dea6dbc542d3e`

## Why Task 198 is not final PASS yet

The repaired candidate changes production plugin bytes. Repository RED -> GREEN proves the isolated contention invariant, but the accepted live Windows host still needs proportional requalification of the changed runtime surface.

Required live closure is intentionally smaller than a fresh lifecycle acceptance:

1. supported install-over of exact candidate `9f4eaa...`;
2. prove installed repaired plugin/package identity;
3. prove Gateway, managed Ollama provider, recovery/delivery state and SQLite integrity remain healthy;
4. exactly one genuine human Discord Send in a known healthy Discord room;
5. prove one Ticket / one model call / one visible native Discord result / `delivery_confirmed` / `completed` with no duplicate or recovery residue;
6. prove the tested send does not produce `before_agent_run hook failed`.

The live test must not artificially lock production SQLite. The deterministic repository test already owns that reproduction. Live acceptance checks for transport/runtime regression only.

A `cnx_assistant_delivery` row is not an acceptance requirement for the native Discord Direct path. A remaining `missing-run-correlation` Dashboard-observer diagnostic is also not a failure by itself if the actual Ticket/native-delivery lifecycle is correct.

## Final disposition

```text
REQUALIFICATION_SCOPE_EXPANSION_REQUIRED
```

Repository diagnosis and repair are accepted as RED -> GREEN at exact candidate `9f4eaa429b2540540e7d6f6c2af99067960e45fb`.

Task 198 requires one separate bounded Windows/Discord requalification task before it can be closed `PASS`.