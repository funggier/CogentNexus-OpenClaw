# CNX-20260918-422 — reply_dispatch Ticket-first Repair and OpenClaw 2026.9.4 Isolated Qualification

## Result

Final classification:

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE`

CNX-422 repaired the harness gap by moving eligible external-owner Ticket admission to a shared kernel reachable from `reply_dispatch` before model/harness execution, while retaining `before_agent_run` as an idempotent defense-in-depth adapter. The repaired candidate builds and passes focused tests against both the installed baseline and OpenClaw v2026.9.4, starts and shuts down cleanly in isolated v2026.9.4 fresh state, migrates a fully isolated live-state copy successfully, and has a proven rollback procedure.

This classification does **not** authorize or perform the live upgrade. A future controlled-upgrade task must take a complete pre-upgrade state/config/session/workspace snapshot. Binary-only downgrade from v2026.9.4 to 2026.7.1-2 is proven insufficient after state migration.

## Authority and exact HEADs

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-422`
- Parent: `CNX-20260918-421`
- Starting remote/local HEAD: `eaff8c79ccf71affb166afa4ae24aed7a2179897`
- Qualified implementation HEAD: `5ae72d9ecc3f91da496b72d7b909f50bde07149a`
- Final report/coordination publication HEAD: verified after publication and reported in the executor closeout because embedding the commit that contains this report would be self-referential.
- GitHub remote was fetched and matched local baseline immediately before implementation publication work began.
- No force push, history rewrite, tag, release, or `main` mutation occurred.

The operator directed ChatGPT to continue CNX-422 through LConnect. GitHub remote state plus `ACTIVE.md`, `STATUS.md`, the CNX-422 task, and predecessor reports remained the authority.

## Upstream OpenClaw provenance

Target source was the isolated clone at the exact annotated tag:

- Tag: `v2026.9.4`
- Annotated tag object: `8bec206f3c1f787e1e9c45cfd34d3de2a78c7b8e`
- Peeled commit: `3a9d69db306cd7f081e06254cb89c4bcc14a7107`
- Qualification package confirmed `node_modules/openclaw/package.json = 2026.9.4`

Installed live baseline remained:

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Gateway: `127.0.0.1:18789`
- Live Gateway was not restarted for upgrade and was healthy at the end of qualification.

## Corrected reply_dispatch contract

Direct inspection of v2026.9.4 established that `reply_dispatch` is a valid harness-agnostic pre-model adapter for this repair:

- the event carries the real host `runId`;
- `event.ctx` is `FinalizedMsgContext`;
- canonical inbound text is available through the finalized message context;
- session identity is available through the event/context;
- v2026.9.4 exposes `InboundAccessAuthorized`;
- Gateway client scopes remain available as a compatibility trust fallback when explicit ingress authorization is absent;
- `reply_dispatch` can run for both `agent` and `acp` dispatch kinds before normal model/harness execution.

The repaired flow is:

`reply_dispatch -> shared Ticket admission kernel -> TicketStore.accept/route -> OpenClaw-selected harness/provider/model`

`before_agent_run` calls the same kernel for defense-in-depth/idempotency. Admission policy is not duplicated across the two adapters.

## Production repair

### New shared admission kernel

Added:

`plugins/cogentnexus-openclaw/src/ticket-admission-kernel.ts`

The kernel owns:

- exact session/run/prompt validation;
- explicit trust validation;
- subagent/control/delivery/continuation exclusion;
- direct vs durable classification;
- one logical idempotent `TicketStore.accept()`;
- at-most-once route transition through the Ticket store;
- persistence-failure fail-closed behavior;
- no provider/model/harness selection or mutation.

The `reply_dispatch` adapter also:

- prefers canonical `agentText`, then `BodyForAgent`, `rawText`, and `Body`;
- rejects contradictory event/context session identity;
- accepts `InboundAccessAuthorized=true` as explicit v2026.9.4 trust proof;
- treats `InboundAccessAuthorized=false` as authoritative denial and does **not** allow privileged Gateway scopes to override it;
- uses `operator.write` / `operator.admin` only as compatibility fallback when the explicit ingress field is absent;
- rejects a Ticket-required owner turn without an exact real `runId`;
- never fabricates a run ID.

### Runtime wiring

Modified:

- `plugins/cogentnexus-openclaw/src/index.ts`
- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`

The new admission registration uses:

- hook: `reply_dispatch`
- registration ID: `cogentnexus-openclaw-ticket-first-admission`
- priority: `2500`
- eligible dispatch kinds: `agent`, `acp`

Historical WebChat/Discord legacy delivery fences remain in place; only this named Ticket admission registration is permitted through those fences.

Direct requests remain unclaimed so OpenClaw retains model/harness execution authority. Durable requests are committed and claimed before conversational inference.

### v2026.9.4 public-SDK compatibility

Modified:

`plugins/cogentnexus-openclaw/src/v095-runtime-hook-attestation.ts`

v2026.9.4 no longer exports `getGlobalPluginRegistry` through the public `openclaw/plugin-sdk/plugin-runtime` surface. The repair does not import private/internal OpenClaw modules. Runtime attestation now uses public `getGlobalHookRunner()` only and conservatively reports plugin-specific ownership as unavailable/`AMBIGUOUS` when the public SDK cannot prove it.

## TDD RED evidence

### Primary pre-repair RED

After correcting the local test harness so it supplied the required session ID, the new CNX-422 suite against the pre-repair implementation produced:

- `15` tests total
- `7` passed
- `8` failed

The failures demonstrated that `reply_dispatch` did not create the Ticket before either embedded-agent or ACP/Codex-style execution and did not provide the required fail-closed identity/trust behavior.

### Trust contradiction RED

After the main repair, a final trust review added an explicit contradiction case:

`InboundAccessAuthorized=false + operator.write/operator.admin`

Before hardening, the test failed because one Ticket was created when zero was required:

- `15` passed
- `1` failed

The minimal repair made explicit `false` authoritative over scope fallback.

## GREEN evidence

Final CNX-422 admission suite:

- `16/16` PASS

It proves:

1. Dashboard embedded/agent admission occurs before `before_agent_run`.
2. ACP/Codex-style dispatch is admitted before harness execution.
3. Durable dispatch is committed and claimed before conversational inference.
4. `reply_dispatch` followed by `before_agent_run` yields one logical Ticket.
5. Route event cardinality remains one.
6. Direct requests remain unclaimed for normal OpenClaw model/harness execution.
7. Canonical inbound text is persisted without provider/model/harness rewrite.
8. Internal delivery markers do not create owner Tickets.
9. Post-compaction continuation does not duplicate a Ticket.
10. Direct recovery continuation does not duplicate a Ticket.
11. Subagent/synthetic sessions are excluded.
12. `InboundAccessAuthorized=true` is accepted as explicit trust proof.
13. Missing/untrusted ingress fails closed.
14. Explicit authorization denial cannot be overridden by privileged scopes.
15. Contradictory session identity fails closed.
16. Missing exact real `runId` fails closed.

Final focused baseline regression set:

- `9` test files
- `91/91` tests PASS

This included admission, core index behavior, Dashboard delivery, model-call lease, direct recovery, session ownership, Discord direct delivery/receipt lifecycle, and Ticket contention.

Package validation:

- TypeScript build: PASS
- canonicalized dist files: `50`
- mixed-plugin artifact verification: PASS (`46` config properties, `5` tools)
- Ticket DB bootstrap: PASS (`9` required tables + v095 registration fence)
- package contents verification: PASS
- packed file count: `260`

## Broad regression characterization

Full plugin suite after the final trust repair:

- Test files: `80 passed / 1 failed` (`81` total)
- Tests: `359 passed / 1 failed` (`360` total)

The single failure is the pre-existing, intentionally RED predecessor:

`src/cnx383-hook-policy-projection.test.ts`

It is unchanged from authoritative remote baseline. CNX-383/CNX-384/CNX-385 explicitly record that this test demonstrates the old host normalized-config projection boundary and is expected to remain RED until that separate host-owned issue is addressed. CNX-422 did not modify the test or the executable `hooks.allowConversationAccess` declaration. No new broad-suite failure was introduced by CNX-422.

The repaired v2026.9.4 `reply_dispatch` path was independently observed registering and executing in isolated runtime, so this known predecessor RED is not treated as a CNX-422 regression or an unresolved Ticket-first trust blocker.

## Provider/model/harness non-mutation proof

The CNX-422 tests attach provider/model/harness fields to the event and verify they remain unchanged after admission. Production repair code does not choose or rewrite those fields.

Isolated runtime logs may show the model chosen by OpenClaw for that isolated state, but CogentNexus does not set or switch it and no semantic model request was sent.

Semantic provider traffic during CNX-422: `0`.

## v2026.9.4 target build

The final candidate was copied into the isolated v2026.9.4 qualification package and rebuilt against that target.

Result:

- target OpenClaw: `2026.9.4`
- TypeScript build: PASS
- target focused suite: `7` files, `89/89` tests PASS

The target suite included CNX-422 admission, core index behavior, Dashboard delivery, model-call lease, direct recovery, session ownership, and runtime-hook attestation.

## Fresh-state isolated runtime

Fresh non-live state used the installer-equivalent Ticket DB bootstrap before plugin load.

Observed on isolated port `19794`:

- Gateway reached `ready`;
- candidate loaded from the isolated `dist/v091-release-entry.js`;
- `reply_dispatch` registration was observed;
- plugin load completed without CNX plugin error;
- startup recovery found no work and performed no semantic action;
- live port `18789` remained separate and untouched.

A Windows-native `CTRL_C_EVENT` was then delivered to the isolated Gateway console. OpenClaw logged:

- `signal SIGINT received`
- `received SIGINT; shutting down`
- `active-work drain settled; beginning server close`
- `[shutdown] completed cleanly in 17ms`

The process exited with code `0`, port `19794` disappeared, and live `18789` remained listening.

A temporary qualification-only issue was also characterized: a PowerShell-created BOM in a disposable `package.json` caused the loader to ignore package metadata and fall back to another candidate file. Removing the BOM restored normal package entry discovery. This was a disposable harness artifact, not a repository/package defect.

## Fully isolated copied-state qualification

Because the first copied-state attempt accidentally retained a live workspace path, it is **not** used as acceptance evidence. That incident is documented separately below.

A second clean qualification was created at:

`%LOCALAPPDATA%\Temp\cnx422-copied-live-state-v2`

Snapshot method:

- explicit file copies for legacy sessions and required workspace files;
- Node `node:sqlite backup()` for the live locked shared state DB, agent DB, and CogentNexus DB;
- `PRAGMA integrity_check = ok` for all three copied databases.

Exact copied workspace/session file hashes matched the live sources before migration. The sanitized v2 configuration contained zero live workspace references.

### Pre-migration copied state

- shared OpenClaw DB: user_version `1`
- agent DB: user_version `1`
- CNX DB: user_version `0`
- legacy sessions: `19`

CNX residue used strictly as copied test input:

- Tickets: accepted `3`, cancelled `4`, completed `17`
- Ticket events: `874`
- outbox: `0`
- direct recovery: awaiting_delivery `1`, cancelled `2`, pending `2`
- assistant delivery: delivered `14`, pending `1`
- direct model calls: ended `21`
- inference attempts: ended `4`

### v2026.9.4 migration

`openclaw doctor --fix --non-interactive --yes --no-workspace-suggestions` on the isolated copy succeeded.

Observed migration:

- shared state DB: `v1 -> v17`
- agent DB: `v1 -> v19`
- legacy session entries: `19`
- SQLite session entries after migration: `19`
- transcript events imported: `166`
- legacy transcript artifacts archived: `50`
- unreferenced JSONL artifacts archived: `117`
- legacy workspace setup state migrated into SQLite
- shared auth/plugin/workspace state migrated
- isolated `HEARTBEAT.md` migrated into cron scratch
- isolated `TOOLS.md` archived/removed according to v2026.9.4 migration semantics

All of those workspace mutations occurred under the isolated v2 temp workspace. Hashes of the four corresponding live workspace files were captured before and after the migration and matched exactly `4/4`.

CNX DB residue counts remained unchanged across migration and isolated startup.

### Copied-state v2026.9.4 startup

On isolated port `19797`:

- Gateway reached `ready`
- health: `ok=true`
- CNX plugin loaded with no plugin error
- sessions path was the migrated agent SQLite DB
- session count remained `19`
- `reply_dispatch` registration was observed
- crash-start recovery reported no mutation: `directReopened=0`, `outboxReset=0`, and no recovery/delivery reset
- runtime attestation: `runnerReady=true`, `globalHookCount=7`, plugin-specific count unavailable via public SDK, classification `AMBIGUOUS`
- CNX residue counts remained unchanged
- semantic provider sends: `0`

## Migration and rollback decision

OpenClaw v2026.9.4 performs material one-way-on-disk migrations relative to 2026.7.1-2.

### Binary-only downgrade

Proven **unsafe**.

After the copied state migrated to shared schema `17`, attempting to launch OpenClaw `2026.7.1-2` failed with exit code `1`:

`OpenClaw state database ... uses newer schema version 17; this OpenClaw build supports 1.`

Therefore package/binary downgrade alone is not a rollback procedure.

### Full snapshot restore

Proven **successful**.

The complete pre-migration isolated snapshot was restored into a new rollback directory. With the restored state:

- shared DB returned to user_version `1`
- agent DB returned to user_version `1`
- OpenClaw `2026.7.1-2` config validation passed
- isolated 2026.7.1-2 Gateway reached `ready`
- health: `ok=true`
- session path returned to legacy `sessions.json`
- session count remained `19`

Required rollback procedure for a future controlled live upgrade is therefore:

1. stop/quiesce live OpenClaw under the future upgrade task's authority;
2. capture a consistent pre-upgrade snapshot before any v2026.9.4 migration;
3. preserve the current OpenClaw binary/package identity;
4. preserve config and relevant workspace migration files;
5. preserve shared state SQLite, agent state/DB, legacy sessions/transcripts, and CNX runtime DB;
6. perform the upgrade/migration;
7. if rollback is required, stop the upgraded runtime;
8. restore the pre-upgrade binary **and the complete pre-upgrade state/config/session/workspace snapshot together**;
9. validate/restart the restored 2026.7.1-2 runtime and verify session/CNX integrity.

CogentNexus installer/reset/uninstall assumptions must not treat plugin uninstall or binary downgrade as sufficient rollback for an OpenClaw host-version migration.

## Qualification incident and recovery

During the first copied-state experiment, the temp OpenClaw state directory was isolated but `agents.defaults.workspace` still referenced the live workspace. Running v2026.9.4 doctor therefore migrated four live workspace artifacts unintentionally:

- `AGENTS.md`
- `HEARTBEAT.md`
- `TOOLS.md`
- `openclaw-workspace-state.json`

The issue was detected before repository publication.

Recovery evidence:

- `HEARTBEAT.md` restored with exact archived SHA-256:
  `ECCE558615751A35AA173731E892FF3993F44BB4F5A1219C0A02994790C85528`
- `TOOLS.md` restored with exact archived SHA-256:
  `4BD351AACB7FA76ABB0BE06AB3205D6D77BCA2CDD9CA57B8FC23257878F3BE77`
- original workspace-state restored with exact SHA-256:
  `FCF1919D658397B672F0A2B6580B5C9A3BE87D93857510355601273C90E7CC27`
- `AGENTS.md` was deterministically reversed using the exact v2026.9.4 migration transformations and the installed 2026.7.1-2 template; final hash:
  `0305C0F4667E9279EA72B8B6E8E28CD84B8F58945536E1B189DAF077A1FA0921`
- the migrated workspace-state side artifact was removed after the original canonical state was restored
- live Gateway remained 2026.7.1-2 and returned healthy
- incident evidence was retained under a disposable temp evidence directory

Acceptance evidence does **not** rely on that first attempt. The fully isolated v2 copied-state qualification was rebuilt from live sources after recovery, used zero live workspace references, and proved all four live workspace hashes unchanged before/after v2026.9.4 migration.

## Known predecessor RED

`cnx383-hook-policy-projection.test.ts` remains intentionally RED and unchanged from the authoritative branch baseline. It records a separate historic host normalized-config projection boundary. v2026.9.4 runtime evidence in this task directly observed the CNX candidate's `reply_dispatch` registration, so CNX-383 does not invalidate the repaired harness-agnostic admission path.

No attempt was made to weaken, delete, or falsely GREEN that predecessor test.

## Remaining risks and controlled-upgrade preconditions

1. **Rollback is stateful.** A future live upgrade must create and verify a complete pre-upgrade snapshot; binary-only downgrade is not acceptable.
2. **Public attestation is conservative on v2026.9.4.** `getGlobalPluginRegistry` is no longer public. Global hook-runner presence is observable, but plugin-specific ownership remains `AMBIGUOUS` through the supported SDK. No private import is used.
3. **Known CNX-383 RED remains historical evidence.** It is not a new regression and is not the admission seam used by this task.
4. **Live semantic acceptance remains for the successor controlled-upgrade task.** CNX-422 intentionally sent zero semantic provider requests and did not install/activate v2026.9.4 live.
5. **Upgrade tooling must respect host migrations.** Reset/uninstall/install-over logic needs explicit snapshot/restore handling for OpenClaw host-version migration boundaries.

## Changed product/test files

Qualified implementation commit:

`5ae72d9ecc3f91da496b72d7b909f50bde07149a`

Files:

- `plugins/cogentnexus-openclaw/src/index.ts`
- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
- `plugins/cogentnexus-openclaw/src/v095-runtime-hook-attestation.ts`
- `plugins/cogentnexus-openclaw/src/ticket-admission-kernel.ts`
- `plugins/cogentnexus-openclaw/src/cnx422-reply-dispatch-admission.test.ts`

Implementation diff:

- `610 insertions`
- `39 deletions`

The report and coordination transition are published separately on top of the qualified implementation commit.

## Hard-fence accounting

- Semantic sends: `0`
- External provider probes: `0`
- Browser mutation: `0`
- Live provider/model mutation: `0`
- Live OpenClaw upgrade: `0`
- Live session/transcript migration: `0`
- Live plugin install-over/uninstall: `0`
- Live Gateway restart for upgrade: `0`
- Manual live Ticket/outbox/recovery/SQLite mutation: `0`
- Release/tag/main: `0`
- Force push/history rewrite: `0`

The copied-state workspace-path incident is disclosed above separately; its file effects were recovered and then excluded from acceptance evidence by a clean v2 qualification with live hash invariance.

## Final decision

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE`

The admission repair and isolated host-version qualification are complete. The successor must remain a separately reviewed, controlled live-upgrade task and must make a full pre-upgrade rollback snapshot a hard prerequisite. CNX-422 itself does not perform that upgrade.
