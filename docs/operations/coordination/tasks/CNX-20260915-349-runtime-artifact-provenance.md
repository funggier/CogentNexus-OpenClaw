# CNX-349 — Runtime Artifact & Effective Hook Provenance

## Status

**READY_FOR_HERMES**

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- GitHub branch: `cnx-349-runtime-artifact-provenance`
- Baseline: `5d02a044007ece94b66d1845ecbdf7d686678498`
- Parent investigation: CNX-348
- Executor: Hermes
- Reviewer: ChatGPT
- Human authority: Human Operator
- **GitHub remote is authoritative. Local-only work is not evidence.**

## Objective

Determine whether the OpenClaw process associated with the CNX-344 symptom loaded a stale/different CogentNexus artifact/module (D), whether the Dashboard execution path bypasses `before_agent_run` (E), or whether the distinction remains unresolved.

## Scope

Read-only diagnosis only. Do not repair production behavior in CNX-349.

## Required boundary

```text
GitHub source
 -> build/dist artifact
 -> installed plugin artifact
 -> running OpenClaw process
 -> loaded module identity
 -> actual plugin registration metadata
 -> effective hook registry
 -> Dashboard execution path
 -> before_agent_run invocation
```

## Required work

1. Verify the GitHub branch and exact HEAD before working.
2. Read the CNX-349 design and implementation plan from GitHub.
3. Inventory existing repository/OpenClaw provenance diagnostics before adding code.
4. Build the smallest evidence-only probe that can compare source/build/install/running identities where the environment exposes them.
5. Prefer exact paths, hashes, module URLs, fingerprints, registration metadata, process IDs, or existing diagnostics over assumptions.
6. Distinguish D from E using only authorized read-only evidence.
7. Add a test-only negative control where useful, but do not treat synthetic control evidence as proof about the live OpenClaw process.
8. Run fresh focused tests; run full suite/build when test/source structure changes require it.
9. Commit + push every durable change to GitHub branch `cnx-349-runtime-artifact-provenance`.
10. Verify final remote HEAD and changed paths directly from GitHub.
11. Publish the final CNX-349 report on GitHub.

## Hard fences

- No production fix without a reproducible RED test.
- No change to `durableAdmissionEligible`.
- No timeout authority change.
- No second admission owner.
- No provider-routing change.
- No runtime/config/database mutation.
- No install/reinstall.
- No OpenClaw restart.
- No semantic Dashboard request.
- No UI interaction.
- No CNX-344 replay/resend.
- No v0.9.5 tag/history mutation.
- No force-push/history rewrite.
- No self-acceptance.

## Terminal states

### D proven

Stop at diagnosis. Report exact evidence showing the running process/module/artifact differs from the GitHub-intended identity. Create no repair in this task.

### E proven

Stop at diagnosis. Report exact read-only evidence showing the Dashboard execution path bypasses `before_agent_run`. Create no repair in this task.

### Unresolved

Remain `BLOCKED`. State which evidence boundary could not be observed and recommend the smallest next read-only probe.

## GitHub delivery contract

Before reporting completion, the report must contain:

- exact remote branch;
- exact final GitHub HEAD SHA;
- parent baseline/lineage;
- exact changed files;
- exact fresh test/build commands and results;
- source/build/install/runtime provenance observations;
- D/E classification or unresolved statement;
- production-change declaration;
- confirmation of all hard fences.

**Never report local commit SHA or local test state as completion evidence without GitHub remote verification.**
