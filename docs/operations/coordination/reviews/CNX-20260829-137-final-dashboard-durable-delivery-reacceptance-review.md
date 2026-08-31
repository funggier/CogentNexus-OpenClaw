# CNX-20260829-137 — Independent Review

## Review disposition

**ACCEPT**

## Acceptance verdict

**FAIL_PRODUCT_OR_RUNTIME CONFIRMED. OFFLINE DIAGNOSIS AND NARROW REPAIR REQUIRED BEFORE ANY NEW LIVE DASHBOARD ACCEPTANCE.**

Task 137 is accepted as clean evidence that the accepted v0.9.3 source/runtime candidate does not currently satisfy the final Dashboard durable-delivery contract for the observed direct-response path.

Unlike Task 136, this run was not contaminated by an external executor interruption, duplicated final composer content, an additional semantic send, or an observation horizon shorter than the actual runtime outcome. The one authorized Send was consumed, the exact requested ACK became visibly present in the Dashboard, and the runtime itself subsequently failed the Ticket because the final direct payload had not been durably captured.

This review accepts the **defect class** as product/runtime durable direct-result capture/delivery failure. It does **not** yet claim the exact source-level root cause. That must be established by a deterministic offline reproducer before production source is changed.

## Evidence accepted

From the Task-137 report:

- coordination start HEAD `a162d995ad30c6d1838131df045fce957612d94e`;
- accepted source candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201`;
- accepted installed payload/plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- fresh pre-send baseline was managed/Ollama with Gateway and Ollama healthy, recovery `READY`, delivery `READY`, `pendingOutbox=0`, SQLite integrity `ok`, and no unexplained active semantic work;
- Task-136 historical failure remained preserved and was not retried or normalized;
- fresh nonce `CNX-DDA2-20260829T082853Z-8A603A` was absent before Send;
- the final pre-send composer contained exactly one intended request with no duplicated full message;
- exactly one deliberate Dashboard Send activation occurred and the Task-137 ledger is permanently consumed `1 / 1`;
- semantic resend and alternate semantic transport remained zero;
- executor interruption after Send was **none**;
- exactly one new Ticket was created: `CNXT-a38e1408-205f-4606-a5c8-ec54e9515aea`;
- exactly one direct model-call row was created for that Ticket;
- Ticket-first ordering was positively proven: `accepted` at `08:32:28.619Z`, `routed` at `08:32:28.624Z`, then `direct_model_call_started` at `08:32:28.724Z`;
- model execution ended at `08:34:04.928Z` and `response_ready` was durably recorded at `08:34:04.995Z`;
- the visible Dashboard assistant result was exactly `ACK CNX-DDA2-20260829T082853Z-8A603A`;
- the Ticket then reached durable `failed` plus `failure_delivery_suppressed` at `08:36:05.062Z`;
- the failure message was exactly `direct response delivery became unverifiable before the final payload was durably captured; refusing regeneration to avoid duplicate output`;
- post-run durable state contained zero `ticket_outbox`, zero `cnx_assistant_delivery`, and zero `cnx_direct_recovery` rows for the observed direct-result path;
- no duplicate Ticket, concurrent execution, resend, alternate semantic side effect, source edit, install/reinstall, lifecycle action, recovery action, provider/model/config mutation, cleanup, or normalization occurred;
- final runtime/recovery/delivery/Gateway/Ollama/SQLite state remained otherwise coherent.

The roughly 120-second interval between `response_ready` and the fail-closed terminal event is consistent with the configured durable receipt-deadline class, but this timing alone is not accepted as source-level root-cause proof.

## Independent source-boundary reading

The current branch source is unchanged from accepted candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201`; the commits after that candidate through Task-137 report HEAD modify coordination documentation only.

The relevant shipped source establishes these intended invariants:

1. `v091-dashboard-verified-delivery.ts` intends `stageDashboardDirectResult(...)` to commit one `cnx_assistant_delivery` row of kind `direct_result` and the corresponding durable result metadata **before native Dashboard transport begins**.
2. The registered `reply_dispatch` / dispatcher `appendBeforeDeliver` path is the runtime boundary that is expected to extract the final text and call that staging function.
3. `v092-durable-delivery-boundary.ts` deliberately prevents inference regeneration once a durable direct result exists; transport must own retries after durable capture.
4. `v091-dashboard-verified-delivery.ts` deliberately fails closed when a Dashboard direct Ticket has `response_ready_at` but no durable `direct_result` after the receipt deadline, using the same failure message observed in Task 137.
5. Existing tests prove direct staging, a synthetic registered hook path, durable idempotency, and the fail-closed fallback, but Task 137 proves that at least one real OpenClaw 2026.7.1-2 Dashboard callback path can still reach `response_ready` without the durable direct-result row.

Therefore the next task must investigate the runtime hook/callback/correlation/filter/staging boundary and prove the exact failing condition. Candidate causes such as callback payload shape, final-count filtering, run correlation, hook ordering/registration, session authority, or staging timing remain hypotheses only until reproduced.

## Classification

- **Acceptance result:** `FAIL`;
- **Review disposition:** `ACCEPT`;
- **Task-137 Send ledger:** consumed `1 / 1`;
- **Resend under Task 137:** permanently forbidden;
- **Executor contamination:** none established;
- **Product/runtime defect class:** `CONFIRMED`;
- **Defect boundary:** Dashboard direct final payload durable capture / delivery verification;
- **Exact source root cause:** `UNPROVEN`;
- **Duplicate-prevention behavior:** accepted as safety-preserving and must not be weakened;
- **Installed/runtime mutation during Task 137:** none;
- **Human decision required:** `NO` for the next narrow offline diagnosis-and-repair step.

## Required next step

Open `CNX-20260829-138` as an **offline source TDD diagnosis-and-repair task**.

Task 138 must:

1. preserve the Task-137 report and failed Ticket as immutable historical evidence;
2. reproduce the observed `response_ready`-without-`direct_result` condition deterministically through the relevant registered Dashboard delivery hook/callback boundary;
3. obtain a genuine RED regression test before editing production source;
4. identify the exact root cause from the reproducer and source trace rather than selecting a hypothesis in advance;
5. apply the narrowest production fix that makes the final payload durable before native delivery while preserving session authority, stable idempotency, exactly-once semantics, and fail-closed duplicate protection;
6. run the targeted regression test, existing Dashboard verified-delivery tests, response-ready boundary tests, full plugin test suite, build, and plugin validation;
7. publish the matching Task-138 report with RED evidence, exact changed files, root cause, GREEN evidence, CI/workflow state, and exact HEAD;
8. perform **no** live Dashboard semantic retry, install/reinstall, reset, lifecycle/recovery action, provider/model/config mutation, or release action under Task 138.

A new real-Dashboard acceptance may be considered only after Task 138 is independently reviewed and its offline repair proof is GREEN.
