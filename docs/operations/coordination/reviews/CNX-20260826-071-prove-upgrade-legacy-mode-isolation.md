# Review — CNX-20260826-071 Prove Upgrade/Legacy Mode Isolation

Decision: `ACCEPT`

Disposition: `ACCEPT_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`

Reviewed report result: `PASS_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`

Production candidate HEAD: `9df671670908241486afe2badf8a7f221410c6f8`

Task-071 test-only implementation HEAD: `7a55980e662b50f2d2979eb77a3ac1f89da7912f`

Report HEAD: `d1c8382690d1e06e60ef335e26ba19cdde9152df`

## Independent review findings

### Publication fence — PASS

Independent compare confirms:

- `d903ed17b452d74ad6238a5af5080862d8094289 -> 7a55980e662b50f2d2979eb77a3ac1f89da7912f` is exactly one commit adding only `tests/test_upgrade_legacy_mode_isolation_proof.py`;
- `7a55980e662b50f2d2979eb77a3ac1f89da7912f -> d1c8382690d1e06e60ef335e26ba19cdde9152df` is exactly one report-only commit adding only the Task-071 report;
- no production source was changed in Task 071.

### U1 coherent upgrade fixture — PASS

The new test constructs the actual v0.9.3 ownership surfaces on disk using production `build_manifest()`, `write_manifest()`, `verify_manifest()`, expected paths, and an exact plugin payload accepted by production `_plugin_payload()` semantics.

It then invokes production `classify_install(workspace, app_data=...)` and proves `mode == "upgrade"`. No fresh transaction marker exists before or after classification.

This closes the Task-070 M4 evidence gap without hand-assigning upgrade mode.

### U2 upgrade failure isolation — PASS

The executable PowerShell harness derives `$isFreshTransaction` from the output of the production `classify-install` CLI against the coherent upgrade fixture. It reaches the shared installer boundary, injects `UPGRADE_INJECTED_FAILURE`, propagates the original failure, and would fail loudly if fresh rollback were invoked.

The marker remains absent and fixture sentinel state remains unchanged.

### L1 valid legacy fixture — PASS

The legacy fixture satisfies the actual production `prove_legacy_ownership()` contract with three independent identities:

- legacy skill metadata;
- valid passthrough legacy controller;
- legacy launcher content referencing `.cogent`.

Production `prove_legacy_ownership()` and `classify_install()` both return the expected legacy state and no fresh marker is created.

### L2 legacy reachability/isolation — PASS

The legacy executable harness derives mode from production classification, reaches the shared body and native-handoff entry point, then stops with an injected failure before real migration mutation as expressly allowed by Task 071.

Fresh rollback is not invoked, the Task-069 sentinel is absent, and no fresh transaction marker appears.

### Fresh and safety regressions — ACCEPTED EVIDENCE

The report records fresh reruns of the Task-069 caught-failure rollback harness and the focused transaction/application-data/shared-parent/malicious-marker suites. Full verification reported `347 passed, 2 skipped`, PowerShell syntax clean, npm 11.16.0 and npm 12.0.2 clean install/validate/test gates passing, plugin version `0.9.3`, exact OpenClaw devDependency `2026.7.1-2`, baseline consistency PASS, and clean diff/worktree.

The two skips are the same pre-existing environment-gated skips and are not introduced by this task.

## Scope assessment

Task 071 was intentionally source/test-only and the live machine was not mutated. The executable harnesses stop before real non-fresh migration side effects, exactly matching the task authorization. This is sufficient to close the missing mode-specific evidence gap; no additional production change is justified before the live fresh-install gate.

## Accepted production source for live successor

Task 072 must install the exact production source at:

`9df671670908241486afe2badf8a7f221410c6f8`

Task-071 commits after that point are test/report-only and do not alter the production installer.

## Next gate

Task 072 is authorized to re-prove and remove exactly the two unowned partial-install roots created by Task 066, fresh-install the accepted source once, prove exact CogentNexus-owned runtime binding with no durable Hermes/Codex/temp dependency, observe at least three natural PT1M supervisor ticks with no causal console/conhost trampoline, and finish MANAGED/OpenClaw/Ollama/plugin/ownership/AGENTS/SQLite health acceptance.

Real user-message semantic Ticket -> LLM -> response/delivery acceptance remains a separate successor gate and must not be conflated with Task 072 install/runtime acceptance.
