# CNX-20260831-193 — Recovery Reality Installer Contract Repair

Status: `IN_PROGRESS`
Date: 2026-08-31 ICT
Parent: `CNX-20260831-188`
Executor: ChatGPT
Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-full-stabilization`
Release PR: `#26`

## Problem

PR-triggered workflow `PS5.1 v0.9.3 Ollama Recovery Reality Smoke` run `33395551508` failed at the installer contract step.

The failing workflow asserted that:

- Windows installer must declare `[string]$Provider = "ollama"`;
- POSIX installer must declare `PROVIDER="ollama"`.

That assertion is stale and conflicts with the accepted v0.9.3 responsibility boundary:

- **managed runtime/operator provider contract:** Ollama only;
- **installer contract:** provider-neutral;
- provider selection/readiness is a post-install runtime responsibility, not installer-owned policy.

The current Windows and POSIX installers are intentionally provider-neutral and have already passed the accepted lifecycle/requalification evidence chain.

## RED evidence

Workflow run: `33395551508`

The recovery harness parse/load and process-safety/Ollama-only checks passed. The run failed only because the workflow required an Ollama default in `scripts/install.ps1`.

Exact observed failure:

`Windows installer is not defaulted to Ollama.`

## Scope

Allowed:

- update `.github/workflows/ps51-v093-recovery-reality-smoke.yml` only as needed to make the installer assertion match the accepted provider-neutral installer contract;
- coordination/report/review documentation for this repair.

Not allowed:

- production/runtime/plugin behavior changes;
- installer behavior changes;
- test changes;
- dependency changes;
- provider expansion beyond Ollama for the current managed runtime;
- release publication before the repaired PR checks pass;
- force push.

## Minimal repair contract

The workflow must continue to prove:

1. recovery-reality harness parses under Windows PowerShell 5.1;
2. harness remains process-safe and Ollama-only;
3. Windows installer parses successfully and exposes no provider parameter/default;
4. POSIX installer exposes no provider option/default variable;
5. both installers remain wired to `cnxclaw_v093.py`;
6. v0.9.3 provider/runtime facades compile.

The workflow must not require the installer to own Ollama selection.

## Acceptance

Task 193 passes only if:

- the stale installer assertion is replaced by provider-neutral installer assertions;
- the exact updated PR head gets a successful `PS5.1 v0.9.3 Ollama Recovery Reality Smoke` run;
- Validate, PS5.1 Acceptance Smoke, Windows Installer Pack Smoke and other triggered release-PR checks are reviewed on the same exact PR head;
- no product/runtime/installer/test behavior was changed merely to satisfy CI.
