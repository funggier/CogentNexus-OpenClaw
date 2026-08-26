# CNX-20260826-072 — Bounded Cleanup, Fresh Install, Owned Runtime and No-Flash Live Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_BOUNDED_RESIDUE_CLEANUP_FRESH_INSTALL_OWNED_RUNTIME_NO_FLASH`

Current authorization: `BOUNDED_RESIDUE_CLEANUP_AND_FRESH_INSTALL_LIVE_ACCEPTANCE_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after the operator's continuation signal

## Goal

Complete the live Windows installation/runtime acceptance that Task 066 could not finish.

The supported old installation was already cleanly uninstalled in Task 066. Task 066 then produced exactly two unowned partial-install workspace roots before failing on the now-corrected npm/recovery defects. Tasks 067-071 repaired and independently reviewed those source defects.

This task may:

1. re-prove the exact Task-066 partial residue;
2. remove those exact two unowned roots once under this explicit exceptional authorization;
3. perform one normal fresh install from the exact accepted production source;
4. prove durable runtime authority is CogentNexus-owned rather than Hermes/Codex/executor-owned;
5. observe at least three natural PT1M supervisor executions and prove the old console/conhost flash chain is absent;
6. finish non-semantic MANAGED health acceptance.

Do NOT perform a real user-message/LLM semantic smoke in this task. Ticket -> LLM -> response/delivery is a separate final gate.

## Accepted source

Install source MUST be exactly production commit:

`9df671670908241486afe2badf8a7f221410c6f8`

Task-071 test/report commits after this commit do not alter production and are not the install source.

Required accepted ancestry includes:

- Task 065 runtime-authority correction;
- Task 067 npm 11/npm 12 reproducibility correction;
- Tasks 067-069 fresh transaction/application-data/plugin inverse recovery work;
- Task 070 non-fresh mode isolation restoration.

The source worktree/clone used for install must be clean at the exact commit. No source editing during Task 072.

## Accepted live baseline from Task 066

Task-066 report proves the supported old uninstall completed and left:

- no `CogentNexus-OpenClaw-Supervisor` Scheduled Task;
- no `cnxclaw.cmd` launcher;
- no registered CogentNexus plugin;
- no managed AGENTS block;
- native OpenClaw Gateway healthy;
- Ollama healthy with exact model inventory:
  - `qwen3.5:9b`
  - `muse-glimmer:30b`
  - `qwen3.6:27b`
  - `qwen3.8:27b`
- no valid `ownership.json`;
- exactly the failed fresh-attempt residue at:
  - `<workspace>\.cogentnexus-openclaw`
  - `<workspace>\skills\cogentnexus-openclaw`

Task-066 observed residue shape included:

- `.cogentnexus-openclaw\host\controller.json` in passthrough;
- `.cogentnexus-openclaw\host\managed-policy.md`;
- `.cogentnexus-openclaw\install-staging`;
- copied `skills\cogentnexus-openclaw` source tree;
- no ownership manifest.

Those roots predate the transaction-marker fix. They cannot be silently adopted by the fixed installer.

## Phase A — fresh preflight and preservation re-proof

Before ANY mutation, fetch/read current ACTIVE, STATUS, Task 072, Task-071 review, and Task-066 report from the remote coordination branch. Verify local/source execution state is not stale.

Create a new evidence directory outside all product deletion boundaries under `%LOCALAPPDATA%\Temp` and record its exact path.

Re-prove and record:

1. current timestamp/boot identity;
2. OpenClaw version exactly `2026.7.1-2`;
3. `openclaw gateway status` and local HTTP/dashboard health;
4. Ollama health and exact four-model inventory listed above;
5. Supervisor task absent;
6. launcher absent;
7. current CNX plugin registration/config absent;
8. AGENTS managed block absent and stripped baseline SHA if available;
9. `%LOCALAPPDATA%\CogentNexus-OpenClaw` absent unless an unexpected post-Task-066 change is proven and reconciled;
10. `ownership.json` absent;
11. exact tree/inventory/hashes for BOTH residue roots;
12. no unrelated/user content inside either residue root;
13. unrelated OpenClaw plugin/config baseline hashes sufficient to prove preservation after install;
14. SQLite/native workspace state readable as applicable before cleanup.

### Hard decision gate A

Proceed only if the live condition is materially the accepted Task-066 state and the two residue roots are still exactly attributable to the failed Task-066 fresh attempt.

If a valid ownership manifest, active launcher/task/plugin, unrelated content, or another actor's post-Task-066 mutation is found, STOP and report instead of deleting anything.

## Phase B — one-time bounded legacy-residue cleanup

This is an exceptional one-time cleanup for residue that predates the new transaction marker. It is explicitly authorized only after Phase A re-proof.

Remove exactly and only:

1. `<workspace>\.cogentnexus-openclaw`
2. `<workspace>\skills\cogentnexus-openclaw`

Rules:

- delete each root at most once;
- do not delete `<workspace>\skills`, `<workspace>`, `.openclaw`, `%LOCALAPPDATA%`, npm project parents, or any sibling path;
- do not manually delete OpenClaw plugin projects/config because Task-066 already proved plugin registration/payload absent;
- do not fabricate `ownership.json` or transaction markers;
- do not use reset/uninstall to mask this pre-marker residue;
- retain pre-delete tree/hashes in the evidence directory.

Immediately prove both exact roots absent and all shared parents/unrelated baseline state preserved.

If either bounded deletion cannot be proven safe or complete, STOP and report. Do not broaden cleanup.

## Phase C — normal fresh install from exact accepted source

Use a clean isolated clone/worktree at exactly:

`9df671670908241486afe2badf8a7f221410c6f8`

Record:

- `git rev-parse HEAD`;
- clean `git status --porcelain`;
- Node/npm/Python/OpenClaw versions used by the installer.

Run the normal Windows fresh install path exactly once.

Do NOT use:

- `-SkipPlugin`;
- `-SkipGatewayRestart`;
- `-SkipAgentsPolicy`;
- `-LinkPlugin`;
- source patching;
- manual manifest creation;
- manual npm-project deletion;
- alternate partial/staging shortcuts.

The corrected lock must work with the actual selected npm; do not solve a new failure by silently downgrading npm.

### Installer transaction evidence

Capture enough evidence to prove the new fresh-install transaction path is actually in use:

- fresh classification before mutation;
- incomplete transaction marker created before residue-capable fresh mutation;
- exact product workspace/app-data paths recorded consistently;
- on success ownership is created and verified before transaction commit;
- marker is committed/retired and no longer authorizes rollback.

If the fresh install fails:

- do NOT manually clean or retry destructive effects blindly;
- inspect whether same-run bounded rollback or rerun recovery returned the machine to coherent fresh state;
- report the defect/evidence;
- do not repeat plugin/install effects unless the supported recovery contract proves they were rolled back.

## Phase D — exact owned runtime authority

After successful install, prove the durable runtime is exactly under:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`

Expected foreground interpreter:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe`

Expected background interpreter:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\Scripts\pythonw.exe`

Record and verify the runtime manifest, including its base interpreter provenance.

Current milestone allows the owned runtime to be a venv backed by a verified non-venv system/base Python. The durable authority must nevertheless be the CogentNexus-owned foreground/background interpreter paths above.

Hard reject any durable launcher/task/runtime binding containing:

- `hermes` / `hermes-agent`;
- `codex`;
- executor worktree/temp roots;
- test venvs;
- `%TEMP%`;
- agent-specific venvs.

### Launcher proof

`<workspace>\cnxclaw.cmd` must invoke the exact owned foreground interpreter and the installed v0.9.3 CLI/root. No bare `python`, Hermes interpreter, cmd trampoline to another runtime, or temporary path.

Run a bounded foreground product CLI probe using the launcher/owned foreground interpreter and capture exit/status.

### Scheduled Task proof

`CogentNexus-OpenClaw-Supervisor` must be Enabled/Hidden with PT1M cadence and Execute EXACTLY the owned background interpreter.

Its arguments must target the installed:

`skills\cogentnexus-openclaw\scripts\host_control_v092.py`

with the product state root and `supervisor tick --execute-safe` semantics required by current startup code.

No durable `cmd.exe`, PowerShell wrapper, Hermes venv, uv-agent venv, Codex path, or temp path is acceptable.

Run/verify the owned background interpreter independently with a harmless sentinel/exit probe if needed to prove it starts without a console interpreter trampoline.

## Phase E — natural PT1M no-flash acceptance

Do NOT manually trigger the Scheduled Task three times and call that natural cadence proof.

Observe at least THREE distinct natural PT1M scheduled executions after the fresh install. Four is preferable if evidence capture timing is ambiguous.

Use bounded process-start evidence (CIM polling/event trace/other read-only mechanism appropriate on Windows) covering each natural tick.

For each tick prove:

1. Scheduled Task launch time/cadence corresponds to the natural PT1M schedule;
2. root executable is the exact product-owned `pythonw.exe`;
3. expected supervisor/host-control target is used;
4. no causal `conhost.exe` is spawned by the CogentNexus scheduled chain;
5. no console `python.exe` trampoline is spawned from Hermes/uv/agent venv;
6. no `cmd.exe`/PowerShell wrapper is in the scheduled causal chain;
7. task `LastTaskResult` remains healthy;
8. Gateway remains healthy;
9. Ollama remains healthy with the same model inventory.

Distinguish unrelated system/user `conhost.exe` activity from causal descendants of the CNX scheduled chain.

Classify final flash result exactly as one of:

- `NO_FLASH_MULTI_TICK_PROVEN`
- `FLASH_REMAINS_BOUND`
- `FLASH_NOT_OBSERVABLE`

`NO_FLASH_MULTI_TICK_PROVEN` requires process-chain evidence for at least three natural ticks. A visual report alone is supplemental, not sufficient.

If a user-visible flash is observed post-install, or a causal conhost/console trampoline is captured, STOP and report the exact chain; do not suppress it with unrelated scheduler/cadence changes.

## Phase F — final non-semantic MANAGED health

Prove after the natural-tick window:

1. controller mode `managed`;
2. desired Gateway/provider states running and provider Ollama;
3. startup/Supervisor enabled;
4. Gateway native health and local HTTP/dashboard reachable;
5. Ollama healthy with exactly the four accepted models unchanged;
6. exactly one canonical v0.9.3 CogentNexus plugin registration/payload active as intended;
7. plugin configuration contains the accepted MANAGED values, including ticket-first/pre-inference/auto-workflow/auto-resume semantics and the accepted polling intervals;
8. ownership manifest exists and exact verification passes;
9. launcher and Scheduled Task still bind only to owned runtime paths;
10. AGENTS managed block exists exactly once; stripped baseline remains the accepted native baseline (`c9a664b73200ae5d6b0da0908de3256cdb4dda8ba6fe99f5e6c5115c3983604c`) unless an independently justified unrelated change was already present at Phase A;
11. SQLite integrity/readability passes; durable ticket/event/outbox/session tables are coherent;
12. unrelated OpenClaw/plugin/config state from Phase A is preserved.

Do not require generation `12`; fresh reinstall may legitimately produce a different generation. Record the actual value.

## Semantic smoke prohibition

Do NOT send a real user message through CogentNexus/OpenClaw for LLM inference in Task 072 unless strictly required by the installer itself for health (it should not be).

Hermes's own executor/model calls are control-plane activity and do not count as product semantic smoke. If Ollama model activity appears, determine caller/provenance before classifying it as a scope violation.

Final Ticket -> Ollama LLM -> response/delivery acceptance is reserved for a separate Task 073 after Task 072 is accepted.

## Disruptive-action ledger

Expected disruptive actions in this task are bounded to:

- one-time deletion of each of the two proven Task-066 residue roots;
- one normal fresh install from accepted source;
- installer/lifecycle effects naturally required by that fresh install.

Do not uninstall again. Do not repeat cleanup/install if evidence shows it already completed. On session interruption, re-inspect actual live state before any continuation.

## Forbidden operations

Unless a newly observed safety contradiction requires stopping and reporting:

- no reboot/power cycle;
- no provider/model changes;
- no Ollama model pull/remove;
- no HermesAgent mutation;
- no OpenClaw upgrade/downgrade;
- no source edits;
- no broad manual filesystem cleanup;
- no force push;
- no merge/tag/release;
- no real product semantic LLM smoke.

## Verification and report

Publish a report-only commit adding exactly:

`docs/operations/coordination/reports/CNX-20260826-072-bounded-cleanup-fresh-install-owned-runtime-live-acceptance.md`

Report must include:

- fetched execution/coordination HEAD;
- exact install source HEAD `9df671670908241486afe2badf8a7f221410c6f8`;
- Phase A residue re-proof and preservation evidence;
- one-time cleanup action ledger and post-clean proof;
- fresh install log/result and transaction evidence;
- runtime manifest/base interpreter/foreground/background exact paths;
- launcher and Scheduled Task exact bindings;
- ≥3 natural PT1M tick process-chain evidence;
- flash classification;
- final MANAGED/Gateway/Ollama/plugin/config/ownership/AGENTS/SQLite health;
- explicit semantic-smoke prohibition accounting;
- unrelated-state preservation proof;
- exact report-only publication fence.

## Result tokens

Use exactly one:

- `PASS_FRESH_INSTALL_OWNED_RUNTIME_NO_FLASH_VERIFIED`
- `BLOCKED_RESIDUE_REPROOF_OR_BOUNDED_CLEANUP`
- `BLOCKED_FRESH_INSTALL_OR_TRANSACTION_RECOVERY`
- `BLOCKED_OWNED_RUNTIME_BINDING`
- `BLOCKED_NO_FLASH_MULTI_TICK_ACCEPTANCE`
- `BLOCKED_FINAL_MANAGED_HEALTH`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Pre-authorized successor

If Task 072 is independently accepted, Task 073 may perform one bounded real semantic acceptance flow through the installed product:

`user message -> durable Ticket -> Ollama LLM -> durable result/delivery -> user-visible response`

Task 073 must not repeat install/cleanup and must separately prove durable Ticket/event/outbox/session evidence and idempotent delivery semantics.
