# CNX-20260907-303 — Adopt Task301 Repair Through Supported Path

## Disposition

`BLOCKED_INSTALLER_POST_STAGE_FAILURE__TASK301_WIRING_ADOPTED__NO_RETRY__ENABLE_NOT_AUTHORIZED`

The supported repository installer was invoked exactly once in staging-only mode. It copied the Task301 Host/Supervisor wiring into the live skill root and updated the canonical launcher, but then failed during a later installed-plugin identity check because `-SkipPlugin` left `installedPluginFingerprint` null while the script still called `.ToLowerInvariant()` at `install.ps1:506`. No retry was performed. Task303 does not authorize `cnxclaw enable`.

## Method

Fresh remote re-anchor was performed before preflight. The supported adoption path was the repository's `scripts/install.ps1`, invoked with:

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "<exact checkout>\\scripts\\install.ps1" -Workspace "C:\\Users\\CDQ-P\\.openclaw\\workspace" -SkipPlugin -SkipGatewayRestart -SkipAgentsPolicy
```

This was selected because the installer contract documents staging-only flags and the live controller was already `passthrough`. It avoids plugin replacement and Gateway restart while adopting the skill/runtime wiring. Manual copying and guessed commands were not used.

## Preflight

- remote/local candidate before action: `108c0ce08b49c6990f32649cc22aedb4170bff57`
- live Host: `passthrough`, generation `62`
- Gateway: healthy
- SQLite integrity: `ok`
- target Ticket: accepted, pending, `delivery_confirmed_at=null`
- protected Ticket/session distinct and untouched
- no overlapping installer was found
- Task301 source wiring was present in the exact checkout

## Installer result

Installer stages observed:

```text
pre-install native handoff: not required (already PASSTHROUGH)
backup: created under .cogentnexus-openclaw/install-backups
skill copy: completed
CogentNexus-OpenClaw validation: PASS
owned-runtime-ensure: exit_code=0
launcher update: completed
failure: install.ps1:506
error: null-valued expression while evaluating installedPluginFingerprint.ToLowerInvariant()
process exit: 1
```

The command failed after the skill copy and launcher update, before plugin resolution/activation. Because `-SkipPlugin` was intentional, the null fingerprint is a deterministic installer control-path defect, not evidence of a live plugin defect.

## Postflight adoption evidence

Candidate-to-live exact file comparisons after the failed installer:

```text
supervisor_quiescence.py
candidate/live: 4316 bytes
SHA-256: d52f51a6aaa4fa8fd8361d684c1cf73462c93b3a083132f769374edcb4dd8d4a
exact: true

host.py
candidate/live: 36284 bytes
SHA-256: 6fd58b5ee9a039a82c59826287850564446ab631300e2b0930e3fda39dc1f2c0
exact: true

host_authority_v091.py
candidate/live: 11531 bytes
SHA-256: 6e70eda45fbf61cfa6f345a32aaf3cc6592c7b9aa10bbb56d12356fc1edce310
exact: true

cnxclaw_v093.py
candidate/live: 3829 bytes
SHA-256: 994078bc4c79bc5f653744a9ba08ccdf10fb60d0366e186df0f4b561a8957a85
exact: true
```

The canonical launcher now points to the installed owned Python runtime and live `cnxclaw_v093.py`. The lease file is absent after installer completion/failure; no enable transaction acquired it.

## Scope and live state

The installer did not use `openclaw plugins install`, did not replace the plugin, and did not request Gateway restart because `-SkipPlugin -SkipGatewayRestart` were supplied. Read-only postflight showed:

```text
Host mode: passthrough
Host generation: 62
Gateway: HTTP 200
Ollama: HTTP 200
Supervisor: Enabled / Ready / Last Result 0
SQLite integrity: ok
```

The target Ticket remained accepted with pending delivery and no durable confirmation. The protected Ticket/session remained unchanged. No semantic send, replay, redelivery, disposition, manual state edit, or session mutation occurred.

## Determination

### Adopted

- Task301 `supervisor_quiescence.py` wiring is live and byte-exact.
- Host Supervisor quiescence check is live and byte-exact.
- Host enable lease integration is live and byte-exact.
- Canonical launcher was updated through the supported installer.

### Not completed

- Installer process did not return success.
- Plugin identity/activation postcondition was not completed by this staging-only run.
- Managed enable was not invoked.
- Live worker requalification was not performed.
- Durable Discord delivery remains unconfirmed.

The next safe step is a repository TDD repair to make `install.ps1 -SkipPlugin` skip plugin-only identity/activation checks or provide an explicit non-plugin postcondition, followed by a separately authorized bounded adoption/enable task. Do not retry this installer invocation under Task303.

## Hard-fence accounting

```text
supported staging installer: 1
installer retry: 0
cnxclaw enable: 0
plugin install/replace: 0
Gateway restart/reload: 0
unrelated Scheduled Task/service mutation: 0
manual config/Ticket/SQLite/session/transcript mutation: 0
semantic send: 0
replay/redelivery/disposition: 0
protected-state mutation: 0
force push: 0
```
