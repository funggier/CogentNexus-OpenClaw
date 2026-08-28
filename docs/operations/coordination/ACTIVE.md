# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
Current authorization: `CNX-20260829-125_V093_RECOVERY_REALITY_INTERACTIVE_CONFIRMATION_ACCEPTANCE`
Task ID: `CNX-20260829-125`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance.md`](tasks/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance.md)

Task 125 completes only the still-unproven recovery-reality acceptance. Task 124 already passed reset, uninstall, exact-candidate fresh reinstall, stop, start, and restart once each. None of those phases may be replayed.

## Task 124 closure

Task-124 report:

`docs/operations/coordination/reports/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance-review.md`

Review verdict:

`ACCEPTED PARTIAL PASS — RESET / UNINSTALL / FRESH REINSTALL / STOP / START / RESTART PASSED ONCE; RECOVERY PRODUCT BEHAVIOR WAS NOT TESTED BECAUSE THE EXACT HARNESS CANCELLED AT ITS UNSATISFIED INTERACTIVE CONFIRMATION GATE.`

Accepted Task-124 facts:

- reset `1 / 1` PASS;
- uninstall `1 / 1` PASS with external OpenClaw/Ollama/Gateway preservation;
- fresh reinstall exact same candidate `1 / 1` PASS;
- stop `1 / 1` PASS;
- start `1 / 1` PASS;
- restart `1 / 1` PASS;
- recovery harness process was invoked once but cancelled in `Confirm-Disruptive` before any disruptive scenario began;
- no Dashboard semantic Send occurred.

The exact candidate source requires `Read-Host 'Type y to continue'` followed by an exact lowercase `y`. Task 124 did not supply that interactive confirmation channel, so its recovery exit `1` is an acceptance-invocation defect, not product recovery-failure evidence.

## Exact candidate retained

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload/plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- recovery harness Git blob `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

## Consumed lifecycle ledger

Consumed and forbidden to replay:

- Task-121 install-over `1 / 1`;
- Task-124 reset `1 / 1`;
- Task-124 uninstall `1 / 1`;
- Task-124 fresh reinstall `1 / 1`;
- Task-124 stop `1 / 1`;
- Task-124 start `1 / 1`;
- Task-124 restart `1 / 1`.

Task-124 recovery invocation is closed under Task 124. It executed zero disruptive scenarios. Task 125 grants one new recovery-suite execution only.

## Task 125 sequence

`fresh deterministic read-only fence -> verify true interactive TTY -> exact recovery harness once -> wait for exact Read-Host prompt -> enter one lowercase y + Enter -> baseline/gateway-crash/provider-crash/operator-stop -> final deterministic read-only snapshot -> report -> independent review`

The harness must record `explicit-disruptive-confirmation=PASS` before scenario results can count.

If no true interactive TTY is available, stop `BLOCKED` before invoking the suite. Do not pipe/synthesize confirmation or edit/wrap the harness.

## Verification discipline

Use Task-123 deterministic direct probes for pre/final evidence:

- no generalized `args`/`Args` wrapper;
- no generic `Start-Process` proof wrapper;
- direct `&` calls with explicit paths/literal arguments;
- CNX JSON status/provider/recovery;
- ownership/fingerprint;
- OpenClaw metadata/direct Node/listener proof;
- Ollama REST/listener proof;
- SQLite integrity.

## Hard fence

Task 125 does not authorize:

- install/install-over;
- reset/uninstall/reinstall;
- standalone stop/start/restart outside the exact harness's reviewed operator-stop scenario;
- source/harness edit or alternate confirmation mechanism;
- manual cleanup/normalization;
- candidate/artifact substitution;
- OpenClaw/provider reconfiguration;
- credential/secret access;
- Dashboard semantic Send;
- reboot/generic process-tree kill;
- merge/tag/release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance.md`

Then stop for independent ChatGPT review. Do not create or execute the final Dashboard durable-delivery task automatically.
