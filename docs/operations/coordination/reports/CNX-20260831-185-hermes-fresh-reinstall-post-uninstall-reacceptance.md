# CNX-20260831-185 — Fresh Reinstall Post-Uninstall Reacceptance

- **Task:** `CNX-20260831-185`
- **Disposition:** `PASS — FRESH_REINSTALL_POST_UNINSTALL_CANDIDATE_REACCEPTED`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority HEAD before activation:** `417d77fd4a3ef08b8eab315caa9d10afd7fb1592`
- **Accepted candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx185-evidence-20260831T084500Z`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT

## Disposition

The accepted Task-179 candidate was freshly installed after the accepted Task-184 uninstall boundary through exactly one repository-supported `scripts/install.ps1` invocation. The installer exited `0`, completed all observed stage start/complete pairs with exit code `0`, and emitted the v0.9.3 installation success message.

Independent post-install checks prove the active facade, plugin, ownership, controller, provider, Gateway, Ollama, delivery/recovery, and fresh durable-state requirements. External OpenClaw/Ollama/unrelated surfaces remain preserved. No Dashboard semantic action, model inference, recovery action, reset, uninstall, second installer invocation, or manual repair occurred.

## Fresh authority and candidate

Fresh remote authority before execution:

```text
REMOTE_HEAD=417d77fd4a3ef08b8eab315caa9d10afd7fb1592
ACTIVE status=READY_HERMES
ACTIVE task=CNX-20260831-185
execution mode=WINDOWS_FRESH_REINSTALL_POST_UNINSTALL_REACCEPTANCE_HERMES
STATUS state=READY_HERMES
```

The Task-185 report was absent at the authority tip before creation. A clean detached checkout was materialized at:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx-live-task185-20260831T084500Z
```

Candidate commit and facade:

```text
commit: f6392da3e4112ce441526d5ef19925c90a872b0b
path: skills/cogentnexus-openclaw/scripts/cnxclaw.py
Git blob: 879083d6186589d4b2774b8fd87fa93692dd2dfc
bytes: 17425
sha256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
```

## Phase A — post-uninstall preflight

Fresh read-only preflight confirmed the accepted Task-184 boundary:

```text
CNX launcher: absent
CNX skill: absent
CNX direct extension: absent
CNX state root: absent
CNX local application-data/runtime root: absent
CNX scheduled task: absent
CNX lifecycle residue: absent
```

The independent process probe returned:

```text
NO_CNX_LIFECYCLE_RESIDUE
```

Native/external preflight:

```text
OpenClaw: 2026.7.1-2 (0790d9f)
Gateway: healthy
Ollama API: reachable/healthy/ready
Ollama inventory SHA-256: a9f2214d57e1f279d896e5de687f546066a5e3f35b366eea95fc487deaba935a
unrelated plugin inventory: 71 entries; normalized hash 8d58154632fff0eb998af72dce688326d055707d76e7a4fba464d8f63bd53752
```

The Ollama inventory and unrelated plugin inventory matched the accepted Task-184 baseline before mutation. The accepted Gateway command baseline was also frozen for post-install comparison.

## Exactly one supported fresh install

Installer root invocation count:

```text
1
```

Exact command:

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/AppData/Local/Temp/cnx-live-task185-20260831T084500Z/scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

Installer evidence:

```text
b00-installer.invocation.json
b01-installer.stdout.log
b01-installer.stderr.log
b01-installer.result.json
b01-installer.stdout.log.decoded.txt
b01-installer.stderr.log.decoded.txt
```

Result:

```text
invocation=1
exitCode=0
startedAt=2026-08-31T08:39:57.3129391Z
endedAt=2026-08-31T08:45:09.1260364Z
durationSeconds=311.8130973
stdoutBytes=178268
stderrBytes=2530
```

Observed installer stage pairs, all complete with exit code `0`:

```text
ticket-db-bootstrap
plugin-npm-pack
plugin-install-local-package
plugin-disable-post-install
owned-runtime-ensure
```

Installer completion marker:

```text
CogentNexus-OpenClaw v0.9.3 installation completed successfully.
```

## Active facade and installation provenance

The active installed launcher chain is:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd
  -> owned runtime Python
      -> C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py
          -> installed cnxclaw.py
```

The active installed facade is:

```text
path: C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw.py
bytes: 17425
sha256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
equality with candidate: PASS — byte-identical
```

Post-install plugin provenance:

```text
release/plugin version: 0.9.3
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
plugin id: cogentnexus-openclaw
plugin status: loaded
plugin enabled: true
plugin origin: global
```

## Post-install ownership/runtime health

Read-only checks returned exit `0`:

```text
ownership: OWNERSHIP_PRESENT
legacy namespace: []
controller: managed
generation: 6
selected provider: ollama
provider transition: null
desired Gateway/provider: running
Gateway: healthy on 127.0.0.1:18789
Ollama: reachable/healthy/ready
delivery: READY
recovery: READY
pending outbox: 0
SQLite integrity: ok
OpenClaw: 2026.7.1-2 (0790d9f)
```

The controller generation advanced from the post-reset fresh-install baseline `3` to `6` during installer-owned setup/reload. No semantic or recovery work was generated.

Fresh post-install durable state remained empty:

| Table | Required | Observed | Result |
|---|---:|---:|---|
| `tickets` | 0 | 0 | PASS |
| `ticket_events` | 0 | 0 | PASS |
| `ticket_outbox` | 0 | 0 | PASS |
| `cnx_assistant_delivery` | 0 | 0 | PASS |
| `cnx_direct_model_call` | 0 | 0 | PASS |
| `cnx_direct_recovery` | 0 | 0 | PASS |
| `cnx_sessions` | 0 | 0 | PASS |

No Task-171 identity was recreated. Delivery/recovery checks were read-only, healthy, and had no pending or manufactured recovery work.

## External preservation

Post-install comparison confirmed:

```text
OpenClaw version: 2026.7.1-2 (0790d9f)
Gateway command hash: cf91e215a19bf767791efc671479ba65db110894e5448e3c72218c99a40fbb77
Ollama inventory hash: a9f2214d57e1f279d896e5de687f546066a5e3f35b366eea95fc487deaba935a
Unrelated plugin inventory: 71 entries; normalized hash 8d58154632fff0eb998af72dce688326d055707d76e7a4fba464d8f63bd53752
Gateway HTTP probe: successful; 14406-byte response captured
```

The Ollama model inventory, unrelated plugin inventory, and Gateway command surface matched their accepted Task-184 baselines. Native OpenClaw remained installed and healthy. No unrelated namespace/data removal or mutation was attributed to the fresh install.

## Complete issue register

### Issue 1 — Initial process probe harness boundary failure

- **Observed symptom:** the first read-only process probe attempted PowerShell `-File /dev/fd/...` and failed because Windows PowerShell requires a `.ps1` file (`file does not have a '.ps1' extension`, exit `127`).
- **Product state impact:** none; this occurred before installer invocation.
- **Correction:** created and invoked a real absolute `.ps1` script file.
- **Final result:** `NO_CNX_LIFECYCLE_RESIDUE`.
- **Remaining consequence:** the failed probe is preserved as harness evidence and is not used as the preflight verdict.

### Issue 2 — Initial post-install Gateway hash path error

- **Observed symptom:** the first post-install hash command referenced `workspace/gateway.cmd`, which does not exist.
- **Product state impact:** none; no mutation or lifecycle action was issued by that command.
- **Correction:** used the canonical native Gateway command path `C:/Users/CDQ-P/.openclaw/gateway.cmd`.
- **Final result:** hash matched the accepted baseline exactly.
- **Remaining consequence:** none; the incorrect path is retained as a probe anomaly.

### Issue 3 — npm warnings during installation

- **Observed symptom:** installer stderr contained npm deprecation and `allow-scripts` warnings.
- **Product state impact:** no failure observed; installer exit was `0`, every observed stage completed with exit `0`, and post-install verification passed.
- **Correction/classification:** preserved raw stderr and reported the warnings separately; they are package-manager hygiene notices, not an installer failure.
- **Remaining consequence:** warnings remain an environment/dependency maintenance item outside this acceptance boundary.

No installer timeout, retry, partial completion, facade mismatch, plugin-load failure, ownership failure, runtime failure, durable-state contamination, or external preservation mismatch was observed.

## Acceptance matrix

| Criterion | Result | Evidence |
|---|---|---|
| Fresh Task-185 authority and READY gate | PASS | remote `417d77fd...`, ACTIVE/STATUS |
| Task-185 report absent before work | PASS | remote `git ls-tree` |
| Exact candidate checkout and facade hash | PASS | `a01-candidate-facade.sha256` |
| Accepted post-uninstall boundary | PASS | `a02`–`a04` evidence |
| Native/external preservation preflight | PASS | `a05`–`a09` evidence |
| Exactly one supported installer invocation | PASS | `b00-installer.invocation.json` |
| Installer exit code `0` | PASS | `b01-installer.result.json` |
| All observed installer stage pairs complete | PASS | decoded installer stdout |
| Installer success completion | PASS | completion marker |
| Active facade byte identity | PASS | `c01-facade.sha256` |
| Release/plugin/version/fingerprint | PASS | `c02-status.json`, `c06-plugin.json`, `c09-plugins.json` |
| Plugin loaded and enabled | PASS | `c09-plugins.json` |
| Ownership and legacy namespace | PASS | `c05-ownership.json` |
| Controller/provider/Gateway/Ollama health | PASS | `c02-status.json`, `c13-gateway-http.txt`, `c10-ollama.json` |
| Delivery/recovery readiness | PASS | `c03-delivery.json`, `c04-recovery.json` |
| Fresh zero durable state | PASS | `c07-db.json` |
| SQLite integrity `ok` | PASS | `c07-db.json` |
| OpenClaw preservation | PASS | version/Gateway evidence |
| Ollama/model preservation | PASS | identical inventory SHA-256 |
| Unrelated plugin preservation | PASS | identical normalized inventory hash |
| Gateway command preservation | PASS | identical SHA-256 |
| Semantic/model/recovery actions | PASS — zero | hard-fence audit |

## Reviewer Verification Packet

1. Verify remote authority and Task-185 READY state at `417d77fd...`.
2. Verify detached candidate commit and facade hash against accepted Task-179 provenance.
3. Read `a02-owned-paths.json`, `a03-scheduled.txt`, and `a04-process.txt` to confirm clean post-uninstall preflight.
4. Verify the pre-install OpenClaw version, Gateway health, Ollama digest, and unrelated plugin inventory.
5. Read `b00-installer.invocation.json` and `b01-installer.result.json`; confirm one invocation and exit `0`.
6. Inspect raw and decoded installer streams and confirm all five observed stage pairs completed with exit `0`.
7. Verify `c01-facade.sha256` equals the frozen candidate SHA exactly.
8. Read `c02-status.json`, `c03-delivery.json`, `c04-recovery.json`, `c05-ownership.json`, and `c06-plugin.json` for managed/ollama/healthy/READY/ownership state.
9. Read `c07-db.json`; confirm read-only SQLite integrity and all seven reset-owned tables at zero.
10. Compare pre/post Ollama and unrelated plugin inventories plus Gateway command hash; confirm no Dashboard, model, recovery, reset, uninstall, retry, or manual repair action.

## Hard-fence audit

```text
supported fresh-install root invocations: 1 authorized
reset: 0
uninstall: 0
second install/retry: 0
executor-issued lifecycle helper outside installer: 0
manual Gateway/Ollama lifecycle action: 0
Dashboard Send/composer input/chat.inject: 0
model inference/recovery/regeneration: 0
manual DB/config/transcript/route repair: 0
source/product/test/workflow/dependency changes: 0
release/tag/merge/force push: 0
```

## Publication fence and successor boundary

This report is the only repository path authorized for Task-185 publication. After publication, stop for ChatGPT review. The fresh reinstall and post-uninstall candidate reacceptance boundary is proven. Final Dashboard semantic/durable-delivery acceptance remains unauthorized and requires a later task with the user-controlled UI gates described in `ACTIVE.md` and `STATUS.md`.
