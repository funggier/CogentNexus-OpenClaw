# Independent Review — CNX-20260901-212 Task-211 Normal-Upgrade Recovery Install-Over

## Verdict

`ACCEPT_BLOCKED_INSTALLER_TERMINAL__LAUNCH_SOURCE_AND_HARNESS_ROOT_CAUSE_REQUIRED`

Task 212 correctly refused to claim installation success after the recorded PowerShell PID disappeared with zero-byte stdout/stderr, zero installer stage markers, no exit code, and unchanged live plugin/runtime state. The one Task-212 launch is consumed and must not be replayed under the same evidence model.

However, the current evidence does **not** establish an installer/product failure. Two executor-side authority gaps must be resolved before any further install authorization.

## Accepted Task-212 facts

- exact Task-207 package proof and candidate fingerprint were revalidated;
- preflight reproduced the accepted ordinary-upgrade state: PASSTHROUGH, old live fingerprint `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`, candidate fingerprint `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`, startup absent, Gateway healthy, delivery/recovery READY;
- Task-205 cancellation remained persisted and inert;
- Task 212 launched exactly one recorded PowerShell PID `21836` at `2026-09-01T10:52:23.957Z`;
- the recorded PID was absent on the first bounded sample roughly 27 seconds later;
- retained installer stdout and stderr were both zero bytes;
- zero installer stage START/COMPLETE markers and no success/failure terminal line were captured;
- no process kill, installer retry, lifecycle workaround, manual plugin/ownership/SQLite mutation, or Discord traffic occurred;
- post-state remained the old plugin fingerprint `f826...`, PASSTHROUGH, startup absent, Gateway healthy, SQLite integrity `ok`.

These facts support `BLOCKED_INSTALLER_TERMINAL`, not PASS and not a product FAIL.

## Finding 1 — executed source boundary was not proven to be Task-207

Task 212 explicitly required:

`powershell.exe ... -File <TASK212_VERIFIED_CANDIDATE>/scripts/install.ps1 ...`

The report records the actually launched file as:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx-successor-204-authority-20260901T/scripts/install.ps1`

That path is a retained authority/source directory from an earlier Task-204-era boundary. The report separately proves the Task-207 package archive/fingerprint, but it does not prove that the **source tree containing the executed `install.ps1`** was byte-/commit-/plugin-fingerprint-bound to Task-207 candidate `27fe0181...`.

This matters because `scripts/install.ps1` packages and installs the plugin from its own repository-relative `plugins/cogentnexus-openclaw` tree. Package-proof verification in a different directory does not bind the executed installer source automatically.

Therefore Task 212 has an installer-source provenance gap even before interpreting PID behavior.

## Finding 2 — detached launcher identity/behavior is unproven

Task 212 required root identity by PID + creation time + executable path before interpretation. The report records PID, start time, command, and `detached: true`, but does not retain a fresh OS identity tuple proving that PID `21836` was the expected `powershell.exe` with the exact command line after launch.

The observed shape also differs materially from known-good Task-170 evidence:

- Task 170 captured a wrapper PID and a distinct installer PID;
- the installer lived for ~13.5 minutes;
- stdout grew to ~93 KB;
- all seven stage pairs were captured;
- a watcher timeout did not terminate the installer; the same PID was later polled to natural completion.

Task 212 instead observed zero stream bytes and PID disappearance before the first ~30-second sample. This can be caused by an executor/launcher problem, an immediate PowerShell invocation failure, or another pre-body boundary. The current report cannot distinguish them.

## Root-cause requirement before another install

Do not authorize another product installer yet.

A read-only / harmless-harness successor must first:

1. bind the exact Task-212 executed source root to an identity:
   - hash the executed `scripts/install.ps1`;
   - compute the plugin fingerprint of that root's `plugins/cogentnexus-openclaw` using exact Task-207 tooling;
   - inspect any source/package identity metadata available there;
   - compare against candidate `27fe0181...` / fingerprint `d067...` and old generation `f826...`;
2. preserve and inspect the exact Task-212 `launch-installer.py` and `monitor-installer.py` source/hashes;
3. enumerate exact `subprocess.Popen` arguments, creation flags, stdio handle configuration, cwd/env, shell/close_fds settings;
4. reproduce the launcher behavior using a **harmless PowerShell child**, not the installer, with the same launch options. The probe should write deterministic stdout/stderr markers, remain alive for at least 60 seconds, and exit with a known code while its PID/executable/command line/creation time are independently observed;
5. compare this with the known-good Task-170 root-process observation pattern;
6. leave product/runtime/ownership/SQLite/Discord state untouched.

Only after that diagnostic closes the source/launcher boundary may a later task authorize another installer attempt using an exact Task-207 source tree and a verified observer model.

## Product/release authority

Public `v0.9.3` remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

Repository-GREEN Task-207 candidate remains `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`.

No product-source defect is accepted from Task 212.

## Discord

Task-207 live Discord acceptance remains closed. No Send is authorized until installation/provenance/managed convergence is independently proven.
