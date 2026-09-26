# CNX-20260926-449 — Long-Running Model Lease Guard Report

Status: `IN_PROGRESS`
Classification: `CNX449_LOCAL_GREEN_CI_PENDING`
GitHub issue: `#41`
Working branch: `cnx-449-long-running-model-lease-guard`
Baseline SHA: `bffa539a59f8d0318cbffb062a73b205c8cb8705`
Baseline release: `v0.9.8` (immutable)

## Trigger

CNX-448 live qualification showed a slow `ollama/qwen3.8:27b` call still actively computing when the external Host observed two failed Gateway fast probes and authorized hard-hang recovery before the durable model-call deadline.
The machine is CPU-only for Ollama and large-model inference can legitimately take tens of minutes. A one-second confirmation interval is therefore insufficient evidence that execution is dead.

## Repair

- Ollama default Direct model-call lease: 45 minutes.
- Non-Ollama default Direct model-call lease: 15 minutes.
- Explicit `timeoutMs` remains authoritative within the existing 1–60 minute clamp.
- The Host now queries durable active Direct calls after the second failed Gateway probe and before hard-hang restart.
- An accepted/waiting pre-response call with a future deadline returns `gateway-long-running-protected` and suppresses restart.
- At or after deadline the guard disappears and existing recovery remains reachable.
- Provider/model/auth ownership remains OpenClaw-owned.

## TDD evidence

RED: a double failed Gateway probe with a simulated unexpired Direct lease still called `_restart_unresponsive_gateway`.
GREEN: unexpired lease prevents restart; the guard disappears exactly at deadline; transient probe behavior remains intact; provider-aware lease defaults and explicit override are covered.

## Local validation

- Focused Python Host/recovery suites: `40 passed`.
- Focused plugin lease + CNX-446 + CNX-448: `3 files / 16 tests PASS`.
- Full Python: `747 passed, 5 skipped, 38 subtests passed`.
- Full plugin Vitest: `94 files / 442 tests PASS`.
- TypeScript/build: PASS.
- Evaluation: PASS, evidence SHA-256 `71bff654a2f3005f1528bb6377bdb4145dcee30fa216ae1012299b2e38debd28`.
- Plugin validation: PASS (`46` config properties, `5` tools, `9` required DB tables, `296` packed files).
- Production dependency audit: `0 vulnerabilities`.
- `git diff --check`: PASS.

## Remaining gates

1. exact candidate commit/push;
2. GitHub exact-SHA CI;
3. physical install-over;
4. package/installed parity;
5. fresh installed-candidate Ollama acceptance proving a 45-minute lease and restart protection while active.

## Current classification

`CNX449_LOCAL_GREEN_CI_PENDING`
