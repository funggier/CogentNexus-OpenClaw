# CNX-349 Runtime Artifact & Effective Hook Provenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce read-only evidence that distinguishes stale/different runtime artifact loading (D), Dashboard hook bypass (E), or unresolved status for CNX-344.

**Architecture:** Begin with GitHub-verified source and built artifact identities, then inspect existing OpenClaw runtime/process/plugin metadata without changing runtime state. Add only test/diagnostic code needed to compare identities or exercise existing read-only introspection; never modify production behavior in this task.

**Tech Stack:** TypeScript, Vitest, Node.js filesystem/process read-only APIs, existing OpenClaw plugin/runtime diagnostics.

**Spec:** `docs/superpowers/specs/2026-09-15-cnx-349-runtime-artifact-provenance-design.md`

## Global Constraints

- GitHub remote is authoritative; local-only work is not evidence.
- Parent baseline is `5d02a044007ece94b66d1845ecbdf7d686678498`.
- Diagnostic/evidence-only; no production behavior change.
- No install/reinstall, restart, provider-routing change, runtime/config/database mutation, UI interaction, or semantic Dashboard request.
- No CNX-344 replay/resend.
- No v0.9.5 tag/history mutation.
- No second admission owner.
- No timeout or `durableAdmissionEligible` change.

---

### Task 1: Inventory existing provenance surfaces

**Files:**
- Modify: none initially.
- Test: existing diagnostic tests only if an inventory probe is needed.
- Create: `docs/operations/coordination/reports/CNX-20260915-349-runtime-artifact-provenance-report.md` at closeout.

**Interfaces:**
- Consumes: GitHub source tree at the CNX-349 branch and existing runtime/provenance diagnostics.
- Produces: documented list of exact read-only provenance sources available to test or inspect.

- [ ] **Step 1: Search repository for artifact/module/runtime provenance helpers**

Use repository search for terms such as `import.meta.url`, `process.pid`, `plugin`, `registration`, `fingerprint`, `installed`, `dist`, `module`, `runtime`, and `before_agent_run`.

- [ ] **Step 2: Inspect complete relevant source files**

Read the smallest complete set of source files that expose plugin installation fingerprints, runtime registration state, process metadata, or existing diagnostics. Do not infer runtime state from source alone.

- [ ] **Step 3: Record a boundary matrix**

Document which boundary each existing mechanism can actually prove:

```text
GitHub source identity        -> source revision only
Build/dist identity           -> build artifact only
Installed artifact identity   -> installed files only
Running-process identity      -> actual process only
Hook registry identity        -> effective runtime only
Dashboard invocation evidence -> execution-path only
```

No production edit is allowed in this task.

---

### Task 2: Build the smallest provenance probe

**Files:**
- Create: `plugins/cogentnexus-openclaw/src/cnx349-runtime-artifact-provenance.test.ts`

**Interfaces:**
- Consumes: read-only repository/build/runtime metadata surfaces discovered in Task 1.
- Produces: deterministic evidence records identifying source/build/install/runtime identity where available.

- [ ] **Step 1: Write failing assertions for unavailable identities**

The test must assert only identities that the environment can legitimately expose. Do not fabricate a running-process identity. Where an identity source is expected but absent, fail with an explicit diagnostic message naming the missing boundary.

- [ ] **Step 2: Run the focused test and capture RED/limitation**

Run:

```text
npm test -- --run src/cnx349-runtime-artifact-provenance.test.ts
```

Expected outcome is either a meaningful RED identifying a missing provenance surface or GREEN proving the available read-only provenance path. A generic fixture failure does not count.

- [ ] **Step 3: Implement only test/diagnostic support required for real read-only evidence**

If repository code already exposes a safe read-only function, call it. If a tiny test-only adapter is required, keep it inside the test. Do not alter production runtime behavior merely to expose instrumentation in this task.

- [ ] **Step 4: Re-run the focused test**

Confirm the evidence output distinguishes repository module identity from installed/running-process identity. Do not claim D unless the evidence comes from the actual runtime process.

- [ ] **Step 5: Run adjacent registration tests**

Run the focused CNX-347/CNX-348 tests to ensure the diagnostic work does not alter their behavior.

---

### Task 3: Classify D versus E using only authorized read-only evidence

**Files:**
- Modify: `plugins/cogentnexus-openclaw/src/cnx349-runtime-artifact-provenance.test.ts` only when required by the evidence model.
- Create: `docs/operations/coordination/reports/CNX-20260915-349-runtime-artifact-provenance-report.md`

**Interfaces:**
- Consumes: Task 2 provenance results.
- Produces: D/E classification or explicit unresolved status.

- [ ] **Step 1: Test D using exact artifact/module identity comparison**

Compare GitHub/source identity against any available installed/runtime identity. A path, module URL, content hash, or published fingerprint must be exact enough to establish sameness/difference.

- [ ] **Step 2: Test E without semantic/UI traffic**

Inspect existing execution-path code, hook registration surfaces, and testable call boundaries to determine whether Dashboard/webchat invocation can bypass `before_agent_run`. Do not perform a real Dashboard request.

- [ ] **Step 3: Write one evidence-backed classification**

Use exactly one of:

```text
D — stale/different runtime artifact proven
E — Dashboard execution path bypass proven by existing read-only/test evidence
UNRESOLVED — neither D nor E proven
```

- [ ] **Step 4: Confirm hard fences**

Explicitly record that there was no install/restart, provider routing mutation, runtime/config/database mutation, UI interaction, semantic request, or CNX-344 replay.

---

### Task 4: Full verification and GitHub publication

**Files:**
- Create/modify: CNX-349 report only.

**Interfaces:**
- Consumes: Tasks 1-3 evidence.
- Produces: GitHub-verifiable closeout report and remote commit.

- [ ] **Step 1: Run focused tests fresh**

Run the exact CNX-349 test and relevant CNX-347/CNX-348 tests. Record command and output.

- [ ] **Step 2: Run full suite/build only when diagnostic implementation changed test or source structure**

Run:

```text
npm run build
npm test
```

Record actual results; do not claim success if either is not run.

- [ ] **Step 3: Commit and push to GitHub**

Use only branch `cnx-349-runtime-artifact-provenance`.

- [ ] **Step 4: Verify GitHub remote HEAD**

Fetch the branch/ref from GitHub and verify the exact final SHA and changed paths.

- [ ] **Step 5: Publish the report on GitHub**

The report must include the exact SHA, evidence, D/E classification, tests, and hard-fence declaration.

- [ ] **Step 6: Stop without repair**

Even when D or E is identified, do not modify production in CNX-349. The next production change must be a separate repair task with its own RED test.
