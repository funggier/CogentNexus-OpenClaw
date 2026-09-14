# CNX-342 — Installation Provenance Requalification

- Parent: `CNX-341`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Status: `READY_FOR_HERMES`

## Objective

Repair the proven installation/provenance gap from CNX-341 by rebuilding the already-reviewed CNX-340A repair source as a complete plugin artifact, verifying the entry module and its imported direct-model-call lease module are from the same repaired build, replacing the active installed artifact safely, and refreshing the Gateway load boundary once. Do not perform live semantic requalification in CNX-342.

## Source authority

Use the reviewed repair branch:
`agent/v0.9.6-direct-model-call-timeout-authority-repair`

Do not modify that source branch as part of this task.

## Required repaired-content checks

The resulting complete artifact must contain the repaired direct-model-call lease implementation with:

- `runtimeModelCallTimeoutMs(api, event, ctx)`
- `timeoutMs: runtimeModelCallTimeoutMs(api, event, ctx)` in the `model_call_started` handler

Verify both the entry module and imported lease module by exact SHA-256. Entry-only matching is insufficient.

## Hard fences

- No Dashboard session creation.
- No `New session` click.
- No semantic request.
- No OpenAI/Ollama inference.
- No live timeout requalification.
- No provider/model/timeout configuration changes.
- No production source/test changes.
- No `v0.9.5` history/tag/release changes.
- No force push/history rewrite.
- Exactly one controlled Gateway restart/load refresh, and only after all installation prechecks pass.
- Preserve the previous installed artifact for rollback before replacement.
- If any artifact or installation evidence is ambiguous, stop and report `BLOCKED`.

## Required procedure

1. Verify the exact reviewed repair commit.
2. Build the complete plugin artifact without changing source/tests.
3. Run existing artifact/build validation.
4. Record exact hashes for:
   - `dist/v091-release-entry.js`
   - `dist/v091-direct-model-call-lease.js`
5. Record the pre-install hashes at the active plugin path.
6. Preserve a rollback copy of the complete previous installed plugin.
7. Install the complete rebuilt artifact as one consistent set.
8. Before restart, verify entry/imported lease hashes match the rebuilt artifact and the installed lease module contains the repaired resolver and handler call site.
9. Record an installation manifest binding the repair commit, entry hash, lease hash, and install timestamp. The manifest is evidence only and must not alter runtime configuration semantics.
10. Perform exactly one controlled Gateway restart/load-boundary refresh.
11. After restart, capture old/new Gateway PID, restart outcome, active installed hashes, and available load/startup evidence.
12. Do not send a semantic request after restart.

## PASS criteria

PASS only if the complete rebuilt artifact is internally consistent, both relevant module hashes match after installation, the active imported lease module is the repaired implementation, the rollback copy exists, exactly one Gateway restart succeeds, and the post-restart Gateway is healthy from the repaired installation path.

## FAIL / BLOCKED

- Hash mismatch: `FAIL — ARTIFACT_PROVENANCE_MISMATCH`
- Repaired entry with legacy imported lease module: `FAIL — MIXED_PLUGIN_ARTIFACT`
- Restart/load failure: `FAIL — GATEWAY_RESTART_OR_LOAD_FAILURE`
- Evidence insufficient: `BLOCKED — INSTALLATION_EVIDENCE_INSUFFICIENT`

## Report

Publish:
`docs/operations/coordination/reports/CNX-20260914-342-installation-provenance-requalification-report.md`

Include exact source commit, build/validation results, pre/post hashes, rollback evidence, installation manifest, old/new Gateway PID, restart/load evidence, and explicit proof that no semantic traffic or inference occurred.

Stop for independent ChatGPT review. Do not self-accept CNX-342.
