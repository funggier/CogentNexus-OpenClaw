# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_ACCEPTANCE`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 121 authorizes one bounded real-Windows lifecycle acceptance using production-equivalent attested ownership classification  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry.md`](tasks/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry.md)

Task ID:

`CNX-20260828-121`

## Task 120 independent review

Task-120 report:

`docs/operations/coordination/reports/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-120-v093-real-windows-lifecycle-acceptance-provider-neutral-candidate-review.md`

Verdict:

`ACCEPTED BLOCKED — HARD FENCE WORKED; BLOCK WAS CAUSED BY AN INCOMPLETE ACCEPTANCE-CLASSIFIER INVOCATION, NOT BY A PROVEN LIVE OWNERSHIP FAILURE`

Task 120 stopped before mutation and preserved a coherent machine. The acceptance task had invoked `classify-install` with only workspace/app-data, while the candidate's interrupted-rollover/re-entry contract requires current plugin inventory plus the expected candidate plugin fingerprint for attested classification.

The exact production installer already computes and supplies those values. No production-source change is justified by Task-120 evidence.

## Exact Task-121 candidate

Unchanged exact candidate:

- source SHA `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact ID `9691451156`;
- artifact name `cogentnexus-openclaw-v0.9.3-package-proof-01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

Exact-SHA CI:

- Validate `33185349482` success;
- Windows Installer Pack Smoke `33185349413` success;
- PS5.1 Acceptance Smoke `33185349400` success.

## Task 121 corrected read-only gate

Freshly verify provenance and machine state, then reproduce the production-equivalent classifier inputs without mutating live OpenClaw state:

- prepare only the isolated exact candidate plugin with `npm ci` and `npm run plugin:validate`;
- compute candidate plugin fingerprint with the candidate ownership script;
- capture current `openclaw plugins list --json` exactly;
- call `classify-install` with `--plugin-inventory-json` and `--expected-replacement-fingerprint`;
- require the returned classification to agree with manifest/filesystem/inventory evidence.

No manual ownership normalization is permitted.

## Authorized one-shot sequence

Only after the attested preflight passes:

`install-over -> reset y -> uninstall y -> fresh reinstall same artifact -> stop -> start -> restart -> recovery harness -> final read-only snapshot`

Task 120 executed none of these disruptive phases, so Task 121 retains one authorized attempt for each.

Canonical install/install-over command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No installer `-Provider` argument.

## Fail-stop rule

Each disruptive phase may execute at most once. On first non-zero, ambiguous classification, ownership mismatch, integrity failure, or failed postcondition:

- stop;
- preserve evidence;
- do not replay;
- do not manually clean/normalize;
- publish the exact Task-121 failure boundary.

## Prohibited during Task 121

- candidate/artifact substitution;
- source/live ad-hoc repair;
- manual manifest/plugin/state cleanup or normalization;
- replay of failed/completed disruptive phases;
- OpenClaw changes/rebaseline;
- provider runtime/config/model/endpoint/timeout changes;
- unrelated plugin/workspace mutation;
- credential/secret access;
- Dashboard semantic Send;
- reboot/process-tree kill;
- merge/tag/release/force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-121-v093-real-windows-lifecycle-acceptance-attested-reentry.md`

After publishing, stop for independent ChatGPT review. Do not create or execute the final Dashboard durable-delivery task automatically.
