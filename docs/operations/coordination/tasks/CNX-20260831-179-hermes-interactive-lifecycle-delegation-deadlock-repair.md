# CNX-20260831-179 — Interactive Lifecycle Delegation Deadlock Repair

- **Task:** `CNX-20260831-179`
- **Execution mode:** `REPOSITORY_INTERACTIVE_LIFECYCLE_DELEGATION_DEADLOCK_REPAIR_HERMES`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority HEAD before work:** `e5ad22907cfaa1775c472764fb29bba42167b8d1`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT

## Objective

Repair the production interactive lifecycle delegation boundary exposed by Task 178.

The accepted source path is structurally incompatible with prompt-before-input execution because `cnxclaw.py` captures `host_control_v092.py` stdout/stderr and forwards it only after child completion, while `host_control_v092.py` enters `lifecycle_v092.py` and waits for interactive confirmation.

Task 179 must first safely retire the exact still-running Task-178 process tree if it remains present, then use TDD to prove and minimally repair the nested interactive delegation defect. This task does **not** authorize a new reset, uninstall, install-over, reinstall, semantic action, or release.

## Accepted baseline

- Product repair SHA before this task: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint before this task: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- OpenClaw: `2026.7.1-2`
- Task 177: `ACCEPTED_DIAGNOSTIC_PASS — CMD_BATCH_INCREMENTAL_HARNESS_QUALIFIED`
- Task 178: `ACCEPTED_FAILURE_BOUNDARY — RESET_INTERACTIVE_PROMPT_BLOCKED_BY_NESTED_DELEGATION_CAPTURE`

Task-171 semantic Send count remains permanently frozen at exactly `1`.

## Root-cause evidence to preserve

Current accepted production chain:

```text
cnxclaw.cmd
  -> cnxclaw_v093.py
      -> legacy cnxclaw.py
          -> delegate(...)
              -> subprocess.run(host_control_v092.py, capture_output=True)
                  -> lifecycle_v092.main(reset/uninstall)
                      -> input("Continue? [y/N]: ")
```

Because `delegate()` waits for the captured child to return before forwarding its stdout/stderr, the lifecycle prompt cannot reach an outer interactive terminal/harness before that lifecycle child receives input and exits.

The v0.9.2 lifecycle reset source performs only read-only preflights before `base.confirm("reset")`; destructive mutation begins after confirmation succeeds.

## Phase A — exact Task-178 hung-process cleanup

Before any repository write:

1. fetch fresh remote HEAD, `ACTIVE.md`, and `STATUS.md`; verify Task 179 is active;
2. read the Task-178 evidence ledger/result again;
3. verify `prompt_observed=0`, `input_send_intent=0`, and `input_sent=0` remain the retained Task-178 boundary;
4. perform a fresh read-only process scan for the exact Task-178 identities and command chain, including outer harness session/PID where available, reset `cmd.exe` PID `17864` if still valid, and its exact installed Python descendants;
5. verify current runtime/DB state has not crossed the destructive reset boundary.

If the Task-178 process tree is already gone, record that fact and do not kill anything.

If and only if the exact Task-178 tree is still alive and identity is unambiguous, Task 179 authorizes termination of **only that exact Task-178 harness/reset command tree**. Do not terminate Gateway, Ollama, unrelated Python/cmd processes, OpenClaw service processes, or any process whose identity is ambiguous.

After cleanup, prove no Task-178 reset/harness descendant remains and collect read-only status/DB health. Cleanup is not a new reset and must not send any confirmation input.

## Phase B — TDD RED reproduction

Before production source changes, create the smallest repository-native regression test that reproduces the nested interactive boundary without touching live CogentNexus/OpenClaw state.

The test must model the production topology sufficiently to prove the defect:

```text
outer test/harness
  -> cnxclaw facade delegation
      -> harmless fake host-control child
          -> writes a non-newline confirmation prompt
          -> waits for one input line
```

Preferred approach: temporarily point/monkeypatch the facade's `HOST_CONTROL` dependency to a disposable harmless Python child and execute the delegation path under piped stdin/stdout so the test can assert prompt visibility before supplying input.

RED requirements:

- the test must fail or time out against the pre-fix implementation specifically because the outer observer cannot receive the prompt before child completion;
- no real `reset`, `uninstall`, Gateway/provider lifecycle, DB, transcript, route, or installation mutation may occur;
- capture the exact RED command/output/exit/timeout evidence;
- independently verify that a normal noninteractive delegated child still behaves as expected so the repair scope remains narrow.

Do not edit production source until the RED failure is demonstrated.

## Phase C — minimal production repair

Implement the smallest source change that preserves interactive destructive lifecycle I/O across the facade -> host-control boundary.

The intended design is an explicit interactive delegation path for `reset` and `uninstall` that inherits or directly streams stdin/stdout/stderr instead of using post-completion `capture_output=True` buffering.

A minimal shape is acceptable, for example:

- keep existing `delegate()` behavior for normal noninteractive commands;
- add a narrowly scoped `delegate_interactive()` or equivalent;
- route only `reset` / `uninstall` through the interactive path;
- preserve `--root`, provider arguments, Windows creation flags, child exit code, explicit-y semantics, cancellation semantics, and v0.9.3 Ollama-only policy;
- do not change lifecycle transaction ordering or safety logic unless a separate failing test proves it necessary.

Do not solve this by auto-sending/pre-piping `y`, hidden confirmation flags, source-side default yes, weakening confirmation, or special-casing the acceptance harness.

## Phase D — GREEN and regression validation

After the minimal fix:

1. rerun the new regression test and prove prompt-before-input works;
2. prove exactly one supplied input reaches the harmless child and exact exit/output propagate;
3. prove cancel/non-`y` behavior remains representable without hidden confirmation;
4. rerun relevant lifecycle/facade/provider tests;
5. run the full Python test suite used by stabilization;
6. run relevant plugin TypeScript tests, typecheck/build/package validation if the source/package surface requires them;
7. run any repository-native installer/package contract tests affected by the source payload;
8. produce a package/fingerprint/provenance candidate for the new repair commit, but **do not install it on the live Windows machine in Task 179**.

## Phase E — exact-SHA CI

Because Task 179 changes production source, run the relevant exact-SHA GitHub workflows on the repair commit, including at minimum the stabilization Validate, Windows Installer, and PowerShell 5.1 workflows used for the accepted candidate where applicable.

Record run IDs, attempts, commit SHA, job results, and any coordination/concurrency cancellation separately from product failures. Do not claim exact-SHA CI PASS unless the required workflows complete successfully for the repair commit.

## Hard fence

Task 179 semantic action budget: `0`.

Authorized live mutation is limited to retiring the exact Task-178 hung process tree after identity/zero-input re-verification.

Not authorized:

- new `cnxclaw reset`;
- uninstall;
- install/install-over/reinstall/rollback;
- start/stop/restart/enable/disable to help tests or runtime;
- Gateway/Ollama manual restart;
- Dashboard Send/composer input/`chat.inject`;
- model inference/recovery/regeneration;
- manual durable/config/transcript/route/DB repair;
- upgrade/release/tag/merge;
- force push.

Repository source/test changes required for the TDD repair are authorized.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260831-179-hermes-interactive-lifecycle-delegation-deadlock-repair.md`

The report must follow `EXECUTOR_REPORT_CONTRACT.md` and include:

- disposition;
- exact authority/start/end HEADs;
- Task-178 process cleanup evidence;
- root-cause trace;
- RED proof;
- minimal source diff and rationale;
- GREEN/focused/full validation;
- exact-SHA CI evidence;
- new candidate fingerprint/package provenance if produced;
- acceptance matrix;
- 5–10 claim Reviewer Verification Packet;
- residual unknowns;
- publication fence;
- proposed successor.

After report publication, stop for ChatGPT review. Live installation and another reset remain unauthorized until a successor task explicitly opens them.