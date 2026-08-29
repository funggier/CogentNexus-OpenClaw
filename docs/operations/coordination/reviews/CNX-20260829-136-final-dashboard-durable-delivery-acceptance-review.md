# CNX-20260829-136 — Independent Review

## Verdict

**ACCEPTED AS AN ACCEPTANCE FAIL, BUT INVALIDATED FOR PRODUCT-ROOT-CAUSE CONCLUSIONS.**

Task 136 did not satisfy the final durable-delivery acceptance contract: its one authorized Dashboard Send was consumed, the resulting Ticket ended `failed`, and no terminal durable assistant-delivery/outbox acknowledgement was recorded. That acceptance result remains FAIL and the Task-136 Send authorization remains permanently consumed.

However, the run is not clean evidence of a CogentNexus product defect or of the report's causal statement that duplicated UI text caused the durable failure. The run contains executor/protocol contamination and must not be used to justify a production fix without a new clean reproduction.

## Evidence accepted

From the Task-136 report:

- coordination start HEAD `6c0fdd2160145afb0393e448778615b300c24b9c`;
- accepted candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201`;
- accepted fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- fresh preflight was managed/Ollama with recovery and delivery `READY`, SQLite integrity `ok`, and zero pre-send execution/delivery rows;
- nonce `CNX-DDA-20260829T074041Z-00058D` was absent before Send;
- exactly one Dashboard submission activation was recorded and Task-136 Send ledger is `1 / 1 consumed`;
- resend and alternate semantic injection remained zero;
- exactly one durable Ticket was created: `CNXT-4d67a963-2d1b-4afc-b7c0-0ea48bcf8c62`;
- durable event order was `accepted -> routed -> direct_model_call_started -> direct_model_call_ended -> response_ready -> failed -> failure_delivery_suppressed`;
- `accepted` preceded `direct_model_call_started`, so the Ticket-before-inference invariant was affirmatively demonstrated;
- direct model execution ran from `2026-08-29T07:43:54.879Z` to `2026-08-29T07:58:05.331Z`, approximately 14 minutes 10 seconds;
- `response_ready` existed before the later durable failure;
- final durable state contained zero `ticket_outbox`, zero `cnx_assistant_delivery`, and zero `cnx_direct_recovery` rows;
- final runtime/provider/recovery/delivery/SQLite health was otherwise coherent.

## Contamination / protocol defects

### 1. External executor interruption

After the Task-136 report was published, the operator disclosed that Hermes was accidentally stopped once during the Task-136 execution window.

The retained report does not establish precisely when that interruption occurred relative to Dashboard composition, Send activation, model execution, or post-Send observation. Therefore this review cannot prove that the interruption caused the durable failure, but it also cannot exclude executor/session disturbance as a contributing factor.

A new clean run is required before attributing the failure to production behavior.

### 2. Composer duplication

The report states that the visible user bubble contained the intended acceptance text twice consecutively even though the task intended one exact message.

That is an execution/composer anomaly. The report does not contain source-level or durable causal evidence proving that the duplicated text itself caused `failed` or `failure_delivery_suppressed`.

Accordingly, the statement that the duplicated UI text "consequently" caused the durable failure is **not accepted as root-cause proof**.

A new acceptance must verify the composer contains exactly one copy of the fresh message immediately before Send.

### 3. Observation window was shorter than demonstrated local-model latency

Task 136 authorized post-Send observation "up to 10 minutes". The actual direct model call in the same run lasted approximately 14 minutes 10 seconds, and the operator reports prior `qwen3.5:9b` first-response latency around 20 minutes when used directly through Ollama.

The report later extended read-only observation to 25 minutes. That additional observation was non-mutating and preserved safety, but it exceeded the written Task-136 bounded-observation contract.

The next acceptance must use a realistic bound that cannot misclassify normal local-model first-response latency as failure.

## Classification

Task 136 is classified as:

- **Acceptance result:** `FAIL`;
- **Task-136 Send ledger:** consumed `1 / 1`;
- **Resend under Task 136:** permanently forbidden;
- **Safety violation:** none established; post-Send actions remained read-only;
- **Product root cause:** `UNPROVEN`;
- **Causal run quality:** `CONTAMINATED_BY_EXECUTOR_INTERRUPTION_AND_COMPOSER_ANOMALY`;
- **Production repair authorization:** none;
- **Clean re-acceptance:** allowed only under a new separately authorized task with a fresh nonce and fresh Send ledger.

## Required next step

Open a new Dashboard durable-delivery re-acceptance task without changing production source first.

The new task must:

1. preserve Task-136 durable history; no cleanup or normalization;
2. use a fresh read-only delta baseline and prove no active/nonterminal/pending residue;
3. use a new nonce not present in historical durable state;
4. clear and verify the Dashboard composer contains exactly one copy of the exact message before Send;
5. authorize one new Send only under the new task;
6. allow a realistic local-model observation horizon, with no timeout inference from ordinary first-response latency;
7. treat any external executor interruption after Send as an invalidated run, not product-failure proof, with no resend;
8. require the same Ticket-first, successful-terminal, durable-delivery, acknowledgement, and exactly-once evidence as Task 136.

No source/runtime/plugin repair, lifecycle/recovery replay, provider/model/config mutation, merge, tag, or release is authorized by this review.
