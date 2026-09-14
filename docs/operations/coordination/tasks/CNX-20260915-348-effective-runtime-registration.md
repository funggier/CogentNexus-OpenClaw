# CNX-348 — Effective Runtime Registration Provenance

## Status

**READY_FOR_HERMES**

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub branch: `cnx-348-effective-runtime-registration`
- Baseline: `9863316d54727e76e5e73c73c1b7f843d66f74e6` (design commit)
- Parent investigation: CNX-347
- Executor: Hermes
- Reviewer: ChatGPT
- Human authority: Human Operator
- **GitHub is authoritative. Local-only work is not evidence.**

## Objective

Determine the first effective runtime boundary where the CNX-344 OpenAI Dashboard request diverged from the expected `before_agent_run` → Ticket admission lifecycle.

## Scope

Diagnostic/evidence-only phase. Do not change production behavior.

Required boundary:

```text
OpenClaw process
 -> loaded CogentNexus plugin artifact/module
 -> v091-release-entry.register()
 -> legacy wrapper registration chain
 -> api.on("before_agent_run")
 -> effective host hook registry
 -> Dashboard request
 -> before_agent_run invocation
 -> durable admission
 -> Ticket acceptance
```

## Required work

1. Read the design on GitHub:
   `docs/superpowers/specs/2026-09-15-cnx-348-effective-runtime-registration-design.md`
2. Verify remote branch and exact HEAD before working.
3. Build an evidence-only runtime registration provenance harness as close as practical to the OpenClaw loading boundary.
4. Record module identity, registration invocation, hook registration count, handler identity/priority, effective configuration, Promise timing if applicable, and effective registry visibility.
5. Add an intentional negative control that would fail when the registration boundary is broken. A test that only proves the current source path is valid is insufficient.
6. Distinguish candidate divergence classes A-F from the design.
7. Run the focused tests freshly. Do not represent unrun full suite/build as PASS.
8. If no reproducible RED boundary exists, stop BLOCKED and document why.

## Hard fences

- No production fix without a reproducible RED test.
- No change to `durableAdmissionEligible`.
- No change to timeout authority.
- No second admission owner.
- No provider-routing change.
- No runtime/config/database mutation.
- No OpenClaw install/restart.
- No semantic Dashboard request.
- No UI interaction.
- No CNX-344 replay/resend.
- No mutation of v0.9.5 tag/history.
- No force-push/history rewrite.
- No self-acceptance.

## GitHub delivery contract

All durable work must exist on the GitHub remote branch:

`cnx-348-effective-runtime-registration`

Before reporting completion:

- commit all changes
- push to GitHub
- verify the remote branch HEAD SHA from GitHub
- verify changed paths from GitHub
- publish the CNX-348 report on GitHub
- report exact remote SHA, tests, evidence, classification, and production-change status

Local filesystem state does not count unless the corresponding commit is present and verified on GitHub.

## Terminal states

### RED reproduced

Provide the smallest reproducible failing test and exact evidence of the broken boundary. Do **not** implement the production fix in CNX-348 unless separately authorized by a new repair task.

### GREEN / unresolved

Remain `BLOCKED`. State exactly which boundary remains unresolved and recommend the next evidence-only boundary.
