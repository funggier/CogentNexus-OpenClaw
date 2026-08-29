# CNX-20260829-139 — Repaired Candidate Install-Over and Health Proof

- **Task:** CNX-20260829-139
- **Verdict:** `FAIL_INSTALL_OVER`
- **Execution mode:** supported install-over/update and read-only provenance/health proof only
- **Operator/executor:** ChatGPT / Hermes
- **Started (UTC):** 2026-08-29T11:10:29Z
- **Install attempt observed (UTC):** 2026-08-29T11:25:43Z–2026-08-29T11:25:44Z
- **Report prepared (UTC):** 2026-08-29T11:27:12Z
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Fresh starting HEAD:** `d23e69d21f49347a83d90b70b83c72f2e961e5b6`
- **Exact repaired candidate:** `16f5c396e9be0af8d1bd34824fe2993613501a6f`

## 1. Authority and scope

A fresh clone was created from `https://github.com/funggier/CogentNexus-OpenClaw.git` on branch `agent/v0.9.3-full-stabilization` at 2026-08-29T11:10:29Z. Fresh `ACTIVE.md`, `STATUS.md`, Task 139, Task-138 report, and Task-138 review were inspected. `ACTIVE.md` identified `CNX-20260829-139` as the active task and the task was not superseded.

Task 139 authorizes one supported install-over of the currently installed payload, exact-candidate build/package provenance, and read-only post-install evidence. It forbids Dashboard Send/resend, alternate semantic injection, cleanup/reset/uninstall, manual database/runtime mutation, provider/model/OpenClaw configuration mutation, unrelated process/service changes, and retry after a failed install procedure.

No Dashboard semantic Send, alternate semantic injection, or Task-136/137 nonce/message reuse occurred in this task.

## 2. Pre-install safety baseline

Evidence root:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx139-preflight-20260829T112000Z`

The pre-install checks used the installed runtime state and the candidate `cnxclaw_v093.py` read-only check interface. Results:

- system verdict: `READY`;
- recovery verdict: `READY`;
- delivery verdict: `READY`;
- controller mode: `managed`;
- desired Gateway/provider: `running` / `running`;
- selected provider: `ollama`;
- Gateway: healthy, loopback `127.0.0.1:18789`, connectivity probe `ok`;
- Ollama: installed, reachable, healthy, ready at `http://127.0.0.1:11434`;
- OpenClaw: `2026.7.1-2 (0790d9f)`;
- pending outbox: `0`;
- recovery incident: none active;
- SQLite `PRAGMA integrity_check`: `ok` via read-only URI;
- exactly one pre-install `cogentnexus-openclaw` plugin identity was present at the accepted global path;
- Task-136 and Task-137 historical Tickets were present and terminal (`failed`);
- historical database inventory before install: `2` Tickets, `14` Ticket events, `2` ended direct model calls, `0` outbox rows, `0` assistant-delivery rows, and `0` direct-recovery rows.

The pre-install installed payload fingerprint was:

```text
3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4
```

This differs from the exact candidate source fingerprint below.

The currently installed launcher did not expose `check` subcommands itself; the candidate's read-only checker was used to obtain the required system/recovery/delivery verdicts without changing live state. The initial invalid probe arguments were not interpreted as product state changes.

## 3. Exact candidate build/package provenance

An isolated detached worktree was created at:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue6-20260829T111029Z\exact-16f5c396`

The worktree resolved exactly to:

```text
16f5c396e9be0af8d1bd34824fe2993613501a6f
```

The worktree was clean before packaging. Environment:

```text
node v22.23.2
npm 12.0.2
```

Commands executed:

```text
npm ci --ignore-scripts
npm run build
npm run plugin:validate
npm pack --json
```

Build and validation passed. Validation reported:

```text
mixed-plugin artifact verification: PASS (45 config properties, 5 tools)
ticket DB bootstrap: PASS (9 required tables + v095 registration fence)
packedFileCount: 178
```

Artifact:

```text
openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz
size: 200610 bytes
sha256: 98a00a8a05ef4e7c600be045a4a4bbcbc6cb05f59acce5a3c54aabbacc80c014
```

Candidate source plugin fingerprint:

```text
12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0
```

The candidate artifact was produced from the exact repaired commit. No production source was edited during Task 139.

## 4. Supported install-over attempt

The repository documentation identifies `scripts/install.ps1` as the supported development-candidate installation entry point and explicitly states that there is no `cnxclaw.cmd install` command. The exact procedure used was:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  C:/Users/CDQ-P/AppData/Local/Temp/cnx-continue6-20260829T111029Z/exact-16f5c396/scripts/install.ps1 `
  -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

This was executed exactly once. It was an install-over of the existing product; no clean uninstall, reset, manual deletion, or semantic test message was used.

The installer entered its documented native handoff boundary, changing the controller from `managed` to `passthrough` and disabling the existing plugin before replacement. It then stopped fail-closed during ownership-safe plugin rollover preparation, before `openclaw plugins install` could replace the installed package.

The decisive installer error was:

```text
RuntimeError: plugin is not inside the managed npm projects boundary:
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
ownership-safe plugin generation rollover pre-install proof failed
```

Installer process exit code: `1`.

This is classified as `FAIL_INSTALL_OVER`. The task forbids retry, cleanup, reset, uninstall, or manually repairing the resulting state, so no such action was taken.

## 5. Post-failure read-only state

Post-failure evidence was collected without mutation using the same evidence root.

The resulting state was:

- controller mode: `passthrough`;
- desired Gateway: `running`;
- selected provider: `ollama`;
- provider transition: `null`;
- Gateway: still healthy and listening on `127.0.0.1:18789`;
- Ollama: still healthy/ready;
- OpenClaw: unchanged at `2026.7.1-2 (0790d9f)`;
- system checker: `READY` for the remaining readable state;
- recovery checker: `READY`;
- delivery checker: `READY`;
- pending outbox: `0`;
- installed plugin registration: exactly one identity, disabled, at `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`;
- installed plugin fingerprint: unchanged old value `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- SQLite `PRAGMA integrity_check`: `ok` through read-only URI.

Historical durable evidence remained unchanged:

- `2` terminal failed Tickets;
- `14` Ticket events;
- `2` ended direct model calls;
- `0` `ticket_outbox` rows;
- `0` `cnx_assistant_delivery` rows;
- `0` `cnx_direct_recovery` rows;
- Task-137 Ticket `CNXT-a38e1408-205f-4606-a5c8-ec54e9515aea` remained present and failed;
- no new Ticket, assistant-delivery row, outbox row, or recovery row was created by the installer.

The post-failure SQLite inventory matched the pre-install inventory for all historical Ticket/event/model-call and semantic delivery counts. No cleanup or normalization was performed.

## 6. Semantic-side-effect accounting

The installer procedure and evidence contain no Dashboard Send. No Dashboard semantic payload was entered, sent, retried, or reused. No alternate CLI/Gateway/API/test-harness semantic injection occurred. The Task-136/137 consumed ledger and nonce were not touched.

The only observed lifecycle side effect was the installer's documented native handoff to `passthrough` before its ownership preflight failure. This was part of the supported installer procedure and is recorded above; no follow-up lifecycle mutation was attempted.

## 7. Disposition

Task 139 cannot meet the PASS criteria because the single supported install-over did not complete and the effective installed payload remained the old fingerprint. The first applicable exact classification is:

```text
FAIL_INSTALL_OVER
```

Per the task's failure discipline, this report does not authorize a retry, cleanup, reset, reinstall, provider/configuration change, or semantic acceptance. The workflow stops here for independent ChatGPT review.

## 8. Evidence index

- Preflight and post-failure evidence: `C:\Users\CDQ-P\AppData\Local\Temp\cnx139-preflight-20260829T112000Z`
- Exact candidate worktree: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue6-20260829T111029Z\exact-16f5c396`
- Fresh clone used for report: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue6-20260829T111029Z\clone`
- Required report path: `docs/operations/coordination/reports/CNX-20260829-139-repaired-candidate-install-over-and-health-proof.md`

The final repository HEAD used for this report is recorded after publication verification in the delivery message accompanying this report.
