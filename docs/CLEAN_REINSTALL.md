# Clean reinstall on Windows

`scripts/clean-reinstall.ps1` removes the live CogentNexus-OpenClaw installation/state owned by the current OpenClaw workspace and then runs the normal v0.9.1 installer again.

## Important

A clean reinstall intentionally purges the live `.cogentnexus-openclaw` durable database/state. By default the script creates a timestamped backup **outside the workspace** before deletion. Do not use `-NoBackup` unless loss of existing Tickets, evidence, recovery state, and install history is intentional.

## Safety sequence

1. verify installer and required commands;
2. snapshot CNXCLAW state, skill, launcher, plugin directory, `AGENTS.md`, OpenClaw config and plugin index when present;
3. require `cnxclaw disable` to return OpenClaw to native PASSTHROUGH when an installed launcher exists;
4. uninstall the CogentNexus-OpenClaw plugin through OpenClaw;
5. remove any CNXCLAW extension residue left by linked/manual installs;
6. delete only CNX-owned live paths (`.cogentnexus-openclaw`, `skills/cogentnexus-openclaw`, `cnxclaw.cmd`, CNXCLAW extension directory);
7. run `scripts/install.ps1` from the current release/source package;
8. verify CNXCLAW status, Gateway status, and plugin inventory.

The script fails closed if it cannot safely disable an existing managed installation.

## Run

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\clean-reinstall.ps1
```

Optional custom workspace:

```powershell
.\scripts\clean-reinstall.ps1 -Workspace "D:\OpenClaw\workspace"
```

Skip the external backup only when deliberate:

```powershell
.\scripts\clean-reinstall.ps1 -NoBackup
```

The backup location defaults to `%LOCALAPPDATA%\CogentNexus-OpenClaw\clean-reinstall-backups\<timestamp>`.
