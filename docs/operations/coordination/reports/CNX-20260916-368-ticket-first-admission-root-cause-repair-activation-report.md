# CNX-368 — Ticket-first admission root-cause repair activation report

## Disposition

**Activated: ROOT-CAUSE INVESTIGATION + REPAIR**

CNX-367 is recorded as completed with `CURRENT_RED`. The original Dashboard Ticket-first bypass is reproduced and evidenced. CNX-368 is authorized to investigate that defect and, only after proving the root cause, apply one minimal TDD-gated repair. This activation does not claim that the root cause has been proven or that a repair has been made.

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Exact starting HEAD: `3442c72130a8419fde8c839a6a47387491584e64`
- Starting HEAD was read from the live remote immediately before publication.
- Historical CNX-360 through CNX-367 task/report files were not modified.

## CNX-367 forensic anchor

- Session: `agent:main:dashboard:83027933-3a42-4877-a79a-167caaa396a5`
- Run: `c3e88413-5199-4d0c-bfec-deb33e86928e`
- traceId: `7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`
- Provider/model/API: `openai` / `gpt-5.6-luna` / `openai-chatgpt-responses`
- Dashboard semantic requests: `1`
- OpenAI/model requests: `1`
- Runtime mutations: `0`
- Retry: `0`
- Proven first divergence: `prompt.submitted → model.completed` with no `before_agent_run`, `admission.trace.*`, durable Ticket, Ticket lifecycle, or Ticket-linked Run/Call/Inference/Result/Delivery evidence.

## Root-cause hypothesis and investigation boundary

Initial hypothesis, explicitly unproven: the active OpenAI Dashboard execution crossed a plugin/entrypoint/runtime registration or dispatch boundary that left the CogentNexus Ticket-first admission handler unregistered or bypassed in the Gateway process handling the request. CNX-368 must test this rather than assume it. The investigation must separately prove plugin registration, effective hook registration, event dispatch, OpenClaw integration, session/source eligibility, active installed-entry identity, same-process registration, compatibility boundaries, and whether direct OpenAI execution is outside the plugin hook path.

If the boundary is not observable, diagnostic-only safe-correlated instrumentation must be added first; prompts, credentials, and tokens must not be logged.

## Changes in this activation

Only these live-authority files were added/updated:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`
- `docs/operations/coordination/tasks/CNX-20260916-368-ticket-first-admission-root-cause-repair.md`
- this report

No controller/provider/auth/routing/hook/main/runtime files were changed. No production repair, reinstall, runtime mutation, Dashboard/model request, or semantic requalification was performed.

## Required TDD and verification boundary

CNX-368 must create and verify a focused RED regression test before any production behavior change, implement only the smallest proven root-cause repair, verify GREEN, and run relevant full test/build suites. If root cause cannot be proven, final disposition must be `UNRESOLVED/BLOCKED`; if repaired, live semantic requalification remains separately unauthorized.

## Counts

- Runtime mutation count: `0`
- Dashboard/model request count during this activation: `0`
- Second semantic test count: `0`
- Reinstall count: `0`

## Next authorization

The next permitted work is the bounded CNX-368 root-cause investigation and TDD-gated minimal repair described in the new task. No live Dashboard/model semantic request is authorized until a separate later task explicitly authorizes semantic requalification after CNX-368 publishes its verified disposition.

## Verification status

This report is an activation record. Final remote HEAD and report blob must be verified after the publication commit and are reported in the closeout response, not guessed inside this pre-publication document.
