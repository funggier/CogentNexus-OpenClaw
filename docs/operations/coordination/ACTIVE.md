# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `READONLY_POST_INSTALL_ATTESTATION`
Current authorization: `CNX-20260829-123_POST_INSTALL_DETERMINISTIC_READONLY_ATTESTATION`
Task ID: `CNX-20260829-123`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-123-post-install-deterministic-readonly-attestation.md`](tasks/CNX-20260829-123-post-install-deterministic-readonly-attestation.md)

Task 123 is a **read-only-only post-install attestation** of the machine state produced by the successful Task-121 install-over. It must not execute reset, uninstall, reinstall, lifecycle controls, recovery disruption, or any install/install-over.

## Task 122 closure

Task-122 report:

`docs/operations/coordination/reports/CNX-20260828-122-post-install-verification-recovery-and-lifecycle-continuation.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-122-post-install-verification-recovery-and-lifecycle-continuation-review.md`

Review verdict:

`ACCEPTED BLOCKED — NO NEW MUTATION; THE BLOCK IS A VERIFICATION-CONTRACT/ARGUMENT-FORWARDING DEFECT, NOT A PROVEN PRODUCT FAILURE`

Key review findings:

- Task 122 performed zero new lifecycle mutations;
- the exact candidate intentionally uses an Ollama-only v0.9.3 runtime facade, so Ollama-only launcher text does not contradict provider-neutral installation;
- CNX help output + OpenClaw TUI + Ollama UI strongly indicate the generalized probe wrapper did not forward effective command arguments;
- the Task-121 install-over remains the only consumed destructive operation and must never be replayed.

## Exact candidate retained

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload/plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

## Consumed / unconsumed ledger

Consumed and forbidden to replay:

- Task-121 install-over: **1 / 1**.

Still unconsumed but **not authorized by Task 123**:

- reset `0 / 1`;
- uninstall `0 / 1`;
- fresh reinstall after uninstall `0 / 1`;
- stop `0 / 1`;
- start `0 / 1`;
- restart `0 / 1`;
- recovery harness `0 / 1`.

## Task-123 probe boundary

Do not reuse the Task-121/122 generalized probe wrapper or `Start-Process` for command proof.

Use direct PowerShell call-operator invocations with separate argument strings, explicit resolved Python/script paths, OpenClaw Node/package metadata and listener/process proof, and Ollama loopback REST/listener proof.

Runtime `Ollama-only` text is expected v0.9.3 policy and must not be treated as installer coupling.

## Hard fence

Task 123 authorizes no product/runtime lifecycle mutation:

- no install/install-over;
- no reset/uninstall/reinstall;
- no enable/disable/start/stop/restart;
- no recovery disruption;
- no plugin/provider/runtime/config mutation;
- no manual cleanup/normalization;
- no Dashboard semantic Send;
- no reboot/process kill;
- no merge/tag/release/force push.

Evidence-file creation under a fresh external Task-123 evidence root is allowed.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-123-post-install-deterministic-readonly-attestation.md`

Then stop for independent ChatGPT review. Do not create or execute a lifecycle continuation successor automatically.
