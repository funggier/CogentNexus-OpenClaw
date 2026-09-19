# CNX-20260919-427 — Full Session Handoff After OpenClaw 2026.9.5 Upgrade and Storage Relocation Start

Status: `HANDOFF_READY`

Date: 2026-09-19

Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

Repository base HEAD before this handoff publication:

`019fc91d9878cc9fab39bf3dfaae30023ddc64f4`

Active task:

`CNX-20260919-427 — External Ingress Run Identity and Tailscale Owner Profile Repair`

Primary task document:

`docs/operations/coordination/tasks/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair.md`

Primary task report:

`docs/operations/coordination/reports/CNX-20260919-427-external-ingress-run-identity-and-tailscale-owner-profile-repair-report.md`

This file is the authoritative session handoff for the next ChatGPT session. The next session must inspect live state before making further mutations because runtime/package/storage state changed materially during this session.

---

## 1. Operator intent and working style

The operator wants continuous autonomous repository/runtime repair without routine confirmation.

Expected execution style:

- inspect GitHub/live state before mutation;
- use TDD where code is changed;
- preserve Ticket-first semantics;
- OpenClaw owns provider/model routing;
- do not synthesize fake run IDs;
- do not weaken authentication or profile verification;
- report important checkpoints;
- final classification must use PASS/FAIL/BLOCKED with exact evidence;
- preserve rollback before risky live changes.

Primary local model preference remains:

`ollama/qwen3.8:27b`

The operator accepts that this model is slow.

---

## 2. Current live OpenClaw state

OpenClaw live host has been upgraded from 2026.9.4 to:

`OpenClaw 2026.9.5 (ec9c1a1)`

Current live Gateway state at handoff:

- health: `ok=true`;
- event loop: `degraded=false`;
- plugin errors: 0;
- Discord lifecycle: `ready`;
- Discord connected: true;
- active Discord runs: 0;
- Gateway listener: `127.0.0.1:18789`;
- current Gateway PID observed after successful 9.5 recovery: `29604`;
- scheduled task `OpenClaw Gateway`: Running;
- scheduled task `CogentNexus-OpenClaw-Supervisor`: Enabled / Ready / Last Result 0;
- sessions retained: 26.

CNX runtime attestation after 9.5 startup:

- `runnerReady=true`;
- `globalHookCount=7`;
- classification remains conservative `AMBIGUOUS` because public SDK cannot identify which specific global handlers belong to CNX.

CNX plugin remains:

`0.9.5`

Live `dist/index.js` SHA256:

`6D96AD5FC4F419105E7E6A82EC941926886A05937C143E599C47FE9143A8FBE3`

This hash is the same qualified CNX artifact that was already deployed before the 9.5 upgrade.

---

## 3. Tailscale state

Tailscale backend and OpenClaw Serve are working.

OpenClaw config remains:

- `gateway.bind=loopback`;
- `gateway.tailscale.mode=serve`.

Remote URL:

`https://cdq-p.tail145b6c.ts.net/`

Post-upgrade remote HTTPS test:

- HTTP 200;
- content type `text/html; charset=utf-8`.

Current 9.5 Tailscale Serve proxy observed:

`https://cdq-p.tail145b6c.ts.net:443/ -> http://127.0.0.1:12651`

Do not assume an older proxy port such as 1721; query `tailscale serve status --json` live.

The previous remote owner-profile failure was caused by transient GitHub identity verification HTTP 403, not Tailscale transport. That recovered without disabling authentication.

After an OpenClaw upgrade, old browser tabs can still run an older Control UI build. OpenClaw 9.5 correctly rejects stale 9.4 UI WebSockets with `control-ui-build-mismatch`. Reload the browser if seen.

---

## 4. CNX-427 Track A — Discord Ticket-first history

### 4.1 Original defect

Discord ingress was accepted by OpenClaw, but early CNX `reply_dispatch` saw no authoritative run ID and failed closed:

`CogentNexus-OpenClaw reply_dispatch admission failed closed: missing-run-id`

This suppressed the turn before model execution.

### 4.2 First repair

CNX adapter was changed so that at the **early** trusted `reply_dispatch` boundary:

- `missing-run-id` means defer;
- no Ticket is created early;
- no synthetic run ID is invented;
- all other blocked admission reasons remain fail-closed;
- execution-boundary missing run ID remains fail-closed.

Source commit:

`4ed98c8c5cbd03b3cd26acff8082fc1f14c0537b`

Focused regression after this repair:

`39/39 PASS`

Plugin validation passed.

### 4.3 Live acceptance exposed a second-stage bypass

First visible acceptance message:

`@Ce ตอบคำว่า CNX427_OK เท่านั้น`

Discord visibly replied:

`CNX427_OK`

Trace:

`343c6efbf788333b585d1160af9ed4e6`

Authoritative OpenClaw run:

`a0660423-e586-4e89-a5c9-fca25d842e1d`

But CNX DB had **no Ticket** for this run.

Classification:

`VISIBLE_DELIVERY_GREEN__TICKET_FIRST_BYPASS_REMAINS`

A second operator Discord attempt reproduced the same deterministic defect on OpenClaw 2026.9.4:

Trace:

`73bfcb525d0fbecc95372ddf49151c44`

Authoritative run:

`77b8ed7a-f40c-4ac1-86f4-0884656b4e8e`

Direct CNX DB verification for this run:

- Tickets: 0;
- Ticket events: 0;
- CNX delivery rows: 0.

Therefore OpenClaw 9.4 allowed visible Discord execution after the early deferral but lost Ticket-first continuity before the selected harness execution.

---

## 5. Why OpenClaw 2026.9.5 was selected

Upstream OpenClaw 2026.9.5 contains a directly relevant change:

Commit:

`983782594807a23c006b49bd16172b1ba6980924`

Title:

`fix(agents): preserve admitted runtime generation for channel turns (#127217)`

The 9.4 architecture maintained a generic inbound plugin registry and later selected a runtime/harness generation. Discord/Codex turns could see CNX at early ingress but lose CNX conversation/admission hooks after the runtime generation switch.

The 9.5 upstream change preserves the admitted runtime generation across the channel turn and is architecturally preferable to adding a CNX-specific synthetic second-stage workaround.

Do **not** revive the abandoned experimental `before_agent_reply` workaround unless new evidence disproves the 9.5 continuity fix.

The uncommitted RED experiment for that workaround was restored; repository source content is back to HEAD.

---

## 6. OpenClaw 2026.9.5 qualification evidence

A separate 9.5 sandbox was built before live upgrade.

Focused CNX compatibility qualification:

- 10 test files passed;
- `108/108 tests PASS`;
- included CNX-427, CNX-424, CNX-423, CNX-422, core index, Dashboard delivery, direct recovery, session ownership, runtime hook attestation.

`plugin:validate` on the 9.5 sandbox:

- TypeScript build PASS;
- mixed-plugin schema verification PASS;
- Ticket DB bootstrap PASS;
- package contents PASS.

An initial sandbox startup failed with:

`Plugin entry is outside its captured source package`

This was proven to be a **sandbox topology artifact**, not a production regression. The qualification sandbox had `openclaw@9.5` installed as a devDependency under the CNX plugin tree, which caused the 9.5 package-capture fence to see OpenClaw SDK imports as nested plugin source.

Canonical topology was then tested:

- OpenClaw 9.5 host in a separate root;
- CNX installed from packaged archive into the isolated OpenClaw state;
- peer dependency linked to the external 9.5 host.

Canonical isolated result:

- OpenClaw `2026.9.5 (ec9c1a1)`;
- Gateway health `ok=true`;
- plugin errors 0;
- CNX + Codex loaded;
- CNX runtime attestation `runnerReady=true`.

Therefore the prior source-package error is not a live blocker.

---

## 7. Live 9.5 upgrade procedure and rollback snapshot

Before upgrading live 9.4, Gateway was stopped and CNX Supervisor disabled.

Authoritative rollback snapshot:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\backups\CNX-20260919-427-preupgrade95-20260919T172713`

Important contents:

- `openclaw-home-fidelity`
- `global-openclaw-2026.9.4`
- `candidate`
- `evidence`
- `ROLLBACK-README.txt`

Pre-upgrade snapshot manifest:

`...\evidence\preupgrade-manifest.json`

Snapshot fidelity evidence:

- source reparse count: 10;
- backup reparse count: 10;
- dry mirror RC: 0;
- critical config/wrapper/DB/CNX hashes matched.

Pre-upgrade snapshot SQLite:

- shared DB user_version 17, quick_check ok;
- agent DB user_version 19, quick_check ok;
- CNX DB user_version 0, quick_check ok.

There is also an accidental sibling directory:

`CNX-20260919-427-preupgrade95-20260919T172713+`

It contains only an `evidence` directory and came from an early path-construction mistake. It is **not** the authoritative rollback snapshot.

Pinned OpenClaw candidate archive:

`openclaw-2026.9.5.tgz`

Candidate SHA256:

`1FB6EF4FAE447AF14F1E3B1028334F39146D181A66A4CCE2848D4F741C636340`

The archive package.json verified version:

`2026.9.5`

---

## 8. Live migration details

Global OpenClaw package upgrade completed:

`2026.9.4 -> 2026.9.5`

Initial `doctor --fix` migrated the agent DB:

`v19 -> v21`

Then OpenClaw correctly refused to finish because Codex state migration was pending and instructed:

`openclaw update repair`

followed by:

`openclaw doctor --fix`

That canonical sequence was used.

`update repair` converged official plugins:

- Discord 9.4 -> 9.5;
- llama-cpp 9.4 -> 9.5;
- opencode 9.4 -> 9.5;
- voice-call 9.4 -> 9.5;
- Codex already 9.5;
- CNX archive plugin preserved;
- integrity drifts -> 0.

Post-update `doctor --fix` completed and also cleared stale Codex routing state in four sessions while preserving explicit model overrides in fifteen sessions.

Post-migration SQLite checks:

- shared DB v17: quick_check ok;
- agent DB v21: quick_check ok;
- CNX DB v0: quick_check ok.

---

## 9. Critical OOM finding during first live 9.5 startup

The first live 9.5 Gateway startup reached `gateway ready` and then crashed with native V8 Zone OOM / DataCloneError.

This was **not** caused by OpenClaw heap usage itself.

Machine state at failure:

- physical RAM ~31.46 GB;
- physical free ~12 GB;
- total virtual/commit ~51.46 GB;
- free virtual/commit only ~2.06 GB;
- pagefile ~20 GB and usage `20479 / 20480 MB`.

Root cause:

Ollama still kept `qwen3.8:27b` resident for ~21 hours.

`llama-server.exe` private memory:

~22.94 GB

`ollama ps` showed:

- model `qwen3.8:27b`;
- size 18 GB;
- context 32768;
- keep-alive ~21 hours.

The model was unloaded safely with:

`ollama stop qwen3.8:27b`

This did **not** delete the model and did **not** change the OpenClaw default model.

After unload:

- Ollama loaded model list became empty;
- free virtual/commit recovered to ~25.11 GB;
- pagefile usage fell to ~2013 MB.

Gateway was restarted and OpenClaw 9.5 then became healthy.

At final settled check:

- free physical ~13.03 GB;
- free virtual/commit ~23.34 GB;
- event loop `degraded=false`.

Important implication:

Long Ollama keep-alive for qwen3.8:27b can starve system commit even if Windows shows significant free physical RAM. Future work should consider reducing/controlling keep-alive or adding a memory/commit-aware unload policy before major OpenClaw lifecycle operations.

---

## 10. Current provider/model configuration

Default remains:

`ollama/qwen3.8:27b`

Known explicit Ollama models in OpenClaw config remain:

- `qwen3:1.7b`
- `qwen3.6:27b`
- `qwen3.8:27b`

Ollama base URL remains:

`http://127.0.0.1:11434`

CNX remains:

- providerMode `passthrough`;
- ticketFirst `true`.

OpenClaw, not CNX, owns provider/model selection.

---

## 11. CNX-426 context-budget work remains relevant

CNX-426 completed before this task and repaired model-switch context budgeting.

It established:

- current-turn `ctx.contextTokenBudget` is authoritative when valid;
- stale `sessions.describe.contextTokens` must not override the current-turn budget;
- model switch large->small and small->large both use the current effective budget;
- context-maintenance hold keeps the stored authoritative turn window;
- terminal Tickets should cancel pending context-maintenance residue.

CNX-426 final publication commit:

`46b3ac619727123aee675ed23eb50dc46240b209`

Do not regress these semantics while solving CNX-427.

A separate observation remains important:

OpenClaw model metadata may advertise qwen3.8 context 262144 while `ollama ps` previously showed the live llama-server running `-c 32768`. This mismatch was not fully resolved in CNX-427 and may deserve a later dedicated task.

---

## 12. Current repository state

Branch:

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

Git state was refreshed before writing this handoff.

The false-dirty `cnx427-external-ingress-runid.test.ts` entry had identical worktree/index hashes and was refreshed with no content change.

Temporary packaged `.tgz` under the repo was removed.

At handoff-writing start, worktree was clean.

Important recent commits:

- `019fc91d` — record live Discord Ticket-first bypass;
- `8e052526` — deploy ingress repair and verify Tailscale profile recovery;
- `4ed98c8c` — defer early external ingress without run id;
- `cc26e30f` — open CNX-427;
- `46b3ac61` — CNX-426 final report.

The handoff publication itself will advance remote HEAD beyond `019fc91d...`.

---

## 13. Final CNX-427 acceptance is still pending

Do **not** classify CNX-427 PASS yet.

The final required proof is one new real Discord turn **after live OpenClaw 2026.9.5 is active**.

Required acceptance evidence for the same turn:

1. Discord inbound is accepted;
2. early `reply_dispatch` may defer if runId is not assigned yet;
3. the admitted runtime generation is preserved into the selected harness;
4. authoritative host runId is observed;
5. exactly one CNX Ticket exists for that runId;
6. Ticket creation occurs before inference authority is granted;
7. provider/model remain OpenClaw-owned;
8. exactly one assistant response is delivered to Discord;
9. Ticket reaches the correct terminal delivery/completion state;
10. no stale session lane remains;
11. no duplicate Ticket is created.

Suggested operator acceptance text:

`@Ce ตอบคำว่า CNX427_OK เท่านั้น`

Do not ask the operator to send this until current runtime/storage maintenance state is checked and stable.

---

## 14. New operator request — reclaim C: space by moving backups to T:

The operator reported C: is nearly full and asked that backups created by this work be moved to T:.

Current drive state near handoff:

- C: used ~451.69 GB, free ~13.45 GB;
- T: used ~290.32 GB, free ~641.19 GB.

The intended safe approach:

- move backup data to T:;
- preserve old C: backup paths via NTFS junctions so old rollback/report paths continue to work.

### 14.1 Current migration state — INCOMPLETE

C: backup source currently remains a normal directory:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\backups`

It is **not** a junction.

C: currently contains three backup directories:

1. `CNX-20260919-425-preupgrade-20260919T054451`
2. `CNX-20260919-427-preupgrade95-20260919T172713`
3. `CNX-20260919-427-preupgrade95-20260919T172713+`

A robocopy was started and exited with code 1, which is a robocopy success code meaning copy activity occurred.

However, the originally expected path `T:\CogentNexus-OpenClaw` was not present at final verification.

The data actually observed on T: is under:

`T:\CogentNexus\CogentNexus-OpenClaw`

Observed structure:

- `T:\CogentNexus\CogentNexus-OpenClaw\backups`
- `T:\CogentNexus\CogentNexus-OpenClaw\plugin-generation-rollover-backups`
- `T:\CogentNexus\CogentNexus-OpenClaw\logs`

At final verification, T: `backups` contained only:

`CNX-20260919-425-preupgrade-20260919T054451`

The two CNX-427 backup directories were **not yet observed on T:**.

Therefore:

**DO NOT DELETE, RENAME, OR JUNCTION-SWAP THE C: BACKUPS YET.**

The copy is not verified complete.

The T: `plugin-generation-rollover-backups` directory appeared empty at final check.

### 14.2 Required next-session storage procedure

First priority for the next session should be to finish the operator-requested storage relocation safely.

Recommended procedure:

1. Re-check C: and T: free space and exact filesystem state.
2. Decide the canonical destination. Since the tree already exists, prefer:
   `T:\CogentNexus\CogentNexus-OpenClaw`
   unless live evidence shows a better existing convention.
3. Copy **all** C: backup directories to:
   `T:\CogentNexus\CogentNexus-OpenClaw\backups`
   using robocopy with reparse preservation:
   `/MIR /COPY:DAT /DCOPY:DAT /R:1 /W:1 /SL /SJ`
   Do not use `/XJ` for the fidelity backup because junction/reparse topology matters.
4. Copy `plugin-generation-rollover-backups` to the corresponding T: location.
5. Verify:
   - all expected top-level backup directories exist on T:;
   - source/destination reparse counts where applicable;
   - important manifest/DB/config hashes;
   - robocopy dry mirror `/L` returns no pending differences;
   - authoritative CNX-427 pre-upgrade manifest exists on T:.
6. Only after verification:
   - rename or remove the old C: backup directory;
   - create an NTFS junction at the original C: path pointing to T:;
   - repeat for rollover backups.
7. Re-check old C: report/rollback paths through the junction.
8. Re-check C: free space and quantify recovered GB.
9. Do not move live `.openclaw`, Ollama models, or runtime DBs merely to recover space unless separately designed and authorized.
10. Consider `candidates` only after measuring it; the operator explicitly asked about backups first.

---

## 15. Immediate next-session order

Recommended order:

### Step A — Read authoritative state

Read:

1. this handoff;
2. `ACTIVE.md`;
3. `STATUS.md`;
4. CNX-427 task;
5. CNX-427 report.

Then fetch GitHub and compare local/remote HEAD. GitHub/live runtime are authoritative over this handoff if newer.

### Step B — Re-check live 9.5 health

Verify:

- `openclaw --version`;
- Gateway health;
- Discord connection;
- CNX runtime attestation;
- supervisor result;
- Tailscale Serve and remote HTTPS;
- system free virtual/commit;
- `ollama ps`.

If qwen3.8:27b is resident and commit is again dangerously low, do not perform restart/upgrade work until memory pressure is handled.

### Step C — Finish C: -> T: backup relocation

Follow section 14 exactly.

Do not delete C: source until T: fidelity is proven.

### Step D — Final Discord semantic acceptance on 9.5

After storage maintenance and runtime health are stable, ask the operator for one Discord message and verify the complete Ticket-first chain.

### Step E — Close CNX-427 only on exact evidence

If the same Discord turn has exactly one Ticket and one durable response path, publish final report/ACTIVE/STATUS and classify:

`EXTERNAL_INGRESS_AND_TAILSCALE_OWNER_PROFILE_REPAIR_GREEN`

If 9.5 still produces a visible response with no Ticket, do **not** claim PASS. Capture the run/trace and continue host generation-continuity analysis.

---

## 16. Safety / do-not-do list

- Do not force push.
- Do not mutate main/tag/release.
- Do not invent a run ID in CNX.
- Do not move provider/model routing into CNX.
- Do not weaken profile/auth verification.
- Do not roll back only the 9.4 binary against a 9.5-migrated state.
- If rollback is needed, restore the complete 9.4 package **and** the complete pre-upgrade state snapshot together.
- Do not delete C: backups until T: copy is independently verified.
- Do not assume robocopy exit code 1 means the entire desired migration is complete; it only means copy differences were processed successfully for that invocation.
- Do not treat an Ollama process absent from `ollama ps` as model deletion. `ollama stop` only unloads the model.
- Do not restart Gateway repeatedly while commit/pagefile is exhausted.

---

## 17. Key paths

Repository:

`C:\c\Users\CDQ-P\.hermes\workspace\cnx410-publish`

Live OpenClaw state:

`C:\Users\CDQ-P\.openclaw`

Live CNX DB:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

Live agent DB:

`C:\Users\CDQ-P\.openclaw\agents\main\agent\openclaw-agent.sqlite`

Live shared OpenClaw DB:

`C:\Users\CDQ-P\.openclaw\state\openclaw.sqlite`

Authoritative 9.4 rollback snapshot:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\backups\CNX-20260919-427-preupgrade95-20260919T172713`

Current T: relocation tree:

`T:\CogentNexus\CogentNexus-OpenClaw`

Discord session:

`agent:main:discord:channel:1391855033993138217`

Remote Control UI:

`https://cdq-p.tail145b6c.ts.net/chat/main/discord/channel/1391855033993138217`

---

## 18. Final state at handoff

Primary CNX-427:

`IN_PROGRESS — LIVE_9_5_GREEN_FINAL_DISCORD_TICKET_FIRST_ACCEPTANCE_PENDING`

Tailscale Track B:

`GREEN`

OpenClaw 9.5 live runtime:

`GREEN`

Storage relocation:

`IN_PROGRESS / NOT VERIFIED / C SOURCE MUST BE PRESERVED`

The next session should continue without repeating the full historical investigation unless new evidence contradicts this handoff.
