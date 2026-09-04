# CNX-20260903-236 — Task-235 Exact-Candidate Windows Install-Over Requalification

## Disposition

`BLOCKED_PREFLIGHT_DRIFT`

Installer execution was **not started**. No scheduled-task registration, task
start, installer invocation, plugin mutation, lifecycle mutation, semantic
message, recovery replay, or manual durable-state mutation occurred.

## Fresh authority

- Task: `CNX-20260903-236`
- Remote opening authority: `3b4c0295fdaf0f94a771f7fa564d86f83a46e02f`
- Exact candidate source: `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`
- Expected candidate payload fingerprint:
  `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31` (unchanged)
- Candidate is an ancestor of the current remote coordination authority.
- Task 236 was active and `READY_FOR_HERMES` at preflight.

Exact candidate Actions were freshly read from GitHub and remained successful:

- Validate `33773085803`: SUCCESS
- Windows Installer Pack Smoke `33773085772`: SUCCESS
- PS5.1 Acceptance Smoke `33773085907`: SUCCESS

## Read-only live preflight

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx236-preflight-20260903T
```

Observed before any installer action:

- controller mode: `managed`
- generation: `38`
- selected provider: `ollama`
- Ollama reachable/healthy with configured models including `qwen3.5:9b`
- Gateway: healthy on `127.0.0.1:18789`
- plugin check: `READY`
- Delivery: `READY`, pending `0`
- Recovery: `READY`, no active provider incident/recovery
- SQLite integrity: `ok`
- live installed plugin version: `0.9.3`
- live installed plugin fingerprint: previous expected payload
  `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`
- known Task-233 Ticket remained untouched:
  `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`, run
  `e225013e-8d50-4479-b227-ca9a10b89a46`, status `accepted`,
  `failure_class=interrupted`; this was not replayed, settled, or deleted.

The preflight hazard gate was otherwise quiet: no pending outbox, no active
recovery incident, and no new unexplained nonterminal duplicate lineage.

## Blocking contract mismatch

Task 236 requires the installer invocation to include:

```text
--install-source-commit ffb0dd4ed47affe2e496c17b74ca74d358905bd7
```

The exact candidate installer inspected at:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx-successor-204-authority-20260901T/scripts/install.ps1
```

has the following declared parameters:

```text
[string]$Workspace
[switch]$SkipPlugin
[switch]$SkipGatewayRestart
[switch]$SkipAgentsPolicy
[switch]$LinkPlugin
```

It does **not** declare `-InstallSourceCommit`, and read-only repository search
found no `install-source-commit` implementation or equivalent documented
override. The installer derives its source from `$PSScriptRoot` and has no
verified way, under the current exact tree, to bind the required source-commit
attestation argument.

Because the task explicitly forbids installing from a guessed or reconstructed
SHA, and because passing an unsupported parameter would violate the exact
installer contract, installer registration/start was not attempted.

This is an authority/contract drift blocker, not an installer execution
failure. No installer retry budget was consumed.

## Attempt ledger

| Logical operation | Attempt | Method | Result | Could product state change? | Remaining budget / rationale |
|---|---:|---|---|---|---|
| Fresh GitHub authority | 1 | `git fetch`, remote `ACTIVE.md`/`STATUS.md`, ancestry and tag checks | PASS | No | No retry needed |
| Candidate Actions | 1 | `gh run list --commit ffb0dd4...` | PASS, all 3 SUCCESS | No | No retry needed |
| Live status/delivery/recovery | 1 | read-only `cnxclaw.cmd` checks | PASS / quiet gate | No | No retry needed |
| Installer contract | 1 | read-only `install.ps1` inspection + repository search | BLOCKED: required override absent | No | Stop before registration/start |

Retry classification:

```text
RETRY_POLICY_NOT_NEEDED
```

## Mutation/cardinality ledger

```text
installer task registrations: 0
installer successful starts: 0
installer invocations: 0
installer execution retries after start: 0
manual plugin mutation: 0
manual lifecycle/Gateway mutation: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct operator Discord/API Sends: 0
semantic retries/resubmissions: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
provider/model substitution: 0
process termination: 0
Task-223/Task-233 evidence mutation: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

## Stop boundary

Task 236 is blocked before installer registration/start. A future successor
must reconcile the required `--install-source-commit` contract with the exact
installer implementation, then re-run fresh authority and preflight. Do not
infer permission to install, manually pass an unsupported argument, use a
substitute installer, or proceed to semantic acceptance from this report.
