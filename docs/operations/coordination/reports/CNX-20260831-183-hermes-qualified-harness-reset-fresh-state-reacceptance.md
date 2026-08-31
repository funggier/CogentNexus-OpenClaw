# CNX-20260831-183 — Qualified-Harness Reset Fresh-State Reacceptance

- **Task:** `CNX-20260831-183`
- **Disposition:** `PASS — QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTED`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority HEAD before activation:** `a7c19d32375032499549d53d2bcf8df131821902`
- **Accepted candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx183-evidence-20260831T072000Z`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT

## Disposition

The repaired installed `cnxclaw.cmd` path completed exactly one authorized reset through the Task-177-qualified incremental character-prompt harness and the Task-179 repaired interactive delegation path. The exact real confirmation prompt was observed before input, exactly one literal `y` line was sent, the reset child exited `0`, and the output contained both required success markers.

The resulting state is a genuine fresh-install MANAGED state: all reset-owned CogentNexus durable tables are empty, while the repaired active facade, release, plugin, OpenClaw installation/version, Ollama installation/model inventory, ownership, runtime health, and external assets remain present and healthy. No semantic, model, recovery, Dashboard, installer, uninstall, or second reset action occurred.

## Fresh authority and preflight

Fresh remote authority before activation:

```text
REMOTE_HEAD=a7c19d32375032499549d53d2bcf8df131821902
ACTIVE status=READY_HERMES
ACTIVE task=CNX-20260831-183
execution mode=WINDOWS_QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTANCE_HERMES
STATUS state=READY_HERMES
```

Task-183 report absence was checked at the authority tip before creation. The installed active facade preflight hash was:

```text
aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
```

The fresh pre-reset process scan reported:

```text
NO_OBSERVER_OR_LIFECYCLE_PROCESS
```

Pre-reset read-only state:

```text
controller: managed
generation: 42
desired Gateway/provider: running
selected provider: ollama
provider transition: null
Gateway: healthy on 127.0.0.1:18789
Ollama: reachable/healthy/ready
ownership: OWNERSHIP_PRESENT
legacy namespace: []
delivery: READY
recovery: READY
pending outbox: 0
SQLite integrity: ok
OpenClaw: 2026.7.1-2 (0790d9f)
plugin: 0.9.3; fingerprint e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
```

Pre-reset durable counts:

```text
tickets                  4
ticket_events           29
ticket_outbox            0
cnx_assistant_delivery   1
cnx_direct_model_call    4
cnx_direct_recovery      0
cnx_sessions             4
```

The Task-171 historical Ticket/delivery identity was present before the authorized reset, as required by the task contract.

## One-shot reset action

Reset root invocation count:

```text
1
```

Exact harness command topology:

```text
persistent Python supervisory harness
  -> cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset
      -> installed cnxclaw.cmd
          -> repaired v0.9.3/legacy facade
              -> host_control_v092
                  -> lifecycle_v092
```

The harness persisted incremental fsync-backed events and continuously captured stdout/stderr:

```text
b01-reset.py
b01-reset.events.jsonl
b01-reset.stdout.log
b01-reset.stderr.log
b01-reset.result.json
```

The durable event order was:

```text
harness_started
cmd_process_started
prompt_observed
input_send_intent
input_sent
stdin_closed
stderr_reader_completed
stdout_reader_completed
reset_pass_marker_observed
fresh_install_managed_marker_observed
cmd_process_exited
orphan_scan_completed
run_finalized
```

The required ordering was proven:

```text
prompt_observed < input_send_intent < input_sent
```

Reset result:

```text
invocationCount=1
promptObserved=true
inputSendIntentCount=1
inputSentCount=1
stdinClosed=true
exitCode=0
resetPassMarker=true
freshInstallManagedMarker=true
stdoutBytes=15936
stderrBytes=0
durationSeconds=224.71286869049072
```

The raw stdout contained:

```text
Continue? [y/N]:
Provider  : ollama
COGENTNEXUS-OPENCLAW RESET: PASS
State     : fresh-install MANAGED
```

No second input attempt, reset retry, or alternate semantic action was performed.

## Post-reset fresh-state verification

The installed active facade remained byte-identical to the accepted candidate:

```text
path: C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw.py
sha256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
equality with accepted candidate: PASS
```

Post-reset runtime/provenance checks returned exit `0`:

```text
release: 0.9.3
OpenClaw: 2026.7.1-2 (0790d9f)
plugin version: 0.9.3
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
plugin status: loaded
plugin enabled: true
ownership: OWNERSHIP_PRESENT
legacy namespace: []
controller mode: managed
generation: 3
selected provider: ollama
provider transition: null
Gateway: healthy; loopback HTTP probe successful
Ollama: reachable/healthy/ready; API probe successful
delivery: READY
recovery: READY
pending outbox: 0
SQLite integrity: ok
```

The controller generation was recreated at `3`, consistent with fresh-state reconstruction. Provider selection was committed with source `reset` and no stuck transition.

Post-reset reset-owned durable counts:

| Table | Before reset | After reset | Result |
|---|---:|---:|---|
| `tickets` | 4 | 0 | reset-owned history removed |
| `ticket_events` | 29 | 0 | reset-owned history removed |
| `ticket_outbox` | 0 | 0 | empty |
| `cnx_assistant_delivery` | 1 | 0 | reset-owned history removed |
| `cnx_direct_model_call` | 4 | 0 | reset-owned history removed |
| `cnx_direct_recovery` | 0 | 0 | empty |
| `cnx_sessions` | 4 | 0 | reset-owned history removed |

Task-171 Ticket and run/delivery identities were absent after reset. SQLite was opened read-only and returned `PRAGMA integrity_check=ok`.

## External preservation

The following external assets remained present and usable after reset:

- OpenClaw version remained `2026.7.1-2 (0790d9f)`;
- Ollama loopback API remained reachable with HTTP `200`;
- pre/post Ollama model inventory SHA-256 was identical:
  ```text
  a9f2214d57e1f279d896e5de687f546066a5e3f35b366eea95fc487deaba935a
  ```
- installed CogentNexus release/program files remained present;
- active repaired facade remained exact candidate identity;
- ownership remained valid and legacy namespace empty;
- Gateway remained healthy on loopback `127.0.0.1:18789`;
- no observer, reset, uninstall, or lifecycle residue remained after completion.

## Complete issue register

No product failure or acceptance-boundary ambiguity occurred.

The pre/post verification captured the normal reset-owned transition from controller generation `42` to fresh generation `3` and from four historical tickets to zero reset-owned tickets. This is an expected reset result, not unexpected data loss, because Task-183 explicitly requires removal of CNX-owned durable history while preserving external OpenClaw/Ollama assets and the installed program/release.

No harness correction, timeout, process orphan, stderr output, missing marker, or input-budget violation occurred.

## Acceptance matrix

| Criterion | Result | Evidence |
|---|---|---|
| Fresh Task-183 authority and READY gate | PASS | remote `a7c19d323...`, ACTIVE/STATUS |
| Task-183 report absent before work | PASS | remote `git ls-tree` |
| Active facade preflight hash | PASS | `a01-installed-facade-sha.txt` |
| Clean process boundary | PASS | `a02-process.stdout.txt` |
| Pre-reset runtime/durable gates | PASS | `a03`–`a10` evidence |
| Exactly one reset root invocation | PASS | `b01-reset.result.json` |
| Exact real confirmation prompt observed | PASS | ledger and raw stdout |
| Exactly one literal `y` sent | PASS | `input_send_intent`/`input_sent`, count `1` |
| Prompt/input ordering | PASS | incremental ledger |
| Reset child exit `0` | PASS | result and `cmd_process_exited` |
| RESET PASS marker | PASS | stdout and ledger |
| Fresh-install MANAGED marker | PASS | stdout and ledger |
| Active facade preserved exactly | PASS | `c01-installed-facade-sha.txt` |
| Release/plugin/OpenClaw provenance | PASS | `c02`, `c06`, `c08`, `c11` |
| Plugin loaded/enabled | PASS | `c11-plugins-list.json` |
| Ownership and legacy namespace | PASS | `c05-ownership.stdout.json` |
| Managed Ollama route and provider health | PASS | `c02-status.stdout.json`, Ollama API |
| Gateway health | PASS | status and loopback probe |
| Delivery/recovery readiness | PASS | `c03`/`c04` read-only checks |
| SQLite read-only integrity | PASS — `ok` | `c07-db.stdout.json` |
| Reset-owned durable tables zeroed | PASS | before/after count matrix |
| Task-171 identities absent | PASS | `oldIdentityCounts` all zero after reset |
| External OpenClaw/Ollama preservation | PASS | version/API/model inventory comparison |
| Semantic/model/recovery actions | PASS — `0` | hard-fence audit |

## Reviewer Verification Packet

1. Verify remote authority and Task-183 READY state at `a7c19d323...`.
2. Read `a01-installed-facade-sha.txt` and confirm the accepted active-facade hash.
3. Read `a02-process.stdout.txt` and confirm no observer/lifecycle residue before reset.
4. Read `a08-db.stdout.json` and confirm the four-ticket pre-reset baseline.
5. Read `b01-reset.events.jsonl` and verify prompt, input intent, input sent, stdin close, marker, exit, and finalization ordering.
6. Read `b01-reset.result.json` and confirm exactly one invocation, exactly one input, exit `0`, and both required markers.
7. Read `b01-reset.stdout.log` and confirm the exact reset success text and Ollama provider line.
8. Read `c01-installed-facade-sha.txt` and confirm active facade equality with the candidate.
9. Read `c02`–`c07` plus `c11-plugins-list.json` and confirm fresh managed/loaded/healthy/READY state and zero CNX-owned durable rows.
10. Compare `a10-ollama-tags.json` and `c09-ollama-tags.json`, and confirm no install-over, uninstall, second reset, Dashboard, model, recovery, or manual repair action.

## Hard-fence audit

```text
reset root invocations: 1 authorized
confirmation input sends: 1 literal y line
installer/install-over/reinstall: 0
uninstall: 0
second reset: 0
second confirmation send: 0
executor-issued lifecycle helper: 0
manual Gateway/Ollama lifecycle action: 0
Dashboard Send/composer input/chat.inject: 0
model inference/recovery/regeneration: 0
manual DB/config/transcript/route repair: 0
product/source/test/workflow/dependency changes: 0
release/tag/merge/force push: 0
```

## Publication fence and successor boundary

This report is the only repository path authorized for Task-183 publication. After publication, stop for ChatGPT review. The reset acceptance is complete and the fresh-state boundary is proven. Uninstall remains unauthorized and requires a later explicit coordination task.
