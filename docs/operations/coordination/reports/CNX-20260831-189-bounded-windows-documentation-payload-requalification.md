# CNX-20260831-189 — Bounded Windows Documentation-Payload Requalification

- **Disposition:** `WAITING_HUMAN_SEMANTIC_SEND`
- **Date:** 2026-08-31 ICT
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Working branch:** `agent/v0.9.3-full-stabilization`
- **Parent:** `CNX-20260831-188`
- **Executor:** Hermes on the accepted Windows host
- **Evidence root:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx189-evidence-20260831T101500Z`

## Scope and exact candidate

Task-189 was executed as the bounded subtask of Task-188. The exact immutable product candidate used for acquisition and installation was:

`604569c286e930f1a596362ab926b065b56d486e`

Candidate identity recorded from the isolated checkout:

- version: `0.9.3`
- package payload-v2: `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / `184` files
- installed skill-tree Git tree: `a1e873ba404205507a1623961b49f1b1a0689f9f`
- executable scripts-tree Git tree: `3d9d323ba19443d46e970b87cef52ce878da274f`
- accepted facade Git blob: `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- accepted facade SHA-256: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Repository CI/package gates were already recorded by the live coordination authority as PASS: Validate `33382417045`, Windows Installer Pack Smoke `33382417032`, PS5.1 Acceptance Smoke `33382417028`, and package-proof artifact `9754267508`.

## Phase A — read-only preflight

Preflight was collected before mutation. The host/runtime baseline was:

- Windows host identity: recorded in `a01-host.json`
- OpenClaw: `2026.7.1-2 (0790d9f)`
- CNX mode: `managed`
- selected/managed provider: `ollama`
- Gateway: healthy before installation; loopback Dashboard on `127.0.0.1:18789`
- Ollama: reachable, healthy, ready; inventory count `4`
- active facade: `C:/Users/CDQ-P/.openclaw/workspace/skills/cogentnexus-openclaw/scripts/cnxclaw.py`; SHA-256 `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`
- delivery preflight: `READY`, pending outbox `0`, read-only, no state change
- recovery preflight: no maintenance marker, no active Ollama incident, recovery attempts `0`
- SQLite integrity: `ok`

The pre-install durable baseline was:

| Surface | Count |
|---|---:|
| `tickets` | 5 |
| `ticket_events` | 43 |
| `ticket_outbox` | 0 |
| `cnx_assistant_delivery` | 4 |
| `cnx_direct_model_call` | 5 |
| `cnx_direct_recovery` | 0 |
| `cnx_sessions` | 13 |

This was the preserved historical state from prior accepted lifecycle/semantic work; Task-189 did not require a zero baseline.

The pre-install unrelated plugin inventory contained `71` entries with normalized unrelated-surface SHA-256 `8d58154632fff0eb998af72dce688326d055707d76e7a4fba464d8f63bd53752`. The CNX plugin was present, version `0.9.3`, enabled and loaded.

## Phase B — exact source acquisition

An isolated temporary checkout was used at:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx-live-task189-20260831T100000Z`

Before installation, the checkout was detached at exactly `604569c286e930f1a596362ab926b065b56d486e`. No moving branch tip, main branch, release archive, or alternate candidate was substituted.

## Phase C — exactly one supported install-over

One normal supported source/development-candidate install-over was executed from the exact checkout using the repository installer:

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/AppData/Local/Temp/cnx189-evidence-20260831T101500Z/run-installer189.ps1
```

The wrapper invoked the documented candidate installer once with the target workspace. Invocation evidence: `b00-installer.invocation.json`.

Result:

- invocation count: `1`
- installer exit code: `0`
- duration: approximately `818.99s`
- success message: `CogentNexus-OpenClaw v0.9.3 installation completed successfully.`
- all installer stage start/complete pairs passed with exit `0`
- longest stage: `plugin-rollover-prepare`, approximately `430.3s`

No reset, uninstall, fresh reinstall, state deletion, provider replacement, source edit, test edit, dependency edit, workflow edit, release action, or force push was performed.

## Phase D — provenance, health, and byte proof

After install-over, the changed documentation surfaces were byte-identical between candidate source and active installed surfaces:

| Changed file | Candidate SHA-256 | Installed SHA-256 | Result |
|---|---|---|---|
| `plugins/cogentnexus-openclaw/README.md` | `3fb9eba088693e51c951048c82168c83fa6de050674fd6491a757fc4ededbbfc` | `3fb9eba088693e51c951048c82168c83fa6de050674fd6491a757fc4ededbbfc` | PASS |
| `skills/cogentnexus-openclaw/SKILL.md` | `8e57c7f9649cbdfb6bf99837e27483cf07ffa4f01805826556a334377edb01d3` | `8e57c7f9649cbdfb6bf99837e27483cf07ffa4f01805826556a334377edb01d3` | PASS |
| `skills/cogentnexus-openclaw/references/architecture.md` | `4fec76f5bf38116f5df39563d80f89e3e636c1a3a4144b6aee714d20f3c1aa2f` | `4fec76f5bf38116f5df39563d80f89e3e636c1a3a4144b6aee714d20f3c1aa2f` | PASS |
| `skills/cogentnexus-openclaw/references/scheduler-adapters.md` | `717166769ac591b1693e44a1c7bdc847833b39f5939e187158df18c3d2bfb2cf` | `717166769ac591b1693e44a1c7bdc847833b39f5939e187158df18c3d2bfb2cf` | PASS |

The active executable facade remained byte-identical:

- path: `C:/Users/CDQ-P/.openclaw/workspace/skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- bytes: `17425`
- SHA-256: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Post-install runtime evidence:

- OpenClaw: `2026.7.1-2 (0790d9f)`
- CNX mode: `managed`
- selected provider: `ollama`
- provider transition: `null`
- Gateway: healthy, connectivity probe `ok`, listening on `127.0.0.1:18789`
- Ollama: reachable, healthy, ready; model inventory count `4`
- delivery: `READY`, pending outbox `0`, read-only and state unchanged
- SQLite integrity: `ok`
- durable counts remained exactly `5 / 43 / 0 / 4 / 5 / 0 / 13` for the surfaces listed in the preflight table

The post-install CNX plugin was version `0.9.3`, enabled and loaded. Its post-install supported identity fingerprint was:

`d06f4db6c8ad924829545e5059a6d3e362064cb9d92063220eb74a7cc751269f`

The change from the historical fingerprint `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19` is expected because the live plugin identity domain includes the corrected plugin README. It is not the repository package payload-v2 fingerprint.

Unrelated plugin inventory preservation was checked before and after installation; the pre-install normalized unrelated inventory contained `71` entries and SHA-256 `8d58154632fff0eb998af72dce688326d055707d76e7a4fba464d8f63bd53752`.

## Phase E — human semantic boundary

The required remaining acceptance shape is:

`1 human Send -> 1 Ticket -> 1 session/run -> 1 Ollama model call -> 1 durable assistant delivery -> 1 logical Dashboard assistant result`

This Hermes/ChatGPT session does not expose the genuinely human Dashboard Send connector required by the live Task-189 transport gate. Therefore Hermes did not type/send a semantic message, did not press Enter as Send, did not invoke `chat.inject`, did not retry, and did not invoke recovery/regeneration.

Exact one-message boundary for the human UI actor after review:

```text
ตอบกลับข้อความนี้เพียงว่า CNX189-<UTC timestamp>-<short random suffix>
```

The nonce must be generated immediately before the single human Dashboard Send. The prompt must remain a direct-lane echo/acknowledgement prompt and must not include durable-contract keywords, file operations, tests, research, or tool actions. No second Send or retry is authorized by this report.

Because the human semantic turn was not performed, there is no Task-189 Ticket/session/model-call/delivery/Dashboard result to claim. The report disposition is therefore `WAITING_HUMAN_SEMANTIC_SEND`, not PASS.

## Anomalies and impact

1. **Initial preflight script syntax defect:** the first generated PowerShell preflight contained an invalid empty pipeline element and exited before probes ran. It was corrected as a local evidence-script issue; no product or runtime mutation occurred.
2. **Initial entrypoint discovery defect:** the first probe searched the extension tree for the OpenClaw entrypoint and found none. The supported entrypoint from live status was then used: `C:/Users/CDQ-P/AppData/Roaming/npm/node_modules/openclaw/dist/index.js`. Version verification passed; no product effect.
3. **Evidence filename assumption:** initial read attempts used non-existent unprefixed artifact names. The actual phase-prefixed artifacts were located through the evidence inventory. No product effect.
4. **Gateway warm-up after installer lifecycle:** the first post-install recovery snapshot was `READY_WITH_WARNINGS` because the installer-managed Gateway process was running while port `18789` temporarily returned `ECONNREFUSED`. No manual restart or recovery was issued. After a read-only wait, Gateway reached healthy/`Connectivity probe: ok` and the port was listening; Ollama remained healthy throughout.
5. **Installer warnings:** npm deprecation and `allow-scripts` warnings were present. Installer exit code and all stage results were `0`; provenance, docs byte proof, runtime health, and durable preservation passed. No dependency/product change was made.
6. **Transport boundary:** no genuine human Dashboard Send connector is exposed in this session. This is the sole remaining acceptance boundary and is the reason for the disposition.

## Stop/fence statement

Task-189 performed exactly one supported exact-candidate install-over and stopped before semantic simulation because the human Send boundary was unavailable. Reset, uninstall, and fresh reinstall were not performed. No release PR, merge, tag, GitHub Release, Release workflow dispatch, or force push was performed from Task-189.

Hermes must stop after publishing this report for ChatGPT review.
