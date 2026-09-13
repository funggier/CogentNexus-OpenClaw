# CNX-338R.1 — Controller Authority Path Reconciliation

**Date:** 2026-09-14 (Asia/Bangkok)
**Verdict:** `PASS`
**Classification:** `AUTHORITY_PATH_MISMATCH`

## Scope and safety boundary

This was a read-only reconciliation gate. No controller file was modified, no schema or mode was migrated, no Gateway was restarted, and no Dashboard traffic, model inference, registration test, Ticket, recovery, fallback, retry experiment, TicketStore, ownership-state, or release-history operation was performed. CNX-339 remains unauthorized. CNX-338R must not be rerun until this report is accepted.

## Fixed provenance

| Item | Value |
|---|---|
| Repository | `funggier/CogentNexus-OpenClaw` |
| Candidate branch | `agent/v0.9.6-schema-authority-repair` |
| Candidate source HEAD | `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7` |
| Repair commit | `3efb971eeed55f0d48908281974577fdbed48612` |
| Installed candidate artifact | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` |
| Installed artifact SHA-256 | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| CNX-338A report commit | `328d6f83ad0c4612de29d71a7496e141a1315df4` |
| CNX-338R report commit | `07bc5e0f28b88cd1f9608fb106780b0fa7a41c2d` |
| v0.9.5 tag | `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` |

The live repository check confirmed the v0.9.5 tag resolves exactly to `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`. The installed JavaScript artifact is 10,121 bytes and hashes to the fixed candidate artifact hash above.

## Required evidence summary

| Item | Result |
|---|---|
| OpenClaw workspace | `C:\Users\CDQ-P\.openclaw\workspace` |
| CogentNexus configured root | **None**; `cogentNexusOpenClawRoot` is absent from the active plugin config |
| Runtime-resolved root | `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw` |
| Runtime-resolved controller | `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json` |
| Workspace-level alternate controller | Present; SHA-256 `14ac439bfc74511cf326507810ec2aff772fdec7114654b1e57f978c06c1d77c`; 193 bytes |
| `.cogentnexus-openclaw` controller | Present; SHA-256 `1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98`; 251 bytes |
| Canonical controller state | `schemaVersion=2`, `cnxMode=active`, `generation=101`, `updatedAt=2026-09-13T15:09:06.411038+00:00` |
| CNX-338A baseline preserved | PASS |
| Configuration override found | PASS — none found |
| Actual production authority identified | PASS |
| Confirmed mutation of production authority | NO |
| Registration test executed | MUST BE NO — no |

## Runtime workspace and configuration

The active OpenClaw configuration is `C:\Users\CDQ-P\.openclaw\openclaw.json`. Its enabled `cogentnexus-openclaw` entry explicitly contains:

```json
{
  "enabled": true,
  "config": {
    "workspaceDir": "C:\\Users\\CDQ-P\\.openclaw\\workspace",
    "providerMode": "passthrough"
  }
}
```

It contains no `cogentNexusOpenClawRoot` key. No equivalent root override was found in the active plugin entry. Therefore the installed runtime's fallback root calculation applies.

## Source/runtime path trace

The installed artifact was inspected directly, not inferred from the shell directory. Its path logic is:

1. `pluginWorkspace(api)` reads `api.pluginConfig.workspaceDir`; otherwise it reads the runtime default workspace; otherwise it falls back to `%USERPROFILE%\\.openclaw\\workspace`. The active configuration supplies `C:\Users\CDQ-P\.openclaw\workspace`.
2. `pluginCogentRoot(api)` reads `api.pluginConfig.cogentNexusOpenClawRoot` only when present and non-empty; otherwise it resolves `join(pluginWorkspace(api), ".cogentnexus-openclaw")`.
3. `hostPluginAuthority(api)` resolves `resolve(root, "host", "controller.json")` and reads that exact file.
4. `releaseEntry.register(api)` calls `hostPluginAuthority(api)` before delegating to the legacy registration boundary. Thus the authority check and the controller read use `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json`.
5. The installed artifact's runtime state loader/registration paths also use `pluginCogentRoot(api)` for the CogentNexus runtime database and related Host-owned state.

The source implementation at `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` matches the installed artifact: workspace configuration first, then runtime workspace, then the `.openclaw\workspace` fallback; root override only when explicitly configured; final controller at `<root>\host\controller.json`.

## Both controller snapshots

### Alternate workspace-level path

`C:\Users\CDQ-P\.openclaw\workspace\host\controller.json`

- Exists: yes
- SHA-256: `14ac439bfc74511cf326507810ec2aff772fdec7114654b1e57f978c06c1d77c`
- Size: 193 bytes
- `schemaVersion`: `1`
- `cnxMode`: absent
- Legacy `mode`: `passthrough`
- `generation`: `1`
- `updatedAt`: `2026-08-29T01:36:31.541994+00:00`

This is not the controller path selected by the installed candidate's `pluginCogentRoot`/`hostPluginAuthority` path.

### Canonical CogentNexus path

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json`

- Exists: yes
- SHA-256: `1cc5b42ba19e5d91620a5c4e754b900d8a986a74a624b0821e5cf363bd673d98`
- Size: 251 bytes
- `schemaVersion`: `2`
- `cnxMode`: `active`
- Legacy `mode`: absent
- `generation`: `101`
- `updatedAt`: `2026-09-13T15:09:06.411038+00:00`
- `desiredGateway`: `running`
- `providerOwnership`: `openclaw`

The canonical controller recorded by CNX-338A still exists at the same path and retains the required schema-2 active generation-101 state. **CNX-338A controller baseline remains intact.**

## Determination

The schema-1 file observed during CNX-338R is an existing alternate workspace-level controller, but it is not the production authority path selected by the installed candidate runtime. The production authority is the `.cogentnexus-openclaw` controller, and its CNX-338A baseline remains unchanged.

Accordingly, there is no evidence that the installed plugin's production authority was downgraded or mutated. The correct classification is:

```text
AUTHORITY_PATH_MISMATCH
```

`CANONICAL_CONTROLLER_DRIFT` is not confirmed. `RUNTIME_ROOT_OVERRIDE` is not applicable because no root override is configured. `UNKNOWN_AUTHORITY_ROOT` is not applicable because the installed artifact's path resolution and active configuration establish the root conclusively.

## Final gate result

`CNX-338R.1 = PASS`

All pass criteria are met: the runtime workspace, root, and controller are conclusively identified; the intended `.cogentnexus-openclaw` authority path is selected; the canonical controller remains schema 2 / active / generation 101; the alternate schema-1 path is non-authoritative; no production-authority mutation was observed; no semantic traffic or registration test occurred; and the v0.9.5 tag remains exactly `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`.

CNX-338R may be rerun only after this reconciliation report has been accepted. CNX-339 remains unauthorized.
