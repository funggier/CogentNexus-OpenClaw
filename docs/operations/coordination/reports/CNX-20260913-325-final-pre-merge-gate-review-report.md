# CNX-20260913-325 — Final Pre-Merge Gate Review Report

**Date:** 2026-09-13 13:45 GMT+7
**Repository:** `funggier/CogentNexus-OpenClaw`
**PR:** #38
**Candidate SHA:** `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
**Coordination authority:** `coord/v0.9.5-final-acceptance`

---

## 1. Candidate SHA Verification

| Field | Value |
|---|---|
| Expected candidate | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| PR #38 headRefOid | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| Branch commit.sha | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |

**Result: MATCH ✅** Candidate SHA is intact and exact.

---

## 2. PR State

| Field | Value |
|---|---|
| state | `OPEN` |
| closed | `false` |
| mergedAt | `null` |
| isDraft | `false` |
| mergeable | `MERGEABLE` |
| mergeStateStatus | `UNSTABLE` |

**Result: PR OPEN, merged=false ✅**

---

## 3. Main HEAD and Mergeability

| Field | Value |
|---|---|
| Main HEAD SHA | `6439dd963003856ee1b1f1f6f802fa2aa60d6612` |
| Main HEAD message | `coord: authorize v0.9.5 acceptance successor candidate` |
| Main HEAD date | `2026-09-13T03:42:56Z` |
| PR ahead of main | 9 commits |
| PR behind main | 0 commits |

**Result: PR is fast-forward ahead of main (9 ahead, 0 behind). Clean linear history. ✅**

---

## 4. Release-Gating CI (all on exact candidate SHA)

### 4.1 Validate

| Field | Value |
|---|---|
| Run ID | `34759839059` |
| Workflow | `Validate` |
| Head SHA | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| Conclusion | `SUCCESS` |
| Event | `pull_request` |

### 4.2 PS5.1 Acceptance Smoke

| Field | Value |
|---|---|
| Run ID | `34759839056` |
| Workflow | `PS5.1 Acceptance Smoke` |
| Head SHA | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| Conclusion | `SUCCESS` |
| Event | `pull_request` |

### 4.3 Windows Installer Pack Smoke

| Field | Value |
|---|---|
| Run ID | `34759839053` |
| Workflow | `Windows Installer Pack Smoke` |
| Head SHA | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| Conclusion | `SUCCESS` |
| Event | `pull_request` |

**Result: All release-gating CI = SUCCESS ✅**

---

## 5. Supporting CI

### 5.1 PS5.1 Live Runner Smoke

| Field | Value |
|---|---|
| Run ID | `34759839049` |
| Workflow | `PS5.1 Live Runner Smoke` |
| Head SHA | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| Conclusion | `SUCCESS` |
| Event | `pull_request` |

**Result: Supporting CI = SUCCESS ✅**

---

## 6. Legacy Failure Analysis

### 6.1 Run Details

| Field | Value |
|---|---|
| Run ID | `34759839091` |
| Workflow | `PS5.1 v0.9.3 Ollama Recovery Reality Smoke` |
| Workflow ID | `339904013` |
| Head SHA | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| Head branch | `feat/v0.9.5-release-readiness-clean` |
| Event | `pull_request` |
| Conclusion | `FAILURE` |
| Status | `completed` |

### 6.2 Failed Step

**Step name:** `Parse Windows installer and require provider-neutral contract`

**Error message:**
```
Windows installer is not wired to the v0.9.3 CogentNexus-OpenClaw CLI facade.
```

### 6.3 Root Cause Analysis

The legacy workflow `ps51-v093-recovery-reality-smoke.yml` contains this assertion:

```powershell
if ($text -notmatch 'cnxclaw_v093\.py') { throw 'Windows installer is not wired to the v0.9.3 CogentNexus-OpenClaw CLI facade.' }
```

PR #38 intentionally changed `scripts/install.ps1` from:
```powershell
$cliScript = Join-Path $targetSkill "scripts\cnxclaw_v093.py"
```
to:
```powershell
$cliScript = Join-Path $targetSkill "scripts\cnxclaw.py"
```

This is the **correct v0.9.5 migration** — the provider-neutral canonical CLI (`cnxclaw.py`) replaces the v0.9.3-specific facade (`cnxclaw_v093.py`). The legacy workflow's assertion is a v0.9.3-specific contract that is **expected to fail** on a v0.9.5 candidate.

### 6.4 Trigger Analysis

The legacy workflow triggers on `pull_request` with path filters including:
- `scripts/install.ps1`
- `scripts/install.sh`

PR #38 modified both files, which correctly triggered the legacy workflow. The trigger is legitimate but the assertion is stale.

### 6.5 Conclusion

| Question | Answer |
|---|---|
| Is this a v0.9.3 legacy workflow? | **Yes** — name and assertions are v0.9.3-specific |
| Triggered by shared installer path filter? | **Yes** — `scripts/install.ps1` and `scripts/install.sh` |
| Failure is stale v0.9.3-specific assertion? | **Yes** — requires `cnxclaw_v093.py` which was intentionally replaced |
| Is this a v0.9.5 runtime/provider/product defect? | **No** — the v0.9.5 migration is correct |

**Result: Legacy failure is a false positive. Expected behavior on v0.9.5 candidate. ✅**

---

## 7. Required-Check / Branch-Protection Semantics

### 7.1 Branch Protection Status

```
GET /repos/funggier/CogentNexus-OpenClaw/branches/main/protection
→ HTTP 404: Branch not protected
```

**Main branch has NO branch protection rules. No required checks are enforced by GitHub.**

### 7.2 UNSTABLE Status Interpretation

GitHub's `mergeStateStatus=UNSTABLE` is an automated status computed from check runs. It is **not** a required-check enforcement. When a branch is unprotected:

- Failed checks do NOT block merge
- UNSTABLE is informational, not authoritative
- The PR remains `MERGEABLE` regardless of check status

### 7.3 Required-Check Determination

| Check | Required? | Blocks merge? |
|---|---|---|
| Validate | No (branch unprotected) | No |
| PS5.1 Acceptance Smoke | No (branch unprotected) | No |
| Windows Installer Pack Smoke | No (branch unprotected) | No |
| PS5.1 Live Runner Smoke | No (branch unprotected) | No |
| PS5.1 v0.9.3 Ollama Recovery Reality Smoke | No (branch unprotected) | **No** |

**Result: Legacy failure does NOT block merge. Branch is unprotected. ✅**

---

## 8. PR Diff High-Level Review

### 8.1 Changed Files (33 total)

| Category | Files |
|---|---|
| Workflow | `.github/workflows/validate.yml` |
| Version metadata | `VERSION`, `plugins/cogentnexus-openclaw/package.json`, `plugins/cogentnexus-openclaw/openclaw.plugin.json`, `plugins/cogentnexus-openclaw/package-lock.json` |
| Installer scripts | `scripts/install.ps1`, `scripts/install.sh` |
| Core scripts | `scripts/check_baseline_consistency.py`, `skills/cogentnexus-openclaw/scripts/checks.py`, `skills/cogentnexus-openclaw/scripts/namespace_ownership.py` |
| Documentation | `README.md`, `docs/BASELINE.md`, `docs/CHECK_SYSTEM.md`, `docs/CLEAN_REINSTALL.md`, `docs/CLEAN_REINSTALL.th.md`, `docs/CURRENT_STATE.md`, `docs/INSTALL.md`, `docs/INSTALL.th.md`, `docs/PROVIDERS.md`, `docs/releases/v0.9.5.md`, `docs/operations/acceptance/V095_PROVIDER_SWITCH_ACCEPTANCE.md`, `docs/operations/acceptance/V095_WINDOWS_INSTALL_OVER_ACCEPTANCE.md`, `docs/operations/coordination/reports/CNX-20260912-release-readiness-audit.md` |
| Plugin metadata | `plugins/cogentnexus-openclaw/README.md`, `skills/cogentnexus-openclaw/SKILL.md`, `skills/cogentnexus-openclaw/templates/lifecycle/README.md` |
| Tests | `tests/test_baseline_checker_v093.py`, `tests/test_baseline_contract.py`, `tests/test_lifecycle_v092.py`, `tests/test_namespace_install_contract.py`, `tests/test_namespace_ownership.py`, `tests/test_plugin_generation_rollover.py`, `tests/test_release_version_094_contract.py`, `tests/test_v091_install_wiring.py`, `tests/test_v095_checks_canonical_state.py`, `tests/test_v095_installer_cli_contract.py`, `tests/test_v095_installer_npm_stderr_boundary.py`, `tests/test_v095_installer_state_compat.py` |

### 8.2 Unexpected Files Check

| Check | Result |
|---|---|
| Unexpected files | **None** — all files are v0.9.5 metadata/docs/tests |
| Unrelated changes | **None** — all changes are v0.9.5 convergence |
| Release/tag artifacts | **None** — no tag or release created |
| Provider/model/config mutation | **None** — no provider config changed |
| Unauthorized workflow mutation | **None** — only `validate.yml` updated to verify 0.9.5 metadata |

### 8.3 Key Source Changes

**`scripts/install.ps1`:**
```diff
-$cliScript = Join-Path $targetSkill "scripts\cnxclaw_v093.py"
+$cliScript = Join-Path $targetSkill "scripts\cnxclaw.py"
```

**`scripts/install.sh`:**
```diff
-CLI_SCRIPT="$TARGET_SKILL/scripts/cnxclaw_v093.py"
+CLI_SCRIPT="$TARGET_SKILL/scripts/cnxclaw.py"
```

**`scripts/check_baseline_consistency.py`:**
```diff
+EXPECTED_VERSION = "0.9.5"
```

**`.github/workflows/validate.yml`:**
- Updated version assertions from `0.9.4` → `0.9.5`
- Updated artifact name from `cogentnexus-openclaw-v0.9.4` → `cogentnexus-openclaw-v0.9.5`
- Updated release notes path from `v0.9.4.md` → `v0.9.5.md`

**Result: All changes are expected v0.9.5 migration. No unexpected mutations. ✅**

---

## 9. Safety Fences Verification

| Fence | Status | Evidence |
|---|---|---|
| No force-push | ✅ | Branch history is linear, 9 commits ahead of main |
| No history rewrite | ✅ | All commits are unique, no force-push detected |
| No tag movement | ✅ | No v0.9.5 tags exist |
| No GitHub Release | ✅ | No v0.9.5 releases exist |
| No provider/model/config mutation | ✅ | No provider config files changed |
| No unrelated service/Scheduled Task changes | ✅ | No Windows service or task changes |

**Result: All safety fences intact. ✅**

---

## 10. Final Decision

### Decision: `READY_FOR_SEPARATE_MERGE_DECISION`

### Rationale

1. **Candidate SHA is exact and intact** — `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23`
2. **PR is OPEN and unmerged** — state confirmed via GitHub API
3. **All release-gating CI passes** — Validate, PS5.1 Acceptance Smoke, Windows Installer Pack Smoke all SUCCESS on exact candidate SHA
4. **Supporting CI passes** — PS5.1 Live Runner Smoke SUCCESS
5. **Legacy failure is a false positive** — v0.9.3 assertion correctly fails on v0.9.5 migration; not a product defect
6. **Legacy failure does NOT block merge** — main branch is unprotected, no required checks enforced
7. **PR diff is clean** — all changes are expected v0.9.5 metadata convergence
8. **All safety fences intact** — no force-push, no tags, no releases, no mutations

### What This Decision Means

- The candidate has passed all automated gates
- The legacy failure is expected and non-blocking
- **Merge is NOT authorized by this report** — it is a separate operator decision
- If the operator chooses to merge, they should be aware of the UNSTABLE status and confirm they accept the legacy false positive

### Blockers

**None.** No genuine v0.9.5 defect found.

---

## 11. Evidence Summary

| Evidence | Value |
|---|---|
| Candidate SHA | `fc3f4bc0b1946815fb9063fb7a9d0675e1eb5a23` |
| Main HEAD SHA | `6439dd963003856ee1b1f1f6f802fa2aa60d6612` |
| PR #38 state | OPEN, merged=false |
| PR #38 mergeable | MERGEABLE |
| PR #38 mergeStateStatus | UNSTABLE (informational only) |
| Validate | SUCCESS (run 34759839059) |
| PS5.1 Acceptance Smoke | SUCCESS (run 34759839056) |
| Windows Installer Pack Smoke | SUCCESS (run 34759839053) |
| PS5.1 Live Runner Smoke | SUCCESS (run 34759839049) |
| Legacy failure | Expected false positive (run 34759839091) |
| Branch protection | None (unprotected) |
| v0.9.5 tags | None |
| v0.9.5 releases | None |

---

*Report generated by Hermes Agent — CNX-20260913-325*
*Coordination authority: coord/v0.9.5-final-acceptance*
*Timestamp: 2026-09-13 13:45 GMT+7*
