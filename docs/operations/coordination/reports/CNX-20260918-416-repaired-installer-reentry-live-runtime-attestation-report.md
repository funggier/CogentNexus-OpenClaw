# CNX-20260918-416 — Repaired Installer Re-entry and Live Runtime Attestation Report

## Final classification

`PASS_REPAIRED_INSTALL_RUNTIME_ATTESTATION_PRESENT`

The exact candidate ownership classifier proved a coherent non-fresh upgrade shape with no pending rollover. One installer invocation completed with exit `0`, production converged naturally, and the single authorized runtime-attestation RPC returned `PRESENT`.

## Fresh GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting remote/local HEAD: `d5f6d3cdb7e5019f597618688d2267f00ac091d0`
- ACTIVE, STATUS, and task: `READY_FOR_HERMES`, `CNX-20260918-416`
- Exact product/source candidate: `c1baa815d6894f0d619d4d3695c61a442e206e38`
- Candidate ancestry: PASS; candidate is an ancestor of the starting remote HEAD.
- Candidate-to-HEAD drift: coordination task/report/review files plus two test files only. No product source, plugin source, skill source, or installer-script drift was present.

## Exact candidate binding

- Disposable checkout: `C:\Users\CDQ-P\.hermes\workspace\cnx416-candidate-c1baa815`
- HEAD: exact candidate, detached and clean before execution; clean again after execution.
- Version: `0.9.5`
- `scripts/install.ps1` SHA-256: `169e14e9382887c144cad5c50e43ec89999b2432dfe91a64955f89c8d2438453`
- Candidate plugin fingerprint after candidate `npm ci` and `plugin:validate`: `fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c`

## Read-only production preflight

Captured at `2026-09-18T08:44:24Z` through the supported OpenClaw/CNX surfaces and SQLite URI `mode=ro`:

- OpenClaw CLI/Gateway: `2026.7.1-2`
- Gateway: healthy/reachable, PID `26416`, port `18789`, Scheduled Task `Ready`, RPC connection healthy
- Controller: `cnxMode=disabled`, derived `mode=passthrough`, generation `106`, desired Gateway `running`
- Supervisor read-only tick: `healthy`, maintenance `null`, `executeSafe=false`, no recoveries; Gateway and Ollama healthy
- Plugin inventory: one `cogentnexus-openclaw` record, version `0.9.5`, canonical direct root/source, `enabled=false`, `status=disabled`
- Installed release entry SHA-256 before install: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Installed `host_v091.py` SHA-256: `99906331ab7e406ea6c6b4b2f493902a904dff8a50e8d79272fcbaca8a698d23`
- Maintenance marker: absent
- Recovery fence: READY/PASS; no active maintenance marker and no active provider incident
- Delivery fence: READY/PASS; pending outbox `0`
- SQLite integrity: `ok`
- Durable counts: tickets `23`, ticket events `864`, outbox rows `0`, assistant deliveries `14`, direct model calls `20`, direct recoveries `5`, sessions `58`, context-maintenance rows `0`
- Ticket states: accepted `3`, cancelled `4`, completed `16`; read-only supervisor found no actionable recovery/delivery work
- Provider/model routing: `ollama/qwen3.8:27b`, unchanged from the accepted predecessor state
- Relevant process inventory: Gateway PID `26416` plus the bounded observer itself; no existing installer, rollover, or lifecycle mutation process
- Ownership/staging inventory was retained read-only. Historical committed rollover records existed, but the exact classifier below proved `pendingRollover=false` and coherent ownership.

The legacy CNX `check system` aggregate was `NOT_READY` only because its retired provider-selection view reports multiple installed providers with no CNX-owned selection. Its OpenClaw model-routing check independently passed with `ollama/qwen3.8:27b`; Gateway, maintenance, provider-incident, ticket-store, and delivery checks all passed. No provider/model mutation was made.

## Exact ownership/re-entry classification

Live inventory was captured once to:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260918-416\plugins-list.json`

Exact command shape:

```text
python <candidate>\skills\cogentnexus-openclaw\scripts\namespace_ownership.py classify-install --workspace C:\Users\CDQ-P\.openclaw\workspace --app-data C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw --plugin-inventory-json <captured inventory> --expected-replacement-fingerprint fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c
```

Exit code: `0`. Exact non-secret result:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": false,
  "manifestPluginPath": "c:\\users\\cdq-p\\.openclaw\\extensions\\cogentnexus-openclaw",
  "replacementPluginPath": null,
  "expectedReplacementFingerprint": "fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c",
  "new": [
    "launcherWindows=C:\\Users\\CDQ-P\\.openclaw\\workspace\\cnxclaw.cmd",
    "skill=C:\\Users\\CDQ-P\\.openclaw\\workspace\\skills\\cogentnexus-openclaw",
    "state=C:\\Users\\CDQ-P\\.openclaw\\workspace\\.cogentnexus-openclaw",
    "applicationData=C:\\Users\\CDQ-P\\AppData\\Local\\CogentNexus-OpenClaw",
    "directPlugin=C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw"
  ],
  "legacy": []
}
```

This proved supported upgrade re-entry, no pending rollover, no mixed/foreign/legacy ownership, and no unresolved transaction requiring recovery. No transaction or ownership file was manually changed.

## One-shot installer and observer ledger

Exact invocation from the detached candidate:

```text
scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace
```

- Retained wrapper PID: `20268`
- Installer PID: `22516`
- Start: `2026-09-18T08:50:00.7180076+00:00`
- End: `2026-09-18T09:00:58.0443492+00:00`
- Duration: approximately 657 seconds
- Terminal installer exit code: `0`
- Installer invocation/start count: `1`
- Retry count: `0`
- Observer fuse: at least 1200 seconds; the interactive observer timed out once without killing or relaunching, then continued observing the same retained process to terminal completion
- Stdout SHA-256 / bytes: `ae09034aaea5271fd60dd9b98f42b316bf698632827d67962b809baaefdefee6` / `21580`
- Stderr SHA-256 / bytes: `ea76e83847b0ed0aa99d9dd5121d2ca4f786781a9d60ebc1b3aa7a8809bec4da` / `116`
- Runner-result SHA-256 / bytes: `12242927fec5588a3e43fd25aed7793f95ffadf844b1c81b3c78fd8e95e16f80` / `724`

The only retained stderr was the expected OpenClaw warning that plugin configuration existed while the plugin was still disabled during the install transition.

### Ticket DB bootstrap acceptance

The retained stdout contains:

```text
CNXCLAW_INSTALL_STAGE_START stage=ticket-db-bootstrap utc=2026-09-18T08:51:27.3390435+00:00
{"result":"ok", ... "pendingOutbox":0, "linkedRunning":0}
CNXCLAW_INSTALL_STAGE_COMPLETE stage=ticket-db-bootstrap utc=2026-09-18T08:51:27.4373430+00:00 elapsed_ms=97 exit_code=0
```

No SQLite `ExperimentalWarning` was emitted in this run. The repaired native boundary preserved the child result and exact native exit `0`; PowerShell did not terminate at the stage. All subsequent recorded stages completed with exit `0`, including package, rollover preparation, local package install, post-install disable, rollover finalize, and owned-runtime ensure. The transcript ended with `CogentNexus-OpenClaw v0.9.5 installation completed successfully.`

## Natural convergence and installed identity

No manual plugin, Gateway, or lifecycle repair occurred after installer execution.

- Installed plugin: canonical direct root, version `0.9.5`, `enabled=true`, `status=loaded`
- Installed plugin fingerprint: exact candidate `fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c`
- Post-install exact classifier: exit `0`, `mode=upgrade`, `pendingRollover=false`, `pluginAlreadyExact=true`, canonical replacement path, `legacy=[]`
- Candidate/installed release entry SHA-256: `343c221db6d9259fb38bb335cf5f3293bb838a7515a909666471b990da056f4b`
- Candidate/installed runtime-attestation module SHA-256: `90d3d95064f1a11b483ce0725dc5782cbaf7fdb6533f1f8b5f443c3da3f33a1d`
- Candidate/installed `host_v091.py` SHA-256: `99906331ab7e406ea6c6b4b2f493902a904dff8a50e8d79272fcbaca8a698d23`
- Runtime-attestation module registers `cogentnexus.runtimeAttestation` with scope `operator.read`; the live RPC was available to the one-shot authorized call below
- OpenClaw remained `2026.7.1-2`
- Controller naturally converged to `cnxMode=active`, derived `mode=managed`, generation `107`
- Supervisor Scheduled Task: installed, enabled, `Ready`, last result `0`
- Gateway: healthy/reachable, new installer-owned PID `13192`, port `18789`, Scheduled Task `Ready`
- Maintenance marker: absent
- Recovery/provider-incident checks: PASS; `incidentOpen=false`
- Delivery/outbox: PASS; pending `0`
- SQLite integrity: `ok`
- Durable counts and ticket-state counts: unchanged from preflight
- Provider/model: unchanged at `ollama/qwen3.8:27b`
- Duplicate/foreign CNX root or generation: none; exact post-install classifier returned one canonical direct plugin and `legacy=[]`

## One-shot runtime attestation

Exact command, invoked once with no retry:

```text
openclaw gateway call cogentnexus.runtimeAttestation --params '{}' --json
```

Exit code: `0`. Exact response:

```json
{
  "schemaVersion": 1,
  "pluginId": "cogentnexus-openclaw",
  "hookName": "before_agent_run",
  "runnerReady": true,
  "globalHookCount": 7,
  "latestRegistryPluginHookCount": 7,
  "classification": "PRESENT"
}
```

Attestation call count: `1`. Attestation retry count: `0`.

## Hard-fence accounting

| Action | Count |
|---|---:|
| Web Chat semantic submissions | 0 |
| Ollama semantic/model requests | 0 |
| OpenAI semantic/model requests | 0 |
| Any provider/model semantic request | 0 |
| Provider/model selection mutations | 0 |
| Provider credential/auth mutations | 0 |
| Manual maintenance-marker mutations | 0 |
| Manual Ticket/outbox/recovery/SQLite mutations | 0 |
| Manual replay/delivery | 0 |
| Manual plugin enable/disable/copy/remove | 0 |
| Installer starts | 1 |
| Installer retries | 0 |
| Manual Gateway repair after installer | 0 |
| Manual lifecycle repair after installer | 0 |
| Attestation RPC calls | 1 |
| Attestation retries | 0 |
| OpenClaw dependency patches/version changes | 0 |
| Release/tag/main operations | 0 |
| Force pushes/history rewrites | 0 |
| CNX-417 creation/start | 0 |

## Final classification

`PASS_REPAIRED_INSTALL_RUNTIME_ATTESTATION_PRESENT`

The authorized one-shot installer and one-shot read-only runtime attestation are complete. No semantic/model/provider request was sent. Stop for ChatGPT review; do not create or start CNX-417.
