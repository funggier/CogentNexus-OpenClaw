# CNX-20260829-144 — Direct Same-Path Registration Canonicality Repair

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_DIRECT_REGISTRATION_CANONICALITY_TDD_REPAIR_ONLY`
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation
Opened: 2026-08-29 ICT

## Objective

Close the lexical active-registration canonicality gap identified by the independent Task-143 review without undoing the valid direct in-place A -> B finalization repair.

Use RED -> minimal fix -> GREEN. This task is offline-only and does **not** authorize any live install/install-over/recovery action or Dashboard semantic Send.

## Starting evidence

Task-143 report:

`docs/operations/coordination/reports/CNX-20260829-143-direct-in-place-rollover-finalization-repair.md`

Independent Task-143 review:

`docs/operations/coordination/reviews/CNX-20260829-143-direct-in-place-rollover-finalization-repair-review.md`

Task-143 production repair under rework:

`59952167f51657ae2ff900a28aae528f835f9b6e`

Accepted from Task 143:

- direct canonical same-path A -> B finalization is a legitimate supported topology;
- managed same-path rollover must remain rejected;
- direct root itself must remain a real non-reparse directory;
- old backup, retired fingerprint, expected replacement fingerprint, unchanged manifest, singular product storage, and exact package/version evidence remain mandatory;
- Task-142 partial live state classifies as an already-exact candidate offline.

The blocking gap is narrower: raw OpenClaw inventory `plugins[].rootDir` is resolved by `_active_registered_plugin()` before replacement identity is consumed. The finalizer computes the lexical registration key but does not reject it when it differs from the canonical direct root.

## Phase 0 — Fresh authority

Before editing:

1. verify fresh branch HEAD and coordination state;
2. verify Task 144 is active and unsuperseded;
3. inspect Task-143 report/review, exact repair `59952167...`, and current tests;
4. perform all work in an offline clone/worktree;
5. do not inspect or mutate the user's live state beyond the durable Task-142 evidence already in the repository.

## Phase 1 — Genuine RED before production edit

Add the narrowest deterministic test through the actual `finalize_plugin_rollover_transaction()` boundary.

Required fixture:

1. prepare a valid canonical real direct retired payload A and coherent manifest;
2. call real `prepare_plugin_rollover_transaction()` for expected candidate B, with B != A;
3. replace the payload at the canonical direct path with valid B;
4. keep the canonical direct root itself a normal real directory;
5. create a distinct filesystem alias path whose target is the canonical direct root;
6. provide a singular OpenClaw plugin inventory whose raw `rootDir` is the **alias path**, not the canonical direct path;
7. ensure the alias resolves to the canonical direct root and the payload/package/version/fingerprint otherwise look valid;
8. call real `finalize_plugin_rollover_transaction()`;
9. before production repair, prove current `59952167...` incorrectly authorizes the transition or otherwise reaches manifest finalization instead of rejecting noncanonical registration.

Preferred portable RED: symlink alias on POSIX-capable CI.

Required Windows proof: use a junction/reparse alias or a narrowly equivalent Windows lexical-registration test. Do not silently skip Windows canonicality proof.

At least one RED should cover an alias **inside** OpenClaw state. If practical, also cover a lexical alias outside the state that resolves back into the canonical direct root, because `_active_registered_plugin()` currently checks containment after resolution.

The RED must fail for the canonical-registration semantic reason, not fixture setup.

## Phase 2 — Minimal repair

Make the smallest repair at the owning finalization/registration boundary.

Required behavior for direct same-path authority:

- raw inventory `rootDir` must lexically identify the exact canonical direct root after only safe lexical normalization appropriate to the platform;
- an alias/symlink/junction/noncanonical lexical registration that merely resolves to the direct root must be rejected;
- the canonical direct root itself must still be attested as a real non-reparse directory;
- resolved replacement root must still equal the transaction's canonical retired direct root;
- current payload fingerprint must equal expected B and differ from retired A;
- backup payload/tree must still prove A;
- ownership manifest hash must remain unchanged since prepare;
- product storage evidence must remain singular and direct;
- package/version and active registration uniqueness proof remain strict.

Do not globally ban supported aliases for unrelated code paths unless root-cause evidence requires it. Prefer the smallest check specific to direct same-path mutation authority.

Do not weaken `_active_registered_plugin()`, `_npm_project_for_plugin()`, Task-141 reparse protections, or rollback/quarantine semantics.

## Phase 3 — Required negative and preservation tests

At minimum prove:

1. canonical direct registration + canonical real root + A -> B same-path transition: accepted;
2. in-state alias registration -> canonical direct root: rejected;
3. Windows junction/reparse alias registration -> canonical direct root: rejected;
4. outside-state lexical alias resolving back into canonical direct root: rejected where testable;
5. direct root itself symlink/junction/reparse: still rejected;
6. A -> A / no fingerprint transition: still rejected;
7. expected fingerprint mismatch: still rejected;
8. backup tamper: still rejected;
9. manifest drift: still rejected;
10. conflicting product storage: still rejected;
11. managed same-path replacement: still rejected;
12. valid managed distinct-generation rollover: unchanged;
13. Task-142 partial-state classification remains `upgrade`, `pluginAlreadyExact=true`, `pendingRollover=false`;
14. lifecycle action resolution does not replay plugin installation solely because of the preserved partial state.

## Phase 4 — GREEN validation

Run at minimum:

- focused new RED/GREEN regression(s);
- full `tests/test_task143_direct_in_place_finalization.py` plus Task-144 test file if separate;
- full `tests/test_plugin_generation_rollover.py`;
- `tests/test_namespace_install_contract.py`;
- `tests/test_installer_transaction_wiring.py`;
- affected classify-install/lifecycle-action tests;
- full Python test suite;
- plugin tests;
- build;
- `plugin:validate`;
- package verification;
- `git diff --check`.

Then verify exact-repair-SHA GitHub Actions:

- Validate;
- Windows Installer Pack Smoke;
- PS5.1 Acceptance Smoke.

Windows CI must exercise the canonical-registration test surface.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`

The report must include:

- exact canonical-registration root cause;
- genuine RED command/output before production edit;
- alias fixture topology and lexical vs resolved paths;
- exact production change;
- Windows junction/reparse alias evidence;
- preserved canonical direct A -> B success;
- preserved managed and all negative ownership boundaries;
- Task-142 partial-state re-entry evidence;
- full test/build/plugin/package results;
- exact repair commit SHA;
- exact CI run IDs/results;
- explicit confirmation of zero live runtime/Dashboard mutation.

Then stop for independent ChatGPT review.

## Hard fence

No live Windows install/install-over/update/uninstall/reset/clean-reinstall; no live cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no ownership-manifest mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no crash/recovery injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.

## Acceptance boundary

A Task-144 PASS is offline source/test/CI evidence only. It must be independently reviewed before any later task may authorize supported live install completion/recovery or final Dashboard durable-delivery acceptance.
