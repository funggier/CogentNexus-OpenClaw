# CNX-20260831-193 — Recovery Reality Installer Contract Repair

Status: `PASS`
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

That assertion was stale and conflicted with the accepted v0.9.3 responsibility boundary:

- **managed runtime/operator provider contract:** Ollama only;
- **installer contract:** provider-neutral;
- provider selection/readiness is a post-install runtime responsibility, not installer-owned policy.

## RED evidence

Workflow run: `33395551508`

The recovery harness parse/load and process-safety/Ollama-only checks passed. The run failed only because the workflow required an Ollama default in `scripts/install.ps1`.

Exact observed failure:

`Windows installer is not defaulted to Ollama.`

## Minimal repair

Only `.github/workflows/ps51-v093-recovery-reality-smoke.yml` was changed.

The repaired contract now proves:

1. recovery-reality harness parses under Windows PowerShell 5.1;
2. harness remains process-safe and Ollama-only;
3. Windows installer parses successfully and exposes no provider parameter/default;
4. POSIX installer exposes no provider option/default variable;
5. both installers remain wired to `cnxclaw_v093.py`;
6. v0.9.3 provider/runtime facades compile.

No production/runtime/plugin behavior, installer behavior, test, dependency, or provider scope was changed.

## GREEN evidence

Exact PR head at repair verification:

`743d51d0d789354a419086072fa83eeeacc048cb`

Successful PR-triggered runs on that head:

- `PS5.1 v0.9.3 Ollama Recovery Reality Smoke` — `33396028030` — `completed/success`;
- `Validate` — `33396028043` — `completed/success`;
- `PS5.1 Acceptance Smoke` — `33396028229` — `completed/success`;
- `Windows Installer Pack Smoke` — `33396028169` — `completed/success`;
- `PS5.1 v0.9.3 Ollama Recovery V2 Smoke` — `33396028128` — `completed/success`;
- `PS5.1 v0.9.3 Ollama Recovery V3 Smoke` — `33396028324` — `completed/success`;
- `PS5.1 v0.9.3 Gateway Convergence Smoke` — `33396028228` — `completed/success`;
- `PS5.1 Partial Repair Smoke` — `33396028052` — `completed/success`;
- `PS5.1 Live Runner Smoke` — `33396028041` — `completed/success`.

Package dry-run on the PR merge ref retained the accepted installable payload identity:

- payload-v2 fingerprint: `b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93`;
- file count: `186`.

## Disposition

`PASS`

Task 193 is closed. PR #26 may proceed to the final exact-head merge gate after coordination-only closeout commits are validated. The current v0.9.3 managed runtime remains Ollama-only; installers remain provider-neutral.
