# CNX-20260920-441 — Installer / Supervisor Native-Handoff Quiescence

Status: `IMPLEMENTED_AWAITING_LIVE_REQUALIFICATION`

Parent: `CNX-20260920-440`

## Trigger

A supported install-over of CNX-440 from exact commit
`a4f27ad097e721edfe566a7495864b7e15ae88e8`
failed closed before plugin mutation.

Installer failure:

`Existing CogentNexus-OpenClaw disable failed; refusing install mutation.`

The transactional disable reported Gateway ETIMEDOUT and preserved prior MANAGED Host state.

Post-failure proof:

- controller remained active/managed generation 109;
- Gateway healthy;
- Discord ready/connected;
- supervisor LastTaskResult 0;
- live v095 adapter hash remained the old hash;
- no candidate plugin mutation occurred.

## Root cause

The external CNX supervisor Scheduled Task runs every minute.

During the long read-only installer preparation phase (npm ci + plugin validation + classification), a supervisor invocation began hard-hang recovery:

- 13:16:03 local — external supervisor enabled recoverable maintenance;
- 13:16:15 — prior Gateway child exited;
- 13:16:16 — OpenClaw Gateway Scheduled Task restarted;
- 13:16:27 — installer entered transactional native handoff;
- 13:16:28 onward — new Gateway was still starting/warming;
- installer RPC to the Gateway timed out.

OpenClaw's state database also showed repeated SQLite lock contention during this interval. The external supervisor's restart-intent write itself reported `database is locked`, although the Scheduled Task restart succeeded.

The installed startup adapter deletes future CNX supervisor scheduling, but a supervisor invocation that already started can continue running. The Host fast-path hard-hang restart occurs before the legacy `runtime.py` supervisor lock, so waiting only on `.supervisor.lock` would not cover the actual race.

## Repair design

Before calling the existing transactional launcher `disable`, the Windows installer now:

1. invokes the INSTALLED current-skill `startup_v091.py ... disable` adapter;
2. thereby removes future CNX supervisor Scheduled Task invocations through the supported startup surface;
3. waits, bounded to 300 s, until no exact
   `host_control_v092.py ... supervisor tick --execute-safe`
   process for the current CNX root remains;
4. requires two consecutive successful
   `openclaw gateway health --json`
   probes within a 180 s bound;
5. only then enters the existing transactional `cnxclaw disable` handoff.

If pre-quiescence occurred and handoff fails before PASSTHROUGH, the installer restores the current supervisor through the installed `startup_v091.py ... enable` adapter. If the launcher already restored it, the rollback path detects the enabled adapter and avoids a redundant restart.

Legacy migration is intentionally excluded from this current-installation pre-quiescence path.

## Why this repair is deployable to the currently installed runtime

The repair lives in the candidate installer and invokes only startup/launcher surfaces that already exist in the installed current skill. It does not require the old live runtime to understand a new lease or marker schema before replacement.

## Validation

TDD RED: 5/5 new quiescence contract tests failed before implementation.

GREEN:

- new quiescence + installer ordering suite: 27/27 PASS;
- expanded installer/lifecycle regression suite: 50/50 PASS;
- combined related CNX-441 validation: 77 PASS;
- `git diff --check`: PASS;
- PowerShell syntax/control-flow validation included through existing installer tests.

## Next gate

Freeze/push this repair, then perform exactly one new supported install-over attempt.

Do not send another Discord acceptance message until:

- install terminal exit 0;
- live v095 adapter hash equals candidate;
- controller/runtime/supervisor are healthy;
- target Discord baseline is clean.

## Classification

Source qualification:

`INSTALLER_SUPERVISOR_HANDOFF_QUIESCENCE_SOURCE_GREEN`
