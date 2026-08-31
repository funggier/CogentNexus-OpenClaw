# CNX-20260828-116 — Independent Review

## Verdict

`ACCEPTED FAIL — CLEAN PRE-BODY PARAMETER-BINDING FAILURE; SUCCESSOR DIAGNOSIS/REPAIR REQUIRED`

Task 116 is accepted as a valid live-acceptance failure. Its Phase 0 read-only evidence proves the live Windows state was coherent enough to enter the lifecycle gate, but the single authorized install-over invocation failed during PowerShell parameter binding before the installer body executed. The executor correctly stopped, did not replay the command, and did not continue to reset/uninstall/reinstall/lifecycle/recovery phases.

## Accepted evidence

The Task-116 report establishes:

- frozen source `47b069daed90f54feae2c9eb26f38c438493f3c8` and artifact `9687249771` were re-verified;
- Windows/OpenClaw/Ollama/CNX/Gateway baseline was healthy and consistent;
- OpenClaw remained exactly `2026.7.1-2`;
- selected provider was `ollama` and healthy;
- SQLite `PRAGMA integrity_check = ok`;
- current ownership classification was the exact supported interrupted-reentry shape:
  - `mode=upgrade`;
  - `pendingRollover=false`;
  - `pluginAlreadyExact=true`;
  - `interruptedRolloverReentry=true`;
  - canonical direct replacement present;
  - retired manifest path absent;
  - `legacy=[]`;
- install-over was attempted once and returned root exit code `1`;
- error text was:

```text
Cannot validate argument on parameter 'Provider'. The argument "3D Objects" does not belong to the set "ollama" specified by the ValidateSet attribute.
```

- no subsequent destructive lifecycle phase ran;
- post-failure read-only state remained healthy/coherent;
- no Dashboard semantic Send occurred.

## Independent source inspection

The frozen candidate `scripts/install.ps1` declares:

```powershell
[ValidateSet("ollama")]
[string]$Provider = "ollama"
```

but the `$Provider` variable is otherwise unused by installer behavior. The installer is already Ollama-only and later prints `Provider: ollama` literally.

This creates an important diagnostic constraint:

- the Task-116 documented command supplies `-Workspace` only;
- with ordinary direct binding, the script-local Provider default should therefore be `ollama`;
- the observed value `3D Objects` cannot be attributed to normal execution of the shown default expression alone.

Therefore `"3D Objects" supplied to Provider` is the proven failure symptom/boundary, but the precise origin of that bad bound value is not yet independently proven from repository evidence.

## Required root-cause direction

The successor task must trace the bad value across the actual invocation boundary before production code is changed. At minimum it must determine whether `3D Objects` originated from:

1. the acceptance executor/caller argument construction or splatting;
2. PowerShell parameter-default/binding state such as `$PSDefaultParameterValues` or another ambient caller binding mechanism;
3. command-tokenization/argument-array construction in the executor;
4. another concrete invocation layer that can be reproduced from evidence.

The successor must inspect the preserved Task-116 evidence and reproduce the binding behavior on Windows without mutating the live CNX/OpenClaw/Ollama installation.

## TDD requirement

No production fix is authorized before a semantic RED exists.

The first implementation commit must be tests/diagnostic-harness only and must reproduce the actual binding failure or the proven faulty caller behavior. A test that merely passes `-Provider "3D Objects"` explicitly is insufficient by itself because that only re-demonstrates the existing `ValidateSet` contract rather than the Task-116 unexpected resolution path.

After RED is proven, make one minimal fix at the actual source of the bad value.

Because v0.9.3 is Ollama-only and `$Provider` is a dead input surface, removing that unnecessary installer parameter is a plausible minimal hardening outcome **only if** root-cause evidence demonstrates that the exposed parameter surface participates in the real failure. Do not pre-commit to this fix if the actual defect is in a repository caller/helper instead.

## Live-machine fence

The successor is source/diagnosis/test/CI/package work only. It must not:

- replay Task 116 install-over;
- run reset/uninstall/reinstall/stop/start/restart/recovery harness;
- manually normalize ownership or residue;
- alter OpenClaw/Ollama/provider/model/configuration;
- touch credentials/secrets;
- send a Dashboard semantic message;
- clean Task-107/Task-116 live residue.

Read-only inspection of the preserved Task-116 evidence and read-only process/environment/PowerShell invocation diagnostics is allowed when necessary to establish root cause.

## Acceptance requirement for successor

A successor candidate may advance only after:

1. exact root cause is reproduced and documented;
2. tests-only RED precedes production repair;
3. minimal repair turns RED to GREEN;
4. direct PowerShell 5.1 invocation using the same Task-116 command shape binds/uses Ollama deterministically;
5. relevant installer/ownership/lifecycle-action suites pass;
6. full validation passes;
7. exact candidate passes Validate, Windows Installer Pack Smoke, and PS5.1 Acceptance Smoke;
8. a new package-proof artifact is independently identity/hash verified;
9. independent review accepts the repaired candidate before any new real-Windows lifecycle retry.

## Final review decision

Task 116 itself is closed as `FAIL`, safely and correctly. The repository/source gate remains strong except for this newly exposed Windows installer invocation/binding defect. A narrowly scoped successor source task is authorized to diagnose and repair it; live lifecycle mutation remains blocked until that successor passes independent review.
