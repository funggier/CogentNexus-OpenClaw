# CNX-20260829-138 — Dashboard Direct-Result Durable Capture Repair

## Final verdict

**COMPLETED**

Task 138 was completed as an offline source TDD diagnosis and minimal repair.
No live Dashboard semantic Send or live Windows runtime mutation was performed.

## Authority and baseline

- Task: `CNX-20260829-138`
- Branch: `agent/v0.9.3-full-stabilization`
- Task-138 starting HEAD: `9e150078a324ffe6e42d5800553290de02523d8c`
- Accepted pre-repair source candidate: `1424d6fbee2c458c8c30440616783d2fa1bc1201`
- Accepted pre-repair installed fingerprint:
  `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- ACTIVE/STATUS were freshly fetched and confirmed Task 138 remained
  `READY_FOR_HERMES` and unsuperseded.
- The starting source tree was clean and had no production drift after the
  accepted candidate; later history through Task 137 contained coordination
  documentation only.

Repository clone used for all source/test work:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-continue5-20260829T093432Z\clone`

Installed runtime paths were not accessed or mutated. `node_modules` was
installed only inside this isolated source clone from its existing lockfile,
using `npm ci --ignore-scripts`.

## Source inspection and registered boundary

The registered release path is:

`v091-release-entry.ts` -> `installV091DashboardVerifiedDelivery(api, config)` ->
`api.on("reply_dispatch", ...)` -> `ctx.dispatcher.appendBeforeDeliver(...)` ->
final payload filter -> `stageDashboardDirectResult(...)`.

The OpenClaw `2026.7.1-2` contract in the isolated dependency tree defines
`appendBeforeDeliver(payload, info)` as a callback that can run before the
currently delivered final is reflected in dispatcher queued counts. The
callback's `info.kind` identifies the final payload, while
`getQueuedCounts().final` reports queued final items.

The source already correctly separates process-global TicketStore patching from
per-runtime hook registration. That prior reload fix was not repeated or
reinterpreted as the Task-137 root cause.

## Genuine RED before production edit

A new regression test was added first to
`src/v091-dashboard-verified-delivery.test.ts`:

`stages a valid final when the dispatcher count excludes the callback currently being delivered`

The test uses the registered `reply_dispatch` hook and its
`appendBeforeDeliver` callback. It models the runtime contract where:

- a Dashboard direct Ticket is accepted and routed;
- the final callback has `info.kind === "final"` and non-empty text;
- `getQueuedCounts()` returns `{ final: 0 }` because the current callback is not
  yet included in the queued count;
- the exact final text must nevertheless be durably staged as one
  `cnx_assistant_delivery` row before native delivery.

RED command:

```text
npm test -- --run src/v091-dashboard-verified-delivery.test.ts -t "stages a valid final when the dispatcher count excludes"
```

Observed RED against unmodified Task-138 source:

```text
AssertionError: expected undefined to match object {
  kind: 'direct_result',
  status: 'pending',
  text: 'callback-count-result'
}
```

The failing assertion showed that no durable delivery row was created. This
was a semantic regression failure, not a test typo or a cleanup error. An
earlier execution of the same test also exposed a Windows SQLite `EBUSY`
cleanup artifact; cleanup was made best-effort in the test so it could not mask
the actual assertion. No production edit occurred before the genuine RED.

## Proven root cause

The verified-delivery callback applied this predicate:

```ts
if (finalCount !== 1) return payload;
```

In the real dispatcher lifecycle, the callback can run while the current final
payload is being delivered and therefore is not yet counted in
`getQueuedCounts().final`. A valid single final can consequently present
`finalCount === 0`. The strict equality filter skipped the valid payload before
calling `stageDashboardDirectResult`, producing the Task-137 class:

- visible final response;
- no durable direct-result row;
- `response_ready` followed by fail-closed delivery suppression.

The existing tests modeled `finalCount === 1` for a callback that was already
represented in the queue and covered rejection of `finalCount === 2`, but did
not cover the callback-excluded `0` sequencing permitted by the registered
runtime contract. The root cause is therefore the final-count sequencing filter,
not Ticket admission, model execution, recovery, or the fail-closed fallback.

## Minimal repair

Production change in
`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`:

```diff
- if (finalCount !== 1) {
+ if (finalCount > 1) {
```

This accepts the current callback when the queue count is `0` or `1`, while
continuing to reject multiple queued finals (`finalCount > 1`). It does not
change:

- Ticket-first admission;
- session authority or generation fencing;
- durable-before-transport staging;
- stable Ticket/generation idempotency;
- changed-final fail-closed behavior;
- native acknowledgement requirement;
- no-regeneration behavior once a durable result exists;
- fail-closed behavior when staging genuinely cannot occur;
- redacted telemetry/no-secret behavior.

The regression test remains registered-boundary based and verifies the exact
pending durable row and final text.

## GREEN validation

Targeted regression after the minimal source change:

```text
1 test passed, 10 skipped
```

Targeted existing boundary tests:

```text
src/v091-dashboard-verified-delivery.test.ts
src/v093-response-ready-boundary.test.ts
12 tests passed
```

Full plugin test suite:

```text
50 test files passed
269 tests passed
```

Build:

```text
npm run build — exit 0
```

Plugin validation:

```text
npm run plugin:validate — exit 0
```

Validation details included:

- mixed-plugin artifact verification: PASS, 45 config properties and 5 tools;
- ticket DB bootstrap: PASS, 9 required tables plus v095 registration fence;
- package verification: `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`,
  178 packed files.

The isolated clone initially lacked dependencies and its first CI polling
attempt used the wrong working directory; those were harness setup issues,
corrected without source/runtime mutation. No relevant validation result was
suppressed or replaced.

## CI on exact repair SHA

Source/test repair commit:

`16f5c396e9be0af8d1bd34824fe2993613501a6f`

Fresh GitHub Actions checks for that exact SHA all completed successfully:

| Workflow | Run ID | Status | Conclusion |
|---|---:|---|---|
| Validate | `33246839934` | completed | success |
| PS5.1 Acceptance Smoke | `33246839944` | completed | success |
| Windows Installer Pack Smoke | `33246839942` | completed | success |

No CI failure required a rerun. No lifecycle or live acceptance workflow was
invoked by this task.

## Scope and diff audit

The source repair commit changed exactly two files:

1. `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
   — one-line final-count predicate repair;
2. `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.test.ts`
   — one deterministic registered-boundary regression test and Windows-safe
   best-effort test cleanup.

Source/test blob identities at repair HEAD:

- source blob: `9eea06dff25c1d501ecd479a45b3a2a9aa5cbf5f`;
- test blob: `2ea9b706347e34cf68514aecebf749d06851d685`.

`git diff --check` passed. No installer, lifecycle, provider, model,
configuration, unrelated recovery, dependency manifest, release, or live-state
file entered the source repair commit.

The matching Task-138 report is intentionally published as a separate
report-only commit after the source repair.

## Safety confirmation

Not performed:

- live Dashboard semantic Send/resend or reuse of Task-136/137 semantics;
- alternate CLI/Gateway/API/database semantic injection;
- install, reinstall, reset, uninstall, or install-over;
- live start/stop/restart/enable/disable;
- recovery or crash injection;
- provider/model/OpenClaw/config mutation;
- manual live Ticket/outbox/delivery/ack mutation;
- live SQLite write, cleanup, or normalization;
- process kill or task/service mutation;
- reboot;
- credentials or secrets access;
- merge, tag, GitHub Release, or force push.

## Publication disposition

After publishing this exact report, stop for independent ChatGPT review. A new
live Dashboard acceptance is not automatic and is not performed by Task 138.
