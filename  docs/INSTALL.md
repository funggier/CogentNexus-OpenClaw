# Install CogentNexus v0.9.2

This guide installs the v0.9.2 Host/control baseline. The accepted compatibility target remains OpenClaw `2026.7.1-2`; newer OpenClaw versions require compatibility validation before the same guarantees should be assumed.

v0.9.2 keeps the accepted v0.9.1 Recovery Core and adds provider-neutral local lifecycle support for Ollama and LM Studio plus read-only system pre-flight checks.

## Requirements

- Windows 10/11 or Windows Server with PowerShell 5.1+;
- OpenClaw installed and working;
- Python 3.11+ with PyYAML;
- Node.js + npm;
- at least one supported local provider if CNX will manage a local provider:
  - Ollama, or
  - LM Studio with the `lms` CLI available.

Ollama and LM Studio may both be installed on the same machine. Their normal loopback ports are different (`11434` and `1234`).

## Recommended: install from a GitHub Release

1. Download `cogentnexus-v0.9.2.zip` (or tar.gz) and `SHA256SUMS.txt` from the v0.9.2 GitHub Release.
2. Verify the archive SHA256.
3. Extract it to a normal source directory outside the live OpenClaw extensions directory.
4. Open PowerShell in the extracted directory.
5. Install with the provider you want CNX to supervise:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1 -Provider ollama
```

or:

```powershell
.\scripts\install.ps1 -Provider lmstudio
```

If exactly one supported provider is installed, `-Provider` may be omitted. If both are installed on a fresh CNX state, explicit provider selection is required.

The Process-scope execution-policy change is temporary and ends with that PowerShell process.

## Source checkout install

```powershell
python -m pip install "PyYAML>=6.0,<7"
.\scripts\install.ps1 -Provider ollama
```

The installer stages the skill, validates it, initializes Host state in PASSTHROUGH, installs/validates the OpenClaw Bridge, writes `cnx.cmd`, performs provider preflight, then transactionally enables MANAGED mode. A failed provider/Gateway activation is not reported as a successful managed install.

There is intentionally no `cnx.cmd install` command. Installation is performed from an extracted release or development checkout.

## LM Studio preparation

LM Studio must expose its local server and `lms` CLI. The default server port is `1234`.

OpenClaw model routing is still configured in OpenClaw. CogentNexus provider selection controls local lifecycle/recovery responsibility; it does not silently rewrite the user's model selection.

After configuring the LM Studio model in OpenClaw, CNX can supervise the provider with:

```powershell
.\cnx.cmd start --provider lmstudio
```

## Post-install pre-flight

From the OpenClaw workspace:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnx.cmd status
.\cnx.cmd check system
```

For a hypothetical provider check without changing the persisted selection:

```powershell
.\cnx.cmd check system --provider lmstudio
```

Expected normal managed state:

- controller mode `managed`;
- one durable `selectedProvider`;
- selected provider installed/reachable;
- Gateway healthy;
- CogentNexus plugin enabled/loaded;
- Ticket database readable/integrity valid;
- no unexpected pending recovery/outbox work for an idle system.

Every `check` command is read-only and ends with `No state was changed.`

## Everyday lifecycle

```powershell
.\cnx.cmd provider list
.\cnx.cmd status
.\cnx.cmd check system
.\cnx.cmd start
.\cnx.cmd start --provider ollama
.\cnx.cmd start --provider lmstudio
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd restart --provider ollama
.\cnx.cmd disable
.\cnx.cmd enable
```

A successful `start --provider ...` remembers that provider. Later `start` and `restart` reuse the latest successfully selected provider.

`disable` means native OpenClaw PASSTHROUGH. `stop` means deliberate CNX MAINTENANCE. Both preserve the selected provider.

## Reset CogentNexus to fresh-install state

With one supported provider installed:

```powershell
.\cnx.cmd reset
```

With both Ollama and LM Studio installed, fresh reset requires an explicit new provider choice:

```powershell
.\cnx.cmd reset --provider ollama
# or
.\cnx.cmd reset --provider lmstudio
```

`reset` is destructive and requires an explicit `y` confirmation. It removes CogentNexus Tickets, recovery/delivery state, runtime/session/workflow state, diagnostics, and CNX configuration changes. It then rebuilds the currently installed release to fresh MANAGED state.

The installed CogentNexus release files/version remain unchanged. OpenClaw, Ollama and LM Studio application/model data are not removed. If reinitialization fails, CogentNexus must not claim MANAGED authority from a partial reset.

## Completely uninstall CogentNexus

```powershell
.\cnx.cmd uninstall
```

`uninstall` is destructive and requires an explicit `y` confirmation. It first returns CogentNexus to PASSTHROUGH/native OpenClaw, removes CNX startup integration and Bridge registration, verifies native Gateway health, then removes CogentNexus-owned state, skill files, plugin residue and launcher.

OpenClaw, Ollama and LM Studio remain installed.

## Operational scope

The accepted Recovery Core remains suitable for general use on the validated Windows/OpenClaw/Ollama stack. LM Studio lifecycle support is included in v0.9.2 but requires its own local live acceptance before the same provider-specific confidence is claimed. Real power-loss/cold-boot acceptance and compatibility with newer OpenClaw releases remain deferred.

See [CURRENT_STATE.md](CURRENT_STATE.md), [PROVIDERS.md](PROVIDERS.md), and [CHECK_SYSTEM.md](CHECK_SYSTEM.md).
