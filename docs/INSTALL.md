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

## Clean reinstall

Use the backup-first clean reinstall wrapper when you want to remove CNX-owned runtime/install state and reinstall from the current package:

```powershell
.\scripts\clean-reinstall.ps1
```

See [CLEAN_REINSTALL.md](CLEAN_REINSTALL.md) before using it. Clean reinstall intentionally deletes the live `.cogent` state after creating a backup unless `-NoBackup` is explicitly used.

## Operational scope

The accepted Recovery Core is suitable for general use on the validated stack. Real power-loss/cold-boot acceptance and compatibility with newer OpenClaw releases are deferred. See [CURRENT_STATE.md](CURRENT_STATE.md).
