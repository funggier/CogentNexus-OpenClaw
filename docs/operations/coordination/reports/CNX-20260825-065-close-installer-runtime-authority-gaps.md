# CNX-20260825-065 — Close Installer Runtime-Authority Gaps Report

Result: `PASS_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`

Executor: Hermes (manual operator continuation signal)
Fetched execution HEAD: `77dd425` (`coord: publish Task 065 installer closure status`; local == remote; Task 064 review commit `5fe706d8…` verified ancestor)
Implementation HEAD: `21686f70520c5e0263e8aea4d644d2c87324e872`
Publication fence: this final commit adds ONLY this report file relative to implementation HEAD `21686f70…`; independently verified via `git ls-remote` after push.

## RED evidence (against Task 064 source `6e424511…`)

Executable tests in `tests/test_installer_runtime_authority.py` run before any production edit:

- T1/B5 RED — the committed installer contained a literal line break inside `scripts\runtime_authority.py`; exact-path assertion failed.
- T2/B6 executable — stale manifest with `python.exe` deliberately left present was NOT repaired by the old conditional ensure (`Test-Path $ownedPython` guard skipped it).
- T4/B6 RED — a deleted/broken `pythonw.exe` was accepted as healthy because reuse only probed foreground.
- T3/B7 RED — MANAGED enable / final status still invoked ambient bare `python`.

## Production corrections

### B5 — one explicit runtime-authority script variable
```powershell
$runtimeAuthorityScript = Join-Path $targetSkill "scripts\runtime_authority.py"
if (-not (Test-Path -LiteralPath $runtimeAuthorityScript)) { throw "..." }
```
Single-line literal, no embedded CR/LF anywhere in any `Join-Path $targetSkill "…"` argument (T1 now asserts this for every such literal plus the exact runtime-authority path).

### B6 — unconditional ensure/validation before durable definitions
`ensure-runtime --application-data-root <exact-product-root>` runs on EVERY install/install-over. The manifest JSON is parsed and BOTH `$ownedPython`/`$ownedPythonw` must exist before launcher/task/lifecycle definitions are written. On the reuse path, `ensure_runtime()` now capability-probes BOTH interpreters (`_probe_foreground` stdlib probe + `_probe_background` sentinel-file probe). A broken background interpreter deterministically triggers safe recreation inside the product boundary or fails closed — never registered as healthy.

### B7 — post-provision authority transition
After provisioning, these execute under `$ownedPython`: MANAGED `enable --provider ollama`, final `status`, `namespace_ownership.py verify`, plugin resolution (`@ownershipArguments`), and `runtime.py supervisor doctor`. Pre-provision bootstrap calls (classify-install, preflight, validate/init, rollover plan/apply at lines ≤288) intentionally remain on bootstrap Python: they necessarily precede provisioning or require PyYAML, are documented bootstrap-only, and none of them is persisted into launcher/task/manifest authority. The generated `cnxclaw.cmd` continues to invoke the owned foreground interpreter exactly.

## GREEN + verification

| Step | Command | Result |
|---|---|---|
| Focused GREEN | `pytest tests/test_installer_runtime_authority.py -q` | 7 passed |
| FULL suite | `pytest tests/ -q` (dev venv) | **302 passed, 2 skipped, 0 failed** |
| Canonical validator | `python scripts/check_baseline_consistency.py` | PASS (Bridge v0.9.3) |
| Whitespace fence | `git diff --check` | clean |
| Worktree after impl commit | `git status --porcelain` | clean |

Prior Task 064 coverage preserved and passing (T5): exact product-root semantics, real Windows provisioning, startup fail-closed against foreign executor `sys.executable`, owned launcher execution, CLI import capability, no-console spawn flags, `startup_v092.py → host_control_v092.py`.

## Live mutation accounting

No live install/install-over/uninstall/reset; no lifecycle mutation; no Scheduled Task change/run/end; no Gateway/Ollama/provider/plugin/config/AGENTS/ownership/SQLite write; no process termination; no primary-workspace git mutation. All tests used temp boundaries outside `%LOCALAPPDATA%\CogentNexus-OpenClaw`.

## Commits

1. Implementation/tests: `21686f70520c5e0263e8aea4d644d2c87324e872`
2. Report-only publication commit: this commit.

## Result

`PASS_INSTALLER_RUNTIME_AUTHORITY_GAPS_CLOSED`
