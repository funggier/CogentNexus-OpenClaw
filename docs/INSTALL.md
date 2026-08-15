# CogentNexus installation guide

CogentNexus v0.8 installs as a **durable Host-managed control layer for OpenClaw**. A normal managed installation configures Ticket-first intake, deterministic recovery supervision, lifecycle control, and the OpenClaw bridge required to resume accepted work after interruption.

For a detailed Windows walkthrough in Thai, see [INSTALL.th.md](INSTALL.th.md).

## Requirements

- Python 3.10+
- PyYAML 6.x
- Node.js 22+
- npm
- OpenClaw
- Git only when installing from a source clone
- Ollama only when your OpenClaw provider is local Ollama

Tested baseline: OpenClaw 2026.7.1-2 or newer.

## Recommended stable install

Use a versioned GitHub Release instead of `main` for a stable machine.

For v0.8.0 on PowerShell:

```powershell
$version = "v0.8.0"
$base = "https://github.com/funggier/cogentnexus/releases/download/$version"
Invoke-WebRequest "$base/cogentnexus-$version.zip" -OutFile "cogentnexus-$version.zip"
Invoke-WebRequest "$base/SHA256SUMS.txt" -OutFile "SHA256SUMS.txt"

$actual = (Get-FileHash ".\cogentnexus-v0.8.0.zip" -Algorithm SHA256).Hash.ToLower()
$expected = ((Get-Content ".\SHA256SUMS.txt" | Select-String "cogentnexus-v0.8.0.zip") -split "\s+")[0].ToLower()
if ($actual -ne $expected) { throw "Release checksum mismatch" }

Expand-Archive ".\cogentnexus-v0.8.0.zip" -DestinationPath ".\cogentnexus-v0.8.0" -Force
cd .\cogentnexus-v0.8.0\cogentnexus-v0.8.0
python -m pip install "PyYAML>=6.0,<7"
.\scripts\install.ps1
```

If PowerShell blocks the script, use a process-scoped policy only:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1
```

## What the Windows installer does

A normal Windows install:

1. checks required commands and PyYAML;
2. backs up an existing CogentNexus skill;
3. installs and validates the skill;
4. updates only the CogentNexus-managed block in workspace `AGENTS.md`;
5. runs `npm ci`, builds and validates the OpenClaw bridge plugin;
6. installs the plugin without disturbing unrelated plugin paths;
7. creates `<workspace>\cnx.cmd`;
8. initializes durable Host state under `<workspace>\.cogent`;
9. enters MANAGED mode and enables Ticket-first settings;
10. enables the hidden deterministic Host supervisor;
11. starts/reconciles Gateway/provider state;
12. verifies Gateway and supervisor health.

The default workspace is `$HOME\.openclaw\workspace`.

## Install from source

```powershell
git clone https://github.com/funggier/cogentnexus.git
cd cogentnexus
python -m pip install -r requirements-dev.txt
.\scripts\install.ps1
```

POSIX:

```sh
git clone https://github.com/funggier/cogentnexus.git
cd cogentnexus
python -m pip install -r requirements-dev.txt
chmod +x scripts/install.sh
./scripts/install.sh
```

Windows is the primary Host-managed install path in v0.8. POSIX packaging remains supported, but platform startup adapters should be validated on the target machine before relying on unattended recovery.

## Installer options

PowerShell:

- `-Workspace PATH` — select a non-default OpenClaw workspace.
- `-SkipPlugin` — do not install the OpenClaw bridge.
- `-SkipGatewayRestart` — install files/config but leave runtime lifecycle untouched; run `cnx enable` later.
- `-SkipAgentsPolicy` — do not install the managed workspace policy.
- `-LinkPlugin` — development mode; link plugin working tree instead of copying it.

Use skip options only when you understand which managed guarantees they remove.

## First verification

After installation:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnx.cmd status
openclaw gateway status
```

Expected Host state includes:

```text
mode = managed
desiredGateway = running
```

Then send a simple message such as `สวัสดีครับ` through your OpenClaw channel and inspect:

```powershell
.\cnx.cmd ticket list
```

The request should be durably accepted without forcing the conversational turn into a STAGED workflow.

## Lifecycle commands

```powershell
.\cnx.cmd start
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd gateway start
.\cnx.cmd gateway stop
.\cnx.cmd gateway restart
```

Semantics:

- `start` -> MANAGED/running, reconcile health and resume eligible committed work.
- `stop` -> MAINTENANCE/stopped, so the supervisor does not fight an intentional stop.
- `restart` -> preserve MANAGED intent, restart, verify, then recover eligible work.
- `gateway ...` -> control only Gateway while preserving Host ownership semantics.

## Disable CogentNexus without disabling OpenClaw

```powershell
.\cnx.cmd disable
```

This enters PASSTHROUGH mode. CogentNexus disables its startup ownership, removes the managed workspace block, disables the bridge plugin, and restarts/starts native OpenClaw. Durable CogentNexus state is preserved.

Verify:

```powershell
.\cnx.cmd status
```

Expected:

```text
mode = passthrough
```

OpenClaw should remain normally usable.

Return to managed operation:

```powershell
.\cnx.cmd enable
```

## Cancel work

List Tickets:

```powershell
.\cnx.cmd ticket list
```

Cancel one Ticket:

```powershell
.\cnx.cmd ticket cancel <ticket-id> --reason "cancelled by operator"
```

Cancel all non-terminal Tickets for a session:

```powershell
.\cnx.cmd session cancel "<session-key>" --reason "session cancelled"
```

Cancellation is terminal and recovery must not resurrect cancelled work.

## Reboot recovery

When Host desired state is MANAGED/running and automatic startup is enabled, the OS launches the deterministic supervisor after startup/logon. The Host then reads persisted state, reconciles Gateway/provider health, identifies stale leases, and resumes only eligible non-terminal work.

If a response is already durably ready, recovery should retry delivery rather than recomputing the model response.

This architecture does not protect against physical storage loss/corruption or messages that never reached the durable acceptance boundary.

## Upgrading

For a stable system:

1. download the new versioned release;
2. verify SHA256;
3. extract to a new directory;
4. rerun the installer.

The installer backs up installed skill/policy files and preserves runtime data under the workspace `.cogent` directory.

Do not delete `.cogent` if you want to preserve Tickets, workflows, checkpoints, and evidence.

## Troubleshooting

### OpenClaw must work without CogentNexus

```powershell
.\cnx.cmd disable
```

### Gateway was intentionally stopped but keeps coming back

Use:

```powershell
.\cnx.cmd stop
```

instead of killing the process without persisting MAINTENANCE intent.

### A message appears stuck

Do not immediately resubmit it. Check:

```powershell
.\cnx.cmd status
.\cnx.cmd ticket list
```

A committed non-terminal Ticket may already be recovering.

### `openclaw` not found

```powershell
where.exe openclaw
openclaw --version
```

Fix the OpenClaw installation/PATH before retrying CogentNexus.

### PyYAML missing

```powershell
python -m pip install "PyYAML>=6.0,<7"
```

### Plugin validation fails

Ensure Node.js 22+ is active, then from `plugins\cogentnexus-rotation` run:

```powershell
npm ci
npm run plugin:validate
```

### Gateway unhealthy

```powershell
openclaw gateway status
openclaw status
.\cnx.cmd restart
```

Use the log path reported by OpenClaw to diagnose provider/Gateway failures that persist after managed restart.
