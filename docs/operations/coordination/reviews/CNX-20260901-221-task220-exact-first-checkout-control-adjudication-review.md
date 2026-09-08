# Independent Review — CNX-20260901-221 Exact First-Checkout Control Adjudication

## Verdict

`ACCEPT_PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN__FAIL_CLOSED_STATIC_BYTE_GUARD_REQUIRED`

Task 221 is accepted as diagnostic PASS. It closes the ambiguity left by Task 220: inherited `core.autocrlf=true` is not sufficient by itself to create the three static CRLF payload differences when the exact target commit is the first working-tree materialization. The divergence requires the two-stage materialization topology reproduced by Task 221.

This review does **not** authorize installer execution yet. The repository still contains the unaccepted Task-219 `-text` experiment and the package validator does not currently fail closed when a contaminated worktree presents CRLF static package bytes.

## Accepted evidence

Target commit:

`4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0`

At that commit the four relevant Git objects are LF-only and `.gitattributes` declares `text eol=lf`.

Task 221 used independent `--no-checkout` repositories so the target commit was the first-ever working-tree materialization. The following all produced LF-only bytes and clean status:

- inherited/default Git policy with system `core.autocrlf=true`;
- explicit local `core.autocrlf=true`;
- explicit local `core.autocrlf=false`.

For all three first-materialization controls, `git ls-files --eol` reported `i/lf w/lf attr/text eol=lf` for `package.json`, `README.md`, `openclaw.plugin.json`, and `scripts/bootstrap-ticket-db.mjs`.

The separate two-stage control reproduced the historical failure exactly:

1. clone and materialize the newer branch state first;
2. detach to `4e31dbd...`, whose static blobs are unchanged but whose `.gitattributes` differs from the later `-text` experiment;
3. `README.md`, `openclaw.plugin.json`, and `scripts/bootstrap-ticket-db.mjs` remain/become CRLF while the index/object side is LF and status remains clean.

Therefore the refined root cause is accepted as:

`TWO_STAGE_ATTRIBUTE_AND_WORKTREE_STATE_CARRYOVER`

This supersedes Task 220's broader direct-`core.autocrlf` classification.

## Product/build interpretation

The generated-output repair from Task 219 remains valid evidence:

- genuine pre-fix RED: 188 LF-build files vs 188 CRLF-build files with 43 differing generated artifacts;
- bounded generated-`dist` canonicalizer lineage: `9af329b4de7c02fda35b467d84e76bb0f0bb0944`;
- post-repair `dist` differences: 0;
- fingerprint algorithm unchanged.

The remaining issue is no longer a TypeScript/build-output defect. It is a static package-input integrity problem at the working-tree/package boundary.

The current branch still carries the unaccepted commit `b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5`, which changed the four package paths from `text eol=lf` to `-text`. Task 221 proves `-text` is unnecessary for a correct exact-first checkout and Task 220 already proved it does not establish CI-equivalent bytes in a contaminated worktree. It should be forward-reverted, not retained as the final policy.

However, merely restoring `.gitattributes` is insufficient as a fail-closed provenance control: Git may retain stale working-tree bytes across commit transitions where the payload blobs themselves are unchanged. The package validation path should therefore reject noncanonical static payload bytes before fingerprinting/packing instead of silently accepting a contaminated worktree.

## Required successor

Open Task 222 as a bounded repository/build repair and requalification task.

Required flow:

1. preserve history; no reset/rebase/force push;
2. create a test-only RED proving the current package validation path accepts a deliberately CRLF-contaminated copy of one or more static package payload files even though canonical package bytes are required;
3. commit RED separately;
4. forward-revert the unaccepted `-text` policy to `text eol=lf` for the four static package paths;
5. minimally extend package validation to fail closed on CRLF/noncanonical newline bytes in the static payload files that are part of package identity; do not mutate or rewrite tracked files during validation;
6. keep generated `dist` canonicalization bounded to generated artifacts only;
7. prove a contaminated two-stage-style fixture is rejected before package identity/packing;
8. prove an exact-first Windows materialization of the final candidate passes under inherited `core.autocrlf=true` and remains clean;
9. run full tests/evaluation/plugin validation and authoritative CI on the exact final candidate;
10. retain the exact package-proof artifact and fresh-build the same candidate on Windows using exact-first materialization; require identical 192-file path set, zero byte differences, exact fingerprint equality, and clean tracked status;
11. only after all gates pass may a later task resume installer requalification using the Task-215 direct Scheduled Task execution topology.

## Runtime boundary

Task 222 must remain repository/build only:

- installer/install-over: forbidden;
- `cnxclaw` lifecycle actions: forbidden;
- live plugin/config/Gateway/SQLite/provider mutation: forbidden;
- Discord Sends: 0;
- Release/tag/asset mutation: forbidden.

## Disposition

`ACCEPT_PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN__FAIL_CLOSED_STATIC_BYTE_GUARD_REQUIRED`
