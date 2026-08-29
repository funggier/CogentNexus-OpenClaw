# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_DIRECT_REGISTRATION_CANONICALITY_TDD_REPAIR_ONLY`
Current authorization: `CNX-20260829-144_DIRECT_SAME_PATH_REGISTRATION_CANONICALITY_REPAIR`
Task ID: `CNX-20260829-144`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`](tasks/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md)

Task 144 is a narrow offline RED-first rework of Task 143. It does **not** authorize any live install/install-over/recovery action and does **not** authorize a Dashboard semantic Send.

## Task-143 disposition

Task-143 report:

`docs/operations/coordination/reports/CNX-20260829-143-direct-in-place-rollover-finalization-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-143-direct-in-place-rollover-finalization-repair-review.md`

Review disposition: **REWORK**.

Accepted from Task 143:

- genuine Task-142 same-path RED existed before production edit;
- canonical direct A -> B same-path finalization is a valid supported topology;
- managed same-path replacement remains invalid;
- backup/fingerprint/manifest/product-storage/root-indirection containment is substantially correct for covered cases;
- exact repair SHA `59952167f51657ae2ff900a28aae528f835f9b6e` has GREEN exact-SHA CI.

Blocking finding:

- `_active_registered_plugin()` resolves inventory `rootDir` before returning replacement identity;
- Task-143 finalization computes the lexical registration key but only uses `registration_key == direct_key` to decide whether to run direct-root attestation;
- a noncanonical alias `rootDir` resolving to the canonical direct root is not explicitly rejected before same-path authority;
- therefore Task 143 has not proven its required canonical active-registration invariant.

## Current live-state boundary

Task 142's partial live state remains intentionally untouched:

- exact candidate plugin payload is present at the canonical direct extension path;
- exact candidate `namespace_ownership.py` is installed;
- one plugin identity remains disabled;
- controller remains `passthrough`;
- pre-attempt ownership manifest remains present;
- Task-142 post-failure evidence had healthy Gateway/Ollama, recovery/delivery READY, pending outbox `0`, SQLite `ok`, unchanged semantic counts, and zero Dashboard Sends.

Task 144 must not normalize or mutate this live state.

## Task-144 execution contract

Task 144 must:

1. create a genuine RED where raw inventory `rootDir` is a noncanonical alias resolving to the canonical direct plugin root;
2. prove Windows junction/reparse alias semantics explicitly;
3. make the smallest repair that requires canonical lexical registration before direct same-path mutation authority;
4. preserve canonical direct A -> B success;
5. preserve managed npm ownership and Task-140/141 root-indirection safety;
6. preserve backup/fingerprint/manifest/storage/registration uniqueness proofs;
7. preserve deterministic Task-142 partial-state re-entry classification/action planning;
8. run full relevant tests/build/plugin/package validation and exact-SHA CI;
9. publish the matching report and stop for independent review.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`

Then stop for independent ChatGPT review.

## Hard fence

No live Windows install/install-over/update/uninstall/reset/clean-reinstall; no live cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no ownership-manifest mutation; no Dashboard semantic Send/resend; no semantic reuse/injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no crash/recovery injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
