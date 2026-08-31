# Install CogentNexus-OpenClaw v0.9.3

CogentNexus-OpenClaw v0.9.3 targets OpenClaw `2026.7.1-2 (0790d9f)` and manages **Ollama only** at the current runtime/operator boundary.

The exact product candidate `f6392da3e4112ce441526d5ef19925c90a872b0b` completed the bounded real-Windows lifecycle and final Dashboard semantic/durable-delivery acceptance sequence. Public v0.9.3 release publication is nevertheless **blocked** at Task 187 because current documentation inside installed/payload-sensitive product surfaces must be corrected; changing those bytes creates a new candidate identity that requires scoped requalification before publication.

There is therefore no public `v0.9.3` GitHub Release/tag yet. Do not assume release assets exist and do not treat a moving development branch as the accepted candidate.

## Requirements

- Windows 10/11 or Windows Server with PowerShell 5.1+;
- OpenClaw installed and working;
- OpenClaw `2026.7.1-2` for the validated compatibility baseline;
- Python 3.11+ with PyYAML;
- Node.js + npm.

These are installer prerequisites. Managed-provider readiness is verified after installation by the runtime checks, not by the installer prerequisite contract.

## Development-candidate source install

Installation is performed from a reviewed source/archive through the repository installer. There is intentionally no `cnxclaw.cmd install` command.

From an exact reviewed checkout or extracted candidate archive on Windows:

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

## What the installer does

The installer is provider-neutral: it stages/validates the skill, initializes owned Host/runtime state safely, installs/validates the OpenClaw Bridge, writes the launcher, and enables the runtime only after installation-owned verification succeeds. Runtime/provider readiness is a separate post-install concern.

LM Studio belongs to the frozen v0.9.2 historical provider layer. v0.9.3 does not manage it. The v0.9.3 runtime/operator provider target is Ollama, but that selection/readiness responsibility is outside the installer prerequisite boundary.

## Accepted-candidate identity

The accepted Windows evidence applies to exactly:

```text
source candidate: f6392da3e4112ce441526d5ef19925c90a872b0b
active facade SHA-256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
OpenClaw: 2026.7.1-2 (0790d9f)
managed provider: ollama
```

Task 187 found that correcting stale current guidance inside the installed skill and npm plugin package would change that product/payload identity. A later corrected candidate must not be presented as the same accepted artifact merely because its executable source is unchanged.

## Runtime/provider readiness after installation

The v0.9.3 runtime/provider target is Ollama only. Provider executable availability, endpoint/model readiness, and provider-specific health checks belong to the runtime layer and are performed after installation.

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

## Reset to fresh-install state

```powershell
.\cnxclaw.cmd reset
```

Where supported, an explicit Ollama target may also be supplied:

```powershell
.\cnxclaw.cmd reset --provider ollama
```

`reset` is destructive and requires explicit `y` confirmation. It clears CogentNexus-OpenClaw-owned Ticket/recovery/delivery/runtime/session/workflow/diagnostic/configuration state and reconstructs fresh state from the currently installed candidate. It must not remove external OpenClaw, Ollama models/data, or unrelated workspace data.

Task 183 accepted this boundary for the frozen candidate.

## Completely uninstall CogentNexus-OpenClaw

```powershell
.\cnxclaw.cmd uninstall
```

`uninstall` is destructive and requires explicit `y` confirmation. It must return to native/PASSTHROUGH safely, remove only CogentNexus-OpenClaw-owned installation/runtime surfaces, and preserve external OpenClaw, Ollama, user data, and unrelated/future product namespaces.

Task 184 accepted this external-preservation boundary for the frozen candidate; Task 185 then accepted fresh reinstall and post-install health.

## Final semantic acceptance already completed for the frozen candidate

Task 186 accepted one bounded Dashboard turn after the lifecycle sequence:

```text
1 human Send
-> 1 Ticket
-> 1 session/run
-> 1 Ollama model call
-> 1 durable assistant delivery
-> 1 logical Dashboard assistant result
```

No retry, duplicate semantic work, direct recovery, or outbox residue occurred.

## Future published-release install

After a corrected documentation-bearing candidate is requalified and `v0.9.3` is actually published, consumer installation should use the assets generated by `.github/workflows/release.yml`:

- `cogentnexus-openclaw-v0.9.3.tar.gz`
- `cogentnexus-openclaw-v0.9.3.zip`
- `SHA256SUMS.txt`

Verify the archive checksum from `SHA256SUMS.txt`, extract the archive, then run the installer from that exact extracted release tree. Until the GitHub Release exists, do not fabricate or guess release download URLs.

See [CURRENT_STATE.md](CURRENT_STATE.md), [PROVIDERS.md](PROVIDERS.md), [CHECK_SYSTEM.md](CHECK_SYSTEM.md), and [CLEAN_REINSTALL.md](CLEAN_REINSTALL.md).
