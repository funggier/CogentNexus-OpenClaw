# CNX-20260829-138 — Independent Review

## Review disposition

**ACCEPT**

## Verdict

**ROOT CAUSE PROVEN; MINIMAL REPAIR ACCEPTED; OFFLINE VALIDATION GREEN.**

Task 138 satisfies its offline diagnosis-and-repair contract. The executor produced a deterministic registered-boundary RED reproducer before changing production source, proved the exact callback sequencing condition that caused Task 137, applied a one-predicate production repair, and obtained targeted, full-suite, build, plugin-validation, and exact-repair-SHA CI GREEN evidence.

This review accepts repaired source commit:

`16f5c396e9be0af8d1bd34824fe2993613501a6f`

as the next candidate for controlled Windows deployment proof. This review does **not** claim final live Dashboard acceptance: Task 138 performed no install/install-over and no live Dashboard semantic Send.

## Evidence accepted

From the Task-138 report and independent GitHub inspection:

- Task-138 starting HEAD was `9e150078a324ffe6e42d5800553290de02523d8c`;
- accepted pre-repair source candidate was `1424d6fbee2c458c8c30440616783d2fa1bc1201`;
- accepted pre-repair installed fingerprint remained `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- all source/test work was isolated from the installed Windows runtime;
- the registered release path was traced through `v091-release-entry.ts` to `installV091DashboardVerifiedDelivery(...)`, `reply_dispatch`, `dispatcher.appendBeforeDeliver(...)`, the final-payload filter, and `stageDashboardDirectResult(...)`;
- a genuine RED regression test was added first through the registered callback boundary;
- the RED case modeled a valid `info.kind === "final"` payload while `getQueuedCounts().final === 0`, matching the runtime contract in which the callback currently being delivered may not yet be represented in queued counts;
- before the production edit, the test failed because no `cnx_assistant_delivery` durable direct-result row was created;
- the exact source predicate causing the miss was `if (finalCount !== 1) return payload;`;
- the minimum production repair changed only that condition to `if (finalCount > 1) return payload;`;
- the repaired behavior accepts legitimate current-final callbacks when the observed queued-final count is `0` or `1`, while continuing to reject true multi-final ambiguity when the count is greater than `1`;
- the repair does not weaken Ticket-first admission, session authority/generation fencing, durable-before-transport staging, stable Ticket/generation idempotency, native acknowledgement, changed-final fail-closed behavior, or no-regeneration duplicate protection;
- targeted new regression: GREEN;
- existing Dashboard verified-delivery plus response-ready boundary tests: 12 passed;
- full plugin suite: 50 test files / 269 tests passed;
- `npm run build`: exit 0;
- `npm run plugin:validate`: exit 0;
- `git diff --check`: passed;
- exact repair commit changed only `v091-dashboard-verified-delivery.ts` and `v091-dashboard-verified-delivery.test.ts`;
- exact-repair-SHA GitHub Actions completed successfully: Validate run `33246839934`, PS5.1 Acceptance Smoke run `33246839944`, and Windows Installer Pack Smoke run `33246839942`.

The report-only commit is `68ed98911f24dd6be005030cb497eba03622afd3` and does not alter the accepted source repair.

## Root cause accepted

The Task-137 product/runtime failure is now source-proven as a **Dashboard final-count sequencing filter defect**.

The runtime callback can receive the current valid final payload before that same final is reflected in `getQueuedCounts().final`. Therefore `finalCount === 0` is valid for one current final. The old strict `finalCount !== 1` predicate skipped durable staging in that legitimate state. The later compatibility path could still commit `response_ready`, leaving no durable `direct_result`; the existing safety boundary then correctly failed closed and refused regeneration to avoid duplicate output.

This explains the Task-137 evidence without changing the safety interpretation of `failure_delivery_suppressed`.

## Classification

- **Task-138 execution result:** `COMPLETED`;
- **Review disposition:** `ACCEPT`;
- **Root cause:** `PROVEN`;
- **Repair scope:** `MINIMAL`;
- **Offline validation:** `GREEN`;
- **Exact repaired source candidate:** `16f5c396e9be0af8d1bd34824fe2993613501a6f`;
- **Live Windows deployment of repaired candidate:** `NOT YET PERFORMED`;
- **Final Dashboard durable-delivery acceptance:** `NOT YET RE-RUN`;
- **Task-137 Send ledger:** remains permanently consumed `1 / 1`;
- **Human decision required for next controlled deployment proof:** `NO`.

## Required next step

Open `CNX-20260829-139` as a controlled **repaired-candidate install-over and post-install provenance/health proof** task.

Task 139 must keep deployment verification separate from semantic acceptance:

1. preserve Task-136/137 historical Tickets and delivery evidence;
2. build/package from exact repaired source commit `16f5c396e9be0af8d1bd34824fe2993613501a6f` using the established supported package/install path;
3. prove the pre-install runtime still matches the old accepted fingerprint and has no active/pending semantic residue;
4. perform one controlled install-over of the repaired candidate without clean uninstall/reset/normalization;
5. prove the installed payload originates from the exact repaired candidate and record its new fingerprint/package provenance;
6. prove post-install managed/Ollama, Gateway/Ollama, recovery, delivery, SQLite, plugin identity, and zero-pending/nonterminal health;
7. prove the historical failed Task-136/137 records remain preserved and that installation itself created no new semantic Ticket/delivery/recovery work;
8. perform **no live Dashboard semantic Send** under Task 139;
9. publish the matching report and stop for independent review.

Only after Task 139 is independently accepted may a separate fresh-ledger Dashboard durable-delivery acceptance be authorized.
