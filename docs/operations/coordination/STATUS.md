# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_TDD_REPAIR`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 117 authorizes source/diagnosis/test/CI/package repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-117-installer-provider-binding-origin-repair.md`](tasks/CNX-20260828-117-installer-provider-binding-origin-repair.md)

Task ID:

`CNX-20260828-117`

## Task 116 accepted failure

Report:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate-review.md`

Verdict:

`ACCEPTED FAIL — CLEAN PRE-BODY PARAMETER-BINDING FAILURE; SUCCESSOR DIAGNOSIS/REPAIR REQUIRED`

Task 116 freshly proved the real Windows state coherent before mutation:

- OpenClaw `2026.7.1-2` exact;
- Ollama selected/healthy;
- CNX passthrough generation 25;
- Gateway healthy;
- SQLite integrity `ok`;
- exact supported interrupted-reentry classification;
- no legacy namespace evidence.

The single authorized install-over then failed during PowerShell parameter binding before installer-body execution:

```text
Cannot validate argument on parameter 'Provider'. The argument "3D Objects" does not belong to the set "ollama" specified by the ValidateSet attribute.
```

No replay occurred. Reset, uninstall, fresh reinstall, stop/start/restart, recovery harness, and Dashboard semantic Send were not executed. Post-failure read-only evidence remained coherent.

## Task 117 root-cause gate

Frozen Task-116 source inspection shows `scripts/install.ps1` exposes:

```powershell
[ValidateSet("ollama")]
[string]$Provider = "ollama"
```

but `$Provider` is otherwise unused and v0.9.3 is Ollama-only.

The exact origin of `3D Objects` must be traced through the actual caller/binding data flow before production repair. The required order is:

`preserved invocation evidence -> isolated non-mutating reproduction -> TESTS-ONLY RED -> minimal repair -> GREEN -> targeted/full validation -> exact candidate CI/package proof -> report`

A trivial explicit `-Provider "3D Objects"` test does not by itself reproduce the Task-116 unexpected resolution path.

Preferred design invariant: no unnecessary provider-selection input in the Ollama-only installer. Remove the dead Provider surface only if root-cause evidence shows it participates in the real failure; otherwise repair the actual repository caller/helper.

## Live mutation fence

Task 117 does not authorize any live lifecycle mutation. In particular:

- do not replay Task-116 install-over;
- do not reset/uninstall/reinstall;
- do not run live stop/start/restart or recovery harness;
- do not manually clean/normalize residue;
- do not change OpenClaw/Ollama/provider/model/configuration;
- do not mutate live SQLite/manifest/plugin/session state;
- do not access credentials/secrets;
- do not send Dashboard semantic content.

Read-only inspection of the preserved Task-116 evidence root and isolated Windows diagnostic reproduction is allowed.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-117-installer-provider-binding-origin-repair.md`

After publishing, stop for independent ChatGPT review. A new real-Windows lifecycle retry may be opened only after Task 117 passes independent review on an exact repaired candidate.
