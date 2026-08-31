# CNX-20260831-178 — ChatGPT Review: Qualified-Harness Reset Reacceptance

## Disposition

**ACCEPTED_FAILURE_BOUNDARY**

Final label:

`FAIL — RESET_INTERACTIVE_PROMPT_BLOCKED_BY_NESTED_DELEGATION_CAPTURE`

Task 178 is accepted as a faithful one-shot failure experiment, not as reset acceptance. The Task-177-qualified outer harness started exactly one installed reset command and retained incremental evidence, but the real lifecycle prompt never became observable and no confirmation was sent. Reset acceptance remains open and uninstall remains unauthorized.

## Reviewed authority

Repository: `funggier/CogentNexus-OpenClaw`

Branch: `agent/v0.9.3-full-stabilization`

Task-178 report publication commit:

`e5ad22907cfaa1775c472764fb29bba42167b8d1`

Report parent / authorization HEAD:

`8212c06bbebe2e0a577dd568433a9c9df24fb5f0`

Independent compare proves the Task-178 publication commit added exactly one file: the Task-178 report. No repository product/source/test/workflow drift was introduced by Task 178.

## Task-178 execution findings

The executor proved:

- fresh preflight was valid;
- exactly one Task-178 reset invocation was started;
- qualified character-level prompt capture and concurrent stdout/stderr draining were active;
- the incremental ledger retained only `harness_started` and `cmd_process_started`;
- `prompt_observed=0`;
- `input_send_intent=0`;
- `input_sent=0`;
- stdout and stderr remained empty;
- no second reset, second input, helper lifecycle action, cleanup kill, semantic action, model call, or recovery action occurred;
- read-only state still showed the original managed runtime and the old Task-171 durable rows.

The reset process remained alive at report preparation time, so reset completion/fresh-state reconstruction was correctly reported as unproven.

## Independent source trace

The accepted v0.9.3 facade delegates into the v0.9.2 facade. For commands not specially handled by `cnxclaw.py`, including `reset` and `uninstall`, `cnxclaw.py` calls `delegate(root, args)`.

`delegate()` executes `host_control_v092.py` with:

```python
subprocess.run(
    [sys.executable, str(HOST_CONTROL), "--root", str(root), *args],
    capture_output=True,
    text=True,
    creationflags=creation_flags(),
)
```

and only writes the child stdout/stderr to its own streams **after that child returns**.

`host_control_v092.py` routes `reset` and `uninstall` into `lifecycle_v092.main(...)`, where the lifecycle code eventually reaches interactive `input("Continue? [y/N]: ")`.

This creates a structural interactive deadlock for an observer that requires prompt-before-input:

1. lifecycle child prints/writes its confirmation text to stdout owned by the intermediate `capture_output=True` pipe;
2. lifecycle child waits for stdin confirmation;
3. `cnxclaw.py` waits for `host_control_v092.py` to finish before forwarding captured stdout;
4. the outer terminal/harness cannot observe the prompt and therefore correctly does not send `y`.

Task 177 qualified `cmd.exe -> .cmd -> Python input()` but did not include this additional Python facade -> captured host-control child boundary. Task 178 exposed that missing production topology.

## Destructive safety classification

The v0.9.2 lifecycle `reset()` performs ownership/provider/route/plugin preflights first, then calls `base.confirm("reset")`. The destructive reset transaction begins only after confirmation succeeds.

Task-178 evidence records no prompt observation, no input intent, and no input sent. The read-only state snapshot also remained at the pre-reset durable state. Therefore an exact cleanup of the still-running Task-178 harness/reset process tree is permitted in the successor only after re-verifying those identities and zero-input ledger state. This authorization does not extend to Gateway, Ollama, unrelated Python/cmd processes, or any new reset attempt.

## Acceptance matrix

| Property | Verdict | Reviewer conclusion |
|---|---|---|
| Report-only publication | `PASS` | one report file only |
| Fresh preflight | `PASS` | baseline coherent |
| Exactly one reset invocation | `PASS` | one Task-178 command tree |
| Qualified outer harness used | `PASS` | Task-177 architecture reused |
| Prompt observed | `FAIL / 0` | no prompt event |
| Confirmation sent | `PASS safety / 0` | no `y` sent without prompt |
| Reset completed | `FAIL / UNPROVEN` | process remained alive |
| Fresh state reconstructed | `FAIL / UNPROVEN` | old state remained |
| No retry/helper/semantic action | `PASS` | hard fence respected |
| Product root cause classified | `PASS` | nested delegation capture blocks interactive prompt propagation |

## Final decision

Task 178 is closed as an accepted failure boundary. The next work is not another reset. The product facade must first be repaired so destructive lifecycle commands preserve interactive stdin/stdout/stderr across the facade -> host-control boundary.

The repair must be TDD-driven and minimal. Normal noninteractive delegation behavior should not be changed unnecessarily. After a new source candidate passes local and exact-SHA validation, it must be installed-over and provenance/health reaccepted before reset is attempted again.