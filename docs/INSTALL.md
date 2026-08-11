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
`<workspace>/.cogent/install-backups`. The plugin is linked to the cloned
repository, so keep the clone in place.

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
   openclaw plugins install --link . --force
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

- `openclaw` not found: install or update OpenClaw and ensure it is on `PATH`.
- Plugin validation fails: use Node.js 22+, run `npm ci`, and retry.
- Gateway is unhealthy: run `openclaw status` and inspect the log path reported
  by `openclaw gateway status`.
- For planned shutdowns, use the wrappers in
  `skills/cogentnexus/templates/lifecycle` to preserve maintenance fencing.
