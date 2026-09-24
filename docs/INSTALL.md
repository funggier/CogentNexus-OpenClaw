# Install CogentNexus-OpenClaw v0.9.7

For production installation, use the exact published v0.9.7 GitHub Release archive and verify `SHA256SUMS.txt`. The accepted release/tag SHA is `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`. A moving branch is not a release identity.

## Requirements

- Windows 10/11 or supported Windows Server with PowerShell 5.1+;
- working OpenClaw installation;
- Python 3.11+ with PyYAML;
- Node.js + npm for source/release-tree installation.

Compatibility evidence is split deliberately:

- regression/dev dependency pin: OpenClaw `2026.7.1-2`;
- latest physical runtime acceptance: OpenClaw `2026.9.5 (ec9c1a1)`.

## Development-candidate source install

There is intentionally no `cnxclaw.cmd install` command. Install from an exact release tree or reviewed source checkout.

```powershell
python -m pip install "PyYAML>=6.0,<7"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

POSIX:

```sh
python -m pip install 'PyYAML>=6.0,<7'
./scripts/install.sh --workspace "$HOME/.openclaw/workspace"
```

## What the installer does

The installer is provider-neutral. Provider/model/auth ownership is established by the runtime/OpenClaw boundary, not invented by the installer.

## Provider boundary

- Managed local provider lifecycle: Ollama.
- Cloud/model/auth routing: OpenClaw-owned pass-through.
- No silent provider fallback.
- CNX does not store or refresh Cloud credentials.

## Advanced Windows installer / rollover recovery parameters

The Windows installer also exposes the implemented advanced switches below for controlled recovery and qualification work:

- `-Workspace <path>`
- `-RecoverRolloverTransaction <path>`
- `-RecoverRolloverTransactionSha256 <sha256>`
- `-RecoverRolloverSourcePluginRoot <path>`
- `-SkipPlugin`
- `-SkipGatewayRestart`
- `-SkipAgentsPolicy`
- `-LinkPlugin`

Rollover recovery must use a **verified-artifact plugin root** and the expected transaction/fingerprint evidence enforced by the installer. There is intentionally no `-InstallSourceCommit` parameter; release identity comes from verified artifacts and the exact candidate/release workflow, not from a caller-supplied commit label.

## Post-install verification

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
```

A healthy managed installation should show:

- active/managed CNX controller;
- loaded v0.9.7 plugin;
- healthy Gateway;
- selected/usable OpenClaw model route;
- Ollama readiness when managed local-provider ownership is active;
- readable Ticket state;
- healthy supervision;
- no unexpected pending outbox/recovery backlog on an idle system.

`check` commands are observational and must not execute inference or mutate lifecycle state.

## Everyday lifecycle

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd start
.\cnxclaw.cmd stop
.\cnxclaw.cmd restart
.\cnxclaw.cmd disable
.\cnxclaw.cmd enable
.\cnxclaw.cmd gateway start
.\cnxclaw.cmd gateway stop
.\cnxclaw.cmd gateway restart
```

`stop` is deliberate MAINTENANCE. `disable` returns to native/pass-through behavior.

## Ticket/session control

```powershell
.\cnxclaw.cmd ticket list
.\cnxclaw.cmd ticket cancel <ticket-id>
.\cnxclaw.cmd session cancel <session-key>
```

Do not edit Ticket/session SQLite files manually.

## Reset / uninstall

```powershell
.\cnxclaw.cmd reset
.\cnxclaw.cmd uninstall
```

These operations are destructive, require explicit confirmation, and must remain ownership-bounded.

## Clean reinstall

See [CLEAN_REINSTALL.md](CLEAN_REINSTALL.md). A clean reinstall intentionally purges CNX-owned durable state after making an external backup unless backup is explicitly disabled.

## Release installation

Published v0.9.7 release assets are:

- `cogentnexus-openclaw-v0.9.7.tar.gz`
- `cogentnexus-openclaw-v0.9.7.zip`
- `SHA256SUMS.txt`
- release notes

Verify archive checksums before installation.

## More information

- [CURRENT_STATE.md](CURRENT_STATE.md)
- [PROVIDERS.md](PROVIDERS.md)
- [CHECK_SYSTEM.md](CHECK_SYSTEM.md)
- [COMMANDS.th.md](COMMANDS.th.md)
- [v0.9.7 release notes](releases/v0.9.7.md)