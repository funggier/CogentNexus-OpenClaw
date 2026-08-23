# CNX-20260822-006 — Validate Corrected V3 Smoke Without Source Changes

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  
Predecessor: `CNX-20260822-005` (BLOCKED)

## Objective

Complete the remaining non-disruptive validation for the already-published v3 convergence harness and corrected smoke contract.

This is validation-only. Do not edit runtime code, the harness, tests, or workflows.

## Source gates

Repository: `funggier/cogentnexus`  
Branch: `agent/v0.9.3-recovery-reality-tests`  
Required harness implementation ancestor: `592a6fbd37da05013b7a8a5875ccd8b17e188cfa`  
Required workflow-fix ancestor: `929fbcc663251941d88f38f09544068a9b3e069d`  
Harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`  
Expected harness blob: `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`  
Workflow: `.github/workflows/v093-ollama-recovery-v3-smoke.yml`  
Expected workflow blob: `35b6796e4868447cfe3db6a86a7528d0288c8411`

Later coordination/report/documentation-only commits are allowed. Before validation, fetch the branch, verify both required ancestors, verify both exact blobs, use a clean isolated worktree, and record `git status --short`.

If either code blob differs, report `BLOCKED`. Do not edit it.

## Proven GitHub evidence to re-verify

Workflow correction commit: `929fbcc663251941d88f38f09544068a9b3e069d`  
V3 smoke run: `32582330616`  
V3 smoke job: `97053475362`

The job is expected to show:

- Windows PowerShell 5.1 parser and `-SyntaxOnly`: success;
- status schema and safety contract: success;
- overall conclusion: success.

Do not treat this as a substitute for the required direct local unittests.

## Required direct validation

Do not install `pytest` or any package. Run exactly:

`python tests/test_provider_recovery_authority.py`

`python tests/test_provider_recovery_v092.py`

`python tests/test_checks_v092.py`

Also run and record:

1. Windows PowerShell 5.1 parser validation for `scripts/test-v093-ollama-recovery-windows-v3.ps1`;
2. the v3 harness with `-SyntaxOnly`;
3. the corrected workflow contract locally, including the three required convergence calls and rejection of the three forbidden immediate assertions;
4. `git diff --check`;
5. final `git status --short`.

Record every exact command, output summary, and exit code.

## Applicable CI gate

Record the exact branch HEAD at task start. It may be a documentation-only descendant of the two required implementation commits.

Use bounded read-only observation until all applicable workflows for that start HEAD have completed. Every required workflow must succeed. A cancelled/skipped workflow is acceptable only if the report proves it was concurrency-superseded by a later documentation-only coordination commit and the replacement run for identical code completed successfully; otherwise report `BLOCKED`.

Explicitly include the v3 smoke run/job above and a complete workflow status table.

Do not manually rerun workflows.

## Allowed changes

Only the matching Codex report may be added.

Do not change:

- the harness;
- workflows;
- runtime implementation;
- tests;
- ChatGPT-owned coordination files.

## Safety invariants

- no disruptive scenario and no `-RunDisruptive`;
- no PID kill or process modification;
- no `cnx start`, `cnx stop`, `cnx reset`, or `cnx uninstall`;
- no install/uninstall/reset/reinstall action;
- no package installation;
- no process-tree kill;
- no change to v0.9.2, LM Studio scope, exact-PID safety, or event/durable-evidence recovery authority;
- preserve unrelated worktrees and files.

## Acceptance criteria

PASS requires:

- every source/isolation gate passes;
- all three direct unittest files pass;
- parser and `-SyntaxOnly` pass;
- corrected local contract passes;
- exact required and forbidden calls are recorded;
- `git diff --check` passes;
- exact start HEAD, both implementation commits, both blobs, and complete CI are recorded;
- v3 smoke run `32582330616` / job `97053475362` is confirmed successful;
- only the matching report changes;
- no disruptive/runtime/lifecycle action occurs;
- the Task 005 provenance error is corrected: `929fbcc663251941d88f38f09544068a9b3e069d` is the workflow-fix commit, while `769416ef269e13fa106b323607cac13325ea03e8` is a STATUS documentation commit.

## Report

Write:

`docs/operations/coordination/reports/CNX-20260822-006-v3-validation-only.md`

Include source gates, exact commands and exit codes, test counts/results, parser/syntax/contract evidence, complete CI table, changed files, safety notes, all remaining unproven items, and the exact recommended later full-suite command:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive`

Commit message must begin:

`report: CNX-20260822-006`

Never force-push. Stop after publishing the report.
