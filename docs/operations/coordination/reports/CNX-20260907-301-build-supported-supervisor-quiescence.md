# CNX-20260907-301 — Build Supported Supervisor Quiescence Mechanism

## Disposition

`NEEDS_CHATGPT__REPOSITORY_TDD_QUIESCENCE_REPAIR_GREEN__LIVE_REQUALIFICATION_NOT_AUTHORIZED`

Task301 repository repair is complete and validated. A task-scoped atomic Supervisor quiescence lease now provides a supported coordination boundary for a future bounded enable transaction. No live deployment, Scheduled Task mutation, service lifecycle action, config mutation in the live installation, or `cnxclaw enable` was performed.

## Method and rationale

The repair uses an atomic lease file under the CogentNexus runtime root:

```text
<root>/host/supervisor-quiescence.json
```

The lease is created with exclusive file creation (`O_CREAT|O_EXCL`), written with a schema version, owner, random token, acquisition time, and expiry, then flushed with `fsync`. This prevents two cooperating CogentNexus writers from simultaneously owning the task-scoped boundary without mutating or disabling the Windows Scheduled Task.

The Supervisor checks the lease before Gateway/provider/runtime probes. An active lease returns an observable `result=quiesced` fast path and performs no reconciliation work. An expired lease is visible as stale and may be reclaimed only after comparing the observed lease contents immediately before removal. Owner/token mismatch fails closed. A bounded wait reports timeout without replacing the existing owner. A crash leaves an expiring lease; the next owner can reclaim it only after expiry. Release is owner-scoped and idempotent when the lease is already absent.

The managed `enable` owning boundary acquires the lease before its config transaction and releases it on success or the transactional failure path. This prevents the recurring Supervisor from entering its writer path while enable is staging/committing native configuration. The existing transactional rollback remains responsible for product state; the lease only coordinates writers and does not settle Tickets or delivery.

## TDD evidence

### RED

A new test module was written before the production module existed. The first run failed during collection with:

```text
ModuleNotFoundError: No module named 'supervisor_quiescence'
```

This demonstrated the requested API was not already present.

After the minimal module was added, the first behavior run exposed three contract/fixture failures: virtual timestamps were read against wall clock, immediate contention returned timeout rather than busy, and the test attempted to read owner from a stale read result. Those were corrected in the test contract and minimal immediate-contention behavior.

### GREEN

Focused quiescence and host integration tests:

```text
6 passed in 0.09s
```

Relevant Host/control/writer-lock regression set:

```text
25 passed in 1.57s
```

Full repository suite after isolating the Host module import from cross-test module overlays:

```text
537 passed, 5 skipped, 4 subtests passed in 109.51s
```

The initial full-suite failure was a test harness module-state collision (`idle` instead of `quiesced`) caused by another test overlaying the shared `host` module. The test was changed to load the owning file under an isolated module name; the rerun passed.

## Files changed

```text
skills/cogentnexus-openclaw/scripts/supervisor_quiescence.py
skills/cogentnexus-openclaw/scripts/host.py
skills/cogentnexus-openclaw/scripts/host_authority_v091.py
tests/test_supervisor_quiescence.py
docs/operations/coordination/ACTIVE.md
docs/operations/coordination/STATUS.md
```

The new focused test covers:

- acquire/release and observable restoration;
- concurrent second owner fail-closed behavior;
- stale lease reclamation and old-owner rejection;
- bounded timeout with incumbent preservation;
- idempotent release after rollback;
- Supervisor no-op/quiesced path before runtime probing.

## Future live invocation

Task301 does not authorize this invocation. A separate successor task should:

1. fresh-fetch and re-anchor the exact accepted candidate;
2. prove the installed runtime contains the exact lease/wiring repair;
3. prove target/protected Ticket and session state, health, and no competing writer;
4. invoke the canonical existing `cnxclaw enable` exactly once, allowing the owning Host boundary to acquire/release the lease automatically;
5. read back the lease as absent after success/failure, managed Host state, plugin and live worker identity, and Gateway/Ollama health;
6. observe the exact pending Ticket without retry, replay, redelivery, disposition, or manual settlement;
7. stop on any lease conflict, restoration failure, missing installed wiring, ambiguous delivery, or worker mismatch.

The proposed future command is still the existing canonical command:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable
```

The difference is that a future accepted installation must contain the repository wiring before the command is authorized. Task301 itself deliberately does not install it.

## Limitations and follow-up

- Repository tests prove the lease primitive and Host Supervisor boundary, not live adoption by the detached worker.
- No live quiescence or enable requalification was attempted because Task301 forbids live mutation.
- The lease is a file-based coordination boundary for cooperating CogentNexus writers; an unrelated external process that edits `openclaw.json` without honoring the lease can still race. A future task must verify the writer population and installed wiring.
- The current `enable` path releases on its normal success and transactional exception paths; a process crash relies on the bounded expiry/reclaim behavior. A future successor may add a context-manager wrapper and richer durable acquisition/restore telemetry if required by review.
- The pending Discord delivery remains unconfirmed; this repair does not alter Ticket, recovery, or delivery semantics.
- Credentials and sensitive values were not retained or published.

## Hard-fence accounting

```text
live cnxclaw enable: 0
live Scheduled Task mutation: 0
live service restart/reload: 0
live config mutation: 0
live installer/install-over/uninstall/reset: 0
semantic send: 0
replay/redelivery/disposition: 0
manual Ticket/SQLite/session/transcript mutation: 0
protected-state mutation: 0
force push/history rewrite: 0
```

## Review decision requested

ChatGPT review is required before a successor may perform live installation/adoption or bounded enable requalification. The successor must bind its live proof to the exact repair commit and verify the lease is present in the actual installed Host/Supervisor path before invoking `cnxclaw enable`.
