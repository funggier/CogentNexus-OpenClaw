# CNX-364 — Path-bound runtime provenance report

## Classification

`BLOCKED`

CNX-361 and CNX-362 cannot be proven to have read the same physical controller file from the durable evidence preserved by either task. The available current machine evidence identifies one canonical root and its present file, but it does not retroactively bind that path/file to the CNX-361 or CNX-362 reads. No repair is authorized or made.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub-authoritative branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Exact remote HEAD re-fetched before work: `fffd8721369cf585a4c7e1df6af2c0a131176293`
- Parent: `CNX-20260915-363`
- Task: `CNX-20260915-364`
- Task status: `READY_FOR_HERMES`
- No force-push and no history rewrite

## Exact evidence gap

```text
CNX-361 controller read
       ?
same physical file?
       ?
CNX-362 controller read
```

## Accepted and observed controller identities

CNX-361 report (`CNX-20260915-361-rollover-canonical-mode-repair-report.md`) records:

```text
schemaVersion=2
cnxMode=active
desiredGateway=running
generation=103
```

It records the supported installer invocation and installed plugin identity, but not a separately preserved absolute controller path, controller hash, workspace/state-root binding, launcher binding, or application-data manifest for that read.

CNX-362 report (`CNX-20260915-362-openai-ticket-first-semantic-requalification-report.md`) records:

```text
schemaVersion=1
mode=passthrough
desiredGateway=running
generation=1
updatedAt=2026-08-29T01:36:31.541994+00:00
```

It records the installed plugin root and entry hash, but not the absolute controller path, workspace/state-root binding, launcher, runtime-authority identity, application-data root, or controller hash for that read.

Installed plugin identity in both reports remained:

```text
id=yswkca
version=0.9.5
enabled=true
status=loaded
entry SHA-256=da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef
```

This common plugin identity does not prove common Host state identity.

## Exact source root/path calculations

The canonical installer implementation is `scripts/install.ps1`:

- lines 3–4: default `Workspace = Join-Path $HOME ".openclaw\\workspace"` unless an explicit `-Workspace` is supplied;
- lines 28–29: `$cogentNexusOpenClawRoot = Join-Path $Workspace ".cogentnexus-openclaw"` and `$controllerPath = Join-Path $cogentNexusOpenClawRoot "host\\controller.json"`;
- lines 34–35: legacy compatibility root `$legacyRoot = Join-Path $Workspace ".cogent"`, with `$legacyControllerPath = Join-Path $legacyRoot "host\\controller.json"`;
- lines 38–39: `$applicationDataRoot = Join-Path $localAppData "CogentNexus-OpenClaw"`;
- lines 549–557: runtime authority script is resolved from the installed target skill as `scripts\\runtime_authority.py`, and is passed the application-data root;
- lines 209–210, 236, 274, 353, and 557: workspace/application-data values are passed to ownership, recovery, transaction, and runtime-authority operations.

Therefore, for the default workspace:

| Value | Exact calculation | Source | Role |
|---|---|---|---|
| `Workspace` | `%USERPROFILE%\\.openclaw\\workspace` | `scripts/install.ps1:3` | installer/Host workspace |
| `stateRoot` | `<Workspace>\\.cogentnexus-openclaw` | `scripts/install.ps1:28`; `namespace_ownership.py:82` | canonical CNX state root |
| `controllerPath` | `<stateRoot>\\host\\controller.json` | `scripts/install.ps1:29`; `host_state_v095.py:22`; `checks.py:36` | canonical Host controller |
| `legacyRoot` | `<Workspace>\\.cogent` | `scripts/install.ps1:34` | installer migration compatibility root |
| `applicationDataRoot` | `%LOCALAPPDATA%\\CogentNexus-OpenClaw` | `scripts/install.ps1:38–39`; `runtime_authority.py:43–49` | owned runtime/application data |
| `launcherPath` | `<Workspace>\\cnxclaw.cmd` | `scripts/install.ps1:30`; ownership manifest schema | workspace launcher |
| `runtimeAuthorityPath` | `<targetSkill>\\scripts\\runtime_authority.py` | `scripts/install.ps1:549` | owned Python runtime authority |

Other source consumers independently default to `<workspace>\\.cogentnexus-openclaw`: `host_state_v095.py`, `host.py`, `host_legacy_v094.py`, `host_control.py`, `host_context.py`, `lifecycle_v091.py`, `lifecycle_v092.py`, `runtime.py`, `startup.py`, `cnxclaw.py`, and the plugin's `v091-release-entry.ts`. The plugin entry computes its controller at `resolve(root, "host", "controller.json")`, where `root` is configured `cogentNexusOpenClawRoot` or `join(pluginWorkspace(api), ".cogentnexus-openclaw")` (`plugins/cogentnexus-openclaw/src/v091-release-entry.ts:48,118`). Portable lifecycle templates can instead use `COGENTNEXUS_OPENCLAW_ROOT` or the current working directory (`templates/lifecycle/*`). This creates a legitimate alternate-root mechanism if callers supply different workspace/root context.

## Root/provenance table

| component | function | root calculation | read/write | canonical/legacy |
|---|---|---|---|---|
| Installer | `install.ps1` | `Workspace` argument/default, then `Workspace/.cogentnexus-openclaw`; also `Workspace/.cogent` for migration source | reads controller; delegates Host and lifecycle; no direct JSON controller write found | canonical target plus legacy compatibility |
| Canonical Host | `host_state_v095.py` / `host.py` | caller-provided root, controller at `root/host/controller.json` | canonical read/write; schema 2 | canonical |
| Legacy Host | `host_legacy_v094.py`, `host_v091.py`, `host_v091_legacy_v094.py` | caller-provided root, same relative controller path | schema-1 read/write; legacy transitions | legacy |
| Ownership/recovery | `namespace_ownership.py`, `reset_v095.py` | expected workspace root or supplied root | reads ownership/controller; recovery helpers can mutate when explicitly invoked | canonical plus compatibility paths |
| Plugin runtime | `v091-release-entry.ts` | configured `cogentNexusOpenClawRoot` or plugin API workspace + `.cogentnexus-openclaw` | controller read only | legacy reader |
| Portable lifecycle | `start/stop-cogentnexus-openclaw.*` | `COGENTNEXUS_OPENCLAW_ROOT` or `$PWD/.cogentnexus-openclaw` | delegates lifecycle; may write through Host | configurable |
| Runtime authority | `runtime_authority.py` | `%LOCALAPPDATA%/CogentNexus-OpenClaw/runtime/python` | runtime manifest/runtime files, not Host controller | application-data |

## CNX-361 provenance reconstruction

Durable evidence establishes:

```text
CNX-361 installer
  -> checkout C:\Users\CDQ-P\.hermes\workspace\cnx361-remote
  -> invoked scripts/install.ps1 with no explicit -Workspace shown
  -> installer default would be C:\Users\CDQ-P\.openclaw\workspace
  -> canonical state root would be C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw
  -> canonical controller would be ...\.cogentnexus-openclaw\host\controller.json
  -> installed plugin root C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
```

The report does **not** preserve the actual resolved `-Workspace` argument, installer environment, Host root argument, absolute controller path, launcher path, runtime-authority manifest, application-data manifest, or Gateway/plugin process command line. Thus this is the source-derived expected chain, not path-bound proof of the historical read.

## CNX-362 provenance reconstruction

Durable evidence establishes:

```text
CNX-362 preflight
  -> checkout C:\Users\CDQ-P\cnx362-checkout
  -> read-only installed plugin inventory at C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
  -> controller contents observed, but no absolute controller path recorded
```

The report does not preserve the preflight workspace argument/environment, Host root, controller path, launcher, runtime-authority identity, application-data root, or process command line. Therefore it cannot be shown that CNX-362 used the default root, the CNX-361 root, or a different root.

## Read-only physical evidence available now

Current local forensic inspection (performed read-only, after the historical reports) found:

- canonical workspace exists: `C:\Users\CDQ-P\.openclaw\workspace`;
- canonical root exists: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`;
- `.cogent` compatibility root is absent at that workspace;
- current controller path is `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json`;
- current controller SHA-256 is `8d8b8bd2629325fdff33acbfa47277ab9cfde8ed32417525513d5fb151a05187`;
- current bytes are schema 2, `cnxMode=active`, `desiredGateway=running`, generation 103, `updatedAt=2026-09-15T16:16:32.390846+00:00`;
- current ownership manifest binds workspace/state root/launcher/plugin root and says `installedVersion=0.9.5`, `migrationSource=null`;
- current launcher explicitly passes `--root "C:\\Users\\CDQ-P\\.openclaw\\workspace\\.cogentnexus-openclaw"` and uses the owned runtime interpreter under `%LOCALAPPDATA%\\CogentNexus-OpenClaw\\runtime\\python`;
- no current `.cogent` controller exists.

These facts establish present canonical ownership, not the historical CNX-361/CNX-362 file identity. The current hash is not claimed as either historical hash.

## Physical identity result

| Claim | Result | Reason |
|---|---|---|
| Same absolute path | **Not proven** | neither historical report recorded it |
| Same bytes | **Not proven** | neither historical controller was hashed |
| Same state root | **Not proven** | workspace/root arguments and environment were not preserved |
| Same ownership manifest | **Not proven** | no historical manifest was bound to either controller read |
| Different root identified | **Not proven** | stale/alternate root is plausible, but no historical absolute Y exists |

Thus neither `PATH_IDENTITY_PROVEN` nor `SAME_FILE_PROVEN` is supportable. Result is `BLOCKED`.

## Timestamp analysis

`updatedAt=2026-08-29T01:36:31.541994+00:00` predates the September 15 CNX-361/CNX-362 sequence. Timestamp alone does not select a cause. All requested possibilities remain logically open: (A) the same file survived; (B) stale/alternate workspace; (C) alternate `.cogent` compatibility root; (D) restoration/copy; (E) legacy Host initialization; (F) migration; (G) runtime reading another workspace; (H) another process writing it. Source confirms that legacy Host initialization/transitions can persist schema 1/passthrough, while canonical v0.9.5 persistence writes schema 2; source does not identify which live invocation occurred.

## Generation analysis

`host_state_v095.py` defaults to generation 1 and increments on transitions. The legacy Host also defaults to generation 1 and increments on transitions. Canonical v0.9.5 code cannot, by the inspected persistence path, decrement generation 103 to 1. Therefore generation 1 is consistent with fresh/default legacy initialization, restored old state, a separate state root, or a legacy/migration boundary. It is not sufficient to distinguish among them, and no source/test evidence establishes stronger semantics.

## Process/runtime ownership findings

The source permits multiple roots when different callers provide different `Workspace`, `--root`, `COGENTNEXUS_OPENCLAW_ROOT`, current working directory, plugin `workspaceDir`, or `cogentNexusOpenClawRoot` values. The current ownership manifest and launcher bind the present canonical root, but the CNX-361/CNX-362 reports lack the historical process command lines, task/service XML instance, environment snapshot, runtime authority manifest, or file handle evidence needed to identify the process that performed either read.

Answer to the specific question:

```text
Could CNX-361 activate root X while CNX-362 later inspect root Y without either report noticing?
```

**Yes, source semantics make that possible; the reports did not preserve path-bound evidence that would have made it visible.** This is possibility, not proof that it happened.

## Single primary hypothesis and test

> I think CNX-362 read a stale or alternate Host state root containing a legacy controller because the controller timestamp predates CNX-361, the historical reports omit absolute path/root bindings, and the repository supports caller-selected roots plus a legacy schema-1 writer.

Read-only source inspection and current filesystem inspection support the compatibility and alternate-root possibility, but do not bind the August 29 controller to a particular historical path, writer, or process. The hypothesis is therefore **not proven**. No second hypothesis was selected and no repair was attempted.

## TDD decision

No RED test was added. The investigation did not prove a deterministic current source defect reproducing the historical identity split; it proved an evidence/provenance gap. Existing canonical state tests were not used to claim a runtime result.

## Explicit boundaries

- Dashboard requests: **0**.
- Model requests/inference: **0**.
- `CNX361-DONE` / `CNX362-DONE` / new semantic tests: **0**.
- Runtime mutations: **0**. No enable, start, restart, disable, stop, reinstall, controller edit, provider/routing/auth change, admission-hook change, or main/tag change.
- OpenAI PASS: **not claimed**.
- CURRENT_RED: **not claimed**.
- Runtime repaired: **not claimed**.

## Exact remaining gap

Obtain a durable, read-only historical binding for each task containing the absolute workspace/root/controller path, controller SHA-256 and metadata, ownership manifest, launcher/runtime-authority configuration, and Gateway/plugin process context, or reproduce the selection boundary under a separately authorized diagnostic that records those values without mutating runtime state. Until then, the CNX-361 → CNX-362 identity split and its writer remain unproven; semantic requalification remains stopped.
