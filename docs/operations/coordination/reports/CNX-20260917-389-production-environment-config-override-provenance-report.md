# CNX-20260917-389 — Production Environment Config-Override Provenance Report

## Classification

`PRODUCTION_CONFIG_ENVIRONMENT_OVERRIDE_NOT_FOUND`

The read-only User/Machine environment inspection found no relevant OpenClaw config, state, or profile override, and the installed OpenClaw source confirms the supported selectors are `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, and `OPENCLAW_PROFILE` (with `--profile` as the equivalent CLI selector). The evidence therefore does not add a materially plausible alternate configuration source to the CNX-388 launch chain. This is provenance evidence, not proof of the historical in-memory production configuration or hook acceptance.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting remote HEAD: `019fa79f73e7e8343f0d8461ff5723c6d95b74e2`
- Starting local HEAD after fetch/re-anchor: `019fa79f73e7e8343f0d8461ff5723c6d95b74e2`
- Task: `CNX-20260917-389`
- Starting coordination status: `READY_FOR_HERMES`

The branch was fetched from GitHub and `git ls-remote` independently returned the same SHA before the investigation. The checkout was clean and detached at the authoritative tip.

## Live process re-correlation

Fresh read-only process and supported CLI observations:

| Item | Evidence |
|---|---|
| PID | `27372` |
| Creation time | `2026-09-17 05:13:48.606 +07:00` (`CreationDate=1789596828606`) |
| Executable | `C:\Program Files\nodejs\node.exe` |
| Command line | `"C:\\Program Files\\nodejs\\node.exe" C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js gateway --port 18789` |
| OpenClaw version | `2026.7.1-2 (0790d9f)`; `openclaw --version` and gateway status agree |
| Endpoint | `127.0.0.1:18789`; supported connectivity probe `ok` |
| State | `running`, Scheduled Task state `Ready` |

No lifecycle command was issued.

## Scheduled Task execution context

Read-only `schtasks.exe /Query /TN '\OpenClaw Gateway' /XML` returned:

- Description: `OpenClaw Gateway (v2026.7.1-2)`
- Principal SID: `S-1-5-21-1723981734-2946015581-220292090-1001`
- Principal logon type: `InteractiveToken`
- Trigger user: `CDQ-P\\CDQ-P`
- Action: `C:\\Users\\CDQ-P\\.openclaw\\gateway.vbs`
- Execution time limit: `PT0S`
- Multiple instances policy: `IgnoreNew`
- No task action arguments, working directory, profile selector, or explicit config/state environment assignment

The task's declared execution context is consistent with `CDQ-P\\CDQ-P`. The XML does not expose the complete environment block inherited by the eventual Node process.

## User and Machine environment evidence

Read-only PowerShell registry-backed inspection used `[Environment]::GetEnvironmentVariables('User')` and `'Machine'`, filtered for names matching `OpenClaw`, `Config`, `State`, or `Profile`.

- User environment for `CDQ-P`: no matching variables returned.
- Machine environment: no matching variables returned.
- Specifically absent from both inspected scopes: `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, and `OPENCLAW_PROFILE`.
- No environment values were changed.

This is the required “no environment override” result, not a claim that the historical process environment can be reconstructed from the process table.

## Supported OpenClaw diagnostics (fresh exact output)

OpenClaw `2026.7.1-2` returned:

```text
Config (cli): ~\\.openclaw\\openclaw.json
Config (service): ~\\.openclaw\\openclaw.json

Gateway: bind=loopback (127.0.0.1), port=18789 (service args)
Runtime: running (pid 27372, state Ready, last run 0, last run time 9/17/2026 5:13:48 AM, Gateway process detected for gateway port 18789.)
Connectivity probe: ok
Listening: 127.0.0.1:18789
```

`openclaw config file` returned:

```text
~\\.openclaw\\openclaw.json
```

`openclaw config get plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess --json` returned:

```text
true
```

The supported diagnostics expose no profile or alternate state directory for this invocation. They identify the current resolver result only; they do not prove the already-running process's historical in-memory object.

## Installed-source verification

The installed package was inspected read-only at:

`C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw`

Package version: `2026.7.1-2`.

Direct source evidence:

- `dist/paths-BMBAvkNf.js:108-114, 136-138, 176-178`: `OPENCLAW_CONFIG_PATH` overrides the config path; otherwise resolution uses the state directory/default path.
- `dist/config-utils-Cn9AD66v.js:65-70`: `OPENCLAW_STATE_DIR` overrides state directory; otherwise the default is the user's `.openclaw` state directory when present.
- `dist/help-DKv2oRp1.js:92`: `--profile <name>` is documented as a supported selector that isolates `OPENCLAW_STATE_DIR` and `OPENCLAW_CONFIG_PATH` under `~/.openclaw-<name>`; `--dev` is a separate built-in profile mode.
- `dist/dotenv-eb21SB3p.js:132-134, 151-158`: the environment loader's relevant OpenClaw names include `OPENCLAW_CONFIG_PATH`, `OPENCLAW_PROFILE`, and `OPENCLAW_STATE_DIR` (among other service/runtime variables).
- `dist/paths-BMBAvkNf.js` and `dist/config-utils-Cn9AD66v.js` also show the canonical fallback to the user's `.openclaw` directory and `openclaw.json`.

The installed source therefore confirms that the searched selectors are causally relevant to config/state/profile resolution. It does not show any discovered User/Machine value that would activate them.

## CNX-388 launch-chain comparison

CNX-388 established the chain:

`Scheduled Task → gateway.vbs → gateway.cmd → Node gateway`

The current process command remains the same Node gateway command and port. Current supported status identifies `gateway.cmd` as the service file and reports both CLI and service config as `~\\.openclaw\\openclaw.json`. The CNX-388 launcher assignments are service metadata/port values and do not include `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, `OPENCLAW_PROFILE`, `--config`, `--state-dir`, or a profile argument.

CNX-389 adds the missing read-only environment scopes: neither User nor Machine environment contains the relevant override names. The Scheduled Task principal is `CDQ-P\\CDQ-P` with `InteractiveToken`, consistent with the user environment scope inspected. On available OS evidence, those scopes could be inherited by the task-launched process, but no relevant value exists to redirect resolution.

## Alternate-source assessment

**Alternate source:** not found.

There is no direct evidence of an inherited OpenClaw config/state/profile override, and the supported resolver points to `C:\Users\CDQ-P\.openclaw\openclaw.json`. The result is therefore not “found value but inheritance unproven.” The remaining limitation is that Windows process inspection without debugger/inspector attachment does not expose the historical environment block of PID `27372`.

## Direct evidence versus inference

### Direct evidence

- Exact GitHub remote branch SHA and local checkout SHA match.
- PID, creation time, executable, command line, version, endpoint, and readiness were freshly read.
- Scheduled Task XML identifies `CDQ-P\\CDQ-P`, `InteractiveToken`, and `gateway.vbs`.
- User/Machine filtered environment inspection returned no relevant variables.
- Supported config/service diagnostics resolve to `~\\.openclaw\\openclaw.json`.
- Supported config lookup returned `true` for `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess`.
- Installed source directly documents the relevant environment and profile selectors.

### Inference and limits

- The matching User/Machine scopes and task principal make inheritance of a nonexistent override immaterial on the observed state.
- The evidence does not prove the historical process environment or historical in-memory `hookPolicy`.
- Supported resolver output does not prove the historical process consumed that exact config object.
- No hook acceptance, host warning absence, registry composition, or Dashboard/Ticket-first semantic outcome is inferred.

## Relation to CNX-385 through CNX-388

- **CNX-385:** normalization preservation remains closed and is not reopened; no contradictory fact was found.
- **CNX-386:** its effective-config provenance limitation remains valid, but the additional User/Machine environment-overrides hypothesis is not supported by this investigation.
- **CNX-387:** prior production hook-registration uncertainty remains; plugin-side registration evidence is not host acceptance evidence.
- **CNX-388:** the explicit Task/VBS/CMD/Node chain is re-correlated and strengthened by the absence of relevant User/Machine override variables. The environment evidence does not add an alternate source of material significance.

The in-memory production `hookPolicy` gap remains. This task does not prove that `allowConversationAccess=true` was present in the historical `registerTypedHook` input, nor that the host accepted the hook.

## Counts and hard-fence compliance

- Semantic/model/provider requests: `0`
- Dashboard requests: `0`
- Semantic request count for this task: `0`
- Production mutation count: `0`
- Gateway restart/reload: `0`
- Config mutation: `0`
- Environment mutation: `0`
- Scheduled Task mutation: `0`
- Dependency/source/artifact mutation: `0`
- Rebuild/deploy: `0`
- Debugger/inspector attachment: `0`
- Retry/semantic probe/permanent instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-388 edits: `0`
- Main/tags/releases changes: `0`
- Force-push/history rewrite: `0`
- CNX-390 created/started: `0`

Only read-only GitHub synchronization, OS process/environment/task inspection, supported OpenClaw diagnostics, and installed-source reads were performed.

## Remaining uncertainty

The exact inherited environment block of the already-running PID and the historical in-memory OpenClaw config/`hookPolicy` at registration time are not directly observable under the task's no-debugger/no-restart fences. This uncertainty does not identify an alternate source and does not establish host hook acceptance or Dashboard Ticket-first semantic success.

## Closeout

After publication, `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. No successor task was created or started.

Final remote HEAD and report blob are recorded in the execution closeout after the final fast-forward push and read-back.
