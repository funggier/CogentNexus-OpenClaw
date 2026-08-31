# CNX-20260831-177 — Windows CMD/Batch Incremental Harness Qualification

- **Task:** `CNX-20260831-177`
- **Execution mode:** `WINDOWS_CMD_BATCH_INCREMENTAL_HARNESS_QUALIFICATION_HERMES`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority HEAD before work:** `29aa8bc75fb3fc79caa94a1b9f69742425ee412a`
- **Disposition:** `PASS — CMD_BATCH_INCREMENTAL_HARNESS_QUALIFIED`
- **Destructive actions:** `0`
- **Semantic actions:** `0`
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx177-evidence-20260831T044500Z`

## Executive result

Task-177 qualified the exact harmless Windows topology required for a future reset acceptance attempt:

```text
outer Python harness
  -> cmd.exe /d /c
      -> disposable .cmd
          -> disposable Python input() child
```

Two independent runs passed with no product import, live runtime mutation, durable-state mutation, model/provider action, destructive lifecycle action, timeout, or orphan. The harness observed the non-newline prompt before input, drained stdout and stderr concurrently from process start through process exit, persisted an append-only event ledger incrementally, sent exactly one unique token line per run, retained exact ACK/output/exit evidence, and completed orphan checks.

This is a harness qualification only. It does not authorize or perform reset.

## Fresh authority and live safety preflight

GitHub remote branch was fetched before work:

- authority HEAD: `29aa8bc75fb3fc79caa94a1b9f69742425ee412a`;
- active task: `CNX-20260831-177`;
- Task-177 report was absent at the authority check;
- Task-176 was accepted as a diagnostic pass while leaving Task-175 reset completion unproven;
- no successor/conflicting reset authorization was present.

Read-only live sanity checks remained coherent:

- installed release: `0.9.3`;
- installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
- accepted product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`;
- OpenClaw: `2026.7.1-2`;
- controller: `managed`, generation `36`;
- Gateway: healthy on `127.0.0.1:18789`;
- Ollama: reachable/healthy/ready;
- delivery: `READY`, pending outbox `0`, `stateChanged=false`;
- recovery: `READY`, no active incident, `stateChanged=false`;
- ownership: `OWNERSHIP_PRESENT`, legacy inventory empty;
- no active reset/uninstall/diagnostic process at the final scan.

## Disposable topology and hashes

Disposable child:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx177-evidence-20260831T044500Z\input_child.py
```

Source:

```python
import sys
value=input("Continue? [y/N]: ")
print("ACK:"+value)
```

Disposable batch file:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx177-evidence-20260831T044500Z\disposable.cmd
```

It only invokes `%PYTHON_EXE%` on `input_child.py` and propagates `%ERRORLEVEL%`.

Harness:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx177-evidence-20260831T044500Z\harness177.py
```

SHA-256:

```text
input_child.py  10a1342ca68bf48d46ba5721a115cbc65ef4d6100c9f08a1ea5ca0ef1da84e18
disposable.cmd  f0374cafa3c337b54afaf40b0d7ee88b8d1aaf609323341065c0c896ef8a777e
harness177.py   846446e4b5ca34f7c88340d8ee69288e944d06e3fe7daf9054e6a5bfa2680cef
summary.json    8659e6a48cc8efa1e21a503b4e800c2869830027024d47e6c4f268558124443e
```

The child contains no CogentNexus/OpenClaw import, path, command, model, provider, or live-state access.

## Harness architecture

For each run the outer Python harness:

1. created a disposable environment with `PYTHON_EXE` pointing to the current Python executable;
2. launched `cmd.exe /d /c <disposable.cmd>` with stdin/stdout/stderr pipes;
3. started independent stdout and stderr reader threads immediately after process start;
4. wrote each captured character incrementally to its stream log and flushed it;
5. consumed stdout at character granularity so the non-newline prompt was observable;
6. persisted each critical event as a separate JSONL record, flushing and `fsync`-ing after every event;
7. detected `Continue? [y/N]: ` before writing any token;
8. guarded input with an in-memory send counter and sent one token line;
9. closed stdin, drained both readers through process exit, recorded the final return code, scanned orphan state, and finalized a per-run result JSON.

The critical prompt and input events were durable in the JSONL ledger before `cmd_process_exited` and before `run_finalized`.

## Run 1

Run ID: `R1-T177-CMD-20260831T044500Z-A1`

- Token: `T177-CMD-20260831T044500Z-A1`
- `cmd.exe` PID: `21520`
- Started: `2026-08-31T04:38:09.471754+00:00`
- Prompt observed: `2026-08-31T04:38:09.527345+00:00`
- Input intent: `2026-08-31T04:38:09.528346+00:00`
- Input sent: `2026-08-31T04:38:09.529346+00:00`
- Input send count: `1`
- stdout: `Continue? [y/N]: ACK:T177-CMD-20260831T044500Z-A1` plus newline
- stderr: empty
- Exit code: `0`
- stdout reader: complete
- stderr reader: complete
- Orphan: `false`
- Timeout: `false`

Ledger: `R1-T177-CMD-20260831T044500Z-A1.events.jsonl`.

Ordered durable events were:

```text
harness_started
cmd_process_started
prompt_observed
input_send_intent
input_sent
stdin_closed
stderr_reader_completed
stdout_reader_completed
cmd_process_exited
orphan_scan_completed
run_finalized
```

## Run 2

Run ID: `R2-T177-CMD-20260831T044500Z-B2`

- Token: `T177-CMD-20260831T044500Z-B2`
- `cmd.exe` PID: `22916`
- Started: `2026-08-31T04:38:09.541558+00:00`
- Prompt observed: `2026-08-31T04:38:09.586169+00:00`
- Input intent: `2026-08-31T04:38:09.587170+00:00`
- Input sent: `2026-08-31T04:38:09.588170+00:00`
- Input send count: `1`
- stdout: `Continue? [y/N]: ACK:T177-CMD-20260831T044500Z-B2` plus newline
- stderr: empty
- Exit code: `0`
- stdout reader: complete
- stderr reader: complete
- Orphan: `false`
- Timeout: `false`

Ledger: `R2-T177-CMD-20260831T044500Z-B2.events.jsonl`.

Ordered durable events were equivalent to Run 1, with `prompt_observed` and `input_sent` persisted before `cmd_process_exited`.

## Installed launcher correlation

The installed launcher was inspected read-only:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd
```

Launcher SHA-256:

```text
f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10
```

The installed launcher topology is:

```text
cmd.exe /d /c cnxclaw.cmd reset
  -> installed runtime Python
      -> cnxclaw_v093.py
          -> accepted lifecycle backend
              -> input("Continue? [y/N]: ")
```

The installed batch launcher invokes the Python facade and propagates `%ERRORLEVEL%`, materially matching the disposable `.cmd` topology. The lifecycle prompt remains non-newline-terminated. The qualification therefore covers the relevant `cmd.exe`/batch/Python stdin and prompt boundary without invoking the live launcher.

Installed source hashes recorded read-only:

```text
cnxclaw_v093.py   994078bc4c79bc5f653744a9ba08ccdf10fb60d0366e186df0f4b561a8957a85
lifecycle_v092.py 82c64e9acb21c22d062fd461cf687a5ea4d96369b972cfca3feaecb261353872
cnxclaw.cmd       f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10
```

The remaining difference is product-owned internal work after confirmation. That work was intentionally not exercised by Task-177 because reset is prohibited.

## Acceptance matrix

| Criterion | Verdict | Evidence |
|---|---|---|
| Fresh authority | `PASS` | Remote HEAD `29aa8bc...`, fresh ACTIVE/STATUS, Task-177 active |
| Exact disposable cmd/batch/Python topology | `PASS` | `disposable.cmd`, `input_child.py`, harness and run PIDs |
| Prompt observed before input | `PASS` | Both JSONL ledgers record prompt before input intent/sent |
| Concurrent stdout/stderr draining | `PASS` | Independent readers started from process start; both complete in both results |
| Incremental ledger before process exit | `PASS` | JSONL prompt/input events precede `cmd_process_exited` |
| Exactly one input per run | `PASS` | `input_send_count=1` in both results and final events |
| Exact ACK and exit `0` | `PASS` | Both retained stdout and result JSON show exact token ACK and return code `0` |
| No timeout/orphan | `PASS` | Both `timeout=false`, `orphan=false`; reader threads complete |
| Installed launcher correlation | `PASS` | Read-only launcher/source chain and hashes; no material stdin topology difference |
| Zero destructive/semantic/live mutation | `PASS` | Only disposable children; no product command/lifecycle/model/state access |
| Report-only publication | `PASS` | Only required Task-177 report will be staged/published |

## Reviewer Verification Packet

1. **Topology:** Each run used outer Python → `cmd.exe /d /c` → disposable `.cmd` → disposable Python `input()` child.
2. **Concurrent drain:** stdout and stderr readers started immediately and completed independently before finalization.
3. **Run 1 ordering:** JSONL records prompt observation at `04:38:09.527345Z`, input intent/sent next, and process exit later at `04:38:09.535434Z`.
4. **Run 2 ordering:** JSONL records prompt observation at `04:38:09.586169Z`, input intent/sent next, and process exit later at `04:38:09.593277Z`.
5. **Exactly one input:** Both final results and `run_finalized` events record send count `1`.
6. **Result reliability:** Both runs produced exact token ACK, empty stderr, exit `0`, completed readers, and no orphan.
7. **Launcher compatibility:** Installed `cnxclaw.cmd` is a batch-to-Python facade with the same relevant stdin inheritance and exit propagation topology; the real lifecycle prompt is confirmed non-newline-terminated by read-only source inspection.
8. **Safety:** No reset, uninstall, lifecycle helper, Gateway/Ollama action, semantic action, model/recovery action, or live-state mutation occurred.
9. **Residual boundary:** Internal reset-owned transaction behavior remains untested and requires a separate future authorization; Task-177 does not imply reset acceptance.
10. **Publication fence:** Only this report is published; stop follows immediately.

## Hard-fence declaration

No reset, uninstall, install/reinstall, start/stop/restart/enable/disable, Gateway/Ollama lifecycle mutation, Dashboard Send, model/recovery action, manual durable/config/transcript mutation, product/source/test/workflow/dependency change, upgrade, release, merge, or force push was performed.

Task-177 is complete as `PASS — CMD_BATCH_INCREMENTAL_HARNESS_QUALIFIED` and is stopped for ChatGPT review. A future reset requires a separate explicit authorization.
