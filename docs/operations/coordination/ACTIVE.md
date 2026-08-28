# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_ACCEPTANCE_CONTINUATION`
Current authorization: `CNX-20260828-122_POST_INSTALL_VERIFICATION_RECOVERY_AND_LIFECYCLE_CONTINUATION`
Task ID: `CNX-20260828-122`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-122-post-install-verification-recovery-and-lifecycle-continuation.md`](tasks/CNX-20260828-122-post-install-verification-recovery-and-lifecycle-continuation.md)

Task 122 continues the real-Windows lifecycle acceptance from the **post-install state produced by Task 121**. It must recover the missing read-only post-install proof using explicit non-interactive probes before any new mutation.

## Task 121 closure

Task-121 report:

`docs/operations/coordination/reports/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry-review.md`

Review verdict:

`ACCEPTED INCOMPLETE — INSTALL-OVER SUCCEEDED ONCE; POST-INSTALL VERIFICATION HARNESS FAILED; PRODUCT FAILURE NOT PROVEN; INSTALL-OVER IS CONSUMED AND MUST NOT BE REPLAYED`

Accepted Task-121 facts:

- production-equivalent attested classifier passed;
- classification was coherent interrupted-rollover/re-entry upgrade;
- provider-neutral install-over ran exactly once;
- install-over returned exit code `0` and reported installation completed successfully;
- the first failed boundary was the executor-created post-install verification wrapper entering Python/OpenClaw/Ollama interactive surfaces in a non-TTY context;
- reset/uninstall/reinstall/lifecycle/recovery did not execute;
- no Dashboard semantic Send occurred.

## Exact candidate retained

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

## Consumed one-shot ledger

- Task-121 install-over: **1 / 1 — consumed; forbidden to replay**.

Still available only after Task-122 read-only gate passes:

- reset: `0 / 1`;
- uninstall: `0 / 1`;
- fresh reinstall after uninstall: `0 / 1`;
- stop: `0 / 1`;
- start: `0 / 1`;
- restart: `0 / 1`;
- recovery harness: `0 / 1`.

## Task-122 first gate

Use explicit, bounded, non-interactive read-only probes only. Never call bare `python`, `openclaw`, or `ollama`.

At minimum verify:

- installed `cnxclaw.cmd status`, `check system`, and provider check;
- ownership manifest through an explicit resolved `namespace_ownership.py verify` path;
- `openclaw --version`, `openclaw plugins list --json`, `openclaw gateway status`;
- `ollama --version`, `ollama list`, `ollama ps`;
- SQLite `PRAGMA integrity_check` through explicit `python -c` or known read-only checker;
- plugin uniqueness, current/legacy namespace inventory, service/task state, and transaction/staging/rollover residue.

If current post-install state is not proven coherent: stop with zero new mutation.

## Remaining one-shot sequence

Only after the read-only gate passes:

`reset y -> uninstall y -> fresh reinstall same artifact -> stop -> start -> restart -> recovery harness -> final read-only snapshot`

The fresh reinstall after successful uninstall is allowed and is not a replay of the consumed Task-121 install-over.

## Hard fence

Task 122 does **not** authorize:

- replay of Task-121 install-over;
- candidate/artifact substitution;
- source/live ad-hoc repair;
- manual manifest/plugin/state cleanup or normalization;
- replay of any completed remaining phase;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- provider runtime/config/model/endpoint/timeout changes;
- unrelated workspace/plugin mutation;
- credential/secret access;
- Dashboard semantic nonce/message/Send;
- reboot/process-tree kill;
- merge/tag/release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-122-post-install-verification-recovery-and-lifecycle-continuation.md`

Then stop for independent ChatGPT review. Do not auto-open or execute the final Dashboard durable-delivery task.
