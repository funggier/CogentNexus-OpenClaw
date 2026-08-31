# CNX-20260831-181 — Historical Task-178 Outer Observer Cleanup

- **Task:** `CNX-20260831-181`
- **Execution mode:** `WINDOWS_HISTORICAL_TASK178_OUTER_OBSERVER_CLEANUP_HERMES`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority HEAD before activation:** `efa8662b5f2290f0fc7a7624b0b2b4e8eb6be394`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT

## Objective

Retire only the historical Task-178 outer evidence-observer chain that remained alive after the actual reset command tree was already retired in Task 179, then prove a clean process/runtime/durable boundary.

This task is intentionally cleanup-only. It does not authorize install-over, reset, uninstall, reinstall, lifecycle helper commands, Gateway/Ollama restart, semantic/model/recovery action, or source/product/test/workflow changes.

## Accepted context

Task 180 is reviewed as:

`ACCEPTED_BLOCKED — PREINSTALL_TASK178_OUTER_OBSERVER_CLEANUP_REQUIRED`

Accepted repository repair candidate remains:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Candidate facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Installed facade remains the pre-repair baseline until a later install-over task proves otherwise:

`e15e8af49e18925fb569cd405b18fe5c57172d1a0e4644e359703b692cacb032`

Task-180 addendum last observed the historical observer chain as:

```text
bash PID 14196
  -> bash PID 22832
      -> Python PID 17052: run_reset178.py
          -> Python PID 17444: run_reset178.py
```

The actual Task-178 reset command/lifecycle descendants were absent. The retained Task-178 ledger had zero `prompt_observed`, `input_send_intent`, and `input_sent` events.

## Phase A — fresh authority and identity verification

Before any kill/termination:

1. fetch fresh remote branch HEAD, `ACTIVE.md`, and `STATUS.md` and prove Task 181 is active;
2. prove the Task-181 report is absent;
3. re-read the retained Task-178 evidence ledger and verify zero prompt/input events;
4. perform a fresh read-only process tree scan;
5. prove no actual `cnxclaw.cmd reset`, `cnxclaw_v093.py reset`, legacy `cnxclaw.py reset`, `host_control_v092.py ... reset`, or lifecycle reset child remains;
6. identify the observer chain using command line, parent/child relationship, executable/script path, creation time where available, and Task-178 evidence-root association;
7. collect read-only controller/Gateway/Ollama/ownership/delivery/recovery/SQLite baseline and prove Task-171 historical durable state remains present.

If identity is ambiguous, or any actual reset/uninstall/product lifecycle child is still alive, do not terminate anything. Publish `BLOCKED — OBSERVER_IDENTITY_UNSAFE_TO_CLEAN` and stop.

## Phase B — bounded observer cleanup

Only if Phase A proves the remaining chain is exactly the historical Task-178 evidence observer and not a live product lifecycle tree:

- terminate only that exact observer chain;
- prefer terminating descendants then wrappers, or a verified root-tree operation that cannot reach unrelated processes;
- do not send stdin or confirmation input;
- do not execute any CogentNexus/OpenClaw lifecycle command as part of cleanup;
- do not kill Gateway, Ollama, OpenClaw service processes, unrelated bash/cmd/Python processes, or ambiguous descendants.

The known historical PID values are evidence hints only. Do not kill by stale PID number without fresh identity verification.

## Phase C — cleanup verification

After cleanup, prove all of the following read-only:

1. no `run_reset178.py` observer process associated with the historical Task-178 evidence root remains;
2. no actual Task-178 reset/uninstall process exists;
3. no orphan descendant from the observer tree remains;
4. controller remains coherent and managed;
5. Gateway remains healthy;
6. Ollama remains reachable/healthy/ready;
7. ownership remains valid with no legacy namespace contamination;
8. delivery/recovery remain READY with pending outbox `0` and no new incident;
9. SQLite `PRAGMA integrity_check` remains `ok`;
10. Task-171 historical Ticket/delivery state remains present;
11. ticket/event/model/recovery counts did not increase from cleanup;
12. no semantic/model/recovery action was manufactured.

Do not attempt the Task-180 install-over after cleanup in this task. A later successor must perform a fresh install-over preflight from a clean process boundary.

## Hard fence

Task 181 semantic action budget: `0`.

Authorized live mutation is limited to identity-checked termination of the historical Task-178 outer observer chain.

Not authorized:

- installer/install-over/reinstall;
- reset/uninstall;
- start/stop/restart/enable/disable;
- Gateway/Ollama manual lifecycle action;
- Dashboard Send/composer input/`chat.inject`;
- model inference/recovery/regeneration;
- manual durable/config/transcript/route/DB repair;
- source/product/test/workflow/dependency changes;
- release/tag/merge/force push.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260831-181-hermes-historical-task178-outer-observer-cleanup.md`

Follow `EXECUTOR_REPORT_CONTRACT.md` and include:

- disposition;
- fresh authority/head;
- exact before-cleanup process identities and command lines;
- Task-178 ledger zero-input proof;
- cleanup command/mechanism and exact terminated identities;
- post-cleanup process scan;
- runtime/provider/ownership/delivery/recovery/SQLite preservation;
- Task-171 history preservation;
- before/after counts;
- semantic/model/recovery action counts;
- acceptance matrix;
- 5–10 claim Reviewer Verification Packet;
- publication fence;
- successor recommendation.

PASS label:

`PASS — HISTORICAL_TASK178_OUTER_OBSERVER_RETIRED_CLEAN_BOUNDARY_PROVEN`

After report publication, stop for ChatGPT review. Install-over and reset remain unauthorized.