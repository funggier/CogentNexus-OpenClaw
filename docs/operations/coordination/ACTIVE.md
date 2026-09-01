# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK220_STATIC_PAYLOAD_CHECKOUT_BOUNDARY_ADJUDICATION`
Current disposition: `TASK219_FAIL_ACCEPTED__DIST_REPAIR_PROVEN__STATIC_CHECKOUT_BOUNDARY_REQUIRED`
Task ID: `CNX-20260901-220`
Parent task: `CNX-20260901-219`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows repository operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Task-219 reviewed result

Report:

`reports/CNX-20260901-219-task218-real-boundary-red-and-dist-canonicalization-repair.md`

Review:

`reviews/CNX-20260901-219-task218-real-boundary-red-and-dist-canonicalization-repair-review.md`

Accepted disposition:

`ACCEPT_FAIL_CROSS_PLATFORM_DETERMINISM__DIST_REPAIR_PROVEN__STATIC_CHECKOUT_BOUNDARY_ADJUDICATION_REQUIRED`

Accepted facts:

- genuine real-boundary RED reproduced 43 LF/CRLF-generated `dist` differences;
- bounded generated-`dist` canonicalizer commit `9af329b4de7c02fda35b467d84e76bb0f0bb0944` closes those `dist` differences locally;
- local/full validation passed and canonicalizer second pass was idempotent;
- final package mismatch remained outside `dist` in exactly three static payload files: `README.md`, `openclaw.plugin.json`, `scripts/bootstrap-ticket-db.mjs`;
- Task-219 Windows evidence reported CRLF/dirty working-tree bytes for those files versus LF CI bytes;
- repository-side inspection shows the reported static files at `4e31dbd...` expose LF object content while `.gitattributes` declares `text eol=lf`, creating an unresolved Git-object-to-working-tree boundary contradiction;
- no live product/install/lifecycle/SQLite/Discord mutation occurred.

## Active Task 220

Hermes must execute:

`tasks/CNX-20260901-220-task219-static-payload-checkout-boundary-adjudication.md`

Task 220 is diagnostic only. It must trace exact static bytes through:

1. Git object bytes;
2. effective `.gitattributes`;
3. Git config + origin;
4. immediate fresh Windows checkout;
5. `npm ci`;
6. `npm run build`;
7. `npm run plugin:validate`;
8. controlled `core.autocrlf` variants;
9. disposable `git add --renormalize` diagnostics.

No source fix is authorized until the first boundary that converts LF↔CRLF is proven.

## Runtime / Discord boundary

Task 220 authorizes `0 Discord Sends`.

No installer/install-over, lifecycle action, live plugin/config mutation, Gateway restart, live SQLite/ownership/transaction mutation, provider/model substitution, Release/tag mutation, force push, or product/source edit is authorized. Isolated checkout/build diagnostics and report publication only.
