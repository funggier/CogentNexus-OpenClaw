# CNX-20260917-388 — Production Config Launch Provenance Correlation

## Classification

`PRODUCTION_CONFIG_LAUNCH_PROVENANCE_CORRELATED`

The read-only launch chain materially corroborates `C:\Users\CDQ-P\.openclaw\openclaw.json` as the configuration source selected for the production gateway startup. This is provenance correlation, not proof of the historical in-memory `hookPolicy` object or of hook acceptance.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting remote HEAD: `2a32ff6c5a6458ed3623aa6e6326307d5fb263e8`
- Starting local HEAD after fetch/re-anchor: `2a32ff6c5a6458ed3623aa6e6326307d5fb263e8`
- Task: `CNX-20260917-388`
- Starting coordination status: `READY_FOR_HERMES`

The remote branch was fetched and verified before investigation. Existing unrelated untracked files were preserved and not modified.

## Live gateway re-correlation

Read-only `openclaw gateway status`, `openclaw plugins list --json`, and process inspection produced:

| Item | Evidence |
|---|---|
| PID | `27372` |
| Creation time | `2026-09-17 05:13:48.606 +07:00` (`CreationDate=1789596828606`)
| Command line | `"C:\\Program Files\\nodejs\\node.exe" C:\\Users\\CDQ-P\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js gateway --port 18789` |
| OpenClaw | `2026.7.1-2 (0790d9f)`; gateway and CLI agree |
| Node runtime | `24.18.0` |
| Endpoint | `127.0.0.1:18789`; loopback connectivity probe `ok` |
| State | `running`, `Ready` |
| Loaded artifact | `C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js` |
| Plugin inventory | `status=loaded`, `enabled=true`, `hookCount=0`, `hookNames=[]` |

No lifecycle action was issued.

## Scheduled Task and launcher chain

Direct read-only Scheduled Task XML for `\\OpenClaw Gateway`:

- task exists, state `Ready`, logon trigger for `CDQ-P\\CDQ-P`;
- action is `C:\\Users\\CDQ-P\\.openclaw\\gateway.vbs`;
- no action arguments, working directory, profile selector, `OPENCLAW_CONFIG_PATH`, or `OPENCLAW_STATE_DIR` assignment appears in the task XML;
- task description/version is `OpenClaw Gateway (v2026.7.1-2)`.

`C:\\Users\\CDQ-P\\.openclaw\\gateway.vbs` directly runs:

```text
CreateObject("WScript.Shell").Run """C:\Users\CDQ-P\.openclaw\gateway.cmd""", 0, False
```

`C:\\Users\\CDQ-P\\.openclaw\\gateway.cmd` contains:

```text
set "TMPDIR=C:\Users\CDQ-P\AppData\Local\Temp"
set "OPENCLAW_GATEWAY_PORT=18789"
set "OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service"
set "OPENCLAW_WINDOWS_TASK_NAME=OpenClaw Gateway"
set "OPENCLAW_WINDOWS_TASK_HIDDEN_LAUNCHER=1"
set "OPENCLAW_SERVICE_MARKER=openclaw"
set "OPENCLAW_SERVICE_KIND=gateway"
set "OPENCLAW_SERVICE_VERSION=2026.7.1-2"
"C:\Program Files\nodejs\node.exe" C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789
```

The launcher sets the gateway port and service metadata only. It does not set `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, a profile, or an alternate state/config selector. The process command line independently matches the final Node command and port in `gateway.cmd`.

## Environment, profile, and supported path diagnostics

- `openclaw gateway status` reported both `Config (cli)` and `Config (service)` as `~\\.openclaw\\openclaw.json`.
- `openclaw config file` is the supported config-file diagnostic; its effective path corresponds to `C:\\Users\\CDQ-P\\.openclaw\\openclaw.json`.
- `openclaw config get plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess` returned `true`.
- No `OPENCLAW_CONFIG_PATH` or `OPENCLAW_STATE_DIR` assignment was found in the inspected launcher/task or current process-relevant shell environment.
- No profile selector is present in the task, VBS launcher, CMD launcher, or process command line.
- The process command has no `--config`, `--state-dir`, or profile argument.

These facts show a single, unoverridden launch path consistent with the supported resolver result; they do not reconstruct historical process environment variables that are not recorded by the process command line.

## Config file evidence

File inspected read-only: `C:\\Users\\CDQ-P\\.openclaw\\openclaw.json`

- Existence: present
- Size: `5541` bytes
- Last write: `2026-09-16 20:07:13.672224500 +0700`
- SHA-256: `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`
- Relevant value: `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess = true`

The config was last written approximately 9 hours 6 minutes 34.934 seconds before PID `27372` creation (using the observed timestamps). Thus it existed and was older than the current gateway start. This removes a temporal mismatch class only; it does not prove the process loaded that exact byte sequence.

## Startup-log correlation

Log: `C:\\Users\\CDQ-P\\AppData\\Local\\Temp\\openclaw\\openclaw-2026-09-17.log`

The PID-correlated startup window contains:

- `05:13:53.895 +07:00` — `loading configuration…`
- `05:13:54.991` — `starting...`
- `05:13:56.541` — discovery lists `cogentnexus-openclaw` at the same effective extension path;
- `05:13:58.242` — plugin-side `hook-registered`, `registrationCount=1`;
- `05:13:59.061` — HTTP server listening, including `cogentnexus-openclaw`;
- `05:14:00.265` — `gateway ready`;
- `05:14:10.383` — later plugin discovery/pre-warm;
- `05:14:10.542` — second plugin-side `hook-registered` event.

The log records configuration loading and the expected plugin startup sequence, but does not record the resolved config path, state/profile selector, or the host-side `registerTypedHook` policy input. The known host rejection diagnostic was not observed. Plugin-side `hook-registered` is not treated as host acceptance evidence.

## Alternate config/profile/state search

The inspected `C:\\Users\\CDQ-P\\.openclaw` tree contains the active `openclaw.json`, three dated `openclaw.before-*.json` snapshots, and a `state` directory. The dated snapshots are historical alternate files, not selected by the task, VBS, CMD, process command, or supported service diagnostic. No active `profiles` directory or separate active state/config selector was found in the directly relevant launch path. The tree also contains plugin/package metadata and unrelated JSON files; these are not OpenClaw config candidates for this gateway.

Absence of alternate-path evidence is not proof that an alternate path never existed. It means no materially plausible alternate source was found in the inspected live launch configuration and supported diagnostics.

## Direct evidence versus inference

### Direct evidence

- Exact remote/local starting HEAD and `READY_FOR_HERMES` state were verified.
- PID, creation time, command line, endpoint, readiness, and OpenClaw version were read from current runtime diagnostics/process inspection.
- Scheduled Task XML, VBS launcher, and CMD launcher were read without mutation.
- The launch chain terminates in the same Node gateway command and port reported by `gateway status`.
- No explicit config/state/profile override was present in the inspected launch chain or command line.
- Supported diagnostics reported `~\\.openclaw\\openclaw.json` for CLI and service.
- The file exists, its timestamp and SHA-256 were freshly read, and the relevant value is `true`.
- The startup log contains the configuration-loading event and PID-correlated plugin/startup sequence.

### Inference supported by the chain

The unoverridden Scheduled Task → VBS → CMD → Node launch path, matching process command, supported service/CLI path, pre-existing config file, and startup sequence materially corroborate that `C:\\Users\\CDQ-P\\.openclaw\\openclaw.json` was the intended and selected configuration source at startup.

### Claims not made

- No claim that production in-memory `hookPolicy.allowConversationAccess` was `true`.
- No claim that the host gate accepted `before_agent_run`.
- No claim that `hookCount=0` is caused by gate rejection or registry composition.
- No claim of Dashboard Ticket-first semantic success.

## Relation to CNX-385 / CNX-386 / CNX-387

- **CNX-385:** normalization preservation remains closed and is not reopened or contradicted.
- **CNX-386:** this task strengthens launch/config provenance beyond the prior resolver/file evidence and closes the materially plausible alternate-launch-path question for the inspected path, but does not close the in-memory consumption gap.
- **CNX-387:** the same live gateway remains loaded/ready with `hookCount=0`, `hookNames=[]`; startup logs still provide plugin-side events but no authoritative host registration result. CNX-387's unresolved host-gate outcome remains unresolved.

The production in-memory hook-policy gap therefore **remains**.

## Hard-fence compliance

| Fence | Count/result |
|---|---:|
| Semantic/model/provider requests | `0` |
| Dashboard requests | `0` |
| Production mutation count | `0` |
| Gateway restart/reload | `0` |
| Production config mutation | `0` |
| Installed dependency mutation/patch | `0` |
| CogentNexus source mutation/repair | `0` |
| Artifact rebuild/deploy | `0` |
| Debugger/inspector | `0` |
| TicketStore/admission/routing/auth changes | `0` |
| Retry/second semantic probe | `0` |
| Permanent instrumentation | `0` |
| Historical CNX-360 through CNX-387 edits | `0` |
| Release/tag/main changes | `0` |
| Force-push/history rewrite | `0` |
| CNX-389 created/started | `0` |

## Remaining uncertainty

The launch provenance is materially correlated, but a non-invasive observation cannot prove that PID `27372` consumed the exact historical bytes or expose the in-memory `hookPolicy` argument at registration. File timestamp precedence, resolver output, and launcher correlation are not equivalent to direct memory observation. The production hook-policy/host-registry outcome remains an independent unresolved boundary.

## Closeout

After publication, `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. No successor task is created or started.
