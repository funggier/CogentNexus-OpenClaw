# CNX-20260918-403 — Production Plugin Discovery Root and Duplicate Candidate Provenance

## Purpose

Continue from CNX-402 after reconciling the production artifact identity.
CNX-401 proves active-registry replacement is mechanically possible. CNX-402 establishes the manifest-selected production entry as v091-release-entry.js with SHA-256 2841b704...c2d95 and records v091-dashboard-verified-delivery.js as a distinct unselected on-disk artifact. The remaining pre-API uncertainty is whether the production Gateway had one unique CogentNexus plugin candidate or multiple discoverable roots/candidates whose filtering, ordering, duplicate-ID precedence, or manifest association could change which candidate reached registration.

This task is diagnosis only and production is strictly read-only.

## Parent
CNX-20260918-402

## Branch
cnx-357-openai-dashboard-ticket-first-requalification-v2

## Executor / Reviewer
Executor: Hermes
Reviewer: ChatGPT
Human final authority: Operator

## Starting authority
Begin from the authoritative branch HEAD and re-read ACTIVE.md, STATUS.md, this task, CNX-402 report, corrected CNX-401 report, CNX-400 report, CNX-399 report, and CNX-398 through CNX-391. Record exact authoritative starting HEAD from GitHub.
Known expected starting HEAD: 0b3220846ea8f769e575310d31f79a347a5d1a72
Verify; do not assume.

## Objective
Establish the exact production plugin discovery candidate set relevant to cogentnexus-openclaw and determine whether multiple roots or duplicate candidates could have affected pre-API selection.
Trace: discovery roots -> candidate paths -> candidate origin -> manifest association -> manifest ID -> duplicate candidate ordering -> seenIds -> selected/overridden candidate -> normalized entry lookup -> eligibility/registration plan.

Distinguish: (1) unique production candidate with no duplicate-selection uncertainty; (2) multiple candidates/roots where duplicate precedence is concrete; (3) conflicting roots/manifest identities; (4) insufficient read-only evidence.

## Required investigation

### 1. Exact installed source
Trace exact OpenClaw 2026.7.1-2 (0790d9f) discovery and loader source for global extension roots, configured load paths, workspace roots, installed/index-derived roots, candidate construction, origin assignment, root canonicalization, manifestByRoot, compareDuplicateCandidateOrder, seenIds, duplicate override semantics, and candidate filtering before normalized-entry lookup. Record exact module hashes and line mappings.

### 2. Production discovery roots
Using read-only inspection only, enumerate every filesystem root that the exact production resolver/config can expose to cogentnexus-openclaw: canonical global extension root, configured plugin load paths, workspace plugin paths, install/index provenance paths, and any other exact resolver-selected root. Do not scan unrelated user data.
For every relevant candidate root record absolute path, origin, existence, manifest presence, manifest ID/version, declared OpenClaw extension entry, effective artifact path if resolvable, artifact SHA-256, and uniqueness/duplication.

### 3. Duplicate candidate analysis
For every candidate with manifest ID cogentnexus-openclaw determine candidate order, ordering inputs, origin, duplicate winner, overridden candidates, whether overridden candidates are activated or only disabled records, and whether ordering can differ across lifecycle contexts. Do not infer from directory names alone.

### 4. Root/manifest identity correlation
For each candidate trace candidate.rootDir -> manifestByRoot lookup -> manifestRecord.id. Compare against plugins.entries.cogentnexus-openclaw. Identify missing manifest, mismatched ID, duplicate same ID, version mismatch, artifact mismatch, or canonicalization mismatch.

### 5. Production process correlation
Read-only only: Gateway PID, command line, current production config, current effective extension root/path, startup log discovery chronology, and any supported diagnostics that name root/origin. No debugger/inspector.

### 6. Artifact identity
Use corrected CNX-402 production identity: v091-release-entry.js / SHA-256 2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95. Treat v091-dashboard-verified-delivery.js / 1276bd... only as an observed alternate unless direct evidence proves participation. Hash declared extension entries for any other plugin copies.

### 7. Isolated exact-source probe
Allowed only when useful without production mutation, global extension installation, dependency patch, debugger, or permanent instrumentation. Prefer a disposable exact comparator/candidate-order fixture. Do not fabricate a production candidate set from relocated copies. Synthetic evidence is mechanism evidence only.

## Required conclusion
Answer directly: Is there exactly one relevant production CogentNexus candidate root? Are there multiple same-ID candidates? Can duplicate precedence change which candidate registers? Can candidate ordering differ between lifecycles? Is there any concrete root/manifest/ID mismatch? Does this materially narrow the remaining missing-hook explanation? What production-local evidence is still unavailable?

## Required classification
Choose exactly one:
PRODUCTION_PLUGIN_DISCOVERY_UNIQUE_ROOT_PROVEN
PRODUCTION_PLUGIN_DISCOVERY_DUPLICATE_SELECTION_RELEVANT
PRODUCTION_PLUGIN_DISCOVERY_CONFLICT_UNRESOLVED
PRODUCTION_PLUGIN_DISCOVERY_INCONCLUSIVE
PRODUCTION_PLUGIN_DISCOVERY_DIAGNOSTICALLY_BLOCKED

Use UNIQUE_ROOT_PROVEN only when all relevant resolver roots are established read-only and no duplicate ambiguity remains. Use DUPLICATE_SELECTION_RELEVANT only when at least two same-ID candidates are directly observed and ordering/precedence can affect the selected candidate.

## Hard fences
- No production Gateway restart/reload.
- No production configuration mutation.
- No environment mutation.
- No Scheduled Task mutation.
- No production global extension installation/mutation.
- No production artifact replacement/deploy/rename/copy-over.
- No OpenClaw dependency patch.
- No CogentNexus source repair.
- No debugger/inspector attachment.
- No semantic/model/provider/Dashboard request.
- No TicketStore/admission/routing/auth changes.
- No production retry.
- No speculative workaround.
- No permanent instrumentation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-402.
- Do not create or start CNX-404 yourself.

Required counts:
- Semantic/model/provider/Dashboard requests: 0
- Production mutations: 0

## Required report
Create docs/operations/coordination/reports/CNX-20260918-403-production-plugin-discovery-root-duplicate-provenance-report.md
Include authoritative starting/final HEAD; exact OpenClaw/artifact/module hashes; discovery roots and origins; candidate/root/manifest/ID table; duplicate ordering/precedence; corrected production artifact identity; process/PID and startup chronology; isolated probe if used; direct evidence versus inference; effect on missing before_agent_run; counts and hard-fence compliance.

## Closeout
After report publication: set ACTIVE.md and STATUS.md to WAITING_FOR_CHATGPT_REVIEW; verify local HEAD equals remote HEAD; verify clean worktree; stop; do not create/start CNX-404; do not modify main, tags, or releases.