# CNX-20260920-441 — Installer / Supervisor Native-Handoff Quiescence

Status: `COMPLETE`

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

## Live qualification

The first live supported install-over of the CNX-441 repair completed successfully.

Exact evidence:

- candidate/local/remote HEAD:
  `5263b6aed9acf77a4db39be47c4d96fecfe8a431`;
- LConnect process session:
  `proc-1789885920190-35`;
- installer PID:
  `10220`;
- installer terminal exit:
  `0`;
- installer reported successful v0.9.5 completion;
- live v095 Discord adapter SHA-256 equals candidate:
  `7809B18C4BAE1209624D5E69112722EF9AD7F5E39A92A2815C6889DFF6C646A1`;
- controller returned to active/managed generation `111`;
- Gateway is healthy and event loop is not degraded;
- Discord lifecycle is ready and connected;
- `CogentNexus-OpenClaw-Supervisor` was restored Enabled/Ready with `LastTaskResult=0`;
- no duplicate installer remained;
- Ollama had no resident model after convergence.

This demonstrates that pre-quiescing the old supervisor prevents the prior installer/native-handoff race while preserving supported restoration on the success path.

Report:

`docs/operations/coordination/reports/CNX-20260920-441-installer-supervisor-native-handoff-quiescence-report.md`

## Classification

Source qualification:

`INSTALLER_SUPERVISOR_HANDOFF_QUIESCENCE_GREEN`
