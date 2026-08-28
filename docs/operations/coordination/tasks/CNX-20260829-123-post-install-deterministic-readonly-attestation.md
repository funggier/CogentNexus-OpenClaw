# CNX-20260829-123 — Post-Install Deterministic Read-Only Attestation

- Status: `READY_FOR_HERMES`
- Execution mode: `READONLY_POST_INSTALL_ATTESTATION`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Prove or disprove the current post-install state produced by the successful Task-121 install-over using deterministic, non-interactive, argument-safe read-only evidence only.

This task exists because Task 122's verification contract made two mistakes:

1. it incorrectly treated expected `v0.9.3 Ollama-only` runtime help text as inconsistent with a provider-neutral installer;
2. its generalized probe/capture path appears to have dropped command arguments, producing CNX help, OpenClaw TUI, and Ollama UI behavior.

Task 123 performs **no lifecycle mutation at all**. If it passes, a separate successor may authorize the still-unconsumed lifecycle phases.

## Exact candidate and frozen live boundary

Retain exactly:

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload count `178`;
- payload/plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Task-121 install-over:

- executed exactly once;
- returned exit code `0`;
- reported installation completed successfully;
- is **consumed 1 / 1 and forbidden to replay**.

Still unconsumed, but **not authorized in Task 123**:

- reset `0 / 1`;
- uninstall `0 / 1`;
- fresh reinstall after uninstall `0 / 1`;
- stop `0 / 1`;
- start `0 / 1`;
- restart `0 / 1`;
- recovery harness `0 / 1`.

## Architectural interpretation — mandatory

Do not confuse installer responsibility with runtime provider support.

The exact candidate intentionally contains an Ollama-only v0.9.3 runtime facade. The following text is expected and is **not** a failure by itself:

- `CogentNexus-OpenClaw v0.9.3 (Ollama-only)`;
- `Ollama is the only supported inference provider in v0.9.3.`;
- compatibility acceptance of explicit `--provider ollama` at runtime/CLI level.

The provider-neutral invariant applies to the installer interface/dependencies/policy ownership, not to broadening v0.9.3 runtime provider support.

## Hard read-only fence

Task 123 authorizes **zero product/runtime lifecycle mutation**.

Do not run:

- install/install-over;
- reset;
- uninstall;
- reinstall;
- enable/disable/start/stop/restart;
- recovery disruptive scenarios;
- plugin install/uninstall/update;
- provider/runtime/model/config changes;
- manifest/state normalization;
- cleanup/deletion/move/rename of live CNX/OpenClaw/provider surfaces;
- Dashboard semantic Send;
- reboot/process kill;
- merge/tag/release/force push.

Writing evidence files under a new external Task-123 evidence root is allowed.

## Probe discipline — mandatory

1. **Do not reuse the Task-121/122 generalized probe wrapper.**
2. Do not use `Start-Process` for command proof.
3. Use PowerShell call operator `&` with each argument supplied as a separate string element.
4. Run probes one command at a time; capture command line/argument array, stdout/stderr, exit code, and duration.
5. If a command unexpectedly prints help/TUI content, record it and stop using that surface; do not retry through another opaque wrapper.
6. Prefer filesystem/config/listener/REST proof where it is more deterministic than a UI-capable executable.
7. Never print or persist credentials/tokens/secrets. Read only narrowly required non-sensitive config fields.

## Phase 0 — fresh repository/coordination reconciliation

Before machine probing:

- fetch current branch HEAD;
- verify Task 123 is active in `ACTIVE.md` and `STATUS.md`;
- verify no newer task supersedes it;
- verify Task-121 and Task-122 reports/reviews;
- verify the consumed-attempt ledger above;
- create a new external evidence root.

No live mutation.

## Phase 1 — installed CNX direct argument-forwarding proof

Resolve:

```powershell
$Workspace = Join-Path $HOME '.openclaw\workspace'
$Cnx = Join-Path $Workspace 'cnxclaw.cmd'
```

Require the launcher exists.

Invoke directly, with literal separate arguments and no generalized wrapper:

```powershell
$statusText = & $Cnx 'status' 2>&1 | Out-String
$statusRc = $LASTEXITCODE

$providerText = & $Cnx 'provider' 'status' '--json' 2>&1 | Out-String
$providerRc = $LASTEXITCODE

$recoveryText = & $Cnx 'check' 'recovery' '--json' 2>&1 | Out-String
$recoveryRc = $LASTEXITCODE
```

Requirements:

- `status` exit `0` and valid status JSON;
- provider status exit `0` and valid JSON;
- recovery check exit `0` or documented read-only warning exit `1`, with valid JSON;
- arguments are demonstrably forwarded (help/banner-only output does not satisfy the gate);
- runtime may legitimately report selected provider `ollama`.

Also run `check system` only if the direct argument-forwarding proof above succeeds; record its exit/output separately.

## Phase 2 — ownership and exact installed payload attribution

Resolve explicit paths:

```powershell
$Python = Join-Path $env:LOCALAPPDATA 'CogentNexus-OpenClaw\runtime\python\Scripts\python.exe'
$OwnershipScript = Join-Path $Workspace 'skills\cogentnexus-openclaw\scripts\namespace_ownership.py'
$OwnershipRoot = Join-Path $Workspace '.cogentnexus-openclaw'
```

Require `$Python` and `$OwnershipScript` exist before invocation.

Run directly:

```powershell
$verifyText = & $Python $OwnershipScript 'verify' '--root' $OwnershipRoot '--workspace' $Workspace 2>&1 | Out-String
$verifyRc = $LASTEXITCODE
```

Require exit `0` and valid ownership verification output.

Additionally:

- read `ownership.json` narrowly and record non-secret ownership fields;
- compute installed plugin fingerprint with the explicit installed ownership tool;
- require fingerprint equals `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- compare SHA256 for critical installed files against the exact candidate extraction where practical, including `cnxclaw_v093.py` and `namespace_ownership.py`;
- verify installed launcher/runtime help text matching Ollama-only policy is expected candidate content, not a provider-neutrality failure.

## Phase 3 — OpenClaw proof without `.cmd` wrapper dependency

Do not use `openclaw.cmd` as the primary proof surface in this task.

Resolve:

```powershell
$Node = (Get-Command node.exe -ErrorAction Stop).Source
$OpenClawRoot = Join-Path $env:APPDATA 'npm\node_modules\openclaw'
$OpenClawEntry = Join-Path $OpenClawRoot 'dist\index.js'
$OpenClawPackage = Join-Path $OpenClawRoot 'package.json'
```

Require all paths used exist.

### 3A — exact installed version

Read only the `version` field from `package.json`; do not dump the full package/config tree.

Require exact version `2026.7.1-2`.

Optionally corroborate with direct Node invocation:

```powershell
& $Node $OpenClawEntry '--version'
```

using separate arguments and no wrapper. Package metadata remains acceptable version proof if the direct CLI surface is unsuitable.

### 3B — plugin inventory

Invoke the Node entrypoint directly:

```powershell
$pluginText = & $Node $OpenClawEntry 'plugins' 'list' '--json' 2>&1 | Out-String
$pluginRc = $LASTEXITCODE
```

Require valid JSON and a coherent unique `cogentnexus-openclaw` registration/root if this command surface works normally.

If the direct Node command itself unexpectedly selects TUI despite correctly separated arguments, do **not** retry through another CLI wrapper. Instead use narrowly parsed non-secret OpenClaw config/plugin-registration fields plus ownership/plugin filesystem evidence to complete attribution, and record that fallback explicitly.

### 3C — Gateway proof

Do not require `openclaw gateway status` if that CLI surface is unreliable in non-TTY execution.

Read only the configured gateway port from OpenClaw config without logging secrets. Then prove:

- a listener exists on that exact port;
- owning PID/process exists;
- process identity/command line is consistent with Node/OpenClaw gateway execution;
- current CNX status/check evidence agrees with Gateway readiness.

Use `Get-NetTCPConnection` and `Get-CimInstance Win32_Process` read-only.

## Phase 4 — Ollama preservation/readiness via loopback REST, not desktop UI

Do not invoke `ollama.exe` for Task-123 proof.

Require loopback listener `127.0.0.1:11434` or equivalent configured local Ollama endpoint already owned by runtime configuration.

Use bounded read-only HTTP requests such as:

```powershell
Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:11434/api/version' -TimeoutSec 5
Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 5
```

Optionally use `/api/ps` if available; absence of running models is not itself a preservation failure if runtime checks otherwise prove readiness.

Record:

- Ollama API reachable;
- version response;
- model/tag identities sufficient to show user provider data remains present;
- no provider mutation occurred.

Do not change/load/pull/delete a model.

## Phase 5 — SQLite integrity

Identify applicable CNX-owned SQLite databases only within known owned roots.

Use the explicit resolved Python interpreter and `python -c` style read-only `sqlite3` checks, or an existing reviewed read-only checker. Do not execute arbitrary database migrations or repair.

Require `PRAGMA integrity_check` result exactly `ok` for each applicable database.

Record database path, size, and integrity result without dumping sensitive row contents.

## Phase 6 — service, namespace, and residue inventory

Read-only capture:

- `CogentNexus-OpenClaw-Supervisor` scheduled task/service state as applicable;
- current launcher/skill/state/plugin roots;
- ownership manifest path;
- current plugin candidate roots and fingerprint(s);
- legacy generic names: `cnx.cmd`, `cnx`, `skills/cogentnexus`, `.cogent`, `cogentnexus-rotation`;
- `.cogentnexus-openclaw` staging/backup/transaction/rollover surfaces.

Historical backups/staging residue are not automatically failures. Classify whether each item is active/conflicting, retired/historical, transaction-owned, or expected evidence. Fail only on an active ambiguous/conflicting ownership state.

## Phase 7 — read-only gate verdict

PASS only if the combined evidence proves:

- Task-121 install-over result is currently coherent;
- exact v0.9.3 candidate ownership verifies;
- installed plugin fingerprint is exact;
- CNX status/provider/recovery state is coherent;
- Ollama-only runtime policy is treated as expected;
- OpenClaw exact baseline `2026.7.1-2` is preserved;
- CogentNexus-OpenClaw plugin registration/root is unique and attributable;
- Gateway listener/process is healthy/coherent;
- Ollama REST/provider data is preserved/reachable;
- SQLite integrity is `ok`;
- no active conflicting legacy/current ownership exists;
- no mutation occurred during Task 123.

If any required fact remains genuinely unproven, verdict `BLOCKED`. Do not mutate to resolve it.

## Phase 8 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-123-post-install-deterministic-readonly-attestation.md`

Report must include:

- exact current branch/task reconciliation;
- evidence root;
- explicit direct invocation argument arrays/commands and exit codes;
- CNX JSON proof;
- ownership verification and installed plugin fingerprint;
- critical installed-vs-candidate hash comparison;
- OpenClaw package version and plugin/gateway proof method;
- Ollama REST/listener/model-preservation proof;
- SQLite integrity results;
- service/namespace/residue classification;
- explicit statement that Ollama-only runtime text is expected and does not contradict provider-neutral installation;
- mutation ledger showing all product lifecycle mutations `0` in Task 123;
- verdict `PASS` or `BLOCKED`;
- exact unresolved blocker if not PASS.

Then stop for independent ChatGPT review.

Do **not** create or execute the lifecycle continuation successor automatically.
