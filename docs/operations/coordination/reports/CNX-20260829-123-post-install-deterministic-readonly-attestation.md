# CNX-20260829-123 — Post-Install Deterministic Read-Only Attestation

## Verdict

**PASS — the post-install state produced by Task 121 is coherent under deterministic, argument-safe, read-only attestation.**

Task 123 performed no product/runtime lifecycle mutation. Task-121 install-over remains consumed and was not replayed.

## Coordination and frozen candidate

Fresh reconciliation identified Task 123 as the active `READY_FOR_HERMES` task on branch `agent/v0.9.3-full-stabilization`.

Frozen candidate identity:

- source SHA: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- artifact ID: `9691451156`
- artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`
- ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`
- tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`
- payload count: `178`
- payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

The prior exact artifact identity remained unchanged. The exact candidate plugin was already prepared and attested in the retained Task-121 candidate boundary; its ownership fingerprint matched the frozen payload fingerprint.

## Evidence root

`C:\Users\CDQ-P\AppData\Local\Temp\cnx123-readonly-attestation-20260829-direct`

Evidence files include:

- `a01-cnx-status.txt`
- `a02-cnx-provider-status.txt`
- `a03-cnx-recovery.txt`
- `a04-ownership-verify.txt`
- `a05-installed-fingerprint.txt`
- `a06-openclaw-version.txt`
- `a07-openclaw-plugins.txt`
- `a08-metadata.json`
- `a09-ollama-version.json`
- `a10-ollama-tags.json`
- `a11-ollama-ps.json`
- `a12-listeners.json`
- `a13-sqlite-integrity.txt`
- `a14-process-identity.json`
- `a15-residue-inventory.json`
- `a16-scheduled-tasks.json`

## Deterministic probe results

### CNX state and provider

Direct PowerShell call-operator invocations used separate literal arguments; no `Start-Process`, generalized wrapper, bare executable, or UI-capable provider command was used.

- `cnxclaw.cmd status`: exit `0`, valid JSON
- `cnxclaw.cmd provider status --json`: exit `0`, valid JSON
- `cnxclaw.cmd check recovery --json`: exit `0`, verdict `READY`, `readOnly: true`, `stateChanged: false`

Observed state:

- mode: `managed`
- generation: `30`
- desired gateway: `running`
- desired provider: `running`
- selected provider: `ollama`
- provider transition: `null`
- pending outbox: `0`
- no active provider recovery incident
- gateway health: `true`

The v0.9.3 Ollama-only runtime facade and its provider text are expected candidate behavior. They do not contradict the provider-neutral installer boundary.

### Ownership and installed payload

Explicit installed ownership verification returned exit `0` and reported the canonical workspace, state root, skill path, plugin path, and launcher path.

Installed plugin fingerprint:

```json
{
  "root": "c:\\users\\cdq-p\\.openclaw\\extensions\\cogentnexus-openclaw",
  "version": "0.9.3",
  "fingerprint": "3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4"
}
```

The installed fingerprint equals the frozen candidate fingerprint. Critical installed script hashes were compared with the candidate extraction:

- `cnxclaw_v093.py`: `9d9e71c9034b116d2fbfd04a9ee17a5e79c5470d338ef03e198f50117922ee0f` on both sides
- `namespace_ownership.py`: `c7477b74824dc6faddf2bb790d6b6ff25e0c1e6793f70365828ce460218902e8` on both sides

### OpenClaw

Read-only package metadata proved:

- version: `2026.7.1-2`
- package path: `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\package.json`
- entrypoint: `dist\index.js`

Direct Node entrypoint invocations used separate arguments and returned exit `0`. The plugin inventory was valid JSON and contained exactly one `cogentnexus-openclaw` registration:

- status: `loaded`
- enabled: `true`
- root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- source: `...\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js`
- registry diagnostics: `[]`

### Gateway

Configured gateway port: `18789`.

Read-only listener/process proof:

- listener: `127.0.0.1:18789`
- PID: `13152`
- process: `node.exe`
- command line: OpenClaw `dist\index.js gateway --port 18789`
- CNX gateway check: healthy, connectivity probe `ok`

### Ollama preservation/readiness

No `ollama.exe` UI command was used for proof. Loopback REST was used instead:

- `/api/version`: reachable, version `0.32.15`
- `/api/tags`: reachable, 4 models present:
  - `qwen3.5:9b`
  - `muse-glimmer:30b`
  - `qwen3.6:27b`
  - `qwen3.8:27b`
- `/api/ps`: reachable, running model `qwen3.5:9b`
- listener: `127.0.0.1:11434`
- PID: `11896`
- process command line: `ollama.EXE serve`

No model/provider mutation occurred.

### SQLite

Read-only `PRAGMA integrity_check` through the owned runtime Python interpreter returned exactly:

```text
ok
```

Database checked:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

### Services, namespaces, and residue

Scheduled-task evidence showed:

- `CogentNexus-OpenClaw-Supervisor`: state `Ready`
- `OpenClaw Gateway`: state `Ready`

The ownership root contained expected `host`, `runtime`, `workflows`, `ownership.json`, and historical installer backup/staging/transaction surfaces. Existing `install-backups`, `install-staging`, and `install-transaction.json` were preserved and classified as historical/transaction-owned residue. No active conflicting legacy/current product root was found in the ownership/inventory evidence.

## Mutation ledger

| Operation | Task-123 executions |
|---|---:|
| install/install-over | 0 |
| reset | 0 |
| uninstall | 0 |
| reinstall | 0 |
| enable/disable/start/stop/restart | 0 |
| recovery disruption | 0 |
| plugin/provider/runtime/config mutation | 0 |
| cleanup/normalization | 0 |
| process kill/reboot | 0 |
| Dashboard semantic Send | 0 |

## Conclusion and next gate

All Task-123 read-only acceptance criteria are proven. Task 123 authorizes no lifecycle continuation itself. A separate successor task and explicit authorization are required before consuming the remaining one-shot phases:

`reset -> uninstall -> fresh reinstall -> stop -> start -> restart -> recovery harness -> final snapshot`

This report is published as the sole report-file change. Execution stops for independent ChatGPT review. No lifecycle continuation successor was created or executed automatically.
