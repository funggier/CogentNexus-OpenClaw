# CNX-20260918-421 — OpenClaw Current Upgrade Qualification and Harness-Agnostic Ticket-First Admission

## Result

Final classification:

`BLOCKED_CURRENT_UPGRADE_QUALIFICATION`

The task completed read-only authority/source characterization, but the required TDD RED → minimal repair → GREEN sequence and isolated v2026.9.4 qualification were not completed. No live upgrade or semantic traffic occurred. The report therefore does not claim an admission repair, target compatibility, migration success, or upgrade readiness.

## Authority and reconciliation

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Starting remote HEAD: `5954b96125135f710a64a7970ecee5a50b7b8a43`
- Starting local HEAD: `5954b96125135f710a64a7970ecee5a50b7b8a43`
- Handoff-embedded expected HEAD: `5954b96125135f710a64a7970ecee5a50b7b8a43`
- Remote/local discrepancy: none
- Task: `CNX-20260918-421`
- Parent: `CNX-20260918-420`
- Parent decision: `ACCEPTED_PASS`
- Parent classification: `PASS_OPERATOR_FRESH_SESSION_OLLAMA_TICKET_FIRST_VERTICAL_SLICE`

The authority files initially read at the live remote tip stated `READY_FOR_HERMES`. During closeout they were changed in this publication worktree to `WAITING_FOR_CHATGPT_REVIEW`; this is a local pending publication change until the final push/read-back.

## Baseline and safety gate

Read-only baseline:

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Gateway: healthy, PID `13192`, loopback port `18789`
- Plugin projection: `cogentnexus-openclaw`, version `0.9.5`, enabled/loaded, origin `global`
- `plugins list --json` projection: `hookCount: 0`, `hookNames: []`
- Effective plugin config included `hooks.allowConversationAccess=true`, `ticketFirst=true`, `preInferenceAdmission=true`, and `providerMode=passthrough`
- SQLite integrity: `ok`
- Active model calls: `0`
- Pending outbox rows: `0`

The delivery/recovery hazard gate was **not safe for installer or runtime qualification**. Read-only SQLite showed one pending assistant-delivery row and three nonterminal direct-recovery rows, all old Discord lineage. No durable state was changed and no cleanup or recovery action was attempted. This blocks any claim of a clean isolated copied-state migration based on the live baseline.

The `hookCount: 0`/`hookNames: []` fields are an inventory projection and are not, by themselves, proof that the live host rejected or failed to compose hooks. That causal claim remains unresolved without direct live registry evidence.

## Upstream provenance

- Tag: `v2026.9.4`
- Annotated tag object: `8bec206f3c1f787e1e9c45cfd34d3de2a78c7b8e`
- Peeled commit: `3a9d69db306cd7f081e06254cb89c4bcc14a7107`
- Source was cloned read-only to a disposable temp directory.

## 2026.7.1-2 versus v2026.9.4 source comparison

| Contract | Installed 2026.7.1-2 | v2026.9.4 source | Finding |
|---|---|---|---|
| `before_dispatch` | Present in the compiled dispatch path | Present; guarded by runtime takeover/permission policy | Pre-model inbound hook; event has content/session identity but no stable `runId` in the inspected contract |
| `reply_dispatch` | Present in compiled dispatch path | Present; explicit `dispatchKind` eligibility in newer source | Runs before normal dispatch/model path in the inspected route and receives `runId`; event does not expose the original prompt directly |
| `before_agent_run` | Conversation gate used by CogentNexus | Still a fail-closed conversation gate | Not universal across harnesses; CNX-419 remains evidence of a bypass path |
| `chat.send` | Propagates a run identifier into dispatch options | Same contract, with clearer session/run handling | Run correlation is available at `reply_dispatch` |
| Harness selection | Host/OpenClaw-owned | Host/OpenClaw-owned with clearer harness policy/runtime-source tracking | CogentNexus must not route provider/model/harness |
| Hook registry | CLI projection showed zero hooks | Source has typed hook registration and dispatch-kind filtering | Projection is insufficient to classify live registration failure |

Exact source evidence included:

- Installed compiled dispatch: `dispatch-DnzGTpPs.js`, `before_dispatch` around lines 1728–1776 and `reply_dispatch` around lines 1778–1815.
- v2026.9.4 `src/auto-reply/reply/dispatch-from-config.choose-route.ts`, `before_dispatch` around lines 539–623.
- v2026.9.4 `src/auto-reply/reply/dispatch-from-config.reply-dispatch-hook.ts`, construction of `runId` and dispatch context around lines 19–69.
- v2026.9.4 `src/plugins/hook-types.ts`, `PluginHookBeforeDispatchEvent` around lines 513–546 and `PluginHookReplyDispatchEvent` around lines 548–597.
- v2026.9.4 `src/plugins/hooks.ts`, hook runners around lines 1255–1291 and `before_agent_run` around lines 1384–1414.

## Reachability matrix

| Path | Trusted boundary | Session/run identity | Earliest relevant seam | `before_agent_run` | Ticket expectation | Evidence status |
|---|---|---|---|---|---|---|
| Dashboard → Ollama embedded | Dashboard/WebChat owner context | Session key and `chat.send` runId | `before_dispatch`/`reply_dispatch` before normal model dispatch; existing CNX admission is deeper | Proven for CNX-420 fresh Ollama lineage; universal coverage not proven | One eligible external owner Ticket | Fresh Ollama PASS; universal seam unproven |
| Dashboard → Codex/OpenAI harness | Dashboard/WebChat owner context | `reply_dispatch` runId available in host contract | Same host dispatch seam; CNX-419 demonstrated bypass of current deeper boundary | Not universal | One eligible external owner Ticket | Gap remains; no repair evidence |
| Discord owner turn | Authenticated channel owner context | Channel session/run where supplied | `before_dispatch`/dispatch path | Must be characterized with channel trust | Ticket only for eligible owner turns | No new semantic probe authorized |
| Internal verified delivery | Internal marker plus exact owner/session/run binding | Existing Ticket/run | Specialized delivery binding | Deeper marker path | No ordinary new Ticket | Existing source/tests; no mutation |
| Post-compaction continuation | Existing committed Ticket/session authority | Existing lineage | Specialized continuation/recovery guard | Deeper recovery path | No duplicate Ticket | Existing source/tests; no new qualification |
| Direct recovery | Existing direct Ticket and recovery state | Existing Ticket/run | Recovery owner | Deeper recovery path | Recover existing Ticket, not re-admit | Existing source; live hazard present |
| Subagent/synthetic worker | Explicitly excluded namespace/control path | Excluded from owner intake | Excluded | Excluded as designed | No owner Ticket | Existing predicate/tests; no new qualification |

No seam is declared universal by this report.

## Admission seam decision

`reply_dispatch` remains the strongest **candidate** for a run-correlated pre-model adapter because the host passes the real `runId` and the hook runs before normal model dispatch. It is not proven sufficient by this task because its event contract does not expose the original prompt directly. `before_dispatch` exposes content and trusted inbound identity but does not expose the same stable run ID in the inspected contract. No fake run ID was created.

The likely repair shape is a shared admission kernel called by an early adapter and retained by `before_agent_run` for defense-in-depth/idempotency. This is a design candidate only; no production repair was implemented.

Rejected alternatives:

- `before_agent_run` alone: rejected because CNX-419 demonstrates harness-specific bypass.
- `before_dispatch` alone: rejected as unproven for run correlation; its inspected contract lacks the stable `chat.send` run ID.
- Provider/model routing in CogentNexus: rejected because OpenClaw owns provider, model, fallback, session override, and harness selection.
- Synthetic/fabricated run IDs: rejected by the task fence and identity requirements.

## Trust-boundary and ownership findings

Existing source evidence:

- `durableAdmissionEligible` excludes missing session keys and `:subagent:` sessions, but defaults missing `senderIsOwner` to trusted for some existing paths.
- `ticketIntakeEligible` excludes delivery/control/continuation classes.
- `TicketStore.accept()` derives a unique request key from owner session plus run ID and is idempotent.
- `TicketStore.route()` separately controls route-event cardinality.
- Internal delivery must bind the exact owner session and run; it must not enter ordinary owner intake.

An early adapter must require explicit trusted WebChat/channel identity and authenticated owner scope, reject contradictory/missing identity, preserve control-path exclusions, fail closed on storage errors, and pass provider/model/harness fields through unchanged.

## TDD evidence

No CNX-421 production repair was authorized as proven because the seam contract was not sufficiently established. Existing focused baseline tests were run after local `npm ci`:

```text
src/index.test.ts                         42 passed
src/v091-dashboard-verified-delivery.test.ts 11 passed
src/v154-dashboard-public-hook-fallback.test.ts 2 passed
Total: 55 passed
```

A new CNX-421 RED suite was **not committed**, and therefore no valid RED → minimal repair → GREEN evidence exists. This is a material completion gap, not a PASS.

## Isolated v2026.9.4 qualification

Not completed. No verified isolated Gateway startup/shutdown, copied-state session/transcript migration, plugin load against the target SDK, or rollback test was retained as task evidence. The upstream source clone and source inspection do not substitute for those qualification gates.

Migration/rollback status:

- Live session/transcript migration: not performed.
- Copied-state migration: not performed and not proven.
- Rollback/downgrade: not exercised.
- Live scheduled task/service takeover: none.
- Live OpenClaw upgrade: none.

## Timeout-authority characterization

CNX-420 recorded `timeoutMs=900000` and a completed call of `2,682,699 ms` (~44m42.699s), with no retry/recovery. Read-only source/config characterization found:

- `v091-direct-model-call-lease.ts` defines the default emitted deadline as `15 * 60_000`.
- The same lease path caps the recorded timeout but does not itself abort the provider call.
- The live OpenClaw config contained `agents.defaults.timeoutSeconds=2700` (45 minutes).
- The recovery/stall logic treats the model-call deadline as a claim/recovery observation, not direct provider cancellation.

Classification: `OBSERVATIONAL_DEADLINE_NOT_AUTHORITATIVE; SUPERSEDED_BY_RUNNER_TIMEOUT`

This explains the observed completion path as consistent with a longer OpenClaw runner timeout, but the exact live process authority chain was not proven by a fresh model request (forbidden). No timeout configuration was changed.

## Changed files and commits

Source/tests: none.

Publication changes intended for this task:

- `docs/operations/coordination/reports/CNX-20260918-421-openclaw-current-upgrade-qualification-and-harness-agnostic-ticket-first-admission-report.md`
- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

Untracked `CNX-421-analysis.md` and `CNX-421-summary.txt` were disposable subagent artifacts, not authoritative deliverables, and are excluded from publication.

## Closeout decision

`BLOCKED_CURRENT_UPGRADE_QUALIFICATION`

The blocker is incomplete required evidence: no CNX-421 RED characterization suite, no minimal repair/GREEN result, and no retained isolated v2026.9.4 qualification. The live delivery/recovery hazard also prevents treating the current state as a clean migration baseline. ChatGPT review is required before any successor live-upgrade task or further disruptive action.

Hard-fence counts:

- Semantic sends: `0`
- Direct Ollama/OpenAI/provider probes: `0`
- Browser mutation: `0`
- Live provider/model mutation: `0`
- Live OpenClaw upgrade: `0`
- Live session/transcript migration: `0`
- Live plugin install-over/uninstall: `0`
- Live Gateway restart for upgrade: `0`
- Manual Ticket/outbox/recovery/SQLite mutation: `0`
- Release/tag/main: `0`
- Force push/history rewrite: `0`
