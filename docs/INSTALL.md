# Install CogentNexus-OpenClaw v0.9.3

CogentNexus-OpenClaw v0.9.3 is currently a development candidate. The validated compatibility target is OpenClaw `2026.7.1-2`, and the v0.9.3 managed provider surface is **Ollama only**.

There is no published v0.9.3 GitHub Release yet. Until repository stabilization, exact-candidate freeze, real-Windows lifecycle acceptance, and human release review are complete, use this document only for reviewed source/development-candidate installation work.

## Requirements

- Windows 10/11 or Windows Server with PowerShell 5.1+;
- OpenClaw installed and working;
- OpenClaw version `2026.7.1-2` for the currently validated compatibility baseline;
- Python 3.11+ with PyYAML;
- Node.js + npm.

LM Studio belongs to the frozen v0.9.2 historical provider layer. v0.9.3 does not manage it.

## Development-candidate source install

Use only a reviewed/frozen candidate when performing acceptance work. From the candidate checkout or extracted candidate archive:

```powershell
python -m pip install "PyYAML>=6.0,<7"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

On POSIX systems:

```sh
python -m pip install 'PyYAML>=6.0,<7'
./scripts/install.sh --workspace "$HOME/.openclaw/workspace"
```

There is intentionally no `cnxclaw.cmd install` command. Installation is performed from the source/archive installation entry point.

For final real-machine acceptance, the archive/source identity must already be frozen and recorded with the exact commit SHA, payload-v2 fingerprint, payload file count, archive SHA256, and GitHub Actions evidence. Do not install an ad-hoc modified worktree and call it the same candidate.

## Future published-release install

After v0.9.3 is actually published, release installation documentation may point to the published archive and checksums. Until then, do not assume a v0.9.3 release asset exists.

## What the installer does

The installer stages and validates the CogentNexus-OpenClaw skill, initializes owned Host/runtime state safely, installs/validates the OpenClaw Bridge, writes the launcher, and enables the runtime only after installation-owned verification succeeds. It does not select or preflight a provider.

The v0.9.3 operator-facing provider target is Ollama.

## Runtime/provider readiness after installation

The current v0.9.3 runtime/provider target is Ollama only. Provider executable availability, endpoint/model readiness, and provider-specific health checks belong to the runtime layer and are performed after installation.

## Post-install pre-flight

From the OpenClaw workspace:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
```

Expected managed readiness includes:

- controller mode `managed`;
- managed provider Ollama;
- Ollama installed/reachable;
- Gateway healthy;
- CogentNexus-OpenClaw plugin enabled/loaded;
- Ticket database readable and integrity-valid;
- no unexpected recovery/outbox backlog on an idle system.

Every `check` command is read-only and must not mutate lifecycle/configuration/Ticket state.

## Everyday lifecycle

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd provider list
.\cnxclaw.cmd check system
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd stop
.\cnxclaw.cmd restart
.\cnxclaw.cmd restart --provider ollama
.\cnxclaw.cmd disable
.\cnxclaw.cmd enable
```

`disable` means native OpenClaw PASSTHROUGH. `stop` means deliberate CNXCLAW MAINTENANCE.

## Reset CogentNexus-OpenClaw to fresh-install state

```powershell
.\cnxclaw.cmd reset
```

An explicit Ollama target may also be supplied where the supported interface permits it:

```powershell
.\cnxclaw.cmd reset --provider ollama
```

`reset` is destructive and requires explicit `y` confirmation. It clears CogentNexus-OpenClaw-owned Ticket/recovery/delivery/runtime/session/workflow/diagnostic/configuration state and reconstructs fresh state from the currently installed candidate. It must not remove external OpenClaw, Ollama models/data, or unrelated workspace data.

## Completely uninstall CogentNexus-OpenClaw

```powershell
.\cnxclaw.cmd uninstall
```

`uninstall` is destructive and requires explicit `y` confirmation. It must return to native/PASSTHROUGH safely, remove only CogentNexus-OpenClaw-owned installation/runtime surfaces, and preserve external OpenClaw, Ollama, user data, and unrelated/future product namespaces.

## Acceptance boundary

During the repository stabilization phase, do **not** run uninstall/install/reset/restart against the live target installation and do not send a new Dashboard semantic acceptance message.

Only after the repository candidate is frozen should a separate bounded real-Windows task exercise:

1. clean uninstall;
2. fresh install of the exact frozen candidate;
3. install-over/reset/uninstall/reinstall lifecycle tests;
4. runtime readiness and installed fingerprint parity;
5. one final Dashboard semantic/durable-delivery acceptance probe.

See [CURRENT_STATE.md](CURRENT_STATE.md), [PROVIDERS.md](PROVIDERS.md), and [CHECK_SYSTEM.md](CHECK_SYSTEM.md).
