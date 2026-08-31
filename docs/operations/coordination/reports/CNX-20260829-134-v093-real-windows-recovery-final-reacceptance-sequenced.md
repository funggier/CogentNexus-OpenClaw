# CNX-20260829-134 — v0.9.3 Real-Windows Recovery Final Re-Acceptance (Sequenced Harness)

## Verdict

**PASS — one-shot real-Windows recovery acceptance completed.** The exact Task-133 candidate harness ran once through a true interactive PowerShell PTY, the single lowercase confirmation was entered after the literal prompt, all four recovery scenarios passed, and the final read-only snapshot remained coherent. No installer replay, source/harness edit, Dashboard Send, or manual normalization was performed.

## Authority and exact candidate

- Task: `CNX-20260829-134`
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Exact coordination start HEAD: `ac27df1308b9573ec83d8944b097e5eeee71b2f9`
- Accepted source candidate: `1424d6fbee2c458c8c30440616783d2fa1bc1201`
- Exact harness Git blob: `a4138e00e2056db89b0a9eceed1b54e001c4e319`
- Execution checkout: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue-20260829T063406Z\candidate`
- Execution harness SHA-1 Git object: `a4138e00e2056db89b0a9eceed1b54e001c4e319`
- Evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue-20260829T063406Z\evidence\`

Task 133 was independently accepted before this task. Its exact package proof was retained as the accepted provenance:

- artifact ID: `9709798190`
- outer digest: `sha256:e8dbb2f742bfeffc93a80a7cda62a8c273ced9e2b1e9b47a3962dead52ccfeef`
- payload count: `178`
- payload fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

The installed runtime/plugin was not redeployed. The source candidate was used only for the exact acceptance harness while live commands were directed through the installed launcher.

## Phase 0 — authoritative safe preflight

Explicit installed launcher read and hash:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd
SHA256: f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10
```

The launcher explicitly invokes:

```text
C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe
C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py
--root C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw
%*
```

The authoritative state root was therefore verified as:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Read-only preflight results:

- ownership manifest verification: PASS;
- mode: `managed`;
- desired Gateway/provider: `running`;
- host selected provider: `ollama`;
- provider-status selected provider: `ollama`;
- recovery verdict: exact `READY`;
- no active provider recovery incident or transition;
- installed plugin resolution: exactly one matching payload;
- plugin version: `0.9.3`;
- installed payload fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- OpenClaw version: `2026.7.1-2`;
- OpenClaw plugin inventory: exactly one `cogentnexus-openclaw`, `enabled=true`, `status=loaded`;
- Gateway listener: `127.0.0.1:18789`, PID `14620` at preflight;
- Ollama listener: `127.0.0.1:11434`, PID `18180` at preflight;
- Ollama API `/api/version`, `/api/tags`, `/api/ps`: HTTP `200`;
- Ollama version: `0.32.15`;
- preflight model inventory: `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b`;
- SQLite authoritative path: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`;
- SQLite opened with URI `mode=ro`; `PRAGMA integrity_check`: exact `ok`;
- supervisor task: `Ready`, last result `0`, product-owned `pythonw.exe`, explicit state-root argument;
- no duplicate active recovery operation observed.

One early probe passed OpenClaw's version string to the plugin resolver's `--version` parameter and correctly received a rejection; this was a probe-argument error, not a live-state result. A corrected direct probe used plugin version `0.9.3` and passed with the exact fingerprint above. No state was changed during either probe.

## Phase 1 — interactive confirmation and one-shot ledger

The exact process was started once in a true PTY with this literal command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/AppData/Local/Temp/cnx-continue-20260829T063406Z/candidate/scripts/test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

The PTY visibly reached:

```text
Type y to continue:
```

Exactly one lowercase `y` followed by Enter was submitted. The process exited once with exit code `0`. No suite or scenario was rerun.

Harness evidence:

- log: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-133839.txt`
- JSON: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-133839.json`
- retained copies: `evidence\acceptance-suite.txt` and `evidence\acceptance-suite.json`
- suite result: `PASS`
- schema version: `4`
- recorded steps: `59`
- explicit disruptive confirmation: `PASS`

## Scenario results

### Baseline

- baseline assertion: PASS;
- managed/Ollama state: PASS;
- exact ordinary recovery verdict: `READY`.

### Gateway crash

- pre-crash Gateway listener PID: `14620`;
- exact validated target identity: OpenClaw Gateway `node.exe`;
- process-tree kill: not used;
- recovered Gateway listener PID: `11788`;
- recovered listener was different from the pre-crash PID: PASS;
- durable convergence: PASS;
- ordinary convergence verdict: `READY`;
- scenario: PASS.

### Provider crash

- pre-crash Ollama listener PID: `18180`;
- exact validated target identity: `ollama.exe serve`;
- process-tree kill: not used;
- recovered Ollama listener PID: `5220`;
- recovered listener was different from the pre-crash PID: PASS;
- provider circuit: closed;
- provider convergence: PASS under the accepted carried-incident contract;
- convergence verdict: `READY_WITH_WARNINGS`;
- exactly one allowed WARN: Provider recovery incident;
- incident ID: `ollama:3`;
- classification: `provider_unreachable`;
- incident open: true;
- circuit open: false;
- adapter row: exactly one with `expected=false`;
- all other recovery checks: PASS;
- scenario: PASS.

### Provider-to-operator boundary

`assert-managed-operator-before`: PASS.

The same harness process accepted the carried incident only because:

- immediately preceding scenario was `provider-crash`;
- incident ID exactly matched `ollama:3`;
- classification matched `provider_unreachable`;
- verdict was `READY_WITH_WARNINGS`;
- exactly one WARN was the open/circuit-closed Provider recovery incident;
- managed/Ollama structural state and both listeners were healthy;
- adapter was exactly one row with `expected=false`.

Standalone or non-carried warning acceptance was not used.

### Operator stop and post-start convergence

- harness-owned `cnxclaw stop`: PASS;
- maintenance state with desired Gateway/provider stopped: PASS;
- Gateway stopped and remained stopped during the intentional observation: PASS;
- `intentional-stop-no-auto-recovery`: PASS;
- harness-owned `start-after-intentional-stop`: PASS;
- Gateway and Ollama listeners returned: PASS;
- post-start convergence used strict ordinary path without carried-warning exception: PASS;
- final post-start verdict: exact `READY`;
- final scenario: PASS.

Final post-start listener PIDs were Gateway `14468` and Ollama `18852`, both different from the corresponding pre-disruption processes.

## Phase 3 — final read-only snapshot

Final read-only probes were executed after suite completion through the same authoritative launcher/root plus direct read-only identity/API probes:

- final mode/desired state: managed / running / running;
- final selected provider: `ollama`;
- final recovery verdict: `READY`;
- final Provider recovery incident: no active incident, circuit closed;
- final adapter: exactly one row, `expected=false`;
- final Gateway and Ollama listeners: healthy;
- final Ollama `/api/version`, `/api/tags`, `/api/ps`: HTTP `200`;
- final model inventory equals preflight inventory (four named models above);
- final SQLite read-only `PRAGMA integrity_check`: exact `ok`;
- final supervisor task observation: retained and read-only;
- no Dashboard Send;
- no manual cleanup, repair, or normalization.

## Mutation ledger

Authorized effects occurred only inside the single exact harness process:

- recovery suite launches: `1 / 1`;
- interactive confirmation: one lowercase `y`;
- Gateway exact-PID crash injection: `1`;
- Ollama exact-PID crash injection: `1`;
- harness-owned intentional `cnxclaw stop`: `1`;
- harness-owned `cnxclaw start` after intentional stop: `1`;
- generic process-tree kill: `0`;
- installer/install-over/reset/uninstall/reinstall: `0`;
- lifecycle operation outside the exact harness: `0`;
- provider/model/OpenClaw/config mutation outside the harness: `0`;
- scheduled-task/service mutation: `0`;
- manual normalization/cleanup: `0`;
- reboot: `0`;
- credentials/secrets accessed: `0`;
- Dashboard semantic Send: `0`;
- merge/tag/release: `0`;
- force push: `0`.

The harness's built-in best-effort reconciliation was not required after the successful suite.

## Next state

Task 134 is complete and this report is published for independent ChatGPT review. Per the task fence, execution stops here. No Dashboard durable-delivery acceptance or successor live task was opened automatically.
