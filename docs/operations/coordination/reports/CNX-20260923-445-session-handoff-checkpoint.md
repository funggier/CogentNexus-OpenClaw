# CNX-20260923-445 — Session Handoff Checkpoint

Status: `PAUSED_SAFE_FOR_LCONNECT_RECONNECT`

Parent task: `CNX-20260922-444-v097-gateway-interruption-direct-recovery.md`

Working branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

Checkpoint purpose: preserve the exact v0.9.7 qualification state before LConnect is upgraded/reconnected. LConnect process/session IDs are disposable; this repository checkpoint and fresh machine/repository inspection are the resume authority.

## Exact repository state

- HEAD: `036eef28842044499fec2588ab6c8605ad6bdd7c`
- subject: `fix(v0.9.7): close interrupted inference attempt`
- upstream: `origin/cnx-357-openai-dashboard-ticket-first-requalification-v2`
- local/remote divergence at checkpoint: none
- worktree at checkpoint: clean
- v0.9.6 remains the published immutable baseline; v0.9.7 is not yet release-accepted.

Recent repair chain:

1. `3875c1dcc4067aa372fa725de2a05b2b3e3b8098` — dispatch durable delivery wake through the Host delivery bridge;
2. `3c0db0c69e658c2501086886e0ff02e3cd44022d` — bypass the Windows `.cmd` shim for Gateway RPC and invoke Node + `openclaw.mjs` shell-free;
3. `036eef28842044499fec2588ab6c8605ad6bdd7c` — close the exact canonical inference attempt when a Direct model call is authoritatively interrupted by the replaced Gateway boundary.

## Exact-SHA CI for current HEAD

All required workflows for `036eef28842044499fec2588ab6c8605ad6bdd7c` completed SUCCESS on attempt 1:

- Validate: run `35880664043`;
- PS5.1 Acceptance Smoke: run `35880664080`;
- Windows Installer Pack Smoke: run `35880664055`.

Do not create a replacement candidate merely to re-run these already-GREEN workflows.

## Live installation state at checkpoint

The current installed `host_stall_v091.py` hash matches the source at HEAD:

`90A105B1E43256154501659418A2804586C470B8B2B9213181B1DCB0EBF41F0B`

Canonical Supervisor read immediately before this checkpoint:

- state: `Ready`;
- enabled: `true`;
- `LastTaskResult=0`.

Last verified managed runtime baseline carried into this checkpoint:

- OpenClaw/Gateway: `2026.9.5`;
- CNX mode: active/MANAGED;
- provider/model route: `ollama/qwen3.8:27b`;
- provider/model/auth routing remains OpenClaw-owned.

After LConnect reconnect, re-read this state from the machine. Do not assume a stale LConnect session/process handle survived.

## Durable-delivery proof already completed

Historical live recovery Ticket:

`CNXT-df3d2a62-f057-4008-b893-df75d7fdf0b8`

The repaired delivery path settled its already-persisted response without regeneration:

- response: `CNX444_RECOVERY_OK`;
- Ticket: `completed`;
- Direct recovery: `done`, recovery attempt count `1`;
- delivery: `delivered`;
- marker occurrence in OpenClaw history: exactly `1`;
- response occurrence in OpenClaw history: exactly `1`;
- no new recovery inference was created for the retry;
- wake authority returned `idle/no-actionable-work` after settlement.

This Ticket is consumed evidence. Do not replay it.

## Fresh physical interruption proof before current HEAD

Fresh live Ticket:

`CNXT-c683028b-21d1-4e28-97d4-db24a75c0c72`

Run:

`cnx444-fresh-3c0db0c6-20260923`

Prompt:

`Reply with exactly CNX444_FRESH_3C0DB0C6_RECOVERY_OK and nothing else.`

This was a real Direct turn under `ollama/qwen3.8:27b`. The production Host replaced the current Gateway boundary while the Direct model call was active. Evidence proved:

- Direct model call started at `2026-09-23T14:44:42.218Z`;
- exact current-boot Gateway interruption was authorized once;
- Direct model-call outcome became `host-gateway-interruption-authorized`;
- exactly one Direct recovery was created;
- recovery runtime started once;
- detached recovery produced `CNX444_FRESH_3C0DB0C6_RECOVERY_OK`;
- recovery attempt count = `1`;
- one durable delivery was created and eventually confirmed;
- Ticket reached `completed`;
- no outbox duplicate was created.

However, this live run exposed a release-blocking ledger defect: the original `cnx_inference_attempt` remained `state='active'`, `outcome=NULL`, `ended_at=NULL` after the Direct model call had already become interrupted.

Therefore this live run is diagnostic evidence, not final post-fix acceptance.

## Current repair at HEAD

Commit `036eef28842044499fec2588ab6c8605ad6bdd7c` repairs the defect inside the same quiesced Gateway-interruption transaction.

The repair:

- matches the canonical attempt by exact `ticket_id + run_id + call_id + state='active'`;
- fails closed if more than one active exact attempt exists;
- changes exactly one matching attempt to:
  - `state='ended'`;
  - `outcome='host-gateway-interruption-authorized'`;
  - `ended_at=<classification stamp>`;
- appends exactly one `inference_attempt_ended` event with source `cogentnexus-openclaw-canonical-attempt`;
- leaves non-matching attempts untouched.

The regression that originally reproduced the live defect failed RED before the repair and is included in the current commit.

The current source is installed, but **a fresh physical interruption has not yet been re-run after this exact repair**. This is the next release gate.

## Safe resume procedure after LConnect reconnect

Start from durable authority, not from remembered tool/session state:

1. reconnect/update LConnect;
2. locate/fetch `funggier/CogentNexus-OpenClaw`;
3. read:
   - this checkpoint;
   - `docs/operations/coordination/ACTIVE.md`;
   - `docs/operations/coordination/STATUS.md`;
   - the CNX-444 task;
   - `docs/operations/coordination/reports/CNX-20260922-444-v097-gateway-interruption-direct-recovery-report.md`;
4. verify GitHub remote HEAD before trusting this checkpoint SHA; if no newer authoritative commit exists, expected HEAD is `036eef28842044499fec2588ab6c8605ad6bdd7c`;
5. verify clean worktree and exact-SHA CI;
6. verify installed/source parity, Gateway 2026.9.5 health, MANAGED state, Supervisor Ready+Enabled, route `ollama/qwen3.8:27b`, and no installer/lifecycle process already running;
7. **do not reinstall if parity already matches**;
8. run exactly one new controlled Direct interruption with a new unique run/token/Ticket;
9. wait until the real Direct model call and canonical inference attempt are active;
10. use the production exact hard-hang replacement path (`prepare -> stop --force -> exact current-boot classify -> start`);
11. prove on the new Ticket:
    - Direct model call = `interrupted`;
    - exact canonical inference attempt = `ended`;
    - attempt outcome = `host-gateway-interruption-authorized`;
    - exactly one `inference_attempt_ended` event;
    - exactly one Direct recovery;
    - recovery attempt count = `1`;
    - original provider/model preserved;
    - exactly one response-ready result;
    - exactly one delivered result/marker;
    - Ticket = `completed`;
    - no duplicate outbox/delivery/recovery/inference work;
12. only after that fresh post-`036eef` acceptance passes, update CNX-444 report/ACTIVE/STATUS and continue the remaining bounded lifecycle/release-publication gates.

## Do not do after reconnect

- Do not replay `CNXT-df3d2a62...`.
- Do not reuse `CNXT-c683028b...` as proof for `036eef...`; it predates that fix.
- Do not create another installer while an installer/lifecycle process is already active.
- Do not rerun install-over merely because LConnect lost its process/session memory; inspect machine state first.
- Do not publish v0.9.7 until the fresh post-`036eef` interruption acceptance and remaining release gates are GREEN.
- Do not restore timer-only destructive Direct recovery.

## Checkpoint classification

`CNX444_V097_INTERRUPTED_ATTEMPT_CLOSE_EXACT_SHA_GREEN_LIVE_REACCEPTANCE_PENDING`

This is the intended safe stopping point for LConnect upgrade/reconnection.
