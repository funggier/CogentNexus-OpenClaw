# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_PRODUCT_UNINSTALL_AND_CLEAN_FRESH_REINSTALL_ACCEPTANCE`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continuation; Task 145 is independently ACCEPTed and the next destructive acceptance is one real product uninstall followed by one clean fresh install from the exact accepted candidate  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md`](tasks/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md)

Task ID:

`CNX-20260830-146`

## Task-145 accepted result

Report:

`docs/operations/coordination/reports/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof-review.md`

Disposition: **ACCEPT**.

Accepted production implementation SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Task 145 proved:

- exact accepted candidate provenance recomputed and used;
- coherent canonical partial-state classification;
- `pluginAlreadyExact=true`, no redundant plugin rollover;
- exactly one supported installer invocation, exit `0`;
- ownership helper refreshed to the accepted repaired source;
- plugin singular/canonical/enabled/loaded;
- controller returned to `managed`;
- Gateway/OpenClaw/Ollama/recovery/delivery/SQLite healthy;
- pending deliveries `0`;
- durable history preserved;
- Dashboard semantic Sends `0`.

## Task-146 authority

Task 146 tests the actual operator-facing destructive lifecycle rather than a helper wrapper.

Before mutation Hermes/Codex must re-verify live state, ownership, canonical plugin storage, Gateway/provider/recovery/delivery/SQLite health, and preserve test evidence outside CNX live roots.

Authorized destructive sequence is strictly:

1. exactly one installed `cnxclaw.cmd uninstall` invocation;
2. exactly one explicit lowercase `y` confirmation;
3. prove product-owned Windows deferred cleanup reaches clean CNX-absent/native-OpenClaw state;
4. only then exactly one normal fresh `scripts/install.ps1` invocation from detached exact SHA `fb5781c1...`;
5. prove new fresh MANAGED candidate health.

If uninstall fails, there is no fresh install. If deferred cleanup is incomplete, there is no fresh install. If fresh install fails, there is no retry/manual repair.

`scripts/clean-reinstall.ps1` is prohibited in this task because it would bypass proof of the product's `uninstall` command.

The public GitHub Release distribution/download smoke is intentionally later; Task 146 must not tag or publish a release.

## Semantic fence

Task 146 authorizes **zero Dashboard semantic Sends** and no manual semantic database/Ticket/workflow/outbox/delivery/recovery mutation.

## Prohibited

No Dashboard Send/resend; no reset; no crash/recovery injection; no manual plugin install/uninstall/enable/disable; no manual CNX live-file deletion; no manual controller/ownership-manifest normalization; no clean-reinstall helper; no retry after failure; no alternate installer; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-146-product-uninstall-and-clean-fresh-reinstall-acceptance.md`

Then stop for independent ChatGPT review. Reset/runtime-lifecycle/final Dashboard acceptance are not automatic successors.
