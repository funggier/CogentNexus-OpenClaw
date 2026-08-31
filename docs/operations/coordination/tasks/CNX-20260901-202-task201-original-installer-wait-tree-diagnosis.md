# CNX-20260901-202 — Task 201 Original Installer Wait-Tree Diagnosis

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-201`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Identify the live wait/process boundary that keeps the original Task-200 installer PowerShell process alive, without killing it, replaying installation, forcing managed convergence, or sending Discord traffic.

Task 201 proved the original installer is still the same process and has remained stalled after the passthrough-policy output for an extended interval. The next step is evidence collection across the process tree, not a cleanup or workaround.

## Immutable authorities

Frozen repaired product candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Published v0.9.3 target remains:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Original Task-200 installer identity:

- root PowerShell PID: `11704`
- known conhost PID: `11588`
- retained creation time for PID 11704: `\/Date(1788193889192)\/`

Do not trust PID numbers without matching retained identity.

Human Discord Send budget remains:

`0 / 1 consumed; 1 / 1 available`

No Discord Send is authorized in Task 202.

## Known source boundary

The final retained installer stdout proves:

- all seven instrumented stages through `owned-runtime-ensure` completed with exit 0;
- launcher write completed;
- managed policy apply returned a passthrough/non-applied result;
- no `cnxclaw enable` result appeared;
- no final completion line appeared.

The next installer command is the v0.9.3 facade `enable`, which traverses nested Python/Host/OpenClaw subprocesses and a Gateway process boundary. A known-good Task-159 install-over returned from this region in roughly three minutes. Task 201 observed no progress for a much longer interval.

The repository also contains a prior Windows acceptance finding that some wait APIs can remain blocked on long-lived descendants. This is a hypothesis to test, not an accepted root cause.

## Hard fence

Task 202 is read-only only.

Do **not**:

- terminate/kill/suspend PID 11704 or any descendant;
- rerun `scripts/install.ps1`;
- run `cnxclaw enable`, `disable`, `start`, `stop`, `restart`, `reset`, or `uninstall`;
- start/stop/restart Gateway, supervisor, provider, OpenClaw, or Ollama;
- modify configuration, SQLite, state, Scheduled Tasks, plugin state, provider/model selection, or files;
- send any Discord message;
- inject/synthesize user traffic;
- download/install diagnostic software;
- edit product/source/test/workflow files;
- mutate Release/tag/assets;
- force push.

If evidence collection itself would require mutation, omit that probe and document the limitation.

## Phase A — fresh authority and retained evidence

1. Fresh-sync GitHub coordination state.
2. Confirm Task 201 report/review and Task 202 are current authority.
3. Read Task-200/201 evidence root metadata.
4. Reconfirm exact candidate/install fingerprint only through read-only probes.

## Phase B — recursive process tree

Capture a complete current `Win32_Process` snapshot and build the recursive descendant tree rooted at the exact original PID 11704.

For every process in the tree record at minimum:

- PID;
- PPID;
- process name;
- executable path;
- full command line where accessible;
- creation time;
- kernel/user CPU time;
- working-set/private memory where read-only available;
- handle count where read-only available.

Explicitly look for descendants matching or containing:

- candidate-owned Python interpreter;
- `cnxclaw_v093.py`;
- `cnxclaw.py`;
- `host_control_v092.py` / `host_control_v091.py` / `host_control.py`;
- `host_v092.py` / Host scripts;
- `openclaw`, `openclaw.cmd`, `node.exe`;
- `cmd.exe`;
- Gateway-related child commands;
- Scheduled Task launcher/helper processes.

Do not assume that only direct children matter.

If PID 11704 no longer matches retained identity at Task-202 execution time, stop and report `BLOCKED_PROCESS_IDENTITY` without further inference.

## Phase C — thread/wait and progress sampling

Take two read-only samples separated by a bounded observation interval (recommended 30-60 seconds; no busy loop).

For PID 11704 and every surviving descendant, record where available:

- cumulative CPU time;
- thread IDs;
- thread state;
- thread wait reason;
- handle count;
- responding state;
- process creation time.

For retained installer streams record at both samples:

- file size;
- SHA-256;
- last-write time;
- last relevant output lines.

Classify whether during the sample interval:

- root/descendant CPU advanced materially;
- process tree changed;
- stdout/stderr changed;
- any child exited/appeared;
- the root is idle with no active execution descendant.

Do not claim a deadlock solely from low CPU.

## Phase D — source-boundary correlation

Using process command lines and the exact candidate source, map the deepest surviving execution process to one of these boundaries when evidence permits:

1. PowerShell between policy apply and invoking `cnxclaw enable`;
2. v0.9.3/v0.9.2 CLI provider-transition preflight/route work;
3. watchdog compatibility OpenClaw config get/set;
4. Host `enable` delegation;
5. managed plugin/Gateway reload;
6. forced Gateway restart/process boundary;
7. post-transition provider/Gateway/route verification;
8. another proven command boundary.

If no executable descendant remains below PowerShell, state that explicitly. Do not invent which PowerShell internal wait primitive is responsible.

## Phase E — independent health snapshot

Read-only capture only:

- Host mode/startup state;
- installed plugin state/fingerprint;
- Gateway health;
- Ollama readiness;
- delivery/recovery state;
- SQLite integrity;
- durable counts.

No command may force convergence.

## Required analysis outcomes

Report one of:

### `EVIDENCE_CHILD_BOUNDARY_IDENTIFIED`

Use only if a surviving descendant/command line identifies the active execution boundary with high confidence.

### `EVIDENCE_ROOT_IDLE_NO_EXEC_DESCENDANT`

Use if the exact original PowerShell remains alive, stream output is unchanged across samples, and no meaningful executable descendant remains besides console infrastructure. This proves an orphaned/root wait shape but not its internal PowerShell cause.

### `EVIDENCE_PROCESS_TREE_CHANGED`

Use if the process finally progresses/exits during Task 202. Record terminal state and streams, but do not proceed to Discord or lifecycle actions under this task.

### `BLOCKED_PROCESS_IDENTITY`

Use if the original process cannot be safely identified.

### `BLOCKED_EVIDENCE`

Use if platform permissions/tooling prevent a reliable tree/wait classification.

## Important stop rule

Even if Task 202 identifies the exact child boundary, **do not kill it and do not repair it live**. Publish evidence and stop for ChatGPT review. Source repair/reproduction or bounded cleanup will be authorized only in a separate task after root-cause review.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-202-task201-original-installer-wait-tree-diagnosis.md`

Include:

- fresh authority SHA;
- Task-201 report/review authority;
- exact process identity proof;
- full recursive tree in bounded text/JSON form;
- two sample deltas;
- stream hashes/mtimes/tails;
- source-boundary mapping;
- current read-only health;
- one final analysis outcome from the allowed list;
- explicit mutation ledger proving no forbidden action.

Then stop for ChatGPT review.
