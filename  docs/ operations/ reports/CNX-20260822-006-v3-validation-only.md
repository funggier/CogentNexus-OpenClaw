# CNX-20260822-006 — V3 validation-only report

Status: PASS
Task ID: CNX-20260822-006
Repository: `funggier/cogentnexus`
Branch: `agent/v0.9.3-recovery-reality-tests`
Worktree: `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260822-006-v3-validation-only-20260822-2246`
Start HEAD: `ef1f89eaf51749b741e0c14c32b1dc2e4248e456`

## Source and isolation gates

- Required ancestors present: `592a6fbd37da05013b7a8a5875ccd8b17e188cfa`, `929fbcc663251941d88f38f09544068a9b3e069d`.
- Harness `scripts/test-v093-ollama-recovery-windows-v3.ps1`: expected blob `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`; matched.
- Workflow `.github/workflows/v093-ollama-recovery-v3-smoke.yml`: expected blob `35b6796e4868447cfe3db6a86a7528d0288c8411`; matched.
- Initial and final isolated-worktree status were clean before this report.

## Commands and results

- `python tests/test_provider_recovery_authority.py` — exit 0; 4 tests passed.
- `python tests/test_provider_recovery_v092.py` — exit 0; 7 tests passed.
- `python tests/test_checks_v092.py` — exit 0; 5 tests passed.
- Windows PowerShell parser validation using `System.Management.Automation.Language.Parser::ParseInput` — exit 0; no parse errors.
- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -SyntaxOnly` — exit 0; syntax/load PASS.
- Local corrected workflow contract inspection — PASS. Required calls recorded: `Wait-DurableConvergence 'converge-gateway-after'`, `Wait-DurableConvergence 'converge-provider-after' $true`, and `Wait-DurableConvergence 'converge-after-operator-start'`. Forbidden immediate assertions rejected: `Assert-Baseline 'gateway-after'`, `Assert-Baseline 'provider-after'`, and `Assert-Baseline 'operator-after'`; legacy wrong status-field assertions rejected.
- `git diff --check` — exit 0.
- `git status --short` — clean before report creation; after report creation only this matching report was changed.

## CI evidence

All applicable workflows for start HEAD `ef1f89eaf51749b741e0c14c32b1dc2e4248e456` completed successfully in run `32582614985`:

| Workflow/job | Result |
|---|---|
| Validate / package dry-run (no publish), job `97054166492` | success |
| Validate / windows-latest, Python 3.14, job `97054166603` | success |
| Validate / ubuntu-latest, Python 3.14, job `97054166612` | success |
| Validate / macos-latest, Python 3.11, job `97054166639` | success |
| Validate / ubuntu-latest, Python 3.11, job `97054166646` | success |
| Validate / windows-latest, Python 3.11, job `97054166653` | success |
| Validate / macos-latest, Python 3.14, job `97054166661` | success |

Previously required evidence was re-verified: workflow-fix commit `929fbcc663251941d88f38f09544068a9b3e069d`; v3 smoke run `32582330616`; job `97053475362`; all success, including Windows PowerShell 5.1 parser, `-SyntaxOnly`, and status/safety contract. The workflow-fix commit is distinct from STATUS documentation commit `769416ef269e13fa106b323607cac13325ea03e8`.

## Safety and scope

No disruptive scenario, `-RunDisruptive`, lifecycle command, PID/process modification, package installation, or source/test/workflow edit was performed. No unrelated files or worktrees were modified. No items remain unproven for this validation-only task.

## Recommended next step

The later full-suite command is:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive`
