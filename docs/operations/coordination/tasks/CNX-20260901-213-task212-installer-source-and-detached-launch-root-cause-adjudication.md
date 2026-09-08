# CNX-20260901-213 — Task-212 Installer Source + Detached-Launch Root-Cause Adjudication

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-212`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Close the two unresolved Task-212 executor boundaries **without running the CogentNexus installer again**:

1. prove which source/plugin generation the actually executed Task-212 `install.ps1` belonged to;
2. prove whether the Task-212 detached Python/PowerShell launcher can correctly preserve a child process, redirected streams, and OS identity independently of CogentNexus.

This is root-cause investigation only. No product/runtime mutation is authorized.

## Immutable authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-207 repository-GREEN candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Task-207 candidate plugin fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

Known old live/pre-Task-207 plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Task-212 report commit:

`6f4543f05449b26f74ccbc1ffcb167512c84d945`

Task-212 evidence root:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx212-task211-normal-upgrade-install-20260901T`

Recorded Task-212 executed installer path:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx-successor-204-authority-20260901T/scripts/install.ps1`

## Hard fence

Task 213 authorizes **zero CogentNexus/OpenClaw semantic or lifecycle mutations**.

Do NOT:

- run `scripts/install.ps1`;
- run install-over, reset, uninstall, reinstall, enable, disable, start, stop, restart;
- enable/disable/install/remove OpenClaw plugins;
- modify ownership manifest, install-staging, transactions, backups, workspace state, controller state, startup task, provider/model config, or SQLite;
- send Discord traffic of any kind;
- terminate unrelated processes;
- edit product source/tests/workflows;
- mutate Release/tag/assets;
- force push.

A harmless temporary PowerShell process used only to test process-launch mechanics is authorized. It must not reference or execute product scripts.

## Phase A — fresh authority and live preservation

Read current remote HEAD, ACTIVE/STATUS, Task-212 report/review, and this task.

Capture read-only live state:

- controller mode/generation;
- Gateway health;
- selected Ollama/provider readiness;
- startup adapter state;
- delivery/recovery status;
- live plugin fingerprint;
- Task-205 cancellation/inert state;
- SQLite `PRAGMA integrity_check`;
- relevant installer/lifecycle process scan.

Expected preservation shape is still approximately:

```text
mode = passthrough
live plugin fingerprint = f82674172...
startup adapter installed = false
Gateway = healthy
Task-205 recovery = cancelled/inert
SQLite integrity = ok
```

If unexpected active lifecycle/installer processes exist, stop `BLOCKED_ACTIVE_PROCESS` without mutation.

## Phase B — bind the source tree actually executed by Task 212

For:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx-successor-204-authority-20260901T`

perform read-only identity proof.

Required evidence:

1. path exists/not exists;
2. SHA-256 and byte size of `scripts/install.ps1`;
3. SHA-256 comparison against `scripts/install.ps1` from exact candidate `27fe0181...`;
4. inspect any source identity metadata in that tree (`PAYLOAD_IDENTITY.json`, package/source commit markers, Git metadata if present, or other authoritative metadata) without assuming it exists;
5. compute the plugin fingerprint of that tree's `plugins/cogentnexus-openclaw` using the **exact Task-207 `namespace_ownership.py plugin-fingerprint` tool**;
6. compare that fingerprint against:
   - `d0677581...` Task-207 candidate;
   - `f82674172...` old installed generation;
7. if the tree is a Git checkout, obtain `git rev-parse HEAD` read-only and relation to `27fe0181...`;
8. hash key Task-207 repair file in that tree:
   `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
   and compare to exact candidate bytes.

Do not infer source identity from filename/path/date alone.

Classify source binding as one of:

- `EXECUTED_SOURCE_EXACT_TASK207`
- `EXECUTED_SOURCE_PRE_TASK207_OR_OTHER`
- `EXECUTED_SOURCE_INDETERMINATE`

## Phase C — preserve Task-212 harness source exactly

From Task-212 evidence root, read/hash:

- `launch-installer.py`
- `monitor-installer.py`
- `b05-installer-launch.json`
- `b06-installer-samples.json`
- zero-byte stdout/stderr metadata

Extract and report the exact launch mechanics:

- executable and argv;
- `cwd`;
- environment modifications, if any;
- `stdout` / `stderr` handles and modes;
- `stdin` handling;
- `shell`;
- `close_fds`;
- `creationflags` decoded to names/hex;
- `start_new_session` if used;
- any wrapper process or helper process;
- whether handles are closed before/after `Popen`;
- how PID/creation time/executable/command line are captured;
- whether the launcher itself exits immediately.

Do not edit the retained harness scripts.

## Phase D — harmless synthetic detached-launch reproduction

Create a new external evidence-only directory under `%LOCALAPPDATA%\Temp`.

Use the **same process-launch options** as Task-212 `launch-installer.py`, changing only the child command from the product installer to a harmless explicit PowerShell command/script that:

1. writes a unique marker to stdout immediately;
2. writes a different unique marker to stderr immediately;
3. records its own PID and timestamp to stdout;
4. sleeps for at least 60 seconds;
5. writes terminal stdout/stderr markers;
6. exits with a known nonzero code such as `23` so exit capture can be tested without ambiguity.

The synthetic child must not read/write CogentNexus/OpenClaw paths.

Immediately after launch and again at ~10s, ~30s, and ~60s, capture by OS/CIM/WMI:

- PID;
- creation time;
- executable path;
- full command line;
- parent PID;
- process existence;
- stdout/stderr file sizes/hashes/content markers.

After natural exit, capture whether the known exit code can be recovered by the launcher model. Do not kill the child merely to finish the test.

### Interpretation

If the harmless child reproduces Task-212 behavior (rapid disappearance and/or zero-byte streams), the launcher/harness is proven defective or incompatible with this executor environment.

If the harmless child behaves correctly for >=60 seconds with expected stream markers, the generic detached-launch mechanism is not sufficient to explain Task 212; investigate the specific PowerShell installer invocation/source path boundary from retained evidence.

## Phase E — compare against known-good Task-170 pattern

Using repository report evidence and, if still present, read-only retained Task-170 evidence:

- identify wrapper PID vs installer PID model;
- identify whether Task 170 used `DETACHED_PROCESS`, `CREATE_NEW_PROCESS_GROUP`, `Start-Process`, `Popen`, or another mechanism if the retained wrapper source proves it;
- identify how stdout/stderr were inherited/redirected;
- identify how the exact installer PID survived executor timeout;
- list material differences from Task-212 launcher.

Do not guess a flag from outcome alone; label unavailable details as unavailable.

## Phase F — root-cause classification

Allowed final dispositions:

- `PASS_WRONG_SOURCE_BOUNDARY_PROVEN`
- `PASS_DETACHED_LAUNCH_HARNESS_DEFECT_PROVEN`
- `PASS_BOTH_SOURCE_AND_HARNESS_DEFECTS_PROVEN`
- `PASS_SOURCE_EXACT__INSTALLER_INVOCATION_BOUNDARY_ISOLATED`
- `BLOCKED_SOURCE_IDENTITY`
- `BLOCKED_HARNESS_REPRODUCTION`
- `BLOCKED_ACTIVE_PROCESS`
- `BLOCKED_EVIDENCE`

A PASS here means diagnostic closure only, **not product acceptance**.

The report must state the single strongest root-cause claim supported by evidence and explicitly separate proven facts from hypotheses.

## Discord budget

`0 Discord Sends`.

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-213-task212-installer-source-and-detached-launch-root-cause-adjudication.md`

Then stop for ChatGPT review. Do not continue into another installer attempt in Task 213.
