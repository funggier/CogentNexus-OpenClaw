# CNX-20260831-182 — Repaired Candidate Windows Install-Over Reacceptance

- **Task:** `CNX-20260831-182`
- **Disposition:** `PASS — REPAIRED_CANDIDATE_INSTALL_OVER_ACTIVE_FACADE_PROVEN`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority HEAD before activation:** `fc9f52ca8d56013731f9f123d5093c83817f5183`
- **Accepted candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx182-evidence-20260831T070500Z`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT

## Disposition

The accepted Task-179 repair candidate was installed over the existing Windows v0.9.3 installation exactly once through the repository-supported `scripts/install.ps1` path. The installer exited `0` and emitted its successful completion message. Independent post-install checks prove that the active facade reached through `cnxclaw.cmd` has byte-identical content to the frozen candidate facade.

Controller, plugin, provider, Gateway, delivery, recovery, ownership, SQLite, and historical Task-171 durable state remain coherent. No reset, uninstall, semantic Dashboard action, model inference, recovery action, manual state repair, or second installer invocation occurred.

## Authority and frozen candidate

Fresh remote authority before execution:

```text
REMOTE_HEAD=fc9f52ca8d56013731f9f123d5093c83817f5183
ACTIVE status=READY_HERMES
ACTIVE task=CNX-20260831-182
execution mode=WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_REACCEPTANCE_HERMES
STATUS state=READY_HERMES
```

The exact candidate was materialized detached at:

```text
C:\Users\CDQ-P\AppData\Local\Temp\cnx-live-task182-20260831T070500Z
```

Candidate commit:

```text
f6392da3e4112ce441526d5ef19925c90a872b0b
```

Candidate facade:

```text
skills/cogentnexus-openclaw/scripts/cnxclaw.py
bytes: 17425
sha256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
Git blob: 879083d6186589d4b2774b8fd87fa93692dd2dfc
```

The Task-182 report was absent at the authoritative tip before report creation. The fresh pre-install process scan reported:

```text
NO_OBSERVER_OR_LIFECYCLE_PROCESS
```

## Pre-install read-only baseline

Before mutation, read-only probes passed:

```text
controller: managed
generation: 36
desired Gateway/provider: running
selected provider: ollama
provider transition: null
Gateway: healthy on 127.0.0.1:18789
Ollama: reachable/healthy/ready
ownership: OWNERSHIP_PRESENT
legacy ownership entries: []
delivery: READY
recovery: READY
pending outbox: 0
SQLite integrity: ok
OpenClaw: 2026.7.1-2 (0790d9f)
plugin version: 0.9.3
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
```

Pre-install database counts:

```text
tickets                  4
ticket_events           29
ticket_outbox            0
cnx_assistant_delivery   1
cnx_direct_model_call    4
cnx_direct_recovery      0
cnx_sessions             4
```

The active launcher before and after installation remained the `cnxclaw.cmd` chain resolving to the owned runtime Python and `cnxclaw_v093.py`.

## Exactly one supported install-over

Installer invocation count:

```text
1
```

The wrapper invoked exactly:

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/AppData/Local/Temp/cnx-live-task182-20260831T070500Z/scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

The installer was run with the repository's supported `scripts/install.ps1`, with native Node/GitHub CLI paths prefixed while preserving the existing toolchain PATH. Installer evidence:

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
exitCode: 0
durationSeconds: 317.5884696
stdoutBytes: 180982
stderrBytes: 2512
```

The installer output included:

```text
CNXCLAW_INSTALL_STAGE_START stage=ticket-db-bootstrap
CNXCLAW_INSTALL_STAGE_COMPLETE stage=ticket-db-bootstrap ... exit_code=0
CNXCLAW_INSTALL_STAGE_START stage=owned-runtime-ensure
CNXCLAW_INSTALL_STAGE_COMPLETE stage=owned-runtime-ensure ... exit_code=0
CogentNexus-OpenClaw v0.9.3 installation completed successfully.
```

The captured stage-marker stream contained two start/complete pairs, both with exit code `0`. Other installer-owned internal operations were preserved in the complete raw stdout rather than inferred from the marker count.

## Active facade provenance

After installation, the active facade reached through:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd
```

was:

```text
C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw.py
bytes: 17425
sha256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
```

Candidate/installed equality:

```text
PASS — byte-identical
```

This exact active-facade hash, rather than the unchanged npm package fingerprint, is the primary proof that the Task-179 repair is installed and active.

## Post-install provenance and health

Read-only post-install checks returned exit `0`:

```text
release: 0.9.3
OpenClaw: 2026.7.1-2 (0790d9f)
plugin version: 0.9.3
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
plugin id: cogentnexus-openclaw
plugin status: loaded
plugin enabled: true
plugin root: C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
ownership: OWNERSHIP_PRESENT
legacy namespace: []
controller mode: managed
generation: 42
selected provider: ollama
provider transition: null
Gateway: healthy; loopback HTTP 200
Ollama: reachable/healthy/ready; HTTP 200
```

The generation advanced from `36` to `42` during installer-owned maintenance/reload activity. This is an expected installer-owned state transition; no semantic work was performed and no unsafe drift was observed.

Delivery and recovery:

```text
delivery verdict: READY
pending outbox: 0
readOnly: true
stateChanged: false
recovery verdict: READY
active provider recovery incident: none
```

SQLite was opened through a read-only URI and retained `PRAGMA integrity_check=ok`.

Post-install database counts:

| Table | Before | After | Result |
|---|---:|---:|---|
| `tickets` | 4 | 4 | unchanged |
| `ticket_events` | 29 | 29 | unchanged |
| `ticket_outbox` | 0 | 0 | unchanged |
| `cnx_assistant_delivery` | 1 | 1 | unchanged |
| `cnx_direct_model_call` | 4 | 4 | unchanged |
| `cnx_direct_recovery` | 0 | 0 | unchanged |
| `cnx_sessions` | 4 | 4 | unchanged |

Task-171 historical Ticket/delivery state remained present. No new ticket, event, model call, recovery row, delivery row, session, outbox item, or semantic action was manufactured.

## Complete issue register

### Issue 1 — Harness path typo during report-absence check

- **Observed symptom:** an initial `git` command used a nonexistent `070000Z` checkout path instead of `070500Z` and exited `126` before repository inspection.
- **Product state impact:** none; the command did not reach the repository or live runtime.
- **Correction:** reran the read-only report-absence check against the correct native path.
- **Remaining consequence:** none for installation evidence; the corrected check returned `REPORT_ABSENT`.

### Issue 2 — npm warnings captured on installer stderr

- **Observed symptom:** stderr contained `npm warn deprecated node-domexception@1.0.0` and `npm warn allow-scripts` notices for five packages.
- **Product state impact:** no failure observed; installer exit code was `0`, stage markers completed with exit code `0`, and post-install plugin/runtime checks passed.
- **Correction:** none required; preserved raw stderr and decoded copy.
- **Remaining consequence:** package-manager warnings remain environmental/dependency hygiene items and should not be misclassified as an installer failure.

### Issue 3 — Installer output contained ticket summary `failed: 3`

- **Observed symptom:** embedded status JSON displayed ticket counts `completed: 1, failed: 3`.
- **Product state impact:** no count growth occurred; the same database retained four tickets before and after install-over.
- **Classification:** this is a durable ticket summary, not an installer stage failure. The installer result and post-install health were successful.
- **Remaining consequence:** the three historical failed tickets remain part of existing durable state; they were not created by Task-182 and were not altered.

### Issue 4 — Installer stage-marker coverage

- **Observed symptom:** the captured marker stream showed two explicit stage start/complete pairs, while the full raw stdout contained additional installer-owned output.
- **Product state impact:** none observed; the installer result was complete with exit `0` and independent post-state proof passed.
- **Correction:** preserved the full raw streams and reported the exact observed marker pairs without inventing markers for unmarked operations.
- **Remaining consequence:** stage-level attribution is limited to the markers emitted by this installer version; overall completion is additionally supported by process exit and independent post-install checks.

## Acceptance matrix

| Criterion | Result | Evidence |
|---|---|---|
| Fresh Task-182 authority and READY gate | PASS | remote `fc9f52ca...`, ACTIVE/STATUS |
| Exact candidate commit | PASS | detached candidate `f6392da...` |
| Candidate facade hash | PASS | `a01-candidate-facade-sha.txt` |
| Clean process boundary before mutation | PASS | `a02-process.stdout.txt` |
| Pre-install managed/runtime/durable gates | PASS | `a03`–`a09` evidence |
| Exactly one supported installer invocation | PASS | `b00-installer.invocation.json`, result |
| Installer exit code | PASS — `0` | `b01-installer.result.json` |
| Installer success completion | PASS | decoded stdout completion message |
| Candidate/installed active facade byte identity | PASS | `c01-installed-facade-sha.txt` |
| Release/version provenance | PASS | status, plugin, OpenClaw probes |
| Plugin loaded/enabled | PASS | `c10-plugins-list.stdout.json` |
| Ownership and legacy namespace | PASS | `c05-ownership.stdout.json` |
| Controller/provider/Gateway health | PASS | `c02-status.stdout.json`, HTTP probe |
| Ollama health/readiness/route | PASS | status and HTTP 200 |
| Delivery/recovery readiness | PASS | `c03`/`c04` read-only checks |
| Pending outbox | PASS — `0` | delivery and SQLite |
| SQLite integrity | PASS — `ok` | `c07-db.stdout.json` |
| Task-171 history preserved | PASS | unchanged counts and old identity presence |
| Unexpected durable growth | PASS — none | before/after matrix |
| Semantic/model/recovery action count | PASS — `0` | hard-fence audit |

## Reviewer Verification Packet

1. Verify remote report commit ancestry and exact report-only path.
2. Verify candidate commit and facade SHA against Task-182 authority.
3. Read `a02-process.stdout.txt` and confirm no historical observer/lifecycle residue before mutation.
4. Read `b00-installer.invocation.json` and `b01-installer.result.json`; confirm invocation `1` and exit `0`.
5. Inspect both raw installer streams and their decoded copies; confirm warnings are preserved and success text is present.
6. Verify installed facade path, bytes, SHA-256, and equality with the frozen candidate.
7. Read `c10-plugins-list.stdout.json`; confirm plugin `cogentnexus-openclaw` is version `0.9.3`, loaded, enabled, and sourced from the expected extension root.
8. Read `c02-status.stdout.json`, `c03-delivery.stdout.json`, `c04-recovery.stdout.json`, and `c05-ownership.stdout.json`; confirm managed/ollama/healthy/READY/ownership state.
9. Read `c07-db.stdout.json`; confirm read-only SQLite integrity, unchanged counts, and preserved Task-171 durable identity.
10. Confirm no reset, uninstall, retry, Dashboard Send, model/recovery action, manual repair, or source mutation occurred.

## Hard-fence audit

```text
supported installer root invocations: 1
installer-owned internal stages: permitted within that invocation
reset: 0
uninstall: 0
second installer/retry: 0
executor-issued lifecycle helper: 0
manual Gateway/Ollama restart: 0
Dashboard Send/composer input/chat.inject: 0
model inference/recovery/regeneration: 0
manual DB/config/transcript/route repair: 0
source/product/test/workflow/dependency changes: 0
release/tag/merge/force push: 0
```

## Publication fence and successor boundary

This report is the only repository path authorized for the Task-182 publication commit. After publication, stop for ChatGPT review. The repaired candidate is now installed and its active facade identity is proven. Reset and uninstall remain unauthorized and require a later explicit coordination task.
