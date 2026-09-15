# CNX-351 Process-Scoped Runtime Introspection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the smallest read-only process-scoped introspection path capable of binding the running OpenClaw Gateway to its loaded CogentNexus module and effective hook registration, or document the exact observability gap.

**Architecture:** Start with existing OpenClaw/Windows diagnostics, then trace from the verified Gateway PID to loaded module/runtime registration metadata. Add only test-only or documentation support where an existing safe introspection surface can be exercised. Never mutate production runtime semantics.

**Tech Stack:** TypeScript, Node.js, Vitest when dependencies are present, Windows process inspection, OpenClaw CLI/runtime diagnostics, SHA-256.

**Spec:** `docs/superpowers/specs/2026-09-15-cnx-351-process-scoped-runtime-introspection-design.md`

## Global Constraints

- GitHub remote is authoritative; local-only work is not evidence.
- Parent baseline is `f0426865160e6a4e2fdef35de397a648fc5a314f`.
- Read-only diagnosis only.
- No install/reinstall, OpenClaw restart, provider routing/config change, runtime/database mutation, UI interaction, semantic Dashboard request, or CNX-344 replay/resend.
- No `durableAdmissionEligible` change, timeout-authority change, or second admission owner.
- No v0.9.5 tag/history mutation, force-push, history rewrite, or self-acceptance.

---

### Task 1: Inventory process-scoped observability

**Files:**
- Modify: none initially.
- Create: `docs/operations/coordination/reports/CNX-20260915-351-process-scoped-runtime-introspection-report.md` at closeout.

**Interfaces:**
- Consumes: GitHub branch and existing OpenClaw/Windows diagnostic mechanisms.
- Produces: exact capability matrix for process PID, loaded module, artifact fingerprint, registration metadata, effective hook registry.

- [ ] **Step 1: Verify GitHub baseline**

Run `git fetch origin`, verify `origin/cnx-351-process-scoped-runtime-introspection`, and confirm `f0426865160e6a4e2fdef35de397a648fc5a314f` is an ancestor.

- [ ] **Step 2: Search repository for existing introspection mechanisms**

Search for `process.pid`, `process.execPath`, `require.cache`, `import.meta.url`, `module`, `plugin`, `registration`, `hook`, `before_agent_run`, `gateway status`, `plugins list`, `diagnostic`, and `sha256`. Read complete relevant files.

- [ ] **Step 3: Inventory current read-only commands**

Use only commands verified in the repository/environment, including OpenClaw gateway status, plugin inventory, Windows process inspection, command-line inspection, and file hashing where applicable. Do not invent undocumented commands.

- [ ] **Step 4: Build capability matrix**

Record availability and process-scoped quality for each evidence item. Mark unavailable surfaces explicitly as `UNOBSERVABLE`.

---

### Task 2: Build the smallest test-only diagnostic adapter

**Files:**
- Create: `plugins/cogentnexus-openclaw/src/cnx351-process-scoped-introspection.test.ts` only if a safe repository test seam exists.

**Interfaces:**
- Consumes: read-only introspection surface from Task 1.
- Produces: deterministic assertions separating repository identity, installed identity, and running-process identity.

- [ ] **Step 1: Write the diagnostic assertions first**

Require explicit evidence for the running Gateway PID and, where exposed, module/artifact identity and effective hook registry. Do not fabricate missing fields.

- [ ] **Step 2: Run focused diagnostics**

Run `npm test -- --run src/cnx351-process-scoped-introspection.test.ts`. If dependencies are absent, record the exact blocker and do not install them.

- [ ] **Step 3: Add only test-only/read-only adapters**

Adapters may consume command output or safe process/file reads but must not start/stop/restart/install/mutate OpenClaw.

- [ ] **Step 4: Re-run and record evidence**

The output must clearly label which claims are repository/test-shaped versus process-scoped.

---

### Task 3: Determine D/E observability status

**Files:**
- Modify: CNX-351 test only when needed.
- Create: CNX-351 report.

**Interfaces:**
- Consumes: capability matrix and diagnostic results.
- Produces: D, E, or UNRESOLVED with the exact missing observation.

- [ ] **Step 1: Evaluate D**

A D classification requires exact process-scoped evidence of a mismatch between the running artifact/module and the GitHub-intended/install identity. Do not equate TS-vs-JS hashes with mismatch.

- [ ] **Step 2: Evaluate E**

Use static/read-only execution-path evidence only. No live Dashboard request. E requires a provable path to provider execution without `before_agent_run`.

- [ ] **Step 3: Stop at diagnosis**

Even if D or E is proven, do not modify production in CNX-351.

---

### Task 4: GitHub verification and closeout

**Files:**
- Create/modify: `docs/operations/coordination/reports/CNX-20260915-351-process-scoped-runtime-introspection-report.md`

**Interfaces:**
- Consumes: all prior evidence.
- Produces: GitHub-verifiable final report.

- [ ] **Step 1: Run fresh verification available in the environment**

Run exact focused tests/diagnostics. Run `npm run build` and `npm test` only if dependencies are available and relevant source/test changes warrant them.

- [ ] **Step 2: Commit and push**

Use only `cnx-351-process-scoped-runtime-introspection`.

- [ ] **Step 3: Verify remote HEAD from GitHub**

Read the branch ref from GitHub and record the final exact SHA.

- [ ] **Step 4: Verify changed paths from GitHub**

Confirm all durable files and ensure no production behavior-changing file was modified.

- [ ] **Step 5: Read back the final report from GitHub**

The report must include exact process/module/hook observations, D/E/UNRESOLVED classification, tests, and hard-fence declaration.

- [ ] **Step 6: Stop**

No repair in CNX-351. A production repair requires a new task with a reproducible RED test.