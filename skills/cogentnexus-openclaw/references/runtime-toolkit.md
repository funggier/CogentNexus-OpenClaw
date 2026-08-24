# Runtime Toolkit

Use one deterministic CLI for durable state, bounded execution, environment observations, verification evidence, and append-only history.

## Storage and integrity

Runtime data defaults to `.cogentnexus-openclaw/tasks/<task-id>/`:

- `state.json`: latest committed snapshot
- `revisions/<revision>.json`: immutable snapshots
- `ledger.jsonl`: append-only events
- `verification.json`: latest evidence report
- `transaction.json`: temporary crash-recovery journal
- `.lock`: short-lived cross-process writer lock

Every command recovers a prepared transaction before reading mutable task data. Override storage with `--root` for isolated tests.

## Task and state

```powershell
python skills/cogentnexus-openclaw/scripts/cogent.py task init --task-id CNX-001 --goal "Goal"
python skills/cogentnexus-openclaw/scripts/cogent.py state inspect --task-id CNX-001
python skills/cogentnexus-openclaw/scripts/cogent.py state commit --task-id CNX-001 --status executing --current-step "step"
python skills/cogentnexus-openclaw/scripts/cogent.py state rollback --task-id CNX-001 --revision 1
```

Rollback creates a new revision and never erases ledger history.

## Record semantic events

Record facts and operational rationale, not chain-of-thought:

```powershell
python skills/cogentnexus-openclaw/scripts/cogent.py ledger append --task-id CNX-001 --type DECISION --summary "Use smaller batches" --data reason=memory-pressure
python skills/cogentnexus-openclaw/scripts/cogent.py ledger append --task-id CNX-001 --type FAILURE --summary "Generator timed out" --data class=timeout
```

Manual event types are ACTION, OBSERVATION, DECISION, and FAILURE. Runtime-owned lifecycle event types cannot be forged through this command. Values for keys resembling password, token, secret, authorization, or API keys are redacted.

## Execute

```powershell
python skills/cogentnexus-openclaw/scripts/cogent.py run --task-id CNX-001 --step compile --command "python -m py_compile artifact.py" --timeout 120
```

`run` does not invoke a shell. It records a sanitized ACTION followed by OBSERVATION or FAILURE, including duration, exit code, and bounded output. Use direct tools for operations that cannot be represented safely as an argument vector, then append the semantic event explicitly.

## Probe

```powershell
python skills/cogentnexus-openclaw/scripts/cogent.py probe all --task-id CNX-001
```

Probe results are timestamped observations, not permanent facts.

## Verify and complete

```powershell
python skills/cogentnexus-openclaw/scripts/cogent.py verify run --task-id CNX-001 --exists artifact.py --hash artifact.py --command "python test_artifact.py"
python skills/cogentnexus-openclaw/scripts/cogent.py state commit --task-id CNX-001 --status completed --artifact artifact.py
```

Verification records the current state revision and artifact SHA-256. Completion is rejected when:

- verification is not PASS;
- state changed after verification;
- a declared artifact lacks verified hash evidence;
- an artifact hash changed after verification.

Run verification again after any state or artifact change.

## Audit

```powershell
python skills/cogentnexus-openclaw/scripts/cogent.py ledger tail --task-id CNX-001
python skills/cogentnexus-openclaw/scripts/cogent.py ledger validate --task-id CNX-001
```

Validation checks JSON structure, sequence continuity, task identity, event types, pending transactions, and stale lock state.
