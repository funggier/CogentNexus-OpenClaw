# CNX-350 — Running Gateway Process Provenance

## Status

**READY_FOR_HERMES**

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub branch: `cnx-350-running-gateway-provenance`
- Baseline: `36538a7c8306848f992aa3b0c0bc4f8c0c39b838` (plan commit follows design)
- Parent investigation: CNX-349
- Executor: Hermes
- Reviewer: ChatGPT
- Human authority: Human Operator
- **GitHub remote is authoritative. Local-only work is not evidence.**

## Objective

Determine whether the currently running OpenClaw gateway process actually loaded the intended CogentNexus extension/module and whether the effective runtime exposes the `before_agent_run` registration, so that CNX-344 can be classified as D, E, or UNRESOLVED.

## Scope

Read-only diagnosis only. Do not repair production behavior in CNX-350.

## Required boundary

```text
GitHub source
 -> build/dist artifact
 -> installed extension
 -> running OpenClaw gateway PID
 -> loaded module identity
 -> plugin registration metadata
 -> effective hook registry
 -> Dashboard execution boundary
```

## Required work

1. Read from GitHub:
   - `docs/superpowers/specs/2026-09-15-cnx-350-running-gateway-provenance-design.md`
   - `docs/superpowers/plans/2026-09-15-cnx-350-running-gateway-provenance.md`
2. Verify the GitHub remote branch and exact starting HEAD before investigation.
3. Inventory existing read-only process/runtime diagnostics and repository provenance mechanisms.
4. Bind any plugin/artifact observation to the actual OpenClaw gateway PID. Do not assume a `node.exe` PID is the gateway without evidence.
5. Obtain exact loaded module/path/fingerprint evidence where the environment exposes it.
6. Inspect effective registration metadata or hook registry using read-only means.
7. Compare runtime identity against GitHub/build/install identity. Do not treat TypeScript source hash vs JavaScript dist hash differences as proof by themselves.
8. Trace static Dashboard/webchat execution flow for an E classification only when code/runtime evidence demonstrates bypass.
9. Run fresh focused tests/diagnostics when executable; record exact failures if dependencies are unavailable. Do not install dependencies when prohibited.
10. Commit + push all durable work to the GitHub branch `cnx-350-running-gateway-provenance`.
11. Verify final remote HEAD and changed paths directly from GitHub.
12. Publish the final CNX-350 report on GitHub.

## Hard fences

- No production fix.
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

Only when exact process-scoped evidence shows that the running gateway uses a stale/different artifact/module relative to the GitHub-intended identity.

### E proven

Only when authorized static/read-only execution-path evidence demonstrates that the Dashboard/webchat request path can reach provider execution without invoking `before_agent_run`.

### UNRESOLVED

Neither D nor E is proven. State the exact missing runtime observation and the smallest next probe.

## GitHub delivery contract

Completion requires:

- commit and push to `cnx-350-running-gateway-provenance`;
- exact final GitHub HEAD SHA;
- GitHub verification of changed paths;
- report published and read back from GitHub;
- exact evidence, test/diagnostic results, D/E/UNRESOLVED classification, and hard-fence declaration.

**Do not report local-only evidence as completion evidence.**
