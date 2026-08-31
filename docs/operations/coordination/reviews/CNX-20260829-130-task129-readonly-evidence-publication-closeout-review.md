# Independent Review — CNX-20260829-130

## Verdict

**ACCEPTED PASS — TASK 129/130 NOW PROVIDE SUFFICIENT READ-ONLY EVIDENCE THAT TASK 128 WAS BLOCKED BY AN EXECUTOR/PREFLIGHT ROOT MISMATCH, NOT BY AUTHORITATIVE MANAGED-STATE DRIFT; THE AUTHORITATIVE INSTALLED ROOT IS COHERENT, SQLITE PASSES READ-ONLY INTEGRITY, AND A NEW SEPARATELY AUTHORIZED REAL-WINDOWS RECOVERY RE-ACCEPTANCE MAY BE OPENED.**

## Scope reviewed

Reviewed Task-130 report commit:

`006e5368c617470c706e6aa068e8f2560dbeffc7`

Task-130 start authority:

`b3a86cc95c9dce605ac3545b32ce2a1613543174`

Accepted repository candidate remains:

`1b922bf400fdbccb1f9c7019b89b69fd67f44070`

Exact repaired recovery harness remains:

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Git blob `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`

## Findings

### 1. Task-128 false blocker is now sufficiently proven

The installed launcher is explicitly:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

with SHA256:

`f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10`

and it invokes the installed v0.9.3 CLI with:

`--root C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Task 128 instead probed the workspace parent:

`--root C:\Users\CDQ-P\.openclaw\workspace`

That wrong root explains the synthesized/non-authoritative `passthrough`, null-provider, and missing-SQLite observations.

### 2. Authoritative live state is coherent

Direct installed-launcher read-only probes all exited `0` and report:

- host mode `managed`;
- selected provider `ollama`;
- desired Gateway/provider `running`;
- recovery verdict `READY`;
- provider incident closed;
- provider recovery circuit closed.

The authoritative controller is generation `21`, has no provider transition, and points coherently to Ollama.

### 3. SQLite blocker was also a wrong-root probe defect

The authoritative database is:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

It exists and a URI `mode=ro` SQLite connection returned:

`PRAGMA integrity_check = ok`

Therefore the Task-128 `sqliteExists=false` observation is accepted as a preflight-layer path defect caused by the same wrong root, not as evidence of a missing authoritative database.

### 4. Independent authority paths agree

The `CogentNexus-OpenClaw-Supervisor` scheduled task invokes the installed `host_control_v092.py` and passes the same explicit `.cogentnexus-openclaw` root. No second installed live root was identified by the bounded competing-root inventory. Relevant non-secret root/config environment overrides were null.

### 5. Evidence limitations are disclosed rather than inferred through

The closeout correctly states that:

- `Get-Command cnxclaw.cmd -All` was not retained successfully;
- exact installed-file equality to the Task-127 candidate was not proven for every CLI file;
- Task-125 historical generation/timestamp is insufficient for an exact numerical generation comparison;
- some OpenClaw Gateway task argument/working-directory fields remain unproven.

These limitations do not undermine the root-mismatch diagnosis because the explicit installed launcher path, controller, supervisor task authority, direct installed-launcher probes, and authoritative SQLite path independently converge on the same root.

### 6. Hard fence was respected

Task 130 used retained evidence plus one narrowly scoped read-only file metadata/hash probe, which the Task-130 contract explicitly allowed when a required retained fact was absent.

No recovery suite, lifecycle command, provider/config/model mutation, state/database edit, task/service mutation, process kill, normalization, or Dashboard semantic Send was performed.

Task-128 repaired-harness suite remains unlaunched: `0 / 1`.

## Accepted classification

`LAUNCHER_OR_ROOT_MISMATCH`

plus, limited to the Task-128 acceptance-probe layer:

`SQLITE_PATH_OR_STATUS_PROBE_DEFECT`

There is no accepted evidence of authoritative managed-state drift.

## Advancement decision

Task 129 and Task 130 are accepted closed.

A new separately authorized real-Windows recovery re-acceptance may now be opened against the already accepted Task-127 candidate/harness, with one critical correction: **all external preflight state/status/provider/recovery/SQLite authority must be derived from or invoked through the explicit installed launcher and its parsed `.cogentnexus-openclaw` root.**

Do not reuse the closed Task-128 execution context. Create a new task and one-shot ledger. Do not reinstall, replay the already-passed lifecycle acceptance, or open Dashboard durable-delivery acceptance before the new recovery re-acceptance passes and is independently reviewed.
