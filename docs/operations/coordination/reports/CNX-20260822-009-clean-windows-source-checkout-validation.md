# CNX-20260822-009 — Clean Windows Source Checkout Validation

Status: `PASS`
Task ID: `CNX-20260822-009`
Repository: `funggier/cogentnexus`
Branch: `agent/v0.9.3-recovery-reality-tests`
Start HEAD: `9e53ca8b70a5865a5fc59d5723c4e9a31530c173`
Isolated checkout: `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260822-009-clean-windows-source-checkout-validation-20260823-001`

## Source and CI gates

All required ancestors are present at the start HEAD:

| Requirement | Result |
|---|---|
| Accepted validation ancestor `5a22d9479ad7d62c7a159e4b49e2bc3f79fb6171` | PASS |
| Harness implementation ancestor `592a6fbd37da05013b7a8a5875ccd8b17e188cfa` | PASS |
| Workflow-fix ancestor `929fbcc663251941d88f38f09544068a9b3e069d` | PASS |
| Exact-head applicable CI | PASS; eight workflows completed `success` |

Successful exact-head workflow runs included Validate `32583809623`, PS5.1 v0.9.3 Ollama Recovery V3 Smoke `32583809610`, PS5.1 v0.9.3 Gateway Convergence Smoke `32583809599`, PS5.1 v0.9.3 Ollama Recovery V2 Smoke `32583809625`, PS5.1 Live Runner Smoke `32583809627`, PS5.1 v0.9.3 Recovery Reality Smoke `32583809603`, Windows Installer Pack Smoke `32583809618`, and PS5.1 Acceptance Smoke `32583809606`. Duplicate superseded exact-head runs were cancelled; no workflow was manually rerun.

## Task 008 read-only diagnosis

Inspected the existing checkout `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260822-008-full-windows-v3-process-recovery-20260822-2330` without repair or cleanup. `git rev-parse HEAD` returned `26cedb9b4c2938cfe68dea536074765d601d14f4`. `git status --short` and `git status --porcelain=v1` showed 325 tracked deletions, including the required harness. `git ls-files --error-unmatch scripts/test-v093-ollama-recovery-windows-v3.ps1` succeeded, but the physical leaf check returned `False`. `git sparse-checkout list` reported `fatal: this worktree is not sparse`; no sparse configuration was changed. The source repository worktree listing was read-only. The checkout was not reset, cleaned, deleted, pruned, or reused.

## Fresh full-checkout proof

Redacted origin URL used: `https://github.com/funggier/cogentnexus.git`.

Commands executed (all exit code 0):

```text
git clone --no-local https://github.com/funggier/cogentnexus.git <new-task-009-path>
git checkout --detach 9e53ca8b70a5865a5fc59d5723c4e9a31530c173
```

The new checkout HEAD equals the start HEAD. `git status --porcelain=v1` was empty before validation and remained empty afterward. `git diff --name-only --diff-filter=D` was empty. The harness was tracked and present as a physical leaf at `scripts/test-v093-ollama-recovery-windows-v3.ps1`; its Git blob was `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`. File SHA256 was `5F2DBA46602CA88113B21A0DB8B729BC5AB8DA5FC45E9356F4072DDDD31E929F`, size `18782` bytes, last-write timestamp `2026-08-22T23:26:59.5647913+07:00`.

PowerShell parser validation returned zero errors. The exact load-only command:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -SyntaxOnly
```

returned exit code 0 and printed `CogentNexus v0.9.3 Ollama Recovery Reality harness v3 syntax/load: PASS`.

## Safety accounting

No runtime preflight or lifecycle command was run. No `openclaw`, `ollama`, or `cnx` command, process kill, confirmation input, disruptive harness mode, recovery scenario, evidence generation, package installation, source edit, reset, clean, delete, prune, repair, or force-push occurred.

## Verdict

PASS. Task 009 proves a reproducible clean full isolated checkout at the exact synchronized HEAD with the required harness and validation gates. Recommended next step: ChatGPT review this report before publishing any new task or disruptive authorization.
