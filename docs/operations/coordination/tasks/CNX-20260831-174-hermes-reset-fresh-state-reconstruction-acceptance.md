# CNX-20260831-174 — Hermes Reset Fresh-State Reconstruction Acceptance

Status: `READY_HERMES`

Execution mode: `WINDOWS_RESET_FRESH_STATE_RECONSTRUCTION_ACCEPTANCE_HERMES`

Authorization: `CNX-20260831-174_HERMES_RESET_FRESH_STATE_RECONSTRUCTION_ACCEPTANCE`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Objective

Perform exactly one documented `cnxclaw.cmd reset` on the Task-170-installed accepted frozen candidate, provide exactly one interactive `y` confirmation, and determine whether the implementation-owned reset transaction returns the same installed release to a verified fresh-install `MANAGED` state while preserving OpenClaw, Ollama, installed program identity, and unrelated namespaces.

This is a bounded real-Windows destructive lifecycle acceptance task. It is not a repair task and does not authorize a retry or a helper lifecycle sequence.

## Accepted baseline

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed plugin fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- OpenClaw: `2026.7.1-2`
- Task-171 through Task-173 semantic/durable result: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`
- Task-171 semantic Send count is permanently frozen at exactly `1` and MUST NOT be changed by this task.

The current GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative for coordination state.

## Implementation contract being accepted

The accepted v0.9.3 facade routes `cnxclaw.cmd reset` through the v0.9.2 destructive lifecycle implementation and deterministically targets Ollama.

The implementation contract is not “delete state and stop.” One successful reset invocation owns a complete transaction:

1. verify namespace ownership, provider/route preconditions, and installed plugin bootstrap provenance;
2. require explicit interactive `y` confirmation; any other input cancels without mutation;
3. transition CogentNexus-OpenClaw to PASSTHROUGH and restore/activate the native OpenClaw route;
4. disable CogentNexus-OpenClaw startup integration;
5. reset CogentNexus-OpenClaw plugin configuration;
6. remove CogentNexus-OpenClaw-owned runtime/state root;
7. recreate fresh host/controller state;
8. rewrite the namespace ownership manifest;
9. bootstrap a fresh Ticket database from the installed plugin payload;
10. apply policy;
11. seed/begin the Ollama route transition;
12. transactionally enable CogentNexus-OpenClaw again;
13. force the implementation-owned Gateway process boundary needed to activate the fresh managed route;
14. verify plugin loaded/activated/enabled, Gateway health, Ollama health, and selected route/model;
15. commit route/provider selection;
16. return exit code `0` with `COGENTNEXUS-OPENCLAW RESET: PASS` and `State     : fresh-install MANAGED`.

The reset contract preserves installed CogentNexus-OpenClaw program files and release version. It removes CogentNexus-OpenClaw Tickets, recovery/delivery/runtime state, session authority, workflow runtime data, diagnostics, and CogentNexus-OpenClaw configuration changes. OpenClaw and Ollama data are not removed.

The Gateway process boundary performed internally by the reset implementation is part of the single authorized reset transaction. It does not authorize the executor to run a separate restart command.

## Fresh authority and safety preflight

Before any destructive action, Hermes/Codex must perform read-only checks and record evidence for all of the following:

1. fresh remote branch HEAD;
2. fresh `docs/operations/coordination/ACTIVE.md` and `STATUS.md`;
3. Task 174 is still the active authorization and no conflicting successor has replaced it;
4. the required Task-174 report path is absent;
5. installed plugin fingerprint still equals `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
6. installed package/release identity is still consistent with the accepted Task-170 checkpoint;
7. OpenClaw remains `2026.7.1-2`;
8. CogentNexus-OpenClaw plugin is loaded/enabled and the current controller/runtime is coherent;
9. Gateway and Ollama/provider state are healthy enough to satisfy reset preconditions;
10. SQLite integrity is `ok` and the pre-reset durable state can be read without mutation;
11. capture the current Task-171 historical durable identities before reset, including the frozen Ticket/run/model/delivery records and relevant counts;
12. capture read-only preservation anchors for non-CogentNexus OpenClaw/Ollama state and unrelated namespaces where practical.

At minimum, pre-reset evidence must identify the frozen Task-171 history:

- nonce `T171-20260831T020446Z-3142A528`;
- Ticket `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`;
- run `8b69bede-030f-4c20-8bb8-0aa99e12422c`;
- model call `8b69bede-030f-4c20-8bb8-0aa99e12422c:model:1`;
- one Task-171 `cnx_assistant_delivery` row in the pre-reset database;
- the completed Task-171 Ticket/delivery state accepted by Tasks 171–173.

If any material baseline identity or safety prerequisite is inconsistent, **DO NOT RUN RESET**. Publish `BLOCKED` with the read-only evidence and stop.

## Exactly-one destructive action authorization

If and only if preflight passes, execute exactly one normal installed launcher invocation:

```text
cnxclaw.cmd reset
```

When the documented interactive prompt appears:

```text
Continue? [y/N]:
```

provide exactly one response:

```text
y
```

Record the command start/end, process identity when available, prompt occurrence, confirmation occurrence, exit code, stdout, and stderr.

### Absolute no-retry rule

After the reset invocation has begun, there is no second reset under any condition, including:

- timeout;
- nonzero exit;
- partial output;
- uncertain process completion;
- Gateway health failure;
- plugin health failure;
- route/provider failure;
- fresh database verification failure;
- stale UI;
- observer uncertainty;
- fail-closed/PASSTHROUGH result.

A completed or failed disruptive phase must not be repeated simply because a watcher, executor loop, or reviewer requests more evidence.

## No helper lifecycle intervention

After reset starts, Hermes/Codex MUST NOT manually run any separate lifecycle action to help the reset succeed or to repair its result.

Prohibited helper actions include:

- a second `reset`;
- `start`;
- `stop`;
- `restart`;
- `enable`;
- `disable`;
- manual Gateway restart/reload;
- manual Ollama/provider restart;
- supervisor/startup repair;
- route/config repair;
- manual Ticket database bootstrap;
- installer/install-over;
- uninstall;
- reinstall;
- rollback;
- manual file/state/config/database/transcript mutation.

Implementation-owned subprocesses and process boundaries that occur inside the one reset command are expected and authorized. Executor-issued helper lifecycle commands are not.

If reset fails, preserve the exact failure state and report it. Do not convert the failure into a success by intervention.

## Required post-reset evidence

After the single reset invocation naturally terminates, gather read-only evidence only.

### A. Command-level result

Record:

- exact command;
- reset invocation count;
- interactive prompt count;
- `y` confirmation count;
- process/PID evidence where available;
- start/end timestamps;
- exit code;
- complete relevant stdout/stderr;
- whether `COGENTNEXUS-OPENCLAW RESET: PASS` appeared;
- whether `State     : fresh-install MANAGED` appeared.

### B. Installed provenance preservation

Prove after reset:

- installed plugin fingerprint is still exactly `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
- CogentNexus-OpenClaw installed release remains `0.9.3`/the accepted installed release;
- installed payload/program files were not replaced by another candidate;
- OpenClaw remains `2026.7.1-2`.

Reset must not be treated as reinstall or upgrade.

### C. Fresh MANAGED reconstruction

Prove the reset reconstructed a coherent fresh managed runtime:

- controller state exists and represents fresh `MANAGED` operation;
- desired Gateway/provider state is coherent with managed operation;
- selected provider is Ollama;
- no unresolved provider transition remains;
- policy is present/applied;
- ownership manifest is valid;
- startup integration is in the expected fresh managed condition;
- CogentNexus-OpenClaw plugin is enabled/activated/loaded;
- Gateway is healthy;
- Ollama/provider is healthy;
- OpenClaw route/model is the correct current managed Ollama route;
- no unexplained CogentNexus loader/runtime error remains.

Do not issue a separate lifecycle command to create this state; the reset command itself must produce it.

### D. Fresh durable-state reconstruction

Prove the newly bootstrapped Ticket database/schema is valid:

- SQLite integrity `ok`;
- expected tables/schema exist;
- fresh baseline counts are internally coherent;
- no pending outbox/recovery/delivery work was manufactured;
- no semantic/model work was manufactured by reset.

Because reset explicitly removes CogentNexus-OpenClaw Tickets, delivery/runtime state, session authority, and workflow runtime data, prove that the pre-reset Task-171 durable history is absent from the fresh state after reset, including at minimum:

- Ticket `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf` absent;
- run `8b69bede-030f-4c20-8bb8-0aa99e12422c` absent from current CogentNexus durable work state;
- model-call record `8b69bede-030f-4c20-8bb8-0aa99e12422c:model:1` absent;
- Task-171 `cnx_assistant_delivery` row absent;
- Task-171 recovery/outbox/session/workflow runtime state absent where those tables/surfaces are reset-owned.

The old native OpenClaw transcript is external OpenClaw data and is not required to be deleted by reset. Do not mutate it merely to make the fresh CogentNexus database empty.

### E. External preservation

Prove reset did not delete or replace non-CogentNexus-owned external surfaces relevant to the contract:

- OpenClaw installation/version remains intact;
- Ollama runtime remains installed/intact;
- the configured Ollama model/data needed by the accepted runtime remains available;
- unrelated OpenClaw data/config outside the reset-owned fields remains intact as far as the preflight preservation anchors allow;
- unrelated namespaces are preserved;
- no uninstall/reinstall occurred.

Classify any expected route/config changes that are part of the documented reset transaction separately from unrelated external state.

### F. Semantic and duplicate fence

Task 174 authorizes **zero semantic actions**.

Prove:

- Dashboard Send: `0`;
- Enter semantic submission: `0`;
- `chat.inject`: `0`;
- manual model call: `0`;
- recovery/regeneration injection: `0`;
- new semantic Ticket intended to test delivery: `0`;
- reset invocation: exactly `1`;
- explicit `y`: exactly `1`;
- manual helper lifecycle command after reset start: `0`.

## PASS contract

Task 174 may report `PASS` only if all of the following are proven:

1. fresh authority/preflight was valid before mutation;
2. exactly one `cnxclaw.cmd reset` invocation occurred;
3. exactly one explicit interactive `y` confirmation occurred;
4. the reset command naturally returned exit code `0` and the documented PASS/fresh-MANAGED result;
5. no second reset or executor-issued helper lifecycle action occurred;
6. installed CogentNexus-OpenClaw candidate/release/fingerprint remained unchanged;
7. OpenClaw remained `2026.7.1-2`;
8. the reset command itself reconstructed a healthy fresh `MANAGED` controller/plugin/Gateway/Ollama/route state;
9. the fresh Ticket database/schema passes integrity and baseline checks;
10. pre-reset CogentNexus durable history, including the frozen Task-171 Ticket/delivery/model state, is absent as required by the reset contract;
11. no new semantic/model/recovery work was manufactured by reset;
12. OpenClaw/Ollama data and unrelated namespaces covered by the contract remain intact;
13. no installer/uninstall/reinstall/rollback/product mutation occurred.

If any required condition is false or materially unproven, report `FAIL`, `BLOCKED`, or `UNPROVEN` as appropriate and stop. Do not retry.

## Acceptance matrix

Include at minimum:

| Criterion | Verdict | Evidence |
|---|---|---|
| Fresh authority/preflight | PASS/FAIL/BLOCKED | remote HEAD + installed/runtime baseline |
| Exactly one reset invocation | PASS/FAIL | process/action ledger |
| Exactly one explicit `y` | PASS/FAIL | prompt/confirmation ledger |
| Reset exit/PASS/fresh MANAGED | PASS/FAIL | command output/exit |
| No helper lifecycle/retry | PASS/FAIL | command/process ledger |
| Installed fingerprint/release preserved | PASS/FAIL | pre/post provenance |
| OpenClaw pin preserved | PASS/FAIL | pre/post version |
| Plugin/controller/Gateway/Ollama/route healthy | PASS/FAIL | post-reset checks |
| Fresh DB integrity/schema | PASS/FAIL | SQLite/bootstrap evidence |
| Old Task-171 CogentNexus durable state removed | PASS/FAIL | pre/post exact-ID queries |
| No semantic/model work manufactured | PASS/FAIL | action/model/durable counters |
| External OpenClaw/Ollama/unrelated namespaces preserved | PASS/FAIL/UNPROVEN | preservation anchors |

A `PASS` disposition is invalid if any required row remains `UNPROVEN`.

## Evidence preservation

Retain enough evidence for narrow reviewer verification, including:

- exact remote authority and preflight snapshot;
- exact installed fingerprint/version identities;
- command/action ledger;
- process/PID evidence when available;
- complete relevant reset output and exit code;
- pre/post controller/plugin/provider/route/Gateway evidence;
- pre/post SQLite integrity/table/count snapshots;
- exact pre/post queries for the frozen Task-171 Ticket/run/model/delivery identity;
- preservation anchors for OpenClaw/Ollama/unrelated namespaces;
- hashes for critical evidence artifacts;
- contradictions/anomalies and their impact;
- explicit proof that no prohibited second action occurred.

## Reviewer Verification Packet

Include 5–10 critical claims with exact evidence pointers and narrow reviewer checks. At minimum include:

1. exactly one reset invocation;
2. exactly one explicit `y`;
3. command exit/PASS/fresh-MANAGED result;
4. installed fingerprint/release and OpenClaw pin preserved;
5. fresh MANAGED runtime health;
6. fresh DB integrity and removal of the exact Task-171 durable identities;
7. zero semantic/model/recovery work manufactured;
8. no retry/helper lifecycle action;
9. external preservation evidence;
10. report-only publication fence.

## Hard fence

Authorized only:

- read-only preflight;
- exactly one `cnxclaw.cmd reset` invocation;
- exactly one interactive `y` confirmation to that invocation;
- implementation-owned subprocesses/process boundaries inside that one reset;
- read-only post-reset evidence collection;
- Task-174 report publication.

Prohibited:

- any semantic Dashboard Send or composer submission;
- `chat.inject` or alternate semantic input;
- manual model inference;
- recovery/regeneration injection;
- second reset;
- executor-issued `start`, `stop`, `restart`, `enable`, or `disable` after reset starts;
- manual Gateway/Ollama/Supervisor/OpenClaw lifecycle mutation;
- installer/install-over;
- uninstall/reinstall/rollback;
- manual DB/Ticket/result/outbox/delivery/transcript/config mutation;
- source/product/test/workflow/dependency changes;
- OpenClaw/dependency upgrade;
- release/tag/package publication;
- merge;
- force push.

## Required report

Publish only after the single reset attempt and all permitted read-only evidence collection are complete:

`docs/operations/coordination/reports/CNX-20260831-174-hermes-reset-fresh-state-reconstruction-acceptance.md`

The report must follow `EXECUTOR_REPORT_CONTRACT.md`.

After report publication, stop for ChatGPT review. **Do not proceed to uninstall automatically.** Uninstall is the next roadmap phase only after Task 174 is independently reviewed and accepted.
