# CNX-20260926-449 — Long-Running Model Lease Guard Report

Status: `COMPLETE`
Classification: `CNX449_LONG_RUNNING_OLLAMA_GUARD_GREEN`
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

## Exact candidate and CI

- Candidate SHA: `dfb3706e7c11e61cc7987a7e4928f3c5d7203435`.
- Branch: `cnx-449-long-running-model-lease-guard`.
- Validate run `36224230322`: SUCCESS.
- Windows Installer Pack Smoke `36224230304`: SUCCESS.
- PS5.1 Acceptance Smoke `36224230318`: SUCCESS.

## Physical install-over

The exact candidate was installed over the existing managed v0.9.8 runtime with the supported installer.

- installer exit code: `0`;
- pre-handoff Gateway stability: PASS;
- managed -> PASSTHROUGH handoff: PASS;
- post-install rollover/finalize: PASS;
- controller returned to MANAGED generation `36`;
- Gateway/OpenClaw baseline: `2026.9.5`, healthy on `127.0.0.1:18789`;
- supervisor: installed / enabled / hidden / `LastTaskResult=0`;
- Ollama: reachable / healthy;
- pending outbox: `0`;
- post-commit recovery error: none.

Source/installed payload-v2 parity:

- source: `296` files / `561c3903d2bb0476c37912b10941587ea76f0e07ac26e095d02bde08a04009c9`;
- installed: `296` files / same fingerprint.

Installed runtime surfaces were directly inspected:

- installed plugin contains `OLLAMA_DIRECT_MODEL_CALL_TIMEOUT_MS = 45 * 60_000`;
- installed Host contains the `gateway-long-running-protected` fence.

OpenClaw ownership alignment: live config has `agents.defaults.timeoutSeconds=2700`, so the 45-minute Ollama durable lease matches the current OpenClaw turn timeout instead of extending beyond it.

## Fresh installed-candidate Ollama acceptance

Started a fresh Gateway-routed isolated session `agent:main:cnx449-live-ollama` using `ollama/qwen3.8:27b`.

Live Ticket/model-call evidence while inference is active:

- Ticket: `CNXT-ce33b7ae-2e88-4150-bba9-8d34ee68f1ab`;
- run: `57245acc-0448-4d4b-b3ac-81212e28e45d`;
- call: `57245acc-0448-4d4b-b3ac-81212e28e45d:model:1`;
- provider/model: `ollama/qwen3.8:27b`;
- start: `2026-09-26T07:04:41.820Z`;
- deadline: `2026-09-26T07:49:41.820Z`;
- durable event `timeoutMs`: `2700000` (45 minutes);
- source: `openclaw-model-call-hook`;
- Ticket has not entered `response_ready` while inference is still active.

Installed Host guard proof used the live active Ticket/lease but replaced the probe result with deterministic failure and replaced the restart function with an exception sentinel. Result:

- `gateway-long-running-protected`;
- `action=none`;
- exact Ticket/run/call/provider/model/deadline evidence returned;
- restart sentinel was not called.

Natural scheduled-supervisor evidence during the same live 27B inference:

- supervisor continued running on its one-minute schedule;
- completed samples returned `LastTaskResult=0`;
- Gateway child PID remained `38760` across samples;
- no probe-only Gateway restart occurred.

## Live terminal result

The live `qwen3.8:27b` turn completed successfully:

- CLI process exit code: `0`;
- final marker: `CNX449_OLLAMA_LONG_RUNNING_OK`;
- OpenClaw transcript final: assistant `stopReason=stop`, exact run id `57245acc-0448-4d4b-b3ac-81212e28e45d`;
- model-call outcome: `completed`;
- model-call duration: `1,210,862 ms` (~20m10.9s);
- `response_ready` was written only after `direct_model_call_ended` / `inference_attempt_ended`;
- execution therefore exceeded the old 15-minute lease by more than five minutes without a premature Gateway restart;
- supervisor continued returning success and the Gateway child PID remained `38760` throughout the sampled long-running interval.

CPU liveness was independently sampled while the model was active:

- `llama-server` PID `30808`;
- working set approximately `15.99 GiB`;
- CPU time advanced `35.5s` during a 5-second wall-clock sample, proving active multi-core computation rather than an idle wait.

Because the acceptance used headless `openclaw agent` without `--deliver`, the CLI return-to-caller surface did not emit a CogentNexus delivery-confirmation marker. That separate surface gap is tracked as `CNX-20260926-450-headless-agent-durable-settlement.md` / GitHub issue `#42` (verified open as backlog). It is not used to downgrade the Task-449 long-running lease/restart result. The isolated acceptance Ticket was explicitly cancelled after evidence capture, and final runtime status showed only terminal Tickets with `pendingOutbox=0`.

## Final classification

`CNX449_LONG_RUNNING_OLLAMA_GUARD_GREEN`
