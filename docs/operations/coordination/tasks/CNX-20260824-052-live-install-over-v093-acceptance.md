# CNX-20260824-052 — Live v0.9.3 Install-Over Upgrade Acceptance

Status: `READY_FOR_CODEX`

Execution mode: `MANUAL_WITH_HUMAN_GATE`

Owner: ChatGPT

Executor: Codex after the operator's manual signal

## Goal

Update the coherent live CogentNexus-OpenClaw v0.9.3 installation with the reviewed Task 051 source by invoking the default installer exactly once in `mode=upgrade`, then prove install-over behavior preserves durable state and returns to healthy canonical MANAGED/Ollama operation.

This is an install-over acceptance test. It is not a clean reinstall, migration, reset, uninstall, manual file patch, or fresh installation.

## Human authorization

The operator approved using this update as a real install-over test:

> `ครับเป็นการทดสอบไปในตัวด้วยเลย`

After the Task 051 report appeared, the operator directed:

> `ต่อเลยครับมีรายงานแล้ว`

This authorizes the single reviewed install-over invocation and its ownership-bound effects after every preflight gate passes.

Scheduled execution remains disabled. Codex starts only from the operator's manual signal.

## Required predecessors

Task 050 live installation:

- report: `docs/operations/coordination/reports/CNX-20260824-050-fresh-install-current-v093.md`
- review: `docs/operations/coordination/reviews/CNX-20260824-050-fresh-install-current-v093.md`
- disposition: `ACCEPT_INSTALLED_RUNTIME_WITH_HELP_DEFECT`

Task 051 repository repair:

- implementation commit: `6d90025f832bb36c477176809a0af2e6c1858c19`
- report: `docs/operations/coordination/reports/CNX-20260824-051-align-canonical-check-help.md`
- review: `docs/operations/coordination/reviews/CNX-20260824-051-align-canonical-check-help.md`
- review commit: `82a9a481212fd0ade1a7056b2b89707d65df5504`
- disposition: `ACCEPT_CANONICAL_CHECK_HELP_ALIGNED`

## Exact live target and expected mode

Workspace:

`C:\Users\CDQ-P\.openclaw\workspace`

Before mutation, the current installation must be a coherent exact v0.9.3 `mode=upgrade` installation with:

- launcher `cnxclaw.cmd`;
- skill `skills\cogentnexus-openclaw`;
- state root `.cogentnexus-openclaw`;
- exact-valid ownership manifest;
- exactly one plugin `cogentnexus-openclaw` v0.9.3;
- task `CogentNexus-OpenClaw-Supervisor`;
- controller MANAGED, desired Gateway/provider running, provider Ollama;
- canonical check command healthy;
- no legacy identity.

If classification is fresh, legacy, mixed, partial, ambiguous, or ownership verification fails, stop before installer invocation.

## Phase 0 — source, duplicate, and concurrency fence

1. Freshly fetch branch `agent/v0.9.3-recovery-reality-tests`.
2. Use one new isolated full clone under `%LOCALAPPDATA%\Temp`; do not create/register a Git worktree.
3. Record fetched execution HEAD.
4. Require exact coordination `ACTIVE.md` and `STATUS.md` to identify Task 052 as `READY_FOR_CODEX`.
5. Require Task 051 implementation/review commits as ancestors.
6. Stop if the matching Task 052 report already exists.
7. Require clean isolated clone and no unrelated non-coordination drift after Task 051 implementation except none.
8. Run the focused canonical-help tests, namespace isolation, baseline consistency, and PowerShell installer parser from the isolated source before live mutation.
9. Prove no concurrent install/migration/clean-reinstall/reset/uninstall/lifecycle/report-publisher process.
10. Prove no Procmon process/capture. Do not access retained Task 027/038 evidence.
11. Record primary-repository branch/status without mutation.

## Phase 1 — coherent upgrade and preservation baseline

Before the installer, require and record:

### Ownership and namespace

- classifier exits `0` with exact `mode=upgrade`, `legacy=[]`;
- installed ownership verifier exits `0`;
- ownership manifest exact fields, installed time, version, canonical paths, plugin path, and `migrationSource: null`;
- exactly one resolved plugin payload and fingerprint;
- native plugin inventory succeeds with 72 total: one current plus the same 71 unrelated identities;
- no legacy launcher/skill/state/plugin/config/load-path/install-record/task;
- no duplicate current plugin/root/task.

### Installed-source delta

Prove the live installed skill is the Task 050 pre-fix source for the affected help files and that the Task 051 repository delta relevant to the installed skill is limited to:

- `scripts\cnxclaw.py`
- `scripts\cnxclaw_v093.py`

Before upgrade, record that:

- live help still advertises the stale generic component;
- canonical `cnxclaw.cmd --json check cogentnexus-openclaw` succeeds;
- generic `check cogentnexus` is rejected.

Do not treat the expected generic rejection as unhealthy.

### Durable state

Capture semantic/read-only prestate for:

- complete controller JSON and generation;
- provider selection and route/config identity;
- registered policy path/hash/size;
- Ticket SQLite integrity, schema, row counts by status, ticket IDs, event/outbox counts, and other durable identifiers without exposing content/secrets;
- workflow/task/session registries and counts;
- runtime/startup policy;
- existing install-backup and startup-backup inventories;
- AGENTS full hash/size and canonical marker counts;
- AGENTS baseline obtained by removing the canonical block in memory;
- launcher, skill, plugin payload, ownership manifest, and relevant state hashes;
- OpenClaw config semantic/redacted structure;
- Gateway status/probe/PID/command;
- Ollama endpoint/process/active model and exact four-model inventory;
- unrelated plugin/npm-project identities;
- Task 049 external backup path and manifest hash;
- HermesAgent, Ecosystem, staged-capability-loop, retained evidence, unrelated workspace/OpenClaw user data, and primary-repository sentinels.

Required accepted AGENTS baseline after in-memory block removal:

- 7,196 bytes;
- SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`.

Stop before mutation on unexplained drift, unhealthy native runtime, failed SQLite integrity, ownership ambiguity, current/legacy duplicates, or missing preservation evidence.

## Phase 2 — exact exit-code-retaining installer wrapper

Invoke the default installer exactly once from the isolated clone:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

Do not pass `-SkipPlugin`, `-SkipGatewayRestart`, `-SkipAgentsPolicy`, `-LinkPlugin`, custom provider, backup, or config arguments.

Use a temporary wrapper outside the repository that retains the exact child process object and exit code. The wrapper must:

1. launch exactly one `powershell.exe` child with the exact installer command;
2. use `Start-Process -PassThru` or an equivalent `System.Diagnostics.Process` object;
3. redirect stdout/stderr to unique temporary files;
4. retain the exact PID from process creation;
5. observe that same process until termination without a wrapper timeout that discards its object;
6. call `WaitForExit()`, refresh the process object, and persist/read `.ExitCode` before releasing it;
7. emit a small poststate record containing PID, start/end UTC, duration, observed exit code, stdout/stderr byte counts and hashes;
8. never launch another installer if monitoring/output handling fails after the child began.

The wrapper/logs/poststate remain temporary machine evidence and must not be committed.

Report meaningful stages approximately every 3 minutes by reading new redirected output while the exact child remains active.

### Retry and failure fence

- installer invocation count after script-body entry: exactly one;
- no retry for nonzero exit, timeout, lost output, partial state, or postcheck failure;
- do not force-kill the installer, Gateway, Ollama, scheduler, shell, or unknown processes;
- if the child remains alive, continue bounded observation; do not infer failure or launch another;
- if exit is nonzero, record installer rollback evidence and exact partial/current state, publish blocker, and stop;
- do not manually copy Task 051 files into the installed skill;
- do not manually finish plugin/config/manifest/task updates;
- do not clean reinstall or automatically restore.

A PASS requires an actually observed exit code `0`.

## Expected reviewed install-over sequence

The single default installer may:

1. classify the coherent current installation as `upgrade`;
2. invoke the current `cnxclaw.cmd disable` once to enter PASSTHROUGH/native operation;
3. preserve existing durable state and back up the existing skill;
4. stage and replace the canonical skill with the Task 051 source;
5. validate/init without resetting durable Ticket/workflow/policy state;
6. reapply the canonical AGENTS managed block;
7. package and reinstall exactly the same canonical plugin ID/version without a linked path;
8. recreate the launcher;
9. recreate and exact-verify the ownership manifest;
10. transactionally enable MANAGED/Ollama and canonical supervisor;
11. verify Gateway/runtime health.

These are authorized only inside the exact single installer invocation.

## Phase 3 — install-over and corrected-help proof

After observed installer exit `0`, require:

- classifier exact `mode=upgrade`, `legacy=[]`;
- installed ownership verifier exit `0`;
- ownership manifest v0.9.3 with canonical paths and `migrationSource: null`;
- installed `cnxclaw.py` and `cnxclaw_v093.py` byte-identical to Task 051 implementation commit;
- live `cnxclaw.cmd --help` advertises `check cogentnexus-openclaw`;
- live help/usage does not advertise complete-token generic `check cogentnexus`;
- missing-component usage exits `2` and identifies canonical component;
- canonical `cnxclaw.cmd --json check cogentnexus-openclaw` exits `0` with `READY`;
- generic `cnxclaw.cmd --json check cogentnexus` exits `3` as unsupported; this expected rejection is PASS evidence;
- source/live namespace lint passes;
- no generic permanent launcher/skill/state/plugin/task alias;
- no legacy identity reappears.

## Phase 4 — state preservation and runtime proof

Require and compare:

### Durable state preservation

- pre-existing Ticket IDs/status counts/events/outbox and workflow/task/session durable identities remain; no reset/truncation/reinitialization;
- SQLite integrity remains `ok`;
- registered policy source/hash/size remains unchanged;
- provider selection remains Ollama;
- controller generation may advance through explicit disable/enable, but no unexplained reset or loss occurs;
- runtime/startup policy returns to intended enabled MANAGED state;
- the install-over skill backup exists and contains the exact pre-upgrade help files;
- scheduler backup/transition evidence is consistent with the single upgrade;
- AGENTS final content/hash is unchanged from pre-upgrade or differs only by a semantically identical canonical block rewrite;
- exactly one canonical AGENTS marker pair and zero legacy markers;
- removing the canonical block in memory still reproduces the accepted 7,196-byte baseline hash;
- Task 049 external backup manifest remains byte-identical.

### Ownership and plugin preservation

- exactly one canonical plugin v0.9.3 is enabled/loaded;
- verified plugin payload fingerprint remains equal to pre-upgrade because Task 051 did not change plugin code;
- the same 71 unrelated plugin identities and unrelated npm projects remain;
- no linked plugin path, duplicate wrapper/package, legacy config entry, or unrelated config drift;
- ownership installed time/hash changes are classified as expected; canonical ownership fields remain exact.

### Runtime

- controller is `managed`, desired Gateway/provider `running`;
- `cnxclaw.cmd status`, canonical component check, provider check/status, and non-destructive system check succeed;
- `CogentNexus-OpenClaw-Supervisor` exists, enabled/Ready, uses canonical paths, with no legacy task;
- Gateway status/probe healthy and reachable;
- Ollama healthy with unchanged active model/four-model inventory;
- no installer/npm/plugin/lifecycle orphan.

### Excluded systems/data

Prove no unexplained change to primary repository, unrelated workspace/OpenClaw user data, HermesAgent, Ecosystem, staged-capability-loop, retained Procmon evidence, Ollama data/models, or Task 049 backup.

## Results

Return exactly one:

- `PASS_INSTALL_OVER_V093_ACCEPTANCE`
- `BLOCKED_SOURCE_OR_DUPLICATE_FENCE`
- `BLOCKED_COHERENT_UPGRADE_PREFLIGHT`
- `BLOCKED_DURABLE_STATE_PREFLIGHT`
- `BLOCKED_INSTALLER_EXIT_UNOBSERVED`
- `BLOCKED_INSTALL_OVER_NONZERO_EXIT`
- `BLOCKED_INSTALL_OVER_PARTIAL`
- `BLOCKED_CANONICAL_HELP_NOT_UPDATED`
- `BLOCKED_STATE_PRESERVATION`
- `BLOCKED_POSTUPGRADE_OWNERSHIP`
- `BLOCKED_POSTUPGRADE_RUNTIME`
- `BLOCKED_UNRELATED_DRIFT`
- `BLOCKED_REPORT_PUBLICATION_UNSAFE`

A PASS requires one observed exit `0`, exact Task 051 installed help files, coherent ownership, preserved durable state, healthy MANAGED/Ollama runtime, and no unexplained unrelated effect.

## Report and publication fence

Publish exactly one report:

`docs/operations/coordination/reports/CNX-20260824-052-live-install-over-v093-acceptance.md`

The report must include:

- fetched execution HEAD and source/duplicate/concurrency proof;
- exact pre-upgrade ownership/classifier/help/runtime/state/sentinel evidence;
- exact wrapper design, child PID, timing, observed exit code, output sizes/hashes and stage summary;
- pre/post skill/help/plugin/manifest/controller/policy/SQLite/AGENTS/scheduler evidence;
- exact canonical/generic command results;
- install-backup proof;
- Gateway/Ollama/unrelated plugin/data preservation;
- mutation/retry/restart/repair command counts;
- remaining uncertainty;
- one exact result token.

Do not commit temporary wrapper/logs/poststate, configs, databases, backups, manifests, screenshots, binaries, archives, secrets, command dumps, or machine evidence as separate files. Commit only the Markdown report.

The report commit must change exactly the Task 052 report path relative to fetched execution HEAD. Commit message must begin:

`report: CNX-20260824-052 live install-over acceptance`

No repository implementation repair or coordination-file edit is authorized inside Task 052.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

- source/duplicate/concurrency fence;
- coherent upgrade and durable-state preflight;
- immediately before the single installer;
- PASSTHROUGH handoff;
- skill/plugin/ownership stages;
- exact child termination and captured exit code;
- corrected-help verification;
- durable-state comparison;
- runtime/preservation proof;
- report publication or blocker.

Updates are not pause points unless a stop gate fires.

## Prohibited

No clean reinstall; fresh install; legacy migration/restore; second installer invocation; manual installed-file edit/copy; manual partial completion; reset/uninstall; destructive recovery test; force-kill; broad deletion; wildcard/parent cleanup; OpenClaw upgrade/reinstall; manual SQLite/config edit; Ollama/model mutation; primary-repository Git mutation; HermesAgent/Ecosystem/staged-capability-loop action; Procmon/Task 027/038 access; merge; tag; GitHub Release; archive publication.
