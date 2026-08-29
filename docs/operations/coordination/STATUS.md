# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `REPOSITORY_SOURCE_TDD_REPAIR`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 133 authorizes repository/test/CI/package proof closeout only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md`](tasks/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md)

Task ID:

`CNX-20260829-133`

## Task 132 independent review

Task-132 sequencing repair is directionally accepted but not yet live-advanceable.

Review:

`docs/operations/coordination/reviews/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair-review.md`

Blocking proof gaps:

1. the executable harness-owned negative-case matrix did not explicitly cover adapter `expected=true`, host/provider mismatch, missing Gateway/Ollama listeners, and post-start exception leakage;
2. Task-132 report published a stale artifact outer digest.

Task-132 proposed candidate:

`b7074c8cb5b10c77624cfe7b5223e3bae338c80d`

is not yet accepted for a new live recovery task.

## Package identity clarification

Task-132 artifact `9709442638` itself is coherent and its inner package identity matches `b7074c8c...`, but GitHub metadata gives outer artifact digest:

`sha256:8cb0370b6ba2c741b31f5c972a8de9ce4cfc488ccbe6042d4d6e1d6535db213c`

Task-132 report instead reused `sha256:c5dcbda0...` from an older candidate. Task 133 must generate a fresh artifact and publish the fresh outer digest correctly.

## Task 133 proof closeout

Required non-disruptive behavioral proof through the real PowerShell `-ContractSelfTest` path:

- carried provider incident still accepts only the exact immediate prior provider-crash state;
- standalone/different/missing/duplicate/circuit-open/extra-warning/closed-incident cases reject;
- adapter missing/duplicate/`expected=true` reject;
- host/provider selection mismatch rejects;
- Gateway listener missing rejects;
- Ollama listener missing rejects;
- ordinary/post-operator-start convergence remains strict `READY` and does not inherit the exception.

Then require full repository validation, all four exact-SHA workflows, and fresh package proof with correct outer artifact digest plus inner package identity/hashes.

## Historical live ledger

Consumed/closed:

- install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 suite `0 / 1`, closed blocked;
- Task-131 suite `1 / 1` consumed;
- Task-131 gateway-crash PASS;
- Task-131 provider-crash PASS;
- Task-131 operator-stop `0`.

Task 133 authorizes **zero live lifecycle/recovery operations**.

## Prohibited

No live recovery suite/crash injection, install/install-over/reset/uninstall/reinstall, live start/stop/restart/enable/disable, provider/OpenClaw/model/config mutation, process kill, task/service mutation, cleanup/normalization, reboot, credential/secret access, Dashboard semantic Send, merge/tag/release, or force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md`

Then stop for independent ChatGPT review. Final Dashboard durable-delivery acceptance remains unopened and prohibited.
