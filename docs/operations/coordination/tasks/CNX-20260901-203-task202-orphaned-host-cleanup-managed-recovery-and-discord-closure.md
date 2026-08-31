# CNX-20260901-203 — Task 202 Orphaned Host Cleanup, Managed Recovery, and Discord Closure

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-202`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Recover from the proven Task-202 orphaned PowerShell root-wait shape without replaying installation or changing product bytes. After removing only the exact stale executor PowerShell process, resume from the already-installed repaired candidate through one supported `cnxclaw enable` transition. If managed convergence is proven, complete the still-unused one-human-Discord-Send requalification for Task 198.

## Immutable authorities

Frozen repaired product candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Published `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-202 accepted evidence:

- stale root PID: `11704`;
- retained creation time: `1788193889.192804` / Windows retained equivalent `\/Date(1788193889192)\/`;
- executable: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`;
- only descendant: console infrastructure `conhost.exe` PID `11588` at Task-202 sampling;
- no executable Python/Node/OpenClaw/Host/Gateway descendant;
- root CPU/handles/threads and installer streams unchanged across bounded samples;
- current product state: exact repaired plugin bytes installed, ownership valid, Host `passthrough`, startup/plugin disabled, Gateway/Ollama/delivery/recovery/SQLite healthy;
- Discord human Send consumed: `0 / 1`.

## Important classification

Task 202 did **not** prove an `install.ps1` source deadlock. The root process shape differs materially from the known-good Task-159 standalone `powershell.exe ... -File install.ps1` process pattern. Treat the stale PID cleanup as executor/orphaned-host recovery, not a source fix.

No repository/source/test/workflow change is authorized under Task 203.

## Phase A — final read-only stale-root fence

Before termination, capture current time and revalidate all of the following:

1. PID `11704` still exists;
2. executable path is exactly Windows PowerShell;
3. creation time exactly matches Task-202 retained identity;
4. recursive descendants contain no Python, Node, OpenClaw, Host, `cnxclaw`, Gateway, installer, or other executable work process;
5. root CPU/threads/handles and retained `b01-install.stdout` / `b01-install.stderr` remain unchanged across one final short bounded sample (about 15-30 seconds is sufficient);
6. installed plugin fingerprint still equals `f8267417...`;
7. ownership verify still passes;
8. Host is still `passthrough`, plugin/startup disabled;
9. Gateway/Ollama/delivery/recovery/SQLite remain healthy.

If PID identity changed, executable descendants reappear, streams resume, or product/health state materially changed, **do not terminate anything**. Stop with `BLOCKED_CLEANUP_FENCE` and report.

## Phase B — terminate only the exact orphaned host

If Phase A passes, terminate exactly the stale Task-200/202 PowerShell root PID `11704` using a normal Windows process-termination mechanism.

Rules:

- target only PID `11704` after exact identity validation;
- do not terminate Gateway, Ollama, OpenClaw, supervisor, provider, or unrelated processes;
- do not use a broad process-name kill;
- do not kill any executable descendant because Phase A requires there to be none;
- if the associated `conhost.exe` exits as a consequence, record it; do not separately kill unrelated console hosts;
- wait boundedly and prove PID `11704` is gone;
- capture exit/disappearance evidence and current state immediately after cleanup.

If termination fails or PID remains, stop with `FAIL_ORPHAN_CLEANUP`. Do not retry and do not Discord Send.

## Phase C — coherent installed-state gate

After stale-root removal, perform read-only verification:

- installed fingerprint = exact repaired candidate;
- ownership verify = PASS;
- Host remains `passthrough` before enable;
- Gateway healthy;
- selected provider Ollama and ready;
- delivery READY / outbox 0;
- recovery READY / no active incident;
- SQLite `integrity_check=ok`;
- no unexpected installer/enable process exists.

No installer replay is authorized.

If this gate does not pass, stop with `FAIL_PRE_ENABLE_HEALTH`.

## Phase D — one supported managed recovery transition

Invoke exactly once from the installed workspace:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable`

This is the only authorized lifecycle command in Task 203.

Requirements:

- invocation count: exactly `1 / 1`;
- no `--provider` override is necessary; v0.9.3 must deterministically target Ollama;
- capture root PID/process identity, stdout, stderr, duration and exact exit code;
- do not use `Start-Process -Wait` descendant-wait semantics; observe/wait for the exact root process only using a method that has already proven reliable in repository Windows acceptance (cache the process handle / root-only wait or launch-and-poll the exact root PID);
- do not retry if it fails or becomes ambiguous.

### Managed convergence acceptance

After enable returns, PASS requires:

1. enable exit code `0`;
2. Host mode `managed`;
3. desired Gateway/provider running as expected;
4. startup adapter installed/enabled/ready;
5. `cogentnexus-openclaw` plugin enabled, activated/loaded, no error;
6. Gateway healthy/listening;
7. Ollama selected/reachable/healthy/ready;
8. delivery READY, pending outbox `0`;
9. recovery READY, no active incident and no unexpected recovery attempt;
10. SQLite integrity `ok`;
11. installed fingerprint still equals exact repaired candidate.

If any item fails, stop with `FAIL_MANAGED_RECOVERY`. No second enable and no Discord Send.

## Phase E — exactly one genuine human Discord Send

Only after Phase D managed convergence passes.

Use the known healthy room/session:

`agent:main:discord:channel:1531199905673252946`

Generate a fresh nonce:

`CNX203-<UTC timestamp>-<short random suffix>`

Tell the user the exact single Discord message to send manually:

`ตอบกลับข้อความนี้เพียงว่า <NONCE>`

Then stop and wait for the user to say:

`ส่งแล้ว`

### Send budget

- human Discord Send: exactly `1 / 1`
- Hermes/bot/API/injected send: `0`
- retry: `0`
- regenerate: `0`
- second message/room: `0`

If the single Send visibly fails, do not send again.

## Phase F — durable Discord correlation

After `ส่งแล้ว`, prove:

`1 human Discord Send -> 1 Ticket -> 1 Direct model call -> response_ready -> 1 native visible Discord result -> delivery_confirmed -> completed`

Capture:

- nonce/prompt identity;
- owner session key;
- Ticket ID;
- request key / prompt SHA if available;
- run ID;
- model call ID;
- provider/model;
- ordered Ticket events;
- response-ready time;
- delivery-confirmed time;
- terminal status;
- user-visible Discord result or authoritative channel delivery evidence;
- Ticket/model/outbox/recovery deltas;
- bounded logs around the run.

Required negatives:

- no `before_agent_run hook failed` for the tested Send;
- no duplicate Ticket/model call/reply;
- no Direct Recovery attempt;
- no retry/regenerate;
- no pending outbox or stuck delivery residue attributable to the Send;
- no provider substitution.

Do not fail solely on Dashboard-observer `missing-run-correlation` or `missing-append-before-deliver` diagnostics.

A `cnx_assistant_delivery` row is not mandatory for native Discord Direct delivery; Ticket-level native `message_sent` / delivery confirmation evidence is accepted.

## Phase G — final read-only health

Capture final:

- Host managed mode;
- startup/plugin state;
- Gateway health;
- Ollama readiness;
- delivery/recovery state;
- SQLite integrity;
- exact installed fingerprint;
- durable counts;
- proof stale PID `11704` remains absent.

## Hard fences

Do not:

- rerun `scripts/install.ps1`;
- uninstall/reset/fresh reinstall/install-over;
- invoke enable more than once;
- invoke disable/start/stop/restart;
- change provider/model/config/SQLite manually;
- mutate Release/tag/assets;
- edit source/test/workflow/product files;
- use broad process kills;
- send Discord more than once;
- force push.

## Final dispositions

Use exactly one:

- `PASS`
- `BLOCKED_CLEANUP_FENCE`
- `FAIL_ORPHAN_CLEANUP`
- `FAIL_PRE_ENABLE_HEALTH`
- `FAIL_MANAGED_RECOVERY`
- `FAIL_DISCORD_BEFORE_AGENT`
- `FAIL_DISCORD_SEMANTIC_DELIVERY`
- `FAIL_DURABLE_CORRELATION`
- `FAIL_FINAL_HEALTH`
- `BLOCKED_EVIDENCE`

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-203-task202-orphaned-host-cleanup-managed-recovery-and-discord-closure.md`

Include mutation ledger, exact cleanup identity proof, enable root-process evidence, managed convergence evidence, Discord send budget and durable correlation evidence. Then stop for ChatGPT review.
