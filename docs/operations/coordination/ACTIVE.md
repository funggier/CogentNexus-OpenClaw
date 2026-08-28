# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_ACCEPTANCE_REMAINING_LIFECYCLE`
Current authorization: `CNX-20260829-124_V093_REMAINING_REAL_WINDOWS_LIFECYCLE_ACCEPTANCE`
Task ID: `CNX-20260829-124`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md`](tasks/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md)

Task 124 continues the exact-candidate real-Windows lifecycle acceptance from the coherent post-install state proven by Task 123. It begins at **reset** and must never replay the already-consumed Task-121 install-over.

## Task 123 closure

Task-123 report:

`docs/operations/coordination/reports/CNX-20260829-123-post-install-deterministic-readonly-attestation.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-123-post-install-deterministic-readonly-attestation-review.md`

Review verdict:

`ACCEPTED PASS — CURRENT POST-INSTALL STATE IS COHERENT; REMAINING ONE-SHOT LIFECYCLE MAY ADVANCE FROM RESET WITHOUT REPLAYING INSTALL-OVER.`

Accepted Task-123 facts include:

- CNX managed/READY state;
- exact installed plugin fingerprint matching the frozen candidate;
- OpenClaw exactly `2026.7.1-2`;
- one loaded/enabled current plugin registration/root;
- healthy Gateway listener/process;
- Ollama loopback readiness and four preserved models;
- SQLite integrity `ok`;
- no Task-123 lifecycle mutation or Dashboard semantic Send.

The earlier generalized verification wrapper/PowerShell automatic `$args` collision is closed as an executor-side harness defect. Task 124 must use the deterministic direct-probe discipline from Task 123.

## Exact candidate retained

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload/plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- payload count `178`.

## One-shot ledger

Consumed and forbidden to replay:

- Task-121 install-over: **1 / 1**.

Authorized in Task 124, each at most once:

- reset `0 / 1`;
- uninstall `0 / 1`;
- fresh reinstall after successful uninstall `0 / 1`;
- stop `0 / 1`;
- start `0 / 1`;
- restart `0 / 1`;
- recovery harness `0 / 1`.

## Required sequence

`fresh read-only sanity fence -> reset y -> deterministic post-reset proof -> uninstall y -> preservation proof -> fresh reinstall same exact artifact -> deterministic proof -> stop -> start -> restart -> recovery harness once -> final deterministic read-only snapshot -> report -> independent review`

Every disruptive phase is one-shot. Stop on first non-zero, failed postcondition, ambiguity, or integrity mismatch. Never normalize/clean manually to continue.

## Verification discipline

- no generalized wrapper using `args`/`Args`;
- no `Start-Process` generic command proof;
- use PowerShell `&` with explicit paths and separate literal arguments;
- CNX direct commands;
- OpenClaw package metadata/direct Node entrypoint/listener proof;
- Ollama loopback REST/listener proof;
- explicit ownership script/runtime Python/SQLite checks.

## Hard fence

Task 124 does not authorize:

- replay of install-over;
- candidate/artifact substitution;
- source/live ad-hoc repair;
- manual cleanup/normalization;
- replay of completed/failed lifecycle phases;
- OpenClaw update/rebaseline;
- provider runtime/config/model/endpoint/timeout changes;
- unrelated workspace/plugin mutation;
- credential/secret access;
- Dashboard semantic Send;
- reboot/generic process-tree kill outside the reviewed recovery harness;
- merge/tag/release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md`

Then stop for independent ChatGPT review. Do not create or execute the final Dashboard durable-delivery task automatically.
