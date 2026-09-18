# CNX-20260918-411 — Healthy-Runtime Maintenance Marker Convergence Repair Report

## Classification

`HEALTHY_RUNTIME_MARKER_CONVERGENCE_REPAIR_IMPLEMENTED_PENDING_LOCAL_VALIDATION`

## Root cause

CNX-410 observed an active `healthy-runtime` maintenance marker while:

- Gateway was healthy;
- controller was active/managed;
- desired Gateway was running;
- supervisor snapshot was healthy;
- provider incident was closed;
- pending outbox was zero.

Source tracing of the actual v0.9.5 periodic Supervisor composition shows that the production chain ultimately reaches:

`skills/cogentnexus-openclaw/scripts/host_v091.py::supervisor_tick`

through:

```text
host_control_v092
 -> host_v092
 -> host_provider_v092.supervisor_tick
 -> _run_base_supervisor
 -> host_stall_v091.BASE_SUPERVISOR_TICK
 -> host_v091.supervisor_tick
```

The v0.9.5 `host_v091.supervisor_tick` healthy fast path checked Gateway health and durable wake authority, then returned `idle` when no work was actionable.

It did not inspect the runtime maintenance marker before that idle return.

A hard-hang restart creates:

```text
runtime/maintenance.json
active = true
recoveryPolicy = healthy-runtime
```

through `lifecycle restart`.

If the replacement Gateway becomes healthy after the restart request but before the same Supervisor invocation completes reconciliation, the next healthy/no-work tick could return `idle` forever without reaching a supported marker-retirement path.

This exactly matches the CNX-410 observed state.

## Why manual deletion is not the repair

The runtime lifecycle already owns marker retirement.

`runtime.py lifecycle start`:

- checks current Gateway health;
- does not require provider health unless `--provider` is explicitly requested;
- clears maintenance only after bounded health verification.

Therefore the repair reuses this supported contract instead of unlinking/editing maintenance state directly.

## TDD RED

Commit:

`c30b3788dafba55ebef456c119c66815359c3e05`

Modified:

`tests/test_v091_idle_recovery_hint.py`

Added regression cases:

1. healthy Gateway + `healthy-runtime` marker + execute-safe tick:
   - must not enter legacy heavy Supervisor;
   - must invoke provider-neutral `lifecycle start` exactly once;
   - supported lifecycle path retires marker;
   - tick can then return lightweight idle with reconciliation evidence.

2. healthy Gateway + `healthy-runtime` marker + read-only tick:
   - must not call lifecycle mutation;
   - must not enter legacy heavy Supervisor;
   - marker remains;
   - result is `maintenance-recovery-pending`.

The existing healthy/no-marker/no-work test remains as the regression guard that ordinary idle does not call the heavy Supervisor.

## Minimal repair

Commit:

`368073d67e75cc89b9b04b21b0ee002e76f7e82f`

Modified only:

`skills/cogentnexus-openclaw/scripts/host_v091.py`

Added:

- read-only maintenance-marker parsing;
- a narrow `healthy-runtime` reconciliation helper;
- marker reconciliation before durable wake classification / idle return.

### Execute-safe behavior

When the Gateway is already healthy and an active `healthy-runtime` marker exists:

```text
legacy.runtime(root, "lifecycle", "start", timeout=60, check=False)
```

is invoked without `--provider`.

After the call, the marker is re-read.

Only a zero lifecycle exit with the marker actually retired is classified as reconciled.

The Supervisor then proceeds to the canonical `classify_wake()` decision.

If there is no actionable durable work it still returns the normal lightweight idle shape, augmented with:

`maintenanceRecovery.status = reconciled`

### Read-only behavior

When `execute_safe=false`, the marker is observed but no lifecycle call occurs.

The result is:

`maintenance-recovery-pending`

with `heavyPath=false`.

### Incomplete behavior

If supported lifecycle verification fails or the marker remains after the call:

`maintenance-recovery-incomplete`

is returned.

The code does not manually unlink or edit the marker.

## Provider-neutrality

The repair does not:

- inspect selected provider;
- probe Ollama;
- start/stop a provider;
- change provider/model/auth/routing;
- pass `--provider` to the lifecycle;
- enter the legacy provider-heavy Supervisor merely to clear the marker.

This preserves the v0.9.5 OpenClaw provider-ownership boundary.

## Static source review

The exact lower lifecycle implementation in `runtime.py` confirms:

- `lifecycle start` skips Gateway start when it is already healthy;
- health verification can require only Gateway when `--provider` is absent;
- successful verification calls `clear_maintenance(root)`;
- marker retirement is therefore supported runtime behavior rather than a new state mutation contract.

## Validation status

No local Python test execution was available from the GitHub-only ChatGPT execution environment.

Therefore this report does **not** claim GREEN test execution.

The next bounded task must run the focused and relevant full Python regression suites on the operator's local checkout before deployment.

## Mutation accounting

Production/runtime mutation: 0.

Semantic/model/provider requests: 0.

Repository source changes:

- one RED regression-test commit;
- one minimal source repair commit.

No OpenClaw dependency change, release/tag/main change, or force push occurred.

## Final classification

`HEALTHY_RUNTIME_MARKER_CONVERGENCE_REPAIR_IMPLEMENTED_PENDING_LOCAL_VALIDATION`
