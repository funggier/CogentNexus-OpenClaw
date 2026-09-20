# Active Coordination Task

Status: `IN_PROGRESS`
State: `CNX427_CNX440_441_DEPLOYED_FINAL_DISCORD_ACCEPTANCE_READY`
Execution mode: `CONTROLLED_LIVE_ACCEPTANCE_AND_MAINTENANCE`
Task ID: `CNX-20260919-427`
Parent: `CNX-20260919-426`
Executor: `ChatGPT via LConnect`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## CNX-440 / CNX-441 live deployment update

This section is the current authoritative pre-acceptance state and supersedes older baseline figures later in this file.

Exact candidate:

- branch `cnx-357-openai-dashboard-ticket-first-requalification-v2`;
- local HEAD = remote HEAD = `5263b6aed9acf77a4db39be47c4d96fecfe8a431`;
- CNX-441 implementation commit = `5263b6aed9acf77a4db39be47c4d96fecfe8a431`;
- CNX-440 implementation commit = `a4f27ad097e721edfe566a7495864b7e15ae88e8`.

Supported install-over:

- managed LConnect process session `proc-1789885920190-35`, PID `10220`;
- terminal exit code `0`;
- installer stdout ended with `CogentNexus-OpenClaw v0.9.5 installation completed successfully.`;
- live v095 adapter SHA-256 = candidate SHA-256 = `7809B18C4BAE1209624D5E69112722EF9AD7F5E39A92A2815C6889DFF6C646A1`;
- controller is `cnxMode=active`, `mode=managed`, generation `111`;
- Gateway health `ok=true`, event loop `degraded=false`;
- Discord lifecycle `ready`, running/connected `true`;
- CNX supervisor restored Enabled/Ready with `LastTaskResult=0`;
- OpenClaw Gateway Scheduled Task is Running;
- `ollama ps` is empty.

Current qwen policy:

- primary model `ollama/qwen3.8:27b`;
- OpenClaw `contextWindow=24576`;
- Ollama `num_ctx=24576`;
- `OLLAMA_CONTEXT_LENGTH=24576`;
- `OLLAMA_KEEP_ALIVE=2h`.

Fresh CNX DB baseline before final Discord acceptance:

- Tickets = `47`;
- max Ticket event ID = `1109`;
- direct model calls = `35`;
- inference attempts = `33`;
- assistant deliveries = `26`;
- target channel `1391855033993138217` has zero non-terminal Tickets;
- its prior CNX session is deleted at generation `7`;
- the two remaining accepted Tickets belong to other historical Discord channels;
- their recovery rows are pending redelivery with `active_run_id=null`; no target recovery row is active.

CNX-441 live classification is now:

`INSTALLER_SUPERVISOR_HANDOFF_QUIESCENCE_GREEN`

CNX-440 is deployed and provenance-qualified, but its final live Discord marker/receipt settlement remains pending one human-originated Discord turn.
Task: `docs/operations/coordination/tasks/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair.md`
Report: `docs/operations/coordination/reports/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair-report.md`
Handoff: `docs/operations/coordination/reports/CNX-20260919-427-full-session-handoff-openclaw-9.5-and-storage-relocation.md`

## Primary runtime state

OpenClaw live is now `2026.9.5 (ec9c1a1)` and settled GREEN:

- Gateway health ok;
- event loop not degraded;
- Discord connected/ready;
- plugin errors 0;
- Tailscale Serve active;
- remote HTTPS 200;
- CNX runner ready;
- supervisor Enabled / Last Result 0.

OpenClaw 9.5 was selected because upstream commit `983782594807a23c006b49bd16172b1ba6980924` preserves admitted runtime generation for channel turns, directly matching the Discord/Codex Ticket-first continuity defect reproduced twice on 9.4.

## CNX-428 OpenClaw 9.5 startup-grace repair

The OpenClaw 9.5 cold-start interaction discovered during CNX-427 is repaired and live-qualified.

- repair implementation: `13dfba9a55f4d64ceb9aa8440670c9ee9792354a`;
- actual OpenClaw 9.5 cold start measured about 90.7 s to `gateway ready`;
- the previous two-probe/1-second rule falsely restarted valid cold starts;
- the supervisor now uses a bounded 180-second grace grounded in `gateway_boot_lifecycle`;
- live boot id `2457011a-c738-4e74-912d-3f309236455d` classified `gateway-starting` without calling restart;
- stale `healthy-runtime` maintenance converged through the supported lifecycle path;
- recurring supervisor is Enabled with `LastTaskResult=0` and no new restart request.

Task/report:

- `docs/operations/coordination/tasks/CNX-20260919-428-openclaw-9.5-supervisor-cold-start-grace-repair.md`
- `docs/operations/coordination/reports/CNX-20260919-428-openclaw-9.5-supervisor-cold-start-grace-repair-report.md`

A PID-bound isolated Gateway probe also proved the OpenClaw 9.5 execution generation carries CNX Ticket-first admission correctly: one process -> one user turn -> one host run -> one Ticket -> one model call, with Ticket persistence before model-call authority. The small probe model timed out at 90 s and terminated without duplicate/recovery inference, so it does not replace the final Discord delivery acceptance.

## CNX-436 / CNX-437 live qualification

The remaining OpenClaw 9.5 install/enable blockers found after CNX-428 are now repaired and live-qualified.

CNX-436:

- implementation commit `321fda1e5a2564973a9868141413fb73b8c26805`;
- `lifecycle start` readiness budget repaired from 30 s to bounded 180 s;
- repository affected-surface regression: 107/107 PASS;
- live supported install observed 5 readiness attempts with `timeoutSeconds=180.0`;
- classification: `OPENCLAW95_LIFECYCLE_START_READINESS_GREEN`.

CNX-437:

- implementation commit `d67e86ae212222e62bd6eba2e194c1fd78fcf785`;
- Windows captured subprocess boundaries now decode UTF-8 with replacement instead of locale CP1252;
- exact prior `json.loads(None)` failure covered by TDD;
- real Thai UTF-8 byte regression (including byte 0x81) passes;
- supported install-over from exact candidate completed with terminal exit 0;
- MANAGED generation 109 remains committed;
- CNX supervisor Enabled / Last Result 0;
- Gateway healthy and Discord ready/connected;
- no post-install UnicodeDecodeError, NoneType JSON failure, transactional rollback, or new crash-loop breaker event;
- classification: `WINDOWS_UTF8_SUBPROCESS_AND_GATEWAY_TEMP_COMPAT_GREEN`.

Storage hardening discovered during CNX-437 is also active:

- Gateway process-local TMPDIR/TEMP/TMP -> `T:\CogentNexus\CogentNexus-OpenClaw\temp\openclaw-gateway`;
- LConnect child TEMP/TMP -> `T:\CogentNexus\CogentNexus-OpenClaw\temp\lconnect`;
- C: current `openclaw-plugin-build-*` count = 0;
- C: free space remains about 103.8 GB.

Reports:

- `docs/operations/coordination/reports/CNX-20260920-436-openclaw-9.5-lifecycle-start-readiness-budget-repair-report.md`
- `docs/operations/coordination/reports/CNX-20260920-437-windows-utf8-subprocess-and-gateway-temp-compatibility-repair-report.md`

## CNX-438 recovery-triggered qwen memory-pressure repair

The first post-delete Discord acceptance attempt was rehydrated automatically by OpenClaw main-session restart recovery.

Exact recovery lineage:

- physical Discord session: `38ef9799-a8ed-49fb-963c-aad35519a771`;
- admission run: `9000715c-c8db-4d2c-b040-6663f8235d33`;
- Ticket: `CNXT-26e773e3-9506-4bfb-8ee0-4ec16fea9661`;
- recovery log: `started interrupted main session`;
- qwen3.8 launched with `-c 262144`.

The 262k load drove llama-server private memory to about 28.2 GB and Gateway event-loop delay to about 11.5 seconds, making the Dashboard effectively unusable.

Repair/qualification:

- recovered run aborted through supported `sessions.abort`;
- qwen unloaded and Gateway event loop recovered;
- 64k isolated load remained unsafe (free RAM about 0.6 GB at pressure peak);
- qwen3.8 live `contextWindow` and `num_ctx` reduced to `32768`;
- isolated 32k load completed successfully in about 22.46 seconds;
- target Discord session deleted through supported OpenClaw lifecycle;
- recovery Ticket became `cancelled`;
- session authority became `deleted`, generation 6;
- no direct-recovery row remains;
- historical active model-call/inference rows are terminal-Ticket fenced because Host claim requires `t.status='accepted'`;
- local and Tailscale Dashboard endpoints return HTTP 200;
- Gateway event loop is not degraded;
- Discord ready/connected, activeRuns=0.

Current fresh target baseline:

- target Discord session absent;
- model `ollama/qwen3.8:27b`;
- context cap `32768`;
- Tickets 46;
- max event id 1101;
- direct model-call rows 34;
- inference attempts 32;
- assistant deliveries 26;
- free physical RAM about 21.4 GB.

Task/report:

- `docs/operations/coordination/tasks/CNX-20260920-438-recovery-triggered-qwen-memory-pressure-and-safe-context-cap.md`
- `docs/operations/coordination/reports/CNX-20260920-438-recovery-triggered-qwen-memory-pressure-repair-report.md`

Classification:

`RECOVERY_TRIGGERED_QWEN_MEMORY_PRESSURE_REPAIRED_GREEN`

## Remaining primary acceptance

CNX-427 is NOT final PASS yet.

One new Discord turn on live 9.5 must prove:

- one authoritative host run;
- exactly one CNX Ticket;
- Ticket-first before inference authority;
- one model execution;
- one Discord delivery;
- correct terminal Ticket state;
- no duplicate Ticket or stale lane.

Storage/runtime maintenance and pre-inference Ticket-first qualification are now stable. The next operator action is exactly one genuine new Discord acceptance turn; do not substitute another CLI/synthetic turn for that final ingress proof.

## Secondary operator-requested maintenance

The operator-requested C: -> T: backup relocation is complete and verified.

Current state:

- canonical destination: `T:\CogentNexus\CogentNexus-OpenClaw`;
- C: `backups` is an NTFS junction to the T: backup tree;
- C: `plugin-generation-rollover-backups` is an NTFS junction to the T: rollover tree;
- main backup dry mirror: 509,383 files / 9.479 GiB, copied 0, mismatch 0, failed 0, extras 0;
- rollover dry mirror: 159,271 files / 1.408 GiB, copied 0, mismatch 0, failed 0, extras 0;
- authoritative CNX-427 manifest and critical hashes match source/target;
- authoritative reparse count matches 10 -> 10;
- old C: rollback/report paths resolve through the junction;
- reparse-safe source cleanup completed with no failed deletions;
- C: free space increased from ~13.43 GiB to ~25.48 GiB.

Checkpoint:

`docs/operations/coordination/reports/CNX-20260919-427-storage-relocation-and-pre-acceptance-runtime-checkpoint.md`

The only remaining CNX-427 gate is one new live Discord acceptance turn on OpenClaw 2026.9.5.
