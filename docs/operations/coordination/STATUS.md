# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_ACCEPTANCE`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 120 authorizes one bounded real-Windows lifecycle acceptance against the exact accepted candidate  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`](tasks/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md)

Task ID:

`CNX-20260828-120`

## Task 119 independent review

Task-119 report:

`docs/operations/coordination/reports/CNX-20260828-119-installer-documentation-authority-alignment.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-119-installer-documentation-authority-alignment-review.md`

Verdict:

`ACCEPTED PASS — CANONICAL INSTALL CONTRACT ALIGNED; EXACT CANDIDATE MAY ADVANCE TO A NEW READ-ONLY-FIRST REAL-WINDOWS LIFECYCLE ACCEPTANCE TASK`

Tasks 117–119 now establish one coherent installer boundary:

- PowerShell installer is provider-neutral;
- POSIX installer is provider-neutral;
- no installer provider parameter/default/validation;
- no provider executable prerequisite merely for installation;
- generic lifecycle handoff from installer;
- canonical Windows/POSIX install documentation matches implementation;
- runtime/provider readiness remains a separate runtime concern.

## Exact Task-120 candidate

- source SHA: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID: `9691451156`;
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- package ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- package tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload count: `178`;
- payload fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Exact-SHA CI:

- Validate `33185349482` success;
- Windows Installer Pack Smoke `33185349413` success;
- PS5.1 Acceptance Smoke `33185349400` success.

## Task 120 live gate

First perform exact artifact provenance and a **fresh read-only machine reconciliation/classification**. Task 116 is historical evidence only; do not assume its state is still current.

Only if provenance and current ownership/machine state are coherent may the executor proceed in this exact one-shot order:

`install-over -> reset y -> uninstall y -> fresh reinstall same artifact -> stop -> start -> restart -> recovery harness -> final read-only snapshot`

Canonical install/install-over command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No installer `-Provider` argument.

Runtime/provider readiness is evaluated separately. The current runtime recovery harness remains provider-specific where recovery actually owns that behavior.

## Fail-stop rule

Each disruptive phase may execute at most once. On first non-zero exit, ambiguous classification, ownership mismatch, integrity failure, or failed postcondition:

- stop;
- preserve evidence;
- do not replay;
- do not clean/normalize manually;
- report the exact failure boundary for independent review.

## Prohibited during Task 120

- candidate/artifact substitution;
- live source repair;
- replay of completed/failed destructive phases;
- manual normalization/cleanup to force continuation;
- OpenClaw changes or rebaseline;
- provider runtime/config/model/endpoint/timeout changes;
- unrelated plugin/workspace mutation;
- credential/secret access;
- Dashboard semantic Send;
- reboot/process-tree kill;
- merge/tag/release/force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`

After publishing, stop for independent ChatGPT review. Do not create or execute the final Dashboard durable-delivery task automatically.
