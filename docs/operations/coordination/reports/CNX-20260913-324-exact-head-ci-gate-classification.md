# CNX-20260913-324 — Exact-Head CI Gate Classification

## Candidate & Authority

- **Task ID**: CNX-20260913-324
- **Parent**: CNX-20260913-322
- **Candidate SHA**: `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
- **PR**: #38 on `funggier/CogentNexus-OpenClaw`
- **PR Title**: chore: converge v0.9.5 release candidate
- **PR Branch**: `feat/v0.9.5-release-readiness-clean` -> `main`
- **PR State**: OPEN / UNSTABLE (UNSTABLE due to legacy failure)
- **Authority branch**: `coord/v0.9.5-final-acceptance`
- **Reviewer**: ChatGPT
- **Classification date**: 2026-09-13

## Objective

Classify every CI workflow run on exact candidate `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` into:
- RELEASE-GATING
- SUPPORTING
- LEGACY / STALE / NON-GATING

And determine whether any genuine v0.9.5 code defect exists.

---

## 1. Exact-Head Workflow Runs (Pull-Request Event)

All runs below are bound to the exact PR #38 head SHA `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`.

| # | Workflow | Run # | Status | Conclusion | Classification |
|---|----------|-------|--------|------------|----------------|
| 1 | Validate | 4299 | COMPLETED | **SUCCESS** | **RELEASE-GATING** |
| 2 | PS5.1 Acceptance Smoke | 3186 | COMPLETED | **SUCCESS** | **RELEASE-GATING** |
| 3 | PS5.1 Live Runner Smoke | 938 | COMPLETED | **SUCCESS** | **SUPPORTING** |
| 4 | Windows Installer Pack Smoke | 3177 | COMPLETED | **SUCCESS** | **RELEASE-GATING** |
| 5 | PS5.1 v0.9.3 Ollama Recovery Reality Smoke | 1273 | COMPLETED | **FAILURE** | **LEGACY / STALE / NON-GATING** |

---

## 2. Detailed Workflow Classification

### 2.1 RELEASE-GATING: Validate

- **Workflow ID**: 330791255
- **Path**: `.github/workflows/validate.yml`
- **Trigger**: push, pull_request (no path filter)
- **Matrix**: ubuntu-latest / windows-latest / macos-latest × Python 3.11 / 3.14
- **Steps**: namespace isolation, baseline consistency, validate.py --workspace-singleton, cogent/runtime/workflow self-tests, py_compile all host_control/startup/checks/provider/namespace_ownership scripts, pytest, benchmarks, plugin migration helper, npm pack dry-run
- **Run conclusion**: SUCCESS (all 7 matrix jobs passed)
- **Why gating**: Core repository validation that must pass before any merge.

### 2.2 RELEASE-GATING: PS5.1 Acceptance Smoke

- **Workflow ID**: 339649267
- **Path**: `.github/workflows/ps51-acceptance-smoke.yml`
- **Trigger**: push, pull_request (no path filter)
- **Job**: serializer — runs `scripts/accept-v092-windows.ps1 -SerializerSelfTestOnly` under Windows PowerShell 5.1
- **Run conclusion**: SUCCESS
- **Why gating**: Validates the v0.9.2+/v0.9.5 Windows acceptance serializer is syntactically valid and self-testable.

### 2.3 RELEASE-GATING: Windows Installer Pack Smoke

- **Workflow ID**: 339656795
- **Path**: `.github/workflows/windows-installer-pack-smoke.yml`
- **Trigger**: push, pull_request (no path filter)
- **Steps**: npm 12 pin, npm ci, npm run plugin:validate, verify installer uses plain local archive path, build and inspect npm 12 pack artifact, verify required entries
- **Run conclusion**: SUCCESS
- **Why gating**: Ensures the Windows installer packaging works correctly under npm 12 and the artifact contains required files.

### 2.4 SUPPORTING: PS5.1 Live Runner Smoke

- **Workflow ID**: 339791579
- **Path**: `.github/workflows/ps51-live-runner-smoke.yml`
- **Trigger**: push (branches: agent/v0.9.2-provider-preflight), pull_request (no path filter)
- **Steps**: Parse `scripts/run-v092-live-acceptance.ps1` with Windows PowerShell 5.1
- **Run conclusion**: SUCCESS
- **Why supporting (not strictly gating)**: Syntax-only validation of the live acceptance runner. Important for runner correctness but does not exercise product behavior.

### 2.5 LEGACY / STALE / NON-GATING: PS5.1 v0.9.3 Ollama Recovery Reality Smoke

- **Workflow ID**: 339904013
- **Path**: `.github/workflows/ps51-v093-recovery-reality-smoke.yml`
- **Trigger**: push (branches: agent/v0.9.3-recovery-reality-tests), pull_request (path-filtered to v0.9.3 files)
- **Conclusion**: FAILURE (job `syntax`)
- **Failure reason**: Stale v0.9.3 harness assertion. See Section 3.
- **Why legacy/non-gating**: This workflow enforces v0.9.3-specific process-safety markers and Ollama-only contract on `scripts/test-v093-recovery-reality-windows.ps1` and the v0.9.3 CLI facade (`cnxclaw_v093.py`, `provider_v093.py`). It was not updated for the v0.9.5 release candidate and is not a v0.9.5 release gate.

---

## 3. Legacy Failure Analysis: PS5.1 v0.9.3 Ollama Recovery Reality Smoke

### 3.1 Why This Workflow Triggered

The workflow's `pull_request` trigger includes these path filters:
```yaml
pull_request:
  paths:
    - 'scripts/test-v093-recovery-reality-windows.ps1'
    - 'scripts/install.ps1'
    - 'scripts/install.sh'
    - 'skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py'
    - 'skills/cogentnexus-openclaw/scripts/provider_v093.py'
    - 'docs/V093_RECOVERY_REALITY_TESTS.md'
    - 'docs/V093_OLLAMA_ONLY.md'
    - '.github/workflows/ps51-v093-recovery-reality-smoke.yml'
```

PR #38 touches `scripts/install.ps1` and `scripts/install.sh`, which match this path filter. The workflow ran despite being a v0.9.3 legacy test because the path filter is too broad — it catches any PR that touches the shared installer scripts.

### 3.2 What the Failing Step Asserts

The failing step is **"Enforce process-safety and Ollama-only harness surface"**, which checks for v0.9.3-specific markers in `scripts/test-v093-recovery-reality-windows.ps1`:

```powershell
$text = Get-Content '.\scripts\test-v093-recovery-reality-windows.ps1' -Raw
if ($text -match '(?i)lmstudio') { throw 'Recovery Reality harness must not contain LM Studio paths in v0.9.3.' }
if ($text -match '(?i)taskkill\.exe.*\/T') { throw 'Recovery Reality harness must not kill process trees.' }
foreach ($required in @('firefox.exe','powershell.exe','windowsterminal.exe','Stop-Process exact PID only')) {
  if ($text -notmatch [regex]::Escape($required)) { throw "Missing process-safety marker: $required" }
}
```

This step enforces the **v0.9.3** recovery reality test harness contract — not the v0.9.5 candidate contract.

### 3.3 Why This Is Not a v0.9.5 Runtime/Provider Failure

1. The failing workflow's name explicitly states **"v0.9.3"** — it is a legacy test from the v0.9.3 recovery reality phase.
2. The failing step checks for v0.9.3-specific markers (`firefox.exe`, `windowsterminal.exe`, `Stop-Process exact PID only`) that are relevant to the v0.9.3 recovery reality harness, not the v0.9.5 controller.
3. The workflow also checks that `install.ps1` and `install.sh` are wired to `cnxclaw_v093.py` — a v0.9.3 CLI facade. The v0.9.5 candidate uses `host_control_v092.py` and `cnxclaw.py`, not `cnxclaw_v093.py`.
4. The failure occurred in the `syntax` job, which only parses and checks PowerShell file syntax/content — it does not install, run, or test the v0.9.5 runtime.
5. The actual v0.9.5 runtime health, provider acceptance, idle quiescence, and controlled wake all PASS (see CNX-20260913-322 report).

### 3.4 Additional Legacy Workflow Steps That Would Fail

Even if the process-safety step passed, subsequent steps in the same workflow also enforce v0.9.3-specific contracts:

- **"Parse Windows installer and require provider-neutral contract"** asserts `install.ps1` must NOT have `[string]$Provider` and must contain `cnxclaw_v093.py` (the v0.9.3 facade). The v0.9.5 installer is wired to `host_control_v092.py`, so this step would also fail.
- **"Require POSIX installer provider-neutral contract"** asserts `install.sh` must NOT have `PROVIDER=` and must contain `cnxclaw_v093.py`. The v0.9.5 POSIX installer does not use `cnxclaw_v093.py`.
- **"Compile v0.9.3 Python facades"** runs `py_compile` on `provider_v093.py` and `cnxclaw_v093.py` — both legacy v0.9.3 files.

### 3.5 Verdict

This failure is a **STALE WORKFLOW CONTRACT**. The workflow was authored for the v0.9.3 recovery reality test phase and its path filter (`scripts/install.ps1`, `scripts/install.sh`) catches v0.9.5 PRs that touch the shared installer. The failure does NOT indicate any defect in the v0.9.5 candidate.

---

## 4. Workflows That Did Not Trigger

The following workflows did NOT run on the exact candidate SHA because their path filters or branch filters do not match PR #38:

| Workflow | Reason for not triggering |
|----------|---------------------------|
| Release | workflow_dispatch only; never auto-triggers |
| PS5.1 v0.9.3 Ollama Recovery V2 Smoke | Path filter: only `scripts/test-v093-ollama-recovery-windows-v2.ps1` |
| PS5.1 v0.9.3 Gateway Convergence Smoke | Path filter: only `scripts/test-v093-gateway-convergence-windows.ps1` |
| PS5.1 Partial Repair Smoke | Path filter: only `scripts/repair-v092-partial-windows.ps1` |
| All apply-* / patch-* / fix-* / normalize-* workflows | Push-only to specific feature branches; not pull_request |
| v0.8.x / v0.9.0 / v0.9.1 legacy workflows | Different branch/path triggers |
| v0.9.5-regenerate-lockfile-once | one-shot workflow; already consumed |
| v0.9.5-validation-convergence-once | one-shot workflow; already consumed |

---

## 5. Genuine v0.9.5 Code Defect Check

**Result: NO genuine v0.9.5 code defect found.**

Evidence:
- All RELEASE-GATING workflows pass (Validate, PS5.1 Acceptance Smoke, Windows Installer Pack Smoke).
- The SUPPORTING workflow (PS5.1 Live Runner Smoke) passes.
- The only failing workflow is a legacy v0.9.3 test that triggers due to an over-broad path filter.
- Local validation on the exact candidate: namespace isolation PASS, baseline consistency PASS, workspace singleton PASS.
- Live acceptance (CNX-20260913-322): runtime health PASS, Idle Quiescence PASS, Controlled Wake PASS.
- The v0.9.5 candidate code compiles cleanly under py_compile across all target platforms (ubuntu/windows/macos × Python 3.11/3.14).

---

## 6. Release-Gate Classification Summary

### RELEASE-GATING (must all pass)

| Workflow | Verdict |
|----------|---------|
| Validate (6 OS/Python combinations) | ✅ PASS |
| PS5.1 Acceptance Smoke | ✅ PASS |
| Windows Installer Pack Smoke | ✅ PASS |

### SUPPORTING (important but not final gate)

| Workflow | Verdict |
|----------|---------|
| PS5.1 Live Runner Smoke | ✅ PASS |

### LEGACY / STALE / NON-GATING (does not block v0.9.5 release)

| Workflow | Verdict | Reason |
|----------|---------|--------|
| PS5.1 v0.9.3 Ollama Recovery Reality Smoke | FAIL (stale) | v0.9.3 harness assertion; path filter over-broad; not a v0.9.5 release gate |

---

## 7. Final Recommendation

1. **The v0.9.5 candidate `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` CAN proceed.** All release-gating CI checks pass.

2. **The single CI failure (PS5.1 v0.9.3 Ollama Recovery Reality Smoke) is a false positive.** It is a legacy workflow from the v0.9.3 recovery reality phase whose path filter catches shared installer scripts. The failure is in v0.9.3 harness content assertions, not v0.9.5 runtime behavior.

3. **The PR #38 merge-state shows `UNSTABLE`** because GitHub counts the legacy failure as a required check context. The legacy workflow's `pull_request` trigger path filter should be tightened to exclude it from v0.9.5 PRs (or the workflow should be disabled/removed since v0.9.3 is a historical baseline).

4. **No code changes are required to the v0.9.5 candidate.** The failure is purely a workflow contract mismatch, not a product defect.

5. **No force-push, merge, tag, or release action is taken by this task.** Classification only.

---

## 8. Evidence Index

| Artifact | Location |
|----------|----------|
| Exact candidate SHA | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| PR #38 metadata | https://github.com/funggier/CogentNexus-OpenClaw/pull/38 |
| Validate run (PR) | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34759839059 |
| PS5.1 Acceptance Smoke run (PR) | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34759839056 |
| PS5.1 Live Runner Smoke run (PR) | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34759839049 |
| Windows Installer Pack Smoke run (PR) | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34759839053 |
| PS5.1 v0.9.3 Ollama Recovery Reality Smoke run (PR, FAILING) | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34759839091 |
| Legacy workflow definition | `.github/workflows/ps51-v093-recovery-reality-smoke.yml` |
| Idle Quiescence evidence | `C:/Users/CDQ-P/.hermes/workspace/cnx321/evidence/task322/idle-checker-normalized.json` |
| Task 322 final report | `docs/operations/coordination/reports/CNX-20260913-322-final-acceptance-report.md` |

---

Report generated: 2026-09-13
Candidate SHA: fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23
