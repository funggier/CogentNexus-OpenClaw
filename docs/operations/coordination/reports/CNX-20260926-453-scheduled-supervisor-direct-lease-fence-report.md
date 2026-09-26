# CNX-20260926-453 — Scheduled Supervisor Direct-Lease Fence and Gateway Recovery Settlement Report

Status: `IN_PROGRESS`
Classification: `CNX453_LOCAL_GREEN_CI_PENDING`
GitHub issue: `#45`
Working branch: `cnx-453-supervisor-direct-lease-fence`
Baseline SHA: `09eec4113b371d39334d90a332fa9a6455530db0`
Baseline release: `v0.9.8` (immutable)

## Physical trigger

CNX-451 live acceptance used `ollama/qwen3.8:27b` through session `agent:main:dashboard:cnx451-soft-acceptance-01`.

Original Ticket/run/call:

- Ticket `CNXT-071588b9-4d6b-4e30-8935-51ba99887293`;
- run `b40ea823-e273-4f37-81e2-d987d9d7509a`;
- call `b40ea823-e273-4f37-81e2-d987d9d7509a:model:1`;
- durable lease `10:03:47.895Z -> 10:48:47.895Z` (`2700000 ms`).

The run crossed the historical 15-minute timeout boundary successfully, but at `10:20:26Z` the scheduled Host entered hard-hang maintenance and later stopped the Gateway while the durable Direct lease was still unexpired. The client ended with WebSocket `1006` and was not retried.

Startup reconciliation later restored the Gateway and created an authorized continuation Ticket without user resend, but the original model-call/canonical inference-attempt evidence remained stale `active` under the installed Host generation.

## Confirmed root causes / coverage gaps

### 1. Scheduled supervisor transaction budget was too short

The installed Windows task had:

- `MultipleInstancesPolicy=IgnoreNew`;
- `ExecutionTimeLimit=PT2M`.

The Host recovery transaction can legitimately consume more than two minutes because prepare/stop/start/readiness are individually bounded. Physical evidence matched the limit: maintenance started at `10:20:26Z`, Gateway stop verification completed at `10:22:24Z` (~118 seconds), and the supervisor process disappeared before verified restart/reconciliation finished.

### 2. Destructive recovery needed an outer lease fence

The inner CNX-449 guard passed synthetic and historical-state replay, but physical scheduled execution still reached hard-hang recovery while an unexpired Direct call existed. CNX-453 therefore adds a defense-in-depth fence at the periodic scheduled entrypoint, before compatibility composition can enter lifecycle recovery.

### 3. Recovery lane drift must not hide live Direct evidence

Host Direct-call discovery previously required `workflow_eligible=0`. Physical recovery can change Ticket lane metadata while execution evidence is still active. The restart/orphan classifiers now rely on authoritative active call + Ticket pre-response state instead of lane eligibility alone.

### 4. Startup promotion must settle predecessor execution atomically

The installed generation's `host_recovered_direct` event contained no `settledExecution`, and the predecessor model-call/attempt remained active. The repaired startup promotion closes pre-cutoff active model calls as `interrupted`, ends the canonical inference attempt, records durable settlement events, and only then authorizes the resumable Ticket state.

## Repair

- `host_control_v092.py`: outer scheduled-entry active-unexpired Direct lease fence; fail closed if lease evidence cannot be read; healthy Gateway still delegates normally.
- `host_stall_v091.py`: active-call / boundary discovery no longer drops valid execution evidence solely because `workflow_eligible` drifted to 1.
- `host_v091_legacy_v094.py`: startup promotion settles predecessor model-call and canonical inference-attempt inside the same transaction and writes `settledExecution` evidence.
- Windows supervisor template: `ExecutionTimeLimit` increased from `PT2M` to `PT15M`, while retaining `IgnoreNew`.
- `validate.py`: enforces `IgnoreNew` and `PT15M` on generated Windows task XML.
- Added contract test for the Windows task recovery budget.

## TDD / local validation

- focused CNX-453 Host tests: `32/32 PASS`;
- full Python: `753 passed, 5 skipped, 38 subtests passed`;
- full plugin Vitest: `95 files / 444 tests PASS`;
- build: PASS;
- evaluation: PASS; evidence SHA-256 `83c89865e15166039807a7ba99db517ed8d161037c1e5f2274aa0adffb3eb622`;
- plugin validation: PASS (`46` config properties, `5` tools, `9` required Ticket DB tables, `298` packed files);
- production dependency audit: `0 vulnerabilities`;
- `git diff --check`: PASS;
- skill validator: PASS.

## Operational Ollama keep-alive change

The operator requested extending resident model keep-alive from 2 hours to 6 hours.

- persistent User environment `OLLAMA_KEEP_ALIVE` changed from `2h` to `6h`;
- the currently running Ollama server inherited the old `2h` value and will not see `6h` until a controlled server restart;
- restart is intentionally deferred until CNX-453 settlement/recovery state is clean so no model work is interrupted;
- historical docs that record the former `2h` setting are left unchanged as historical evidence.

## First physical candidate qualification

Candidate `21176b07ad98ada944612d444fe5e2d9a8ee0d2b` passed:
- Validate `36239918676` — SUCCESS;
- PS5.1 `36239918629` — SUCCESS;
- Windows Installer Pack `36239918685` — SUCCESS;
- physical install-over exit `0`;
- source/installed repaired Host files exact;
- Supervisor `ExecutionTimeLimit=PT15M` and `IgnoreNew`;
- Gateway healthy, controller MANAGED generation `40`.

### Follow-up physical finding

After the first candidate install, the original Ticket remained too old for the 15-minute session resume-authority freshness fence. Refusing resume was correct, but the pre-boundary model-call and canonical inference attempt also remained `active`.

RED reproduced the exact semantic gap: stale session authority was not resumed, while the model call incorrectly remained `active`.

The follow-up repair separates these authorities:
- Gateway startup/process-boundary proof settles pre-cutoff execution evidence regardless of session freshness;
- session freshness still controls whether the Ticket may be promoted for resume;
- stale-session settlement uses outcome `host-startup-boundary-settled`;
- fresh resumable settlement preserves `host-startup-interruption-promoted`.

Follow-up validation:
- focused startup settlement `2/2 PASS`;
- CNX-453 Host regressions `33/33 PASS`;
- full Python `754 passed, 5 skipped, 38 subtests passed`;
- full Vitest `95 files / 444 tests PASS`;
- build PASS;
- evaluation PASS, evidence SHA-256 `48e3dc446018c96cc4dcff6d888d06eb281a5e525b0526b2c8cce90c5a1f8d6f`;
- plugin validation PASS (`298` packed files);
- production audit `0 vulnerabilities`;
- `git diff --check` and skill validator PASS.

## Remaining gates

1. commit/push follow-up exact candidate SHA;
2. exact-SHA GitHub CI;
3. physical install-over of the follow-up candidate;
4. confirm the stale prime model-call / canonical attempt are no longer active without authorizing a stale-session resume;
5. perform controlled Ollama restart after durable work is quiescent and verify `OLLAMA_KEEP_ALIVE=6h` is active;
6. live long-running Direct lease requalification, then resume CNX-451 soft-pressure acceptance.

## Current classification

`CNX453_FOLLOWUP_LOCAL_GREEN_CI_PENDING`
