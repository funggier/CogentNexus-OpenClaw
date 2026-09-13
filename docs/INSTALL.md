# Install CogentNexus-OpenClaw v0.9.5

CogentNexus-OpenClaw `v0.9.5` is the current published stable release. The release tag and GitHub Release both resolve to merge SHA `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`.

For public installation, use the exact `v0.9.5` GitHub Release assets and verify `SHA256SUMS.txt` before extraction. A moving branch is not a release identity.

## Requirements

- Windows 10/11 or supported Windows Server with PowerShell 5.1+;
- OpenClaw installed and working;
- validated compatibility baseline: OpenClaw `2026.7.1-2 (0790d9f)`;
- Python 3.11+ with PyYAML;
- Node.js + npm.

Managed-provider readiness is verified after installation; it is not implied by installer prerequisites alone.

## Install from an exact release checkout

There is intentionally no `cnxclaw.cmd install` command. Installation is performed by the repository installer from an exact verified release tree or reviewed source checkout.

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

The installer is provider-neutral. Runtime/provider ownership is established separately after installation.

## v0.9.5 provider boundary

- **Ollama** is the managed provider for health, lifecycle, and recovery.
- **Cloud providers** use OpenClaw-owned pass-through. OpenClaw owns authentication, routing/model selection, runtime, lifecycle, probing, and recovery.
- CogentNexus-OpenClaw never reads, copies, persists, refreshes, or logs Cloud credentials.
- Historical LM Studio/provider behavior is not a current managed-provider contract.

## Post-install verification

From the OpenClaw workspace:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
```

A healthy managed installation should report managed mode, a loaded `0.9.5` plugin, healthy Gateway, reachable/ready Ollama, readable Ticket state, healthy supervision, and no unexpected outbox backlog on an idle system.

Every `check` command is observational and must not mutate lifecycle/configuration/Ticket state or execute model inference.

## Everyday lifecycle

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd provider list
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd stop
.\cnxclaw.cmd restart
.\cnxclaw.cmd restart --provider ollama
.\cnxclaw.cmd disable
.\cnxclaw.cmd enable
```

`disable` means native OpenClaw PASSTHROUGH. `stop` means deliberate CNXCLAW MAINTENANCE.

## Reset and uninstall

```powershell
.\cnxclaw.cmd reset
.\cnxclaw.cmd uninstall
```

Both are destructive and require explicit `y` confirmation. They are ownership-bounded and must preserve external OpenClaw, Ollama models/data, user data, and unrelated namespaces.

## Recovery boundary

A transient model-call failure does not by itself authorize provider replacement or destructive recovery. Recovery requires sufficient evidence and preserves Ticket/session/generation and original provider/model identity. Once a durable result exists, delivery retry is not permission to regenerate inference.

## Known post-release diagnostic anomaly

On the validated v0.9.5 host, `cnxclaw.cmd check system` may still emit a provider-selection diagnostic while `cnxclaw.cmd status` reports an active managed runtime, selected Ollama route, healthy Gateway, and Ollama readiness. This is recorded as a known checker inconsistency, not silently promoted to runtime failure.

The immutable `v0.9.5` tag must not be modified to address it. A correction requires a new development candidate and the normal validation/release process.

## Evidence and current state

See:

- [CURRENT_STATE.md](CURRENT_STATE.md)
- [POST_RELEASE_BASELINE.md](POST_RELEASE_BASELINE.md)
- [PROVIDERS.md](PROVIDERS.md)
- [CHECK_SYSTEM.md](CHECK_SYSTEM.md)
- [CLEAN_REINSTALL.md](CLEAN_REINSTALL.md)
- [v0.9.5 release notes](releases/v0.9.5.md)
