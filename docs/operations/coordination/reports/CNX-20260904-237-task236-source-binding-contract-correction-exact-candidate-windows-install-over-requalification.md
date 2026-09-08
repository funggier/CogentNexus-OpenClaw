# CNX-20260904-237 — Task236 Source-Binding Contract Correction + Exact-Candidate Windows Install-Over Requalification

## Final disposition

`FAIL_INSTALLER_TERMINAL`

The corrected exact-source installer topology was registered and started once.
The installer reached terminal failure during installer-owned plugin rollover
preparation. Per the task fence, no installer retry, second start, manual
repair, semantic acceptance, or recovery replay was performed.

This is an installer terminal failure after authorized execution, not a
source-binding or preflight blocker.

## Fresh authority

Fresh remote authority was fetched immediately before execution:

- Remote branch: `agent/v0.9.3-full-stabilization`
- Authority HEAD: `9d20c98d5a74462df670279e561ec3fc0ada5c7e`
- Active task: `CNX-20260904-237`
- Status: `READY_FOR_HERMES`
- Active disposition: `TASK236_BLOCKER_ACCEPTED__COORDINATION_SOURCE_BINDING_CONTRACT_CORRECTED__LIVE_INSTALL_OVER_REAUTHORIZED`
- Exact candidate source: `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`
- Expected candidate fingerprint:
  `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3` tag remained immutable at:
  `26ce64a624255278a3a0266ad38746e0e6ed2e31`

The candidate was proven an ancestor of the fresh coordination authority.
Candidate-to-authority drift consisted of coordination documentation only;
there was no unexpected product/source/test/workflow drift.

Fresh exact-candidate Actions remained successful:

- Validate `33773085803`: SUCCESS
- Windows Installer Pack Smoke `33773085772`: SUCCESS
- PS5.1 Acceptance Smoke `33773085907`: SUCCESS

No newer coordination task superseded Task 237 before execution.

## Exact detached source binding

Disposable checkout:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-exact-source
```

Immediately before registration and start:

- `git rev-parse HEAD`:
  `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`
- checkout detached: yes
- working tree clean: yes
- `git diff --quiet`: pass
- `git diff --cached --quiet`: pass
- VERSION: `0.9.3`
- source plugin fingerprint:
  `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- candidate `npm ci`: pass
- candidate `npm run plugin:validate`: pass
- `scripts/install.ps1`: exact file from detached checkout
- Task-226 fail-closed namespace-ownership attestation contract: present

The installer was invoked from this exact path:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-exact-source\scripts\install.ps1
```

No `--install-source-commit`, `-InstallSourceCommit`, or equivalent invented
argument was passed. No skip or link switch was passed.

## Read-only preflight and hazard gate

Evidence roots:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-preflight-20260904T
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-install-evidence-20260904T
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-post-20260904T
```

Before registration:

- controller: `managed`, generation `38`
- selected provider: `ollama`
- Gateway: healthy, loopback `127.0.0.1:18789`, OpenClaw `2026.7.1-2`
- Ollama: reachable/healthy/ready, four configured models
- startup policy: enabled, adapter installed, `LastTaskResult=0`
- Delivery: `READY`, pending outbox `0`
- Recovery: `READY`, no maintenance marker, no active provider incident,
  recovery attempts `0`
- SQLite integrity: `ok`
- known Task-233 interrupted/accepted lineage was preserved and not replayed
- previous live plugin fingerprint was the expected predecessor:
  `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`
- no Task-237 installer task or installer process existed

The known historical Task-233 residue was not emittable: outbox was empty,
recovery was ready, and no active incident/replay was present.

## Scheduler registration and execution ledger

The scheduled task used the authenticated Windows Task 230 topology.

Registration artifact:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-registration.json
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-registration-readback.json
```

Registered task:

```text
CogentNexus-OpenClaw-Task237-Installer-1
```

Read-back:

- state before start: `Ready`
- executable:
  `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
- arguments:
  `-NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:\Users\CDQ-P\AppData\Local\Temp\cnx237-installer-runner.ps1"`
- principal: `CDQ-P`, `Interactive`, `Limited`
- execution time limit: `PT45M`
- restart count: `0`

Attempt ledger:

| Logical operation | Attempt | UTC / result | Product state change | Retry status |
|---|---:|---|---|---|
| Scheduled-task registration | 1 | `2026-09-04` inline PowerShell parser error | No | registration retry remained available |
| Scheduled-task registration | 2 | success; task read-back matched | Task registration only | no further registration retry |
| Installer start | 1 | `2026-09-04T00:46:05.6200929Z` issued | Yes, installer-owned | `INSTALLER_RETRY_GATE=CLOSED` |
| Installer invocation | 1 | `2026-09-04T00:46:05.8009488Z` to `00:53:07.7447140Z` | Yes, installer-owned | no retry |
| Installer execution retry | 0 | not attempted | No | prohibited after start |

The first registration failure was a wrapper quoting/tooling failure before the
scheduled task existed. The materially different file-based registration
method succeeded. The task was then started exactly once.

## Installer terminal evidence

Transcript:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-install-evidence-20260904T\installer-transcript.txt
```

Terminal record:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-install-evidence-20260904T\installer-terminal.json
```

Observed terminal record:

- source: exact detached checkout `scripts/install.ps1`
- started: `2026-09-04T00:46:05.8009488+00:00`
- completed: `2026-09-04T00:53:07.8584949+00:00`
- exit code: `1`
- error: `ownership-safe plugin generation rollover pre-install proof failed`

Installer stages:

- native handoff `managed -> passthrough`: PASS
- skill backup/install: PASS
- CogentNexus validation: PASS
- ticket DB bootstrap: PASS
- plugin npm pack: PASS
- `plugin-rollover-prepare`: FAIL, exit `1`

Scheduled-task terminal observation:

- terminal state: `Ready`
- `LastTaskResult=1`
- last run approximately `2026-09-04T00:46:05Z`
- no second start or invocation

The installer did not reach replacement finalization or managed re-enable.
No manual intervention was used after the terminal failure.

## Post-install read-only state

Post evidence:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx237-post-20260904T
```

Observed after terminal failure:

- controller: `passthrough`
- generation: `39`
- desired gateway: `running`
- selected provider: `ollama` (unchanged)
- Gateway: healthy, loopback `127.0.0.1:18789`
- Ollama: healthy/ready with configured models unchanged
- startup policy: disabled; adapter not installed (native handoff state)
- Delivery: `READY`, pending outbox `0`
- Recovery: `READY`, no active incident/recovery
- SQLite integrity: `ok`
- tickets: `13` (unchanged from captured preflight count)
- ticket events: `106` (unchanged)
- `ticket_outbox`: `0`
- `cnx_assistant_delivery`: `8`
- `cnx_direct_recovery`: `2`
- `cnx_direct_model_call`: `13`
- `cnx_sessions`: `20`
- live plugin fingerprint remained predecessor:
  `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

The candidate fingerprint was therefore not proven installed. This is
consistent with the rollover prepare terminal failure and satisfies the
`FAIL_INSTALLER_TERMINAL` disposition; no manual plugin repair is authorized.

The installer-owned native handoff and skill staging were allowed mutations of
this task. The resulting passthrough state is preserved as observed evidence;
Hermes did not manually re-enable or repair managed state.

Historical retained rollover transaction/inventory artifacts were preserved.
No historical Task-223 or Task-233 evidence was edited, deleted, settled, or
replayed.

## Effect and mutation ledger

```text
exact detached source checkouts: 1
scheduled-task registration attempts: 2
installer successful starts: 1
installer invocations: 1
installer execution retries after start: 0
manual plugin install/copy/delete/rename/manifest repair: 0
manual lifecycle/Gateway repair: 0
manual process termination: 0
manual Ticket/outbox/recovery/SQLite mutation: 0
provider/model substitution: 0
Dashboard human semantic submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
semantic retries/replays: 0
recovery replay/resend: 0
Task-223 retained forensic evidence mutation: 0
Task-233 replay/settlement/deletion: 0
Release/tag/asset mutation: 0
production/source/test/workflow edits: 0
force push/history rewrite: 0
```

Installer-owned mutations were limited to the single authorized invocation,
including the managed-to-passthrough handoff, skill staging, generation
advance, database bootstrap, and failed rollover preparation. No manual
product repair was performed afterward.

## Retry classification

`RETRY_POLICY_EFFECTIVE`

One registration retry was used after a genuine wrapper/tooling parser failure,
with a materially different file-based method and proof that the first task did
not exist and did not start. No retry occurred after installer start, as
required by the closed retry gate.

## Stop boundary

Task 237 ends at the installer terminal failure. Do not retry the installer,
manually repair managed state or plugin identity, replay Task-233, send a
Dashboard/Discord semantic message, clean historical evidence, uninstall,
reset, reinstall, or mutate release/tag/assets without a separate successor
authority.
