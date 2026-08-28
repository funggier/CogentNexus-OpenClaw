# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_ACCEPTANCE`
Current authorization: `CNX-20260828-121_V093_REAL_WINDOWS_LIFECYCLE_ACCEPTANCE_ATTESTED_REENTRY`
Task ID: `CNX-20260828-121`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry.md`](tasks/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry.md)

Task 121 is the new **read-only-first real-Windows lifecycle acceptance** using production-equivalent ownership attestation before any mutation.

## Task 120 closure

Task-120 report:

`docs/operations/coordination/reports/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate-review.md`

Review verdict:

`ACCEPTED BLOCKED — HARD FENCE WORKED; BLOCK WAS CAUSED BY AN INCOMPLETE ACCEPTANCE-CLASSIFIER INVOCATION, NOT BY A PROVEN LIVE OWNERSHIP FAILURE`

Task 120 performed zero destructive mutations. Its simplified read-only classifier command omitted the current plugin inventory and candidate plugin fingerprint needed by the exact candidate's attested interrupted-rollover/re-entry classifier path.

The production installer already prepares and supplies those attestation inputs. Therefore no source change is justified; Task 121 corrects only the acceptance preflight.

## Exact candidate retained

Use exactly:

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Exact-SHA CI remains accepted:

- Validate `33185349482` success;
- Windows Installer Pack Smoke `33185349413` success;
- PS5.1 Acceptance Smoke `33185349400` success.

## Corrected Task-121 read-only ownership gate

Before mutation, Task 121 must freshly:

1. verify artifact/source identity;
2. capture current machine/OpenClaw/CNX/Gateway/SQLite/runtime evidence;
3. prepare the candidate plugin only inside the verified extracted candidate boundary with `npm ci` and `npm run plugin:validate`;
4. compute the exact candidate plugin fingerprint using `namespace_ownership.py plugin-fingerprint`;
5. capture exact current `openclaw plugins list --json` inventory;
6. call `classify-install` with both `--plugin-inventory-json` and `--expected-replacement-fingerprint`;
7. require classification to be coherent with manifest/filesystem/inventory evidence.

No manual manifest/plugin/state normalization is permitted.

## One-shot lifecycle sequence

Only after the attested read-only gate passes:

`install-over once -> reset y once -> uninstall y once -> fresh reinstall same artifact once -> stop once -> start once -> restart once -> recovery harness once -> final read-only snapshot`

Task 120 consumed none of these disruptive attempts.

Canonical install/install-over command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No installer `-Provider` argument.

## Fail-stop rule

On first non-zero exit, ambiguous attested classification, ownership mismatch, integrity failure, or failed postcondition:

- stop immediately;
- preserve evidence;
- do not retry;
- do not manually clean/normalize;
- publish Task-121 report.

## Hard fence

Task 121 does **not** authorize:

- candidate/artifact substitution;
- source edit or live repair;
- manual manifest/plugin/state cleanup/normalization;
- replay of failed/completed disruptive phases;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- provider runtime/config/model/endpoint/timeout changes;
- unrelated workspace/plugin mutation;
- credential/secret access;
- Dashboard semantic nonce/message/Send;
- reboot/process-tree kill;
- merge/tag/release/force push.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry.md`

Then stop for independent ChatGPT review. Do not create or execute the final Dashboard durable-delivery task automatically.
