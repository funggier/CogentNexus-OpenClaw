# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_ACCEPTANCE`
Current authorization: `CNX-20260828-120_V093_REAL_WINDOWS_LIFECYCLE_ACCEPTANCE_PROVIDER_NEUTRAL_CANDIDATE`
Task ID: `CNX-20260828-120`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`](tasks/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md)

Task 120 is the new **read-only-first real-Windows lifecycle acceptance** for the provider-neutral exact candidate accepted after Tasks 117–119.

## Task 119 closure

Task-119 report:

`docs/operations/coordination/reports/CNX-20260828-119-installer-documentation-authority-alignment.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-119-installer-documentation-authority-alignment-review.md`

Review verdict:

`ACCEPTED PASS — CANONICAL INSTALL CONTRACT ALIGNED; EXACT CANDIDATE MAY ADVANCE TO A NEW READ-ONLY-FIRST REAL-WINDOWS LIFECYCLE ACCEPTANCE TASK`

Accepted exact candidate:

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- package ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- package tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Exact candidate CI:

- Validate `33185349482` success;
- Windows Installer Pack Smoke `33185349413` success;
- PS5.1 Acceptance Smoke `33185349400` success.

## Provider-neutral installation invariant

Installer responsibility is provider-neutral. The Task-120 Windows installation/install-over command is:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No `-Provider` argument is permitted.

Runtime/provider readiness is verified separately after installation. Provider-specific recovery knowledge is allowed only in the runtime/recovery phase where it is actually required.

## Required Task-120 sequence

`exact artifact provenance -> fresh read-only machine reconciliation/classification -> install-over once -> reset y once -> uninstall y once -> fresh reinstall same artifact once -> stop/start/restart once each -> recovery reality harness once -> final read-only snapshot -> report -> independent review`

No mutation is allowed until candidate provenance and Phase-1 machine classification are coherent.

## Historical live boundary

Task 116 remains the latest historical live evidence before Task 120 begins. Do not assume it is still current.

Task 116 ended safely at a pre-body PowerShell Provider binding failure and did not execute reset/uninstall/reinstall/lifecycle/recovery. Task 120 must freshly reconcile the machine and must not resume/replay Task 116 blindly.

## One-shot / fail-stop rule

Every disruptive phase may run at most once. On the first non-zero exit, failed postcondition, ambiguous ownership/classification, or evidence mismatch:

- stop immediately;
- preserve fresh evidence;
- do not retry;
- do not manually normalize/clean;
- publish the Task-120 report with the exact failure boundary.

## Hard fence

Task 120 does **not** authorize:

- candidate/artifact substitution;
- ad-hoc live source repair;
- replay of failed/completed disruptive phases;
- manual cleanup/normalization to continue;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- provider runtime update/reinstall/reconfiguration;
- provider/model/endpoint/timeout changes;
- unrelated workspace/plugin mutation;
- credential/secret access;
- Dashboard semantic nonce/message/Send;
- reboot/process-tree kill;
- merge/tag/release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`

Then stop for independent ChatGPT review. Do not create or execute the final Dashboard durable-delivery task automatically.
