# Execution Success

Use for delegated, tool-heavy, multi-artifact, local-model, dependency-sensitive, or previously failing work. Scale the workflow down when the task is small.

## Success pipeline

1. **Preflight**
   - Inspect existing files, processes, configuration, queue/session state, and prior verified progress.
   - Confirm the target, platform, tool syntax, write scope, and available validator.
   - For local inference, run a cheap health check before an expensive generation when recent timeout or runtime uncertainty exists.
2. **Definition of Done**
   - State observable artifacts, required behavior, validation commands, and acceptable limitations.
   - Separate must-have checks from optional quality improvements.
3. **Manifest**
   - Inventory deliverables and dependencies before execution.
   - Give every item an identifier, expected output, validator, and status.
   - Use [execution-manifest-template.md](../assets/execution-manifest-template.md) when the task has several artifacts or dependencies.
4. **Capability fit**
   - Match task size to the executor. Give weaker or local models short bounded components; keep orchestration, integration, and acceptance checks outside the generator.
   - Do not delegate a dependency graph as one inference when checkpoints are possible.
5. **Checkpoint execution**
   - Execute one smallest complete unit.
   - Require an artifact or state change, not a plan announcement.
   - Verify immediately and preserve the verified result before continuing.
6. **Independent validation**
   - Treat model/tool output as a candidate until checked against the manifest and Definition of Done.
   - Validate count, non-emptiness, syntax/schema, uniqueness, dependencies, and behavior as applicable.
   - Prefer deterministic checks; use a different evaluator when judgment is required.
7. **Integration**
   - Assemble only validated units.
   - Run final end-to-end checks across boundaries; component success does not prove system success.
8. **Completion gate**
   - Claim success only when every must-have item has evidence.
   - Report partial completion, limitations, and failed checks truthfully.

## Retry ladder

Classify the failure before retrying:

- **Transient tool/service error:** inspect current state, then retry once.
- **Timeout/interruption:** check whether work or a process survived; inspect queue, lock, and orphan state before another run.
- **Validator failure:** return to the original requirements and failed evidence; regenerate or repair the smallest invalid unit.
- **Repeated same symptom:** do not make a third materially identical attempt. Change prompt structure, tool path, task size, or executor.
- **Capability mismatch:** reduce scope, split components, disable unnecessary reasoning, or move to a stronger model.
- **Authorization/external dependency:** stop and request only the missing authority or input.

Never increase timeout or token limits as the sole response to a completeness, dependency, syntax, or termination failure.

## Prompt contract for bounded executors

Include only what changes execution:

- exact target and allowed scope;
- one checkpoint objective;
- observable completion evidence;
- platform/tool constraints;
- validator to run;
- instruction to act before narrating;
- truthful failure reporting.

Avoid asking a bounded model to plan, generate, integrate, validate, and repair a full system in one response.

## Progress state

For long or interruption-prone work, combine the manifest with `task_state.py`. Store:

- verified completed items;
- current item and exact next action;
- failed check and retry strategy;
- evidence location;
- remaining must-have items.

Update status only after validation, not after generation.
