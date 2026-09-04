# CNX-20260904-246 — Independent Review

## Verdict

`ACCEPT_BLOCKED_EXACT_EXCEPTION_UNPROVEN__TASK245_EVIDENCE_PRESERVED_BYTE_IDENTICALLY__POWERSHELL51_NATIVE_STDERR_CAPTURE_HYPOTHESIS_REQUIRES_TDD_PROOF`

## Reviewed authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Reviewed Task-246 report HEAD: `18ec3763bdc8c5a6ffdd8815d863f59447e5e7f7`
- Parent Task-245 report HEAD: `5984e3dfe3503bee37c218cb1f34eff16a071bef`
- Exact executable candidate used by Task 245: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31` (unchanged)

Task-246 report-head Actions were independently checked and are all green:

```text
PS5.1 Acceptance Smoke        33881077771 = SUCCESS
Windows Installer Pack Smoke 33881077746 = SUCCESS
Validate                      33881077796 = SUCCESS
```

The report commit is coordination-only relative to the Task-246 authority HEAD; no product/source/test/workflow drift was introduced by Task 246.

## Accepted findings

### 1. Task-245 raw evidence was preserved before it could age out

Task 246 copied both Task-245 temporary roots into:

```text
C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260904-246/
```

The preservation proof records:

```text
artifacts copied = 34
missing source artifacts = 0
source/destination SHA-256 equality = 34/34
size equality = 34/34
```

The originals were not deleted or edited. This closes the earlier risk that `%LOCALAPPDATA%\Temp` cleanup could erase the Task-245 evidence before independent diagnosis.

### 2. Task 245 remains a real terminal installer failure

The preserved evidence still proves:

```text
ticket-db-bootstrap = exit 0
plugin-npm-pack = exit 0
plugin-rollover-prepare = entered
installer child = started
installer child exit = 1
runner outcome = child_nonzero_exit
LastTaskResult = 1
installer retry = 0
```

The exact detached source/manifest/runner binding from Task 245 remains accepted. Scheduler, runner, and action-binding uncertainty are not reopened.

### 3. The exact Python exception is genuinely unavailable from retained bytes

The complete preserved `child-stderr.txt` contains only npm warnings followed by the first Python traceback line wrapped by Windows PowerShell 5.1 as:

```text
python.exe : Traceback (most recent call last):
...
FullyQualifiedErrorId : NativeCommandError
```

No Python traceback frame, exception class, exception message, or final traceback line survives in the retained bytes. The runner itself recorded no runner exception; it correctly observed a nonzero child PowerShell exit.

Therefore `BLOCKED_EXACT_EXCEPTION_UNPROVEN` is the correct narrow disposition. It would be unsound to label the failure as a particular `prepare_plugin_rollover_transaction()` invariant from the available evidence.

### 4. No Task-245 rollover transaction exists

Exact source proves that the rollover transaction JSON is written only after `prepare_plugin_rollover_transaction()` returns successfully. No Task-245 transaction or partial transaction exists in `install-staging`, so successful prepare return was not reached.

This proves the terminal boundary is inside the prepare call, but does not identify the exact raising operation.

### 5. Backup domains were correctly separated

Task 246 correctly distinguishes:

```text
workspace/.cogentnexus-openclaw/install-backups
```

from:

```text
%LOCALAPPDATA%/CogentNexus-OpenClaw/plugin-generation-rollover-backups
```

The Task-245 workspace backup `cogentnexus-openclaw-20260904-195413` is a skill/install backup and does not prove rollover-generation backup creation or attestation success.

No new Task-245 external generation-rollover backup or new Task-245 rollover transaction was proven.

### 6. Live safety was preserved

Task 246 made no installer, rollover, plugin, lifecycle, DB, recovery, or semantic mutation. The retained postflight remained:

```text
controller = passthrough
generation = 39
provider = ollama
Gateway = READY
Delivery = READY / pending 0
Recovery = READY
SQLite integrity = ok
installed plugin = predecessor e3bcce04...
plugin status = disabled
```

## Independent source finding

The Task-239 observability repair is not yet proven correct on the actual Windows PowerShell 5.1 native-stderr semantics exercised by Task 245.

The exact candidate begins with:

```powershell
$ErrorActionPreference = "Stop"
```

and the rollover prepare capture is:

```powershell
$prepareOutput = (& python ... 2>&1 | Out-String)
```

Task 245 then produced a Windows PowerShell `NativeCommandError` wrapper while retaining only the first line of the Python traceback. The Task-239 regression tests prove that the source contains `2>&1`, that the bounded helper works, and that a PowerShell runtime can execute that helper; they do **not** execute the real native-command stderr capture boundary under Windows PowerShell 5.1 with `$ErrorActionPreference = 'Stop'` and a multi-line failing native child.

This is a concrete coverage gap and a plausible mechanism for why the intended bounded diagnostic never retained the complete traceback. It is not yet accepted as root cause until reproduced with an isolated synthetic child.

## Successor decision

Do **not** authorize another live installer attempt yet.

Authorize one repository-only / isolated-Windows TDD successor whose first obligation is to prove or reject the Windows PowerShell 5.1 native-stderr hypothesis without touching CogentNexus/OpenClaw live state.

The successor must:

1. create a test-only RED using Windows PowerShell 5.1 and a harmless synthetic native/Python child that writes a multi-line stderr traceback sentinel and exits nonzero;
2. exercise the same semantic boundary as the installer under `$ErrorActionPreference='Stop'`;
3. prove whether the current construct truncates/terminates before preserving the full child diagnostic and exit code;
4. make no production edit if the hypothesis is not reproduced;
5. only after a meaningful RED, make the smallest production repair that preserves complete bounded diagnostics while retaining fail-closed nonzero semantics and restoring the caller's error preference exactly;
6. obtain exact-SHA GREEN validation before any later live installer successor is considered.

No change to `namespace_ownership.py`, rollover ownership semantics, backup semantics, plugin lifecycle ordering, provider/model/runtime state, or semantic-delivery behavior is authorized by this review.

## Final disposition

Task 246 is accepted as a correct forensic blocker with durable evidence preservation.

`ACCEPT_BLOCKED_EXACT_EXCEPTION_UNPROVEN__TASK245_EVIDENCE_PRESERVED_BYTE_IDENTICALLY__POWERSHELL51_NATIVE_STDERR_CAPTURE_HYPOTHESIS_REQUIRES_TDD_PROOF`
