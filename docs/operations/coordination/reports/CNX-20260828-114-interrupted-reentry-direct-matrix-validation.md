# CNX-20260828-114 — Interrupted Re-entry Direct Matrix Validation

## Verdict

`PASS` — complete direct `classify_install(...)` matrix was added as a tests-only commit, ran GREEN on the accepted Task-113 production source, and was validated through exact-source CI and a new package-proof artifact. No production edit was required or made for Task 114. No live Windows lifecycle mutation was authorized or performed.

## Reconciliation

- Task 114 confirmed active in `ACTIVE.md` and `STATUS.md`.
- Reconciled starting HEAD: `a21f58b2cc5c0ae774ef9d2310409c5b221fff62`.
- Task-113 source candidate `d8c5f5f5e7936e673a6731f5a8a0f17e7bd39a06` remained unchanged in production semantics.
- No install-over/reset/uninstall/reinstall/recovery replay, live cleanup, SQLite/config/session mutation, credential access, process kill, reboot, merge, tag, release, or force push was performed.

## Tests-only matrix commit

- Commit: `83e8452de116bf6204be884e4cddf9f3b92b90da`
- Changed file: `tests/test_plugin_generation_rollover.py` only
- Matrix selector: `test_task114_complete_direct_classify_install_matrix`
- Result: `17 passed, 40 deselected`

The matrix calls the actual `classify_install(...)` surface. Existing explicit positive direct and managed tests assert `mode=upgrade`, `pendingRollover=False`, `pluginAlreadyExact=True`, `interruptedRolloverReentry=True`, the replacement path, and the missing retired manifest path. The matrix explicitly covers:

1. active/shared wrapper;
2. direct active plus separate conflicting wrapper;
3. managed active plus separate conflicting wrapper;
4. duplicate exact payload;
5. duplicate active registration;
6. outside-state root;
7. noncanonical contained root;
8. wrong plugin ID;
9. wrong package identity;
10. wrong version;
11. fingerprint mismatch;
12. non-passthrough controller;
13. corrupted manifest;
14. missing `SKILL.md`;
15. missing launcher;
16. mixed namespace residue;
17. altered manifest-owned retired path, which does not use the shortcut;
18. unrelated npm project, which is not treated as product evidence.

All negative boundaries rejected or avoided the shortcut as required; unrelated npm storage did not create a false conflict. The matrix was GREEN against current production, so no production repair commit was created for Task 114.

## Validation

- Full pytest: `448 passed, 3 skipped, 4 subtests passed in 78.27s`
- Targeted suite: `151 passed, 1 skipped in 8.83s`
- Python compile: passed
- Installer lifecycle AST: passed
- `npm ci`: passed
- `npm run plugin:validate`: passed
- `git diff --check`: passed
- Working tree clean before report publication

Valid re-entry action selection remained:

```json
{"mode":"upgrade","pendingRollover":false,"pluginAlreadyExact":true,"skipPlugin":false,"installPlugin":false,"rolloverPlugin":false}
```

## Exact same-source CI

Candidate SHA: `83e8452de116bf6204be884e4cddf9f3b92b90da`.

| Workflow | Run ID | Result |
|---|---:|---|
| Validate | `33173131342` | `completed / success` |
| Windows Installer Pack Smoke | `33173131369` | `completed / success` |
| PS5.1 Acceptance Smoke | `33173131410` | `completed / success` |

All Validate matrix jobs, package dry-run, Windows npm-pack, and PS5.1 serializer jobs were completed successfully. The CI watcher used completion-only polling; no substring `watch_patterns` were used.

## New package proof

- Artifact ID: `9686448746`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-83e8452de116bf6204be884e4cddf9f3b92b90da`
- Outer artifact ZIP SHA256: `8706b146b021832c8b167c82dd27f145ad52c2735980f6f0eb39f03d379ce053`
- Inner v0.9.3 ZIP SHA256: `dfcff2d27a1fe0bcac7417f609afa3e5e3254588f0ce1fe22d274c1410ab6349`
- tar.gz SHA256: `9746eb6f9b61f9dd99b7e6e1eb9d2ecad2f49619f7cdacff964bd51257617ceb`
- Source commit in `PACKAGE_IDENTITY.json`: `83e8452de116bf6204be884e4cddf9f3b92b90da`
- Package version: `0.9.3`
- Payload count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- `PAYLOAD_IDENTITY.json` and `SHA256SUMS.txt` agree with the package identity and archive hashes.

Packaged-source proof retained the Task-113 conflicting-product-evidence rejection, Task-112 active-wrapper proof, Task-110 retired-tree exactness, local archive install boundary, and recovery harness identity.

## Stop gate

Task 114 proves the complete direct matrix and exact source/package CI evidence. It does not authorize live Windows acceptance or adoption of historical Task-107 residue. Stop for independent ChatGPT review; do not create or execute a live-Windows task.
