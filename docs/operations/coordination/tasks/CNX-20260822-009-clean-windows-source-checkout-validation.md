# CNX-20260822-009 — Clean Windows Source Checkout Validation

Status: READY  
Owner: ChatGPT  
Executor: Codex  
Priority: current  
Predecessor: `CNX-20260822-008` (BLOCKED; harness never loaded and no runtime side effect)

## Objective

Diagnose the unusable Task 008 checkout and prove a reproducible, complete, clean isolated Windows source checkout that contains the exact v3 harness at its required relative path.

This is a non-disruptive source-validation task. It does not authorize the recovery suite or any CogentNexus/OpenClaw/Ollama runtime or lifecycle action.

## Immutable source

Repository: `funggier/cogentnexus`  
Branch: `agent/v0.9.3-recovery-reality-tests`  
Required accepted validation ancestor: `5a22d9479ad7d62c7a159e4b49e2bc3f79fb6171`  
Required harness implementation ancestor: `592a6fbd37da05013b7a8a5875ccd8b17e188cfa`  
Required workflow-fix ancestor: `929fbcc663251941d88f38f09544068a9b3e069d`  
Harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`  
Required harness blob: `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`

Later ChatGPT-owned coordination/documentation commits are allowed.

## Duplicate-execution fence

Before any local action, fetch the branch and check for:

`docs/operations/coordination/reports/CNX-20260822-009-clean-windows-source-checkout-validation.md`

If it exists, do not inspect the old worktree, create a clone/worktree, run validation, observe CI, or perform any other side effect. Exit awaiting ChatGPT review.

## Read-only diagnosis of Task 008 checkout

Read-only inspect the exact Task 008 worktree path from its report. Record commands, exit codes, and output for:

- `git status --short`;
- `git status --porcelain=v1`;
- `git rev-parse HEAD`;
- `git worktree list --porcelain` from the source repository;
- `git config --show-origin --get core.sparseCheckout`;
- `git sparse-checkout list` where applicable;
- `git ls-files --error-unmatch scripts/test-v093-ollama-recovery-windows-v3.ps1`;
- `Test-Path -PathType Leaf .\scripts\test-v093-ollama-recovery-windows-v3.ps1`;
- a bounded list/count of tracked deletion residue.

Do not repair, reset, clean, delete, prune, or reuse the Task 008 worktree.

## Exact clean-checkout procedure

1. Fresh-fetch `origin/agent/v0.9.3-recovery-reality-tests`.
2. Record the exact Task 009 start HEAD and verify all three required ancestors.
3. Obtain the existing configured origin URL without exposing credentials.
4. Choose a new, unique, previously nonexistent Task 009 directory under the established CogentNexus worktree/checkout parent.
5. Create a full isolated clone from the configured origin into that new directory and detach it at the exact start HEAD. Do not use sparse checkout.
6. If the destination already exists, report `BLOCKED`; do not delete or reuse it.
7. Do not change the source branch or any existing worktree.

Record the exact commands and exit codes. Redact credentials if the origin URL embeds any.

## Required checkout proof

In the new isolated checkout, prove:

- `git rev-parse HEAD` equals the Task 009 start HEAD;
- `git status --porcelain=v1` is empty;
- `git diff --name-only --diff-filter=D` is empty;
- `git ls-files --error-unmatch scripts/test-v093-ollama-recovery-windows-v3.ps1` succeeds;
- the harness is a physical leaf file at the exact relative path;
- `git rev-parse HEAD:scripts/test-v093-ollama-recovery-windows-v3.ps1` equals `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`;
- the file SHA256, byte size, and last-write timestamp are recorded;
- PowerShell parser validation returns zero errors;
- the harness exact `-SyntaxOnly` invocation exits 0;
- the checkout remains clean afterward.

Also record all applicable GitHub workflows for the exact Task 009 start HEAD and require completed `success`. Do not manually rerun workflows.

## Prohibited actions

- no `-RunDisruptive`;
- no confirmation input;
- no recovery scenario or evidence-file generation;
- no Windows runtime preflight;
- no `openclaw`, `ollama`, or `cnx` command;
- no process kill;
- no `cnx start`, `cnx stop`, reset, uninstall, install, or reinstall;
- no source/harness/workflow edit;
- no package/software installation;
- no deletion, reset, clean, prune, or repair of an existing worktree;
- no LM Studio action;
- no v0.9.2 change;
- no force-push.

## Acceptance criteria

PASS requires a reproducible full isolated checkout at the exact start HEAD, no tracked deletion residue, exact harness path/blob, clean status before and after validation, parser and `-SyntaxOnly` success, and complete green CI.

If any requirement fails, report `BLOCKED` with the exact failure. Do not improvise or run the disruptive suite.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260822-009-clean-windows-source-checkout-validation.md`

Include:

- start HEAD and ancestor/CI table;
- Task 008 checkout diagnosis;
- redacted exact clone/checkout commands and exit codes;
- new isolated path;
- clean-status and deletion-residue proof;
- harness tracked/path/blob/SHA256/size/time proof;
- parser and `-SyntaxOnly` results;
- safety accounting;
- verdict and recommended next step.

Commit message must begin:

`report: CNX-20260822-009`

Never force-push. Stop after publishing the report.
