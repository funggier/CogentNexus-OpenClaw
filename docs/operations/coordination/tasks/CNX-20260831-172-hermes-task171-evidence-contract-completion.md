# CNX-20260831-172 — Hermes Task-171 Evidence-Contract Completion

Status: `READY_HERMES`

Execution mode: `TASK171_EVIDENCE_CONTRACT_COMPLETION_HERMES`

Authorization: `CNX-20260831-172_HERMES_TASK171_EVIDENCE_CONTRACT_COMPLETION`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Objective

Complete the mandatory evidence/report contract for the already-executed Task-171 exactly-one-Send semantic experiment without repeating or altering the experiment. Use the preserved Task-171 evidence root plus read-only inspection only to produce the missing acceptance matrix, Reviewer Verification Packet, immutable evidence identities, and exact field-level bindings needed for final ChatGPT review.

This is an evidence-completion task. It is **not** a semantic re-run, repair, installer, restart, or recovery task.

## Authoritative prior action

The only semantic action under review remains Task 171:

- Task: `CNX-20260831-171`
- Task-171 activation HEAD: `b6ebb89860d176222773320087a7d1dfa34656a8`
- Task-171 report commit: `db4cbbbb63d6023653d271e6d15d87a477d6d8bd`
- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- OpenClaw: `2026.7.1-2`
- Task-171 evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx171-evidence-20260831T020231Z`
- Task-171 nonce: `T171-20260831T020446Z-3142A528`
- Expected response: `CNX-171-ACK-T171-20260831T020446Z-3142A528`
- Session: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`
- Ticket: `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`
- Run: `8b69bede-030f-4c20-8bb8-0aa99e12422c`

The Task-171 ChatGPT review disposition is:

`REWORK_REQUIRED — TASK171_SEMANTIC_RESULT_COHERENT_BUT_VERIFICATION_PACKET_MISSING`

This does not reject the semantic result. It requires complete audit evidence before acceptance.

## Absolute no-semantic-action rule

Task 172 authorizes **zero** semantic sends/inferences.

The Task-171 Send count must remain exactly `1` for the whole acceptance attempt. Task 172 MUST NOT:

- click Dashboard Send;
- submit text by Enter or another UI mechanism;
- use `chat.inject`;
- use any alternate semantic input surface;
- invoke a model manually;
- invoke or trigger recovery/regeneration;
- replay the Task-171 prompt;
- create a replacement semantic test.

If existing evidence is insufficient, report `UNPROVEN`/`REWORK_REQUIRED`. Never compensate with another semantic action.

## Preflight

Before evidence collection:

1. read fresh remote branch HEAD, `ACTIVE.md`, `STATUS.md`, Task-171 report/review, and this task;
2. confirm the Task-172 report does not already exist;
3. verify the Task-171 report commit changed only the Task-171 report file;
4. confirm no product/source/test/workflow drift occurred after the accepted repair candidate;
5. confirm the preserved Task-171 evidence root exists before relying on it;
6. record whether current read-only live state is still available, but do not require current UI/runtime state to replace contemporaneous Task-171 evidence.

## Required evidence completion

### 1. Exact Task-171 action identity

Record from preserved evidence:

- exact nonce;
- exact prompt and expected response;
- exact session key;
- prompt hash from `b01-send-ledger.json`;
- exact Send budget/ledger proving one authorized Send and no retry;
- final visible Dashboard user/assistant nonce counts if the preserved screenshot/evidence proves them; otherwise mark the UI-count criterion explicitly `UNPROVEN` while preserving native authority.

### 2. Native transcript authority

For the Task-171 native transcript:

- exact transcript path;
- transcript SHA-256 after Task-171 observation;
- exact user nonce record count;
- exact assistant nonce record count;
- exact expected-response record count;
- exact native user message ID;
- exact native assistant message ID;
- assistant native timestamp;
- exact persisted assistant text before/including marker as appropriate;
- exact CogentNexus marker presence and parsed delivery/idempotency identity;
- demonstrate that the marker identity corresponds to the Task-171 Ticket/delivery row.

Do not alter the transcript.

### 3. Ticket/run/model identity

Record exact field-level evidence for:

- Ticket ID and final status;
- Run ID;
- full direct model-call ID (not abbreviated);
- request/idempotency identity used for the direct model call if stored;
- provider/model;
- model call count scoped to the Task-171 run;
- model start/end timestamps, outcome, duration;
- `response_ready_at`;
- `delivery_confirmed_at`;
- `durableDelivery`/durable payload state;
- complete Ticket event order with timestamps and material payload fields.

### 4. Durable delivery row

Read the exact Task-171 `cnx_assistant_delivery` row and record all acceptance-relevant fields, including when present:

- row ID;
- Ticket ID;
- Run ID;
- idempotency/delivery identity;
- staged text;
- staged text hash or recomputed SHA-256;
- owner/generation fields;
- status;
- attempt count;
- claim token/expiry;
- created/updated/delivered timestamps;
- settlement source;
- final relation to native marker.

Prove exactly one row binds to the Task-171 result.

### 5. Duplicate/recovery/outbox safety

Provide run-scoped evidence, not only aggregate counts:

- zero second model-call rows for the Task-171 run;
- zero `cnx_direct_recovery` rows/actions scoped to the run unless an existing row is part of normal non-semantic bookkeeping, in which case explain it;
- zero `ticket_outbox` rows conflicting with the direct result;
- zero duplicate assistant nonce/expected-response native records;
- zero duplicate durable delivery rows;
- no regeneration/recovery event in the Ticket event sequence.

### 6. Immutable evidence index

For the critical Task-171 local evidence files, compute and report SHA-256 hashes at minimum for:

- `b01-send-ledger.json`;
- `c01-post-send-nonce-search.json`;
- `c02-post-db.json`;
- `c09-native-settlement.json`;
- the Task-171 Dashboard screenshot;
- any additional file used as sole support for a critical acceptance claim.

If any file is missing, say so. Do not regenerate it by repeating the experiment.

### 7. Post-state/read-only consistency

Read-only rechecks are allowed if they do not mutate runtime state. Record:

- current DB integrity;
- current Ticket/delivery row still present and consistent;
- current installed fingerprint/OpenClaw version if easily available read-only;
- any drift since Task 171 that affects confidence.

Do not restart or repair anything.

## Task-171 acceptance matrix

The Task-172 report must contain a table covering **exactly** these nine Task-171 success criteria:

1. exactly one Dashboard semantic Send;
2. exactly one model execution for the request;
3. exactly one native persisted assistant result for nonce/expected answer;
4. expected native delivery marker/identity present;
5. exactly one correctly bound `cnx_assistant_delivery` row;
6. post-persistence settlement succeeds and `delivery_confirmed_at` is authoritative/non-null;
7. final Ticket reaches successful terminal state;
8. no duplicate UI/native result, second inference, recovery reinjection, or conflicting outbox/delivery;
9. installed fingerprint/OpenClaw pin/runtime/storage integrity acceptable after experiment.

Each criterion must be `PASS`, `FAIL`, or `UNPROVEN` with an exact evidence pointer.

A final `PASS` is invalid if any required criterion is `FAIL` or `UNPROVEN`.

## Reviewer Verification Packet

Mandatory: 5-10 critical claims. For each include:

| # | Critical claim | Why it matters | Exact evidence | Suggested reviewer check |
|---|---|---|---|---|

Prioritize:

- one-Send proof;
- one-model proof;
- native transcript marker identity;
- one durable row + Ticket/run binding;
- settlement after native persistence / `delivery_confirmed_at`;
- no recovery/duplicate/outbox conflict;
- preserved installed provenance/health.

## Hard fence

Authorized:

- read-only GitHub/repository inspection;
- read-only inspection/hashing of preserved Task-171 evidence;
- read-only DB/transcript/runtime queries that cause no lifecycle/semantic change;
- publication of the Task-172 report.

Prohibited:

- any semantic Send or model inference;
- `chat.inject`;
- recovery/regeneration action;
- installer/uninstall/reinstall/reset/rollback;
- Gateway/Ollama/Supervisor/OpenClaw restart or lifecycle mutation;
- manual DB/Ticket/result/outbox/delivery/transcript mutation;
- source/test/workflow/product modification;
- OpenClaw/dependency upgrade;
- release/tag/package publication;
- default/release merge;
- force push.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260831-172-hermes-task171-evidence-contract-completion.md`

The report must follow `EXECUTOR_REPORT_CONTRACT.md` completely, including:

- disposition;
- objective/acceptance contract;
- exact authority/start/head;
- investigation/action summary;
- risk/uncertainty;
- validation/evidence matrix;
- the required nine-row Task-171 acceptance matrix;
- immutable evidence index with hashes;
- anomalies/contradictions;
- hard-fence compliance with Task-172 semantic sends explicitly `0`;
- residual unproven items;
- Reviewer Verification Packet;
- recommended successor;
- publication state.

After report publication, stop for ChatGPT review. No semantic successor is authorized by Task 172.
