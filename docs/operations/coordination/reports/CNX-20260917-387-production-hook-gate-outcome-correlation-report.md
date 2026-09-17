# CNX-20260917-387 — Production Hook-Gate Outcome Correlation

## Classification

`PRODUCTION_HOOK_REGISTRATION_OUTCOME_UNRESOLVED`

The read-only production boundary does not expose a correlated host acceptance/rejection result. The exact host policy diagnostic was absent from the inspected log, but absence is not evidence that the gate passed. The plugin-side `hook-registered` events are not proof that `registerTypedHook` inserted `before_agent_run`. The supported inventory reports no CogentNexus hooks, which is a downstream symptom only.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting HEAD: `7280ee25a050cc3389c4ae068102d4ffbdf6257f`
- Final remote/publication HEAD: `5f7252e1416324bb5d7fa2c03c9b53f3d0cb235c`
- Starting status: `READY_FOR_HERMES`
- Task: `CNX-20260917-387`

The authoritative branch was fetched and local HEAD was re-anchored to the supplied HEAD before investigation. Existing untracked files were not modified.

## Live runtime correlation

Read-only supported diagnostics and process inspection correlated the current runtime as follows:

| Item | Evidence |
|---|---|
| Gateway PID | `27372` |
| Process start | `2026-09-17 05:13:48.606 +07:00` (`CreationDate=20260917051348.606053+420`) |
| Process command | `"C:\Program Files\nodejs\node.exe" C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789` |
| OpenClaw | CLI/gateway `2026.7.1-2 (0790d9f)` |
| Runtime | Node `24.18.0` (also recorded in gateway log metadata) |
| Endpoint | `127.0.0.1:18789`, loopback, connectivity probe `ok` |
| Gateway state | `running`, `Ready` |
| Last-run time | `9/17/2026 5:13:48 AM` |
| Effective artifact | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` |
| Artifact SHA-256 | `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95` |

The service and CLI both report `~\.openclaw\openclaw.json` as the configuration path. This does not prove the historical in-memory value at registration time, consistent with CNX-386.

## Exact production log

`C:\Users\CDQ-P\AppData\Local\Temp\openclaw\openclaw-2026-09-17.log`

The gateway itself records this path at `2026-09-17T05:14:00.813+07:00` in the same startup log family.

## Startup and registration window

The process-correlated startup window is:

| Timestamp (+07:00) | Event |
|---|---|
| `05:13:53.895` | `loading configuration…` |
| `05:13:54.991` | `starting...` |
| `05:13:56.541` | plugin discovery lists `cogentnexus-openclaw` at the exact effective artifact path |
| `05:13:58.229` | CogentNexus suppressed legacy `after_compaction` synthetic continuation registration |
| `05:13:58.242` | plugin-side `delivery-observe {"event":"hook-registered","registrationCount":1,"hasReplyDispatch":true,"hasReplyPayloadSending":true}` |
| `05:13:59.061` | HTTP server listening; 12 plugins including `cogentnexus-openclaw`; `3.9s` |
| `05:14:00.167` | CogentNexus pre-runtime fence |
| `05:14:00.179` | CogentNexus crash-start recovery |
| `05:14:00.260` | CogentNexus context pre-start fence |
| `05:14:00.265` | `gateway ready` |
| `05:14:10.383` | later plugin discovery/pre-warm cycle begins |
| `05:14:10.542` | later plugin-side `hook-registered`, `registrationCount`: `2` |

The log also contains earlier same-day startup cycles at `01:20:43`–`01:20:53`; the PID creation time identifies the `05:13:53` cycle as the current gateway's startup window.

### Host policy diagnostic search

Exact searched string:

`typed hook "before_agent_run" blocked because non-bundled plugins must set plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`

Result: **absent** from the inspected production log, including the PID-correlated registration window and the earlier same-day cycles. No timestamp or surrounding line exists for this diagnostic.

Other host diagnostics separating typed-hook acceptance from registry composition were also not observed in the relevant window. The nearby lifecycle evidence is discovery → plugin-side startup/registration event → server listening → readiness, but there is no host-side registration-attempt result.

## Supported plugin inventory

Read-only `openclaw plugins list --json` was run against the live CLI/runtime. The `cogentnexus-openclaw` record was:

```json
{
  "id": "cogentnexus-openclaw",
  "source": "C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js",
  "rootDir": "C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw",
  "origin": "global",
  "status": "loaded",
  "enabled": true,
  "hookCount": 0,
  "hookNames": [],
  "toolNames": []
}
```

The inventory path is consistent with the effective artifact and reports the plugin loaded/enabled, but no visible hooks. `hookCount=0` and `hookNames=[]` do not identify whether the host gate rejected registration or whether a later registry view excluded it.

## Direct evidence versus inference

### Direct evidence

- PID `27372`, process command, start time, endpoint, version, and readiness were read-only correlated.
- The effective artifact path was present in plugin discovery and inventory.
- The effective artifact SHA-256 was freshly computed as stated above.
- The exact production log path was reported by `openclaw gateway status` and recorded by the gateway.
- The exact host policy rejection diagnostic was not present in the inspected log.
- CogentNexus emitted plugin-side `hook-registered` events at `05:13:58.242` and `05:14:10.542`.
- Supported inventory reports `status=loaded`, `hookCount=0`, and `hookNames=[]`.
- Gateway readiness was recorded at `05:14:00.265`.

### Inference not permitted by this evidence

- No gate pass is claimed from warning absence.
- No gate rejection is claimed without the host diagnostic.
- No registry-composition failure is claimed because the evidence does not establish accepted host insertion before any downstream loss.
- The plugin-side `hook-registered` event is not treated as proof that `registerTypedHook` accepted the hook.
- The current config file/path and CNX-385 normalization proof are not treated as proof of the live gateway's historical in-memory gate input.

## Relation to predecessor evidence

### CNX-385

CNX-385 proved that normalization preserves `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true` through the normalized entry and `hookPolicy` path. This task did not reopen normalization and found no production fact contradicting it.

### CNX-386

CNX-386 established that the current config file contains the value and that supported resolution points to that file, while the running gateway's historical in-memory config at registration time remained unobserved. The present log correlation does not close that provenance gap: no host log records the effective `policy?.allowConversationAccess` input.

### CNX-376 / CNX-378 / CNX-380–382

Those reports establish the prior inventory symptom and isolated/source boundaries. They do not substitute for the missing production host-side acceptance event. In particular, plugin-side registration events remain weaker than host registry insertion evidence.

## Registry-composition investigation

A registry-composition investigation remains **justified as an unresolved hypothesis**, but it is not established by CNX-387. The current evidence cannot distinguish composition loss from gate rejection. The first missing observable is the host-side result at `registerTypedHook` (or an equivalent non-invasive production diagnostic that records accepted/rejected registration and its policy input).

## Hard-fence compliance

| Fence | Count/result |
|---|---:|
| Semantic/model/provider requests | `0` |
| Production mutation count | `0` |
| Gateway restart/reload | `0` |
| Production config mutation | `0` |
| OpenClaw dependency patch | `0` |
| CogentNexus source/artifact mutation | `0` |
| Artifact rebuild/deploy | `0` |
| Dashboard request | `0` |
| TicketStore/admission/routing/auth changes | `0` |
| Debugger/inspector attachment | `0` |
| Historical CNX-360 through CNX-386 edits | `0` |
| Main/tags/releases changes | `0` |
| Force-push/history rewrite | `0` |
| CNX-388 created/started | `0` |

Only read-only supported status/inventory commands, process inspection, artifact hashing, and log reads were used for production correlation. No semantic probe or retry was sent.

## Remaining uncertainty

The observable production boundary ends after plugin-side startup/registration logging and supported inventory projection. It does not expose the exact `registerTypedHook` policy argument, whether the host gate accepted `before_agent_run`, the host registry receiving the mutation, or the registry composition inputs. Therefore the required classification remains:

`PRODUCTION_HOOK_REGISTRATION_OUTCOME_UNRESOLVED`

## Closeout

The report was published at the final remote/publication HEAD above, and `ACTIVE.md` and `STATUS.md` were set to `WAITING_FOR_CHATGPT_REVIEW`. No successor task was created or started.
