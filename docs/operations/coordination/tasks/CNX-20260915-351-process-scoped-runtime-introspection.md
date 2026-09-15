# CNX-351 — Process-Scoped Runtime Introspection

## Status

**READY_FOR_HERMES**

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub branch: `cnx-351-process-scoped-runtime-introspection`
- Baseline: `f0426865160e6a4e2fdef35de397a648fc5a314f` (CNX-350 finalization)
- Parent investigation: CNX-350
- Executor: Hermes
- Reviewer: ChatGPT
- Human authority: Human Operator
- **GitHub remote is authoritative. Local-only work is not evidence.**

## Objective

Determine whether the environment can expose a trustworthy process-scoped introspection boundary for the already-running OpenClaw Gateway, so that the installed CogentNexus artifact can be bound to the actual loaded module and effective `before_agent_run` registration.

The task is diagnostic only. It must not repair production behavior.

## Required boundary

```text
GitHub source
 -> installed extension
 -> running Gateway PID
 -> loaded JavaScript module
 -> plugin registration
 -> effective before_agent_run registry
```

## Required work

1. Read these documents from the GitHub branch before working:
   - `docs/superpowers/specs/2026-09-15-cnx-351-process-scoped-runtime-introspection-design.md`
   - `docs/superpowers/plans/2026-09-15-cnx-351-process-scoped-runtime-introspection.md`
2. Verify the GitHub remote branch and exact starting HEAD before investigation.
3. Inventory existing repository/OpenClaw/Windows read-only introspection mechanisms.
4. Bind observations to the actual Gateway process; do not assume a `node.exe` PID.
5. Attempt to expose the loaded CogentNexus module path/URL and artifact fingerprint for the actual Gateway process.
6. Attempt to expose live plugin registration metadata and effective `before_agent_run` registry/handler identity.
7. Distinguish static plugin inventory from process-scoped dynamic state.
8. Add only test-only/read-only adapters where an existing safe introspection boundary can be exercised. Do not alter production runtime semantics merely to expose instrumentation.
9. Run fresh focused tests/diagnostics when executable. Record exact blockers when dependencies are absent. Do not install dependencies solely to run the test.
10. Classify only `D proven`, `E proven`, or `UNRESOLVED` according to the design.
11. Commit, push, and verify all durable work on GitHub branch `cnx-351-process-scoped-runtime-introspection`.
12. Publish the final report to GitHub and read it back from GitHub.

## TDD / evidence rules

- A diagnostic RED that only shows the environment lacks an introspection surface is not proof of the CNX-344 production defect.
- Do not change production behavior to make the diagnostic pass.
- Do not infer D from TypeScript-source vs JavaScript-dist hashes alone.
- Do not infer E from `hookCount=0` in `openclaw plugins list --json` alone.

## Hard fences

- No production behavior change.
- No install/reinstall.
- No OpenClaw restart.
- No provider routing change.
- No runtime/config/database mutation.
- No UI interaction.
- No semantic Dashboard request.
- No CNX-344 replay/resend.
- No change to `durableAdmissionEligible`.
- No timeout-authority change.
- No second admission owner.
- No v0.9.5 tag/history mutation.
- No force-push/history rewrite.
- No self-acceptance.

## Classification rules

### D proven
Only when exact process-scoped evidence shows the running Gateway uses a stale/different CogentNexus artifact/module compared with the GitHub-intended/install identity.

### E proven
Only when authorized static/read-only evidence establishes that the Dashboard/WebChat execution path can reach provider execution without invoking `before_agent_run`.

### UNRESOLVED
Neither D nor E is proven. State the exact missing observation and the smallest next read-only probe.

## GitHub delivery contract

Before reporting completion:

- commit all durable changes;
- push to `cnx-351-process-scoped-runtime-introspection`;
- verify final remote HEAD directly from GitHub;
- verify changed paths directly from GitHub;
- publish `docs/operations/coordination/reports/CNX-20260915-351-process-scoped-runtime-introspection-report.md` on GitHub;
- read the report back from GitHub;
- report exact remote SHA, tests/diagnostics, evidence, classification, production-change status, and hard-fence status.

**Local-only work is not evidence and must not be reported as completion.**

## Terminal behavior

If process-scoped introspection is unavailable, stop at `UNRESOLVED / BLOCKED`. Do not invent a runtime interface and do not create a repair task until a real defect boundary is evidenced.