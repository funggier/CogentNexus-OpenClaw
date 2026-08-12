# Installation guide

CogentNexus requires Python 3.10+, PyYAML, Node.js 22+, npm, OpenClaw, and Git. The
installer copies the skill into an OpenClaw workspace, validates it, builds and
links the rotation plugin, restarts Gateway, and verifies runtime health.

Install the Python dependency once if needed:

```sh
python -m pip install -r requirements-dev.txt
```

## Automated installation

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

The default workspace is `~/.openclaw/workspace`. Select another workspace
with `-Workspace PATH` on PowerShell or `--workspace PATH` on POSIX systems.
The POSIX installer also accepts `OPENCLAW_WORKSPACE`.

Use `-SkipPlugin` or `--skip-plugin` to install only the skill. Use
`-SkipGatewayRestart` or `--skip-gateway-restart` to leave Gateway unchanged.
If a skill already exists, the installer creates a timestamped backup under
`<workspace>/.cogent/install-backups`. By default the plugin is copied into
OpenClaw, so the downloaded release directory may be removed after a successful
installation. Developers can use `-LinkPlugin` or `--link-plugin` to link the
plugin to a working tree instead.

When upgrading from an older linked installation, the installer removes only
load paths that identify themselves as `cogentnexus-rotation`; unrelated plugin
paths and the existing CogentNexus configuration are preserved.

## Install a GitHub Release

Because this repository is private, authenticate GitHub CLI first with
`gh auth login`. Then download and verify a fixed release:

```powershell
gh release download v0.2.0 --repo funggier/cogentnexus --pattern "cogentnexus-v0.2.0.zip" --pattern "SHA256SUMS.txt"
$actual = (Get-FileHash .\cogentnexus-v0.2.0.zip -Algorithm SHA256).Hash.ToLower()
$expected = ((Get-Content .\SHA256SUMS.txt | Select-String 'cogentnexus-v0.2.0.zip') -split '\s+')[0]
if ($actual -ne $expected) { throw "Release checksum mismatch" }
Expand-Archive .\cogentnexus-v0.2.0.zip
cd .\cogentnexus-v0.2.0
.\scripts\install.ps1
```

On Linux or macOS, download `cogentnexus-v0.2.0.tar.gz`, verify it with
`sha256sum -c SHA256SUMS.txt --ignore-missing`, extract it, and run
`./scripts/install.sh`.

## Manual installation

1. Copy `skills/cogentnexus` to `<workspace>/skills/cogentnexus`.
2. Validate the installed skill:

   ```sh
   python <workspace>/skills/cogentnexus/scripts/validate.py --workspace-singleton
   ```

3. Build, validate, and link the plugin:

   ```sh
   cd plugins/cogentnexus-rotation
   npm ci
   npm run plugin:validate
   openclaw plugins install . --force
   ```

4. Restart and verify:

   ```sh
   openclaw gateway restart
   openclaw gateway status
   python <workspace>/skills/cogentnexus/scripts/phase3.py supervisor doctor
   python <workspace>/skills/cogentnexus/scripts/phase3.py supervisor tick --execute-safe
   ```

## Updating

Run `git pull --ff-only`, then rerun the platform-specific installer. Existing
skill files are backed up before replacement, and plugin installation is
idempotent.

## Troubleshooting

- WebChat shows `Your message could not be sent` followed by `CogentNexus
  admitted this as durable workflow ... (blocked by cogentnexus-rotation)`:
  copy the workflow ID from the notice and inspect
  `.cogent/workflows/<id>/state.json`. If the workflow exists, is owner-bound,
  and has state `running`, the request was accepted successfully. OpenClaw
  labels every pre-inference `block` hook decision as an unsent message;
  CogentNexus uses that decision to prevent duplicate model execution after
  durable admission. Do not resubmit solely because of this wording.
- `openclaw` not found: install or update OpenClaw and ensure it is on `PATH`.
- Plugin validation fails: use Node.js 22+, run `npm ci`, and retry.
- Gateway is unhealthy: run `openclaw status` and inspect the log path reported
  by `openclaw gateway status`.
- For planned shutdowns, use the wrappers in
  `skills/cogentnexus/templates/lifecycle` to preserve maintenance fencing.
