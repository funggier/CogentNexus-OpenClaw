# CNX-20260915-360 — Runtime Activation Verification

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Parent: `CNX-20260915-359`
Execution mode: `SUPPORTED_RUNTIME_ACTIVATION_OBSERVATION_ONLY`
Base release: `v0.9.5`

## Objective

Prove, before any new Dashboard request, that the live OpenClaw runtime has loaded the exact CNX-359 diagnostic candidate source commit:

`1aa7b37c23e2bb2abdd150a893f1f37102731089`

Required evidence chain:

`SOURCE COMMIT -> PACKAGE -> INSTALLED ARTIFACT -> ACTIVE RUNTIME`

## Authority and branch fence

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Execute only from the exact GitHub-authoritative branch and a clean exact-candidate checkout.
- Do not touch `main`, tag/release `v0.9.5`, or rewrite history.
- No force-push.

## Hard fences

- Do not send or control any Dashboard request.
- Do not reuse `CNX359-DONE`.
- Do not change provider routing, OpenAI authentication, model selection, admission semantics, or unrelated configuration.
- Do not manually edit runtime/plugin files outside the supported repository installer/lifecycle.
- Do not infer active identity from build/package success alone.
- Observational checks must not perform model inference.

## Allowed scope

1. Inspect the exact CNX-359 task/report, candidate commit, current branch state, installer, and supported lifecycle.
2. Use the repository's supported installer from the exact verified candidate checkout to install the candidate artifact.
3. Use only the supported reload/restart lifecycle required by that installer; record before/after Gateway health.
4. Run existing read-only status/health/plugin/config/diagnostic observers; no model inference.
5. Publish one evidence-rich report with exact identities, hashes, timestamps, commands, and limitations.

## Required evidence

Record, with exact paths and hashes where supported:

- candidate commit and changed paths;
- package filename, package hash, and package contents/manifest;
- installed plugin version and installed artifact identity/source identity;
- active runtime/plugin module identity and loaded file hash;
- Gateway state before and after activation/reload;
- managed mode, `ticketFirst`, and `preInferenceAdmission` state;
- plugin package/hash or equivalent runtime fingerprint;
- reload/restart timing and healthy postcondition;
- observational checks with no model inference.

The report must explicitly state whether the live runtime identity is proven equal to the candidate commit. If any edge is unproven, classify `BLOCKED` and do not proceed to Dashboard.

## Completion gate

- If active runtime identity is proven: update CNX-360 report, STOP, and hand off to Operator for one new Dashboard session only. Do not perform that Dashboard action.
- If activation or identity proof fails: publish `BLOCKED` with the first unproven edge and STOP.

## Future human handoff (not authorized in this task)

Only after successful activation proof, Operator may create a new Dashboard session, select OpenAI / `gpt-5.6-luna`, reset it, and send exactly:

`Reply exactly with CNX360-DONE.`

No second request is authorized by this task.
