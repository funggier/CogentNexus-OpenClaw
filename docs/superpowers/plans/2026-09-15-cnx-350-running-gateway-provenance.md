# CNX-350 Running Gateway Process Provenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Obtain read-only, process-scoped evidence that distinguishes stale/different runtime artifact loading (D), Dashboard bypass of `before_agent_run` (E), or an unresolved runtime boundary for CNX-344.

**Architecture:** Start from GitHub-verified source and installed-extension identity, then bind the analysis to the actual running OpenClaw gateway PID using read-only OS/process/runtime diagnostics. Prefer existing diagnostics; add only test-only/documentation support where necessary, and never change production behavior.

**Tech Stack:** TypeScript, Node.js, Vitest where dependencies are present, Windows process inspection, OpenClaw CLI/runtime diagnostics, SHA-256 hashing.

**Spec:** `docs/superpowers/specs/2026-09-15-cnx-350-running-gateway-provenance-design.md`

## Global Constraints

- GitHub remote is authoritative; local-only state is not evidence.
- Parent baseline is `b1ecee8a552821872bb4e815c7ba35bd0418e541`.
- Read-only diagnosis only; no production behavior change.
- No install/reinstall, restart, provider-routing change, runtime/config/database mutation, UI interaction, or semantic Dashboard request.
- No CNX-344 replay/resend.
- No v0.9.5 tag/history mutation.
- No second admission owner.
- No timeout or `durableAdmissionEligible` change.
- No force-push/history rewrite.
- No self-acceptance.

---

### Task 1: Inventory existing runtime/process diagnostics

**Files:**
- Modify: none initially.
- Create: `docs/operations/coordination/reports/CNX-20260915-350-running-gateway-provenance-report.md` at closeout.

**Interfaces:**
- Consumes: GitHub repository tree and the Windows/OpenClaw environment available to Hermes.
- Produces: exact inventory of read-only commands/diagnostics capable of binding a plugin artifact to a running gateway process.

- [ ] **Step 1: Verify GitHub baseline**

Run:

```text
git fetch origin
git rev-parse origin/cnx-350-running-gateway-provenance
git merge-base --is-ancestor b1ecee8a552821872bb4e815c7ba35bd0418e541 origin/cnx-350-running-gateway-provenance
```

The branch and ancestry must match GitHub before any investigation proceeds.

- [ ] **Step 2: Inspect existing repository provenance mechanisms**

Search GitHub source for `process.pid`, `process.execPath`, `import.meta.url`, `require.cache`, `module`, `plugin`, `hook`, `registration`, `fingerprint`, `sha256`, `plugins list`, and existing diagnostics. Read complete relevant files.

- [ ] **Step 3: Inventory read-only host/runtime commands**

Determine whether the environment exposes a read-only combination of:

```text
openclaw gateway/status/diagnostics
openclaw plugins list --json
process enumeration
command-line inspection
loaded module inspection
file SHA-256
plugin registration metadata
```

Do not invent command names. Only use commands actually present in the environment or documented in repository code.

- [ ] **Step 4: Record capability matrix**

Produce a matrix such as:

```text
Evidence                  Available  Process-scoped  Exact identity
Gateway PID               yes/no     yes/no          exact/none
Plugin path               yes/no     yes/no          exact/none
Artifact SHA-256          yes/no     yes/no          exact/none
Loaded module URL         yes/no     yes/no          exact/none
Registration metadata     yes/no     yes/no          exact/none
Effective hook registry   yes/no     yes/no          exact/none
Dashboard hook path       yes/no     yes/no          exact/none
```

A missing capability is evidence about the boundary; do not fill it with assumptions.

---

### Task 2: Add only the smallest test/diagnostic support needed

**Files:**
- Create: `plugins/cogentnexus-openclaw/src/cnx350-running-gateway-provenance.test.ts` only if repository tooling can exercise the discovered read-only boundary.

**Interfaces:**
- Consumes: actual read-only provenance mechanism identified in Task 1.
- Produces: deterministic checks that distinguish source identity from process-scoped runtime identity.

- [ ] **Step 1: Write the failing diagnostic assertion**

When a runtime provenance surface is expected and absent, fail with an explicit message identifying the exact missing boundary, for example:

```text
Expected process-scoped OpenClaw gateway PID provenance; no gateway PID was exposed by authorized diagnostics.
```

Do not create a synthetic PID or fake loaded-module record.

- [ ] **Step 2: Run focused test to capture RED or environment limitation**

Run:

```text
npm test -- --run src/cnx350-running-gateway-provenance.test.ts
```

If dependencies are absent and installation is prohibited, record the exact failure and do not install them.

- [ ] **Step 3: Implement only test-only read-only adapters**

Use existing command outputs or safe file/process reads. The adapter must not start, stop, restart, install, or mutate OpenClaw.

- [ ] **Step 4: Re-run focused test**

The result must explicitly distinguish:

```text
repository identity
installed identity
running-process identity
```

A repository identity alone cannot classify D.

---

### Task 3: Determine D versus E without live semantic traffic

**Files:**
- Modify: CNX-350 test only when necessary.
- Create: CNX-350 report.

**Interfaces:**
- Consumes: Task 1 capability matrix and Task 2 evidence.
- Produces: D, E, or UNRESOLVED classification.

- [ ] **Step 1: Test D**

Compare the exact running-process identity against the GitHub-intended source/build/install identity. D requires an exact mismatch, not merely different TypeScript-vs-JavaScript hashes.

- [ ] **Step 2: Test E statically/read-only**

Trace the Dashboard/webchat execution path through available source/runtime evidence. Prove a bypass only if the execution path can reach provider execution without invoking `before_agent_run`.

- [ ] **Step 3: Do not use semantic traffic**

No Dashboard message, UI interaction, replay, resend, or provider call is permitted.

- [ ] **Step 4: Assign exactly one classification**

```text
D — stale/different runtime artifact proven
E — Dashboard execution bypass proven
UNRESOLVED — neither D nor E proven
```

- [ ] **Step 5: Stop at diagnosis**

Even D/E proven is not authorization to repair production in CNX-350.

---

### Task 4: Verification and GitHub closeout

**Files:**
- Create/modify: `docs/operations/coordination/reports/CNX-20260915-350-running-gateway-provenance-report.md`

**Interfaces:**
- Consumes: Tasks 1-3 evidence.
- Produces: GitHub-verifiable report and remote commit.

- [ ] **Step 1: Run fresh verification available in the environment**

Run the exact focused tests. Run `npm run build` and `npm test` only if dependencies and source/test changes make those commands executable; otherwise record the exact blocker and do not claim PASS.

- [ ] **Step 2: Commit all durable changes**

Commit only on:

`cnx-350-running-gateway-provenance`

- [ ] **Step 3: Push to GitHub**

Push the branch and do not force-push.

- [ ] **Step 4: Verify remote HEAD from GitHub**

Fetch the remote ref from GitHub and verify the exact final SHA.

- [ ] **Step 5: Verify changed paths from GitHub**

Confirm every durable file in the final report is present on the remote branch and that no production source was changed.

- [ ] **Step 6: Publish report and stop**

The report must include exact process/artifact evidence, D/E/UNRESOLVED classification, tests, and all hard-fence confirmations. Do not self-accept.
