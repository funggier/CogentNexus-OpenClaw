# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_ACCEPTANCE_REMAINING_LIFECYCLE`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 124 authorizes only the remaining one-shot lifecycle phases beginning at reset  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md`](tasks/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md)

Task ID:

`CNX-20260829-124`

## Task 123 independent review

Task-123 report:

`docs/operations/coordination/reports/CNX-20260829-123-post-install-deterministic-readonly-attestation.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-123-post-install-deterministic-readonly-attestation-review.md`

Verdict:

`ACCEPTED PASS — CURRENT POST-INSTALL STATE IS COHERENT; REMAINING ONE-SHOT LIFECYCLE MAY ADVANCE FROM RESET WITHOUT REPLAYING INSTALL-OVER.`

Task 123 proved the current Task-121-installed machine state with deterministic direct read-only probes:

- CNX managed and recovery READY;
- installed plugin fingerprint equals the frozen exact candidate;
- OpenClaw exactly `2026.7.1-2`;
- one current loaded/enabled CogentNexus-OpenClaw plugin root;
- Gateway healthy;
- Ollama REST healthy with four preserved models;
- SQLite integrity `ok`;
- no lifecycle mutation and no Dashboard semantic Send.

The prior PowerShell automatic `$args`/wrapper argument-forwarding problem is executor-harness history, not product evidence. Do not reuse that wrapper pattern.

## Exact candidate

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload/plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- payload count `178`.

## One-shot ledger

Consumed and prohibited from replay:

- Task-121 install-over: **1 / 1**.

Authorized once each in Task 124:

- reset `0 / 1`;
- uninstall `0 / 1`;
- fresh reinstall after successful uninstall `0 / 1`;
- stop `0 / 1`;
- start `0 / 1`;
- restart `0 / 1`;
- recovery harness `0 / 1`.

## Task 124 sequence

`fresh sanity fence -> reset y -> post-reset proof -> uninstall y -> preservation proof -> fresh reinstall same exact artifact -> proof -> stop -> start -> restart -> recovery harness -> final snapshot -> report`

Use Task-123 deterministic direct-probe discipline after every completed phase. Every disruptive phase is at most once; stop on the first non-zero, failed postcondition, ambiguity, or integrity mismatch.

## Prohibited during Task 124

- replaying install-over;
- candidate/artifact substitution;
- source/live ad-hoc repair;
- manual cleanup/normalization;
- replaying completed/failed lifecycle phases;
- OpenClaw changes/rebaseline;
- provider runtime/config/model/endpoint/timeout changes;
- unrelated plugin/workspace mutation;
- credential/secret access;
- Dashboard semantic Send;
- reboot/generic process-tree kill outside the exact recovery harness contract;
- merge/tag/release/force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md`

After publishing, stop for independent ChatGPT review. Do not automatically create or execute the final Dashboard durable-delivery task.
