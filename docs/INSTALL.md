# Install CogentNexus v0.9.1

This guide installs the current v0.9.1 operational baseline. The accepted compatibility target is OpenClaw `2026.7.1-2`; newer OpenClaw versions require compatibility validation before the same guarantees should be assumed.

## Requirements

- Windows 10/11 or Windows Server with PowerShell 5.1+;
- OpenClaw installed and working;
- Python 3.11+ with PyYAML;
- Node.js + npm;
- Ollama or another already-configured OpenClaw model route if local inference is desired.

The installer validates required commands and plugin/build prerequisites.

## Recommended: install from a GitHub Release

1. Download `cogentnexus-v0.9.1.zip` (or tar.gz) and `SHA256SUMS.txt` from the v0.9.1 GitHub Release.
2. Verify the archive SHA256.
3. Extract it to a normal source directory outside the live OpenClaw extensions directory.
4. Open PowerShell in the extracted directory.
5. Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1
```

The Process-scope policy change is temporary and ends with that PowerShell process.

## Source checkout install

From the repository checkout:

```powershell
python -m pip install "PyYAML>=6.0,<7"
.\scripts\install.ps1
```

The installer stages the skill, validates it, initializes Host state in PASSTHROUGH, installs/validates the plugin, writes `cnx.cmd`, then transactionally enables MANAGED mode. A failed activation should not be reported as a successful managed install.

There is intentionally no `cnx.cmd install` command. A new installation is always performed from an extracted CogentNexus release (or a development source checkout).

## Post-install checks

From the OpenClaw workspace:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnx.cmd status
openclaw gateway status
openclaw plugins list
```

Expected state for normal managed use:

- controller mode `managed`;
- Gateway healthy;
- CogentNexus plugin enabled/loaded;
- no unexpected pending recovery/outbox work for an idle system.

## Everyday lifecycle

```powershell
.\cnx.cmd start
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd gateway start
.\cnx.cmd gateway stop
.\cnx.cmd gateway restart
.\cnx.cmd disable
.\cnx.cmd enable
```

`disable` means native OpenClaw PASSTHROUGH. `stop` means deliberate CNX MAINTENANCE.

## Reset CogentNexus to fresh-install state

```powershell
.\cnx.cmd reset
```

`reset` is destructive and requires an explicit `y` confirmation. It removes CogentNexus Tickets, recovery/delivery state, runtime/session/workflow state, diagnostics, and CogentNexus configuration changes. It then rebuilds the current installed release to the same fresh MANAGED state produced by a normal installation.

The installed CogentNexus release files and version remain unchanged. OpenClaw and Ollama data are not removed. If reinitialization fails, CogentNexus must not claim MANAGED authority from a partial reset.

## Completely uninstall CogentNexus

```powershell
.\cnx.cmd uninstall
```

`uninstall` is destructive and requires an explicit `y` confirmation. It first returns CogentNexus to PASSTHROUGH/native OpenClaw, removes the CNX startup adapter and OpenClaw plugin registration, verifies native Gateway health, then removes CogentNexus state, skill files, plugin residue, and `cnx.cmd` itself.

OpenClaw and Ollama remain installed. To use CogentNexus again after uninstall, perform a normal installation from a GitHub Release as described above.

## Operational scope

The accepted Recovery Core is suitable for general use on the validated stack. Real power-loss/cold-boot acceptance and compatibility with newer OpenClaw releases are deferred. See [CURRENT_STATE.md](CURRENT_STATE.md).
