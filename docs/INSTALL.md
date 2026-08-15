# Installation guide

CogentNexus v0.7+ installs as a **durable Host-managed control layer for OpenClaw**. A normal managed installation configures Ticket-first intake, deterministic recovery supervision, lifecycle control, and the OpenClaw integration needed to resume accepted work after interruption.

OpenClaw remains independently usable: `cnx disable` enters PASSTHROUGH mode, removes CogentNexus interception/background ownership, and returns lifecycle control to native OpenClaw without deleting durable CogentNexus state.

## Prerequisites

- Python 3.10+
- PyYAML
- Node.js 22+
- npm
- OpenClaw
- Git when installing from a clone

Install Python development dependencies when working from source:

```sh
python -m pip install -r requirements-dev.txt
```

## What the Windows installer configures

A normal Windows installation:

1. copies and validates the CogentNexus skill;
2. builds, validates, and installs the OpenClaw plugin;
3. safely installs the bounded CogentNexus managed block in workspace `AGENTS.md`;
4. initializes Host Controller state;
5. enables Ticket-first managed settings with conservative one-at-a-time execution by default;
6. creates `cnx.cmd` in the OpenClaw workspace;
7. enables the hidden native Host supervisor; and
8. starts/reconciles the managed runtime and verifies health unless Gateway restart was explicitly skipped.

The Host Controller persists desired runtime state outside model inference. This is what lets CogentNexus distinguish an unplanned Gateway failure from a deliberate operator stop.

## Recommended stable installation

Download the latest stable archive from GitHub Releases and verify it against the published `SHA256SUMS.txt` before installation.

For v0.7.0 on Windows:

```powershell
gh release download v0.7.0 --repo funggier/cogentnexus --pattern "cogentnexus-v0.7.0.zip" --pattern "SHA256SUMS.txt"
$actual = (Get-FileHash .\cogentnexus-v0.7.0.zip -Algorithm SHA256).Hash.ToLower()
$expected = ((Get-Content .\SHA256SUMS.txt | Select-String 'cogentnexus-v0.7.0.zip') -split '\s+')[0]
if ($actual -ne $expected) { throw "Release checksum mismatch" }
Expand-Archive .\cogentnexus-v0.7.0.zip
cd .\cogentnexus-v0.7.0
.\scripts\install.ps1
```

On Linux or macOS, download the matching `.tar.gz`, verify it with `sha256sum -c SHA256SUMS.txt --ignore-missing`, extract it, and run `./scripts/install.sh`.

## Install from source

```sh
git clone https://github.com/funggier/cogentnexus.git
cd cogentnexus
```

Windows PowerShell:

```powershell
.\scripts\install.ps1
```

Linux or macOS:

```sh
chmod +x scripts/install.sh
./scripts/install.sh
```

The default workspace is `~/.openclaw/workspace`. Select another workspace with `-Workspace PATH` on PowerShell or `--workspace PATH` on POSIX systems. The POSIX installer also accepts `OPENCLAW_WORKSPACE`.

## Installer options

- `-SkipPlugin` / `--skip-plugin` — install only the skill/policy pieces that do not require the plugin.
- `-SkipGatewayRestart` / `--skip-gateway-restart` — leave the currently running Gateway lifecycle untouched during installation.
- `-SkipAgentsPolicy` / `--skip-agents-policy` — use only when another workspace policy already provides the required CogentNexus admission behavior.
- `-LinkPlugin` / `--link-plugin` — developer mode that links the plugin to a working tree instead of copying the packaged plugin.

When upgrading, the installer backs up replaced skill/policy content under `<workspace>/.cogent/install-backups`. It preserves user-authored `AGENTS.md` content and manages only the section between:

```text
<!-- cogentnexus:begin -->
<!-- cogentnexus:end -->
```

Re-running the installer updates that section idempotently rather than appending duplicates.

When migrating from an older linked plugin, the installer removes only load paths that identify themselves as `cogentnexus-rotation`; unrelated OpenClaw plugin paths and existing CogentNexus configuration are preserved.

## First commands after installation

On Windows, run from the OpenClaw workspace:

```powershell
.\cnx.cmd status
```

Useful lifecycle commands:

```powershell
.\cnx.cmd start
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd gateway restart
```

Useful work-control commands:

```powershell
.\cnx.cmd ticket list
.\cnx.cmd ticket cancel <ticket-id>
.\cnx.cmd session cancel <session-key>
```

Mode switching:

```powershell
.\cnx.cmd disable
.\cnx.cmd enable
```

Semantics are intentionally distinct:

- `stop` -> **MAINTENANCE**. CogentNexus records that the shutdown is intentional and the supervisor must not restart the runtime against operator intent.
- `start` -> **MANAGED/RUNNING**. CogentNexus reconciles runtime health and resumes eligible committed work.
- `restart` -> preserve managed intent, restart, verify health, then continue eligible work.
- `disable` -> **PASSTHROUGH**. CogentNexus relinquishes interception and lifecycle ownership so OpenClaw operates normally.
- `enable` -> return to **MANAGED** operation and reconcile the CogentNexus-managed runtime.

## Ticket-first behavior

In MANAGED mode, eligible owner messages can be committed to the durable Ticket store before model inference. Ticket creation is deliberately lightweight and does not mean every request becomes a staged workflow.

For example, a greeting can follow this path:

```text
message received
  -> Ticket committed
  -> DIRECT lane
  -> normal model reply
  -> delivered
```

If the Gateway is interrupted after the Ticket was committed, the Host Controller can detect the interruption and promote the accepted Ticket into durable recovery once the runtime is healthy again.

The terminal invariant is:

> accepted work must become delivered/completed, cancelled, or explicitly failed; it must not silently disappear.

## Reboot and power-loss recovery

Managed desired state is persisted to disk. After Windows/system restart, the Host supervisor can reconcile the configured runtime, identify stale leases or interrupted non-terminal work, and resume only work that remains eligible for recovery.

Recovery is evidence-gated. External side effects are not blindly repeated after interruption; cancellation and session-generation fencing prevent deliberately abandoned work from being resurrected.

A real abrupt power-loss test still depends on the local machine, filesystem, OpenClaw configuration, and provider runtime. Automated tests validate state persistence, interruption promotion, cancellation, duplicate fencing, and supervisor behavior, but cannot physically reproduce loss of power to the target computer.

## Manual installation

1. Copy `skills/cogentnexus` to `<workspace>/skills/cogentnexus`.
2. Validate the installed skill:

   ```sh
   python <workspace>/skills/cogentnexus/scripts/validate.py --workspace-singleton
   ```

3. Build and validate the plugin:

   ```sh
   cd plugins/cogentnexus-rotation
   npm ci
   npm test
   npm run evaluation
   npm run plugin:validate
   openclaw plugins install . --force
   ```

4. Install the managed workspace policy and initialize Host state using the same scripts used by the automated installer, or use the automated installer unless you specifically need a custom integration.

5. Restart/reconcile and verify OpenClaw only after the managed state and policy are in place.

## Updating

For source installs, run `git pull --ff-only`, then rerun the platform-specific installer. For stable production use, prefer a versioned release archive and checksum verification.

Existing durable state, Ticket/workflow data, configuration, and user-authored workspace instructions are preserved unless an explicit destructive operation is requested.

## Troubleshooting

- **OpenClaw should run without CogentNexus:** run `cnx disable` / `.\cnx.cmd disable`. This enters PASSTHROUGH; it is not the same as stopping OpenClaw.
- **Gateway intentionally stopped but keeps restarting:** verify the Host state is MAINTENANCE/STOPPED and use `cnx stop` rather than killing the process without recording operator intent.
- **A message was accepted but no reply appeared:** inspect `cnx status` and `cnx ticket list` before resubmitting. A committed non-terminal Ticket may already be scheduled for recovery.
- **`openclaw` not found:** install/update OpenClaw and ensure it is on `PATH`.
- **Plugin validation reports stale metadata:** run the plugin build/metadata generation step and then `npm run plugin:validate` again.
- **Gateway is unhealthy:** inspect `openclaw gateway status` and the log path it reports; Host recovery should only restart after health evidence confirms an unplanned failure.
- **Planned maintenance:** use `cnx stop` or the lifecycle wrappers rather than manually killing managed processes, so deliberate-stop fencing is persisted correctly.
