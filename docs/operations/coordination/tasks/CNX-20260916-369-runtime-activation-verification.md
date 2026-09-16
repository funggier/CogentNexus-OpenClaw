# CNX-369 — Repaired Artifact Runtime Activation Verification

Status: `READY_FOR_HERMES`
Classification: `RUNTIME ACTIVATION VERIFICATION`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Parent: `CNX-20260916-368`

## Objective

Activate the repaired CogentNexus plugin artifact in the exact path-bound OpenClaw runtime and prove that the active Gateway process is using the repaired entrypoint before any live semantic requalification.

Repaired entrypoint SHA-256:
`04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802`

Canonical repaired source SHA-256:
`f033b4a588421da097d3db0f8247e741c1de5cf8782cadcbfb2db993840e6a9a`

## Required sequence

1. Read current GitHub authority and confirm CNX-368 is complete and live semantic requalification is not yet authorized by the current authority.
2. Verify the current canonical state root, controller, ownership manifest, launcher, installed plugin manifest, and installed entrypoint.
3. Verify the installed entrypoint against repaired SHA-256.
4. If the active installed entrypoint is not the repaired artifact, use the supported, bounded activation/reload/install path required to make the repaired artifact active. Do not edit controller state manually or bypass the supported lifecycle.
5. Verify the resulting Gateway process identity and effective plugin registration.
6. Prove the active process has loaded the repaired entrypoint, not merely that the repaired file exists on disk.
7. Verify the plugin authority gate accepts the live canonical schema-v2 controller and that the downstream `before_agent_run` registration path is active.

## Live semantic request fence

CNX-369 must NOT send a Dashboard semantic message or OpenAI/model request. No live requalification occurs in this task.

## Runtime mutation boundary

A supported runtime reload/restart/reinstall may be required solely to activate the already-verified repaired artifact. Any such mutation must be explicitly recorded with exact action, time, process identity before/after, and resulting artifact identity.

No controller normalization, provider/auth/routing change, hook/main source change, or unrelated repair is allowed.

## Success condition

`RUNTIME_ACTIVATION_PROVEN`

only when the active Gateway process is demonstrably using the repaired entrypoint and the effective registration path is proven.

## Failure condition

`UNRESOLVED/BLOCKED` if the active runtime cannot be proven to use the repaired entrypoint or activation cannot be completed safely.

## Deliverable

Publish:
`docs/operations/coordination/reports/CNX-20260916-369-runtime-activation-verification-report.md`

Include exact branch/head, pre/post process identity, exact installed entrypoint SHA, activation action if any, effective registration evidence, request counts, mutation counts, and explicit semantic-test authorization boundary.

After publication, verify the report and branch from GitHub remote and STOP.
