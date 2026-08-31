# CNX-20260831-174 — Windows Reset / Fresh-State Reconstruction Acceptance

- **Task:** `CNX-20260831-174`
- **Execution mode:** `WINDOWS_RESET_FRESH_STATE_RECONSTRUCTION_ACCEPTANCE_HERMES`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority:** GitHub remote branch; preflight authority HEAD `dceaf8467c1ac995442251cb567bcc898549fe45`
- **Executor:** Hermes/Codex
- **Disposition:** `BLOCKED`
- **Semantic action count:** `0`
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx174-evidence-20260831T034900Z`
- **Postflight observed:** `2026-08-31T03:51:16.209282Z`

## Executive result

Task-174 did not reach the destructive reset phase. The single authorized normal installed invocation was started exactly once, but the installed CLI aborted while reading its confirmation input with:

```text
OSError: [Errno 9] Bad file descriptor
```

The captured output included the documented warning and `Continue? [y/N]:` prompt text, but no explicit `y` was sent. The process exited with code `1`. Under the Task-174 hard fence, this is not retried and no second reset or executor-issued lifecycle action is permitted.

Because the required confirmation and fresh-state reconstruction were not completed, Task-174 cannot be reported as `PASS`.

## Frozen accepted baseline

The fresh remote coordination state required the following identity to remain unchanged:

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed plugin fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- OpenClaw: `2026.7.1-2`
- Task-171 semantic Send count: permanently frozen at exactly `1`

## Read-only preflight

Preflight completed before the reset invocation:

| Check | Result |
|---|---|
| Installed candidate identity | `PASS`; fingerprint exact, version `0.9.3` |
| Namespace ownership | `PASS`; `OWNERSHIP_PRESENT`, legacy inventory empty |
| OpenClaw version | `PASS`; `2026.7.1-2` |
| Gateway/provider/controller health | `PASS`; Gateway healthy, Ollama reachable/healthy/ready, controller `managed` |
| Delivery fence | `PASS`; pending outbox `0` |
| Recovery fence | `PASS`; no active maintenance/provider incident, recovery attempts `0` |
| SQLite preflight | `PASS`; integrity `ok`, frozen Task-171 state present as expected |
| Reset-process collision scan | `PASS`; no pre-existing exact reset process |

## Authorized reset attempt ledger

| Item | Observed result |
|---|---|
| Normal installed invocation | Exactly `1`: `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset` |
| Process | PID `22224`, process session `proc_aa4d35cfb541` |
| Confirmation prompt | Prompt text rendered in captured PTY output; rendering showed two prompt lines, so exact one-prompt occurrence is not claimed |
| Explicit confirmation | `y` count `0` |
| Reset exit code | `1` |
| Reset destructive phase | Not reached; abort occurred at `input("Continue? [y/N]:")` |
| Retry | `0` |
| Executor-issued lifecycle helper after reset began | `0` |
| Semantic/model/recovery action | `0` |

Captured failure:

```text
Traceback (most recent call last):
  ...
  answer = input("Continue? [y/N]: ").strip().lower()
OSError: [Errno 9] Bad file descriptor
```

The complete captured warning/traceback is preserved in `b01-reset-output.txt`. The process session log is also preserved by Hermes under `proc_aa4d35cfb541`.

## Read-only post-attempt state

Post-attempt probes were read-only. They show the pre-reset state remained present, so fresh reconstruction did not occur:

- Controller mode remained `managed`.
- Generation remained `36`.
- Gateway remained healthy on `127.0.0.1:18789`, PID `19704`.
- Provider remained `ollama`, reachable/healthy/ready.
- OpenClaw remained `2026.7.1-2`.
- Installed fingerprint remained `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`.
- Namespace ownership remained `OWNERSHIP_PRESENT`.
- Delivery check remained `READY`, pending outbox `0`, `stateChanged=false`.
- Recovery check remained `READY`, no active incident, `stateChanged=false`.
- SQLite remained `integrity=ok`.
- The pre-reset Task-171 durable history remained present; it was not incorrectly claimed as removed.
- Exact reset-process post-scan returned no active reset process.

The unchanged state is evidence that the reset transaction did not pass its confirmation boundary. It is not evidence of successful fresh-state reconstruction.

## Acceptance matrix

| Criterion | Result | Evidence / reason |
|---|---|---|
| Accepted installed candidate remains identified | `PASS` | `b08-post-fingerprint.txt`; exact frozen fingerprint |
| OpenClaw pin remains `2026.7.1-2` | `PASS` | `b06-post-openclaw-version.txt`, `b07-post-gateway.txt` |
| Exactly one reset invocation | `PASS` | process session `proc_aa4d35cfb541`, PID `22224`; no retry |
| Exactly one explicit `y` confirmation | `BLOCKED` | `y` count `0`; PTY failed at confirmation input |
| Reset returns documented fresh-MANAGED PASS | `BLOCKED` | exit code `1`; no fresh result |
| Fresh controller/plugin/Gateway/Ollama/route reconstruction | `UNPROVEN` | reset did not reach implementation-owned transaction |
| Fresh SQLite schema/integrity and old Task-171 removal | `UNPROVEN` | old DB/state remained; no reset reconstruction |
| No semantic/model/recovery work manufactured | `PASS` | hard-fence ledger and read-only postflight; count `0` |
| External OpenClaw/Ollama preservation boundary | `UNPROVEN` | no reset transaction occurred |
| No prohibited retry/helper/lifecycle action | `PASS` | no second reset and no executor-issued lifecycle command |

## Evidence hashes

SHA-256 values for available critical evidence:

```text
b01-reset-output.txt              883ce2f6996524520e54f991bdfd6bd7673224a5ea598c18e96e3b79f4a939ab
b02-post-status.txt               bcac3272c62b989254eabb9855835a735c0c92dd7102cf0c16238df3fd2e317f
b03-post-delivery.txt             a5b9e6d5378897419059dcd8df9ce1bd1e801153b3f328eceda9184f18f3aa0d
b04-post-recovery.txt             9fff3426af115cda2737be7e7f7ca8b7b9e5aad4d42515133057b14f284d5cc5
b05-post-provider.txt             06dff19d744959ab165f46247c73647e29ab3da21a22dd28b3aa3de05f782a12
b06-post-openclaw-version.txt     a6fdfb11f416b511242f86ca7630ced2b59e5ea15db81ea00be4a0acf59c011a
b07-post-gateway.txt              caeb99a136068dc7140daab9be34ecb94b8055831d576aa8a8e49af75a5be1af
b08-post-fingerprint.txt           ddcb261a101c5cbcb201404d9a0f77ad7bef6657da12fc236e0e43f61ffe6525
b09-post-ownership.txt             ea5ab3c77c81d6e673442a0ab1d2abf55ff23cb7bd47ae9d94805690df64edf8
b10-post-recovery-preflight.txt    d559c779b3551e83d0716d606e75eae951942f44c49f63270f2a05c6632f82b3
b11-post-reset-processes-exact.json a5338d955b09046ec0b16f3a9625b7955c763aae07dc722e474e6078745f932f
b12-post-db.txt                   408908d4df18dba1aaad308f74f5fe598b640b9d3f4d05a40757529fd58fcef9
```

The aggregate hash ledger is `c01-critical-hashes.json` in the evidence root. No credentials, tokens, passwords, or connection strings are included.

## Hard-fence declaration

No Dashboard Send, Enter submission, composer input, `chat.inject`, model inference, recovery/regeneration, second reset, lifecycle helper, installer/uninstall/reinstall/rollback, manual DB/config/transcript mutation, source/test/workflow/dependency change, upgrade, release, merge, or force push was performed.

Task-174 is stopped at the documented `BLOCKED` boundary for coordinator/final-reviewer disposition. No retry is authorized by this execution.
