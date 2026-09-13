# CNX-20260914-338A — Candidate Installation and Provenance Report

**Execution timestamp:** 2026-09-13T22:52:24Z (UTC)
**Candidate branch:** `agent/v0.9.6-schema-authority-repair`
**Fresh remote coordination HEAD:** `db3d49e00fc12a709162d22f7b772c7972585f6f`
**Candidate source HEAD used for build:** `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7`
**Repair commit:** `3efb971eeed55f0d48908281974577fdbed48612`

## Metadata and build

| Field | Observed |
|---|---|
| Package | `openclaw-plugin-cogentnexus-openclaw` |
| Package version | `0.9.5` |
| Plugin manifest version | `0.9.5` |
| Ownership metadata | `private: true`; manifest id `cogentnexus-openclaw`; OpenClaw extension `./dist/v091-release-entry.js` |
| Build metadata | `npm ci`; `npm run plugin:build`; npm pack filename `openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz` |
| Source SHA | `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7` |
| Repair SHA | `3efb971eeed55f0d48908281974577fdbed48612` |
| Build verifier | PASS: `CogentNexus-OpenClaw mixed-plugin artifact verification: PASS (46 config properties, 5 tools)` |
| Expected artifact | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| Built artifact | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| Built artifact size | 10,121 bytes |

The candidate metadata remains `0.9.5`. No version bump was made. The immutable source/artifact identity is the candidate identity for this development installation, as authorized by CNX-338A.

## Installation

The repository installer was attempted first from the exact detached candidate checkout:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx338a-candidate/scripts/install.ps1
```

It stopped before mutation with:

```text
Existing CogentNexus-OpenClaw controller has no mode; refusing install mutation.
```

This is the repository installer’s legacy-schema preflight and is incompatible with the existing canonical schema-2 controller. No controller mutation occurred during that attempt.

The supported OpenClaw plugin installation mechanism was then used with the exact package produced from the same candidate checkout:

```text
npm pack --json
openclaw plugins install C:/Users/CDQ-P/AppData/Local/Temp/cnx338a-candidate/plugins/cogentnexus-openclaw/openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz --force
```

OpenClaw reported `Installed plugin: cogentnexus-openclaw` and installed the complete package at:

```text
C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw
```

A single supported lifecycle action was required because OpenClaw reported `Restart the gateway to load plugins`:

```text
openclaw gateway restart
```

It completed with `Restarted Scheduled Task: OpenClaw Gateway` and exit code 0. No restart loop, arbitrary process kill, recovery, fallback, or service debugging was used.

## Installed provenance

| Field | Observed |
|---|---|
| Installed plugin path | `C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw` |
| Installed entry | `C:/Users/CDQ-P/.openclaw/extensions/cogentnexus-openclaw/dist/v091-release-entry.js` |
| Installed artifact SHA-256 | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| Old artifact SHA-256 | `da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef` |
| Old artifact active at expected path | No |
| OpenClaw source | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` |
| Plugin version | `0.9.5` |
| Enabled | `true` |
| Status | `loaded` |
| Dependency status | required and optional dependencies installed; missing `[]` |

`openclaw plugins list --json` after the gateway restart independently reported the expected path, `enabled: true`, and `status: loaded`. A filesystem scan found no second active entry under the expected `.openclaw` installation path; the only other matching file was the pre-existing test checkout copy, not an active OpenClaw extension.

## Controller integrity

Before and after installation:

```text
schemaVersion = 2
cnxMode = active
generation = 101
```

Controller path:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/host/controller.json
```

Before/after controller bytes were identical. No legacy `mode` field was written. The schema-2 translation remained in-memory only.

## Provider and timeout fence

The installed OpenClaw configuration was read after installation and was unchanged:

```text
provider/model = ollama/qwen3.8:27b
workspace = C:\Users\CDQ-P\.openclaw\workspace
tagged agent timeout = 2700 seconds (agents.defaults.timeoutSeconds)
ollama provider timeout = 2700 seconds (models.providers.ollama.timeoutSeconds)
```

No provider, model, or timeout setting was changed.

## Release fence and traffic boundary

Fresh remote verification:

```text
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95 refs/tags/v0.9.5
```

The v0.9.5 tag was not moved. No merge to main, force-push, history rewrite, v0.9.6 release, Dashboard Send, semantic model inference, intentional Ticket, recovery, or fallback was performed.

## Verdict

# PASS

The exact candidate source produced the required artifact, and the complete candidate package is installed and loaded/enabled in the real OpenClaw extension path. The installed SHA-256 equals the required candidate SHA-256, the old artifact is no longer active at that path, the schema-2 controller is unchanged, the provider/timeout fence is unchanged, and the v0.9.5 tag remains immutable.

CNX-338R is authorized as the next gate. CNX-339 remains unauthorized until CNX-338R passes.
