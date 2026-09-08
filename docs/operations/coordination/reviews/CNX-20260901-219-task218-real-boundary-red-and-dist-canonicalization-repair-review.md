# Independent Review — CNX-20260901-219 Real-Boundary RED and Dist Canonicalization Repair

## Verdict

`ACCEPT_FAIL_CROSS_PLATFORM_DETERMINISM__DIST_REPAIR_PROVEN__STATIC_CHECKOUT_BOUNDARY_ADJUDICATION_REQUIRED`

Task 219 is not accepted as PASS and does not authorize installation. It does, however, close the generated-`dist` part of the problem with materially stronger evidence than Task 218.

## Accepted positive evidence

Task 219 established a genuine pre-fix RED at the real plugin build boundary:

```text
LF dist files: 188
CRLF dist files: 188
differing generated files: 43
```

The failure was generated-byte inequality rather than a harness/module/dependency failure.

The bounded GREEN commit `9af329b4de7c02fda35b467d84e76bb0f0bb0944` is independently consistent with the required generated-output boundary:

- normal `build` invokes a post-emit `dist` canonicalizer;
- traversal is sorted;
- the root and descended directories are inspected with `lstat`;
- symbolic-link entries and unsupported filesystem entries are rejected;
- only generated JS/MJS/CJS/DTS/JS-map artifacts are accepted;
- CRLF is converted to LF without changing the payload fingerprint algorithm.

Task-219 evidence further reports zero remaining `dist` differences in the Windows-vs-CI comparison after this repair, focused GREEN PASS, full plugin tests/evaluation/validation PASS, and idempotent second-pass behavior.

## Remaining failure

The package as a whole is still not cross-platform deterministic. For exact candidate `4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0`, authoritative CI package proof recorded:

```text
payload files: 192
CI fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
```

while the fresh Windows preparation recorded:

```text
Windows fingerprint: 4ed5231ce6c2718fad2fed0dcf6cbe104ae856ecc60513904c7e45f29725f9f4
dist differences: 0
static differences: 3
```

The remaining paths were:

- `plugins/cogentnexus-openclaw/README.md`;
- `plugins/cogentnexus-openclaw/openclaw.plugin.json`;
- `plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs`.

Task 219 reports CRLF Windows working-tree bytes versus LF CI package bytes for those three files and a dirty Windows worktree.

## Independent contradiction requiring investigation

The static-byte failure should not be repaired by another guessed `.gitattributes` change yet.

At `4e31dbd...`, the repository contains `.gitattributes` entries declaring the four static package files `text eol=lf`. Independent GitHub blob reads for the reported three differing files expose LF-form content at the repository-object boundary. Nevertheless, Task 219 reports CRLF working-tree bytes after fresh Windows preparation.

This means the unresolved question is now **where the bytes change** between Git object storage and final package preparation. The report does not establish whether the conversion happens during initial checkout/worktree materialization, a later Git operation, `npm ci`, the build path, validation, or an evidence-side operation.

The subsequent `-text` experiment at `b081d55...` does not close that question and is not accepted as a fix.

## Required successor

Open Task 220 as a diagnostic/read-only checkout-boundary adjudication before any further production/build repair.

Task 220 must trace the three static paths through these exact boundaries on Windows:

1. Git object bytes via `git cat-file` / object SHA;
2. effective attributes via `git check-attr`;
3. effective Git configuration and origin (`core.autocrlf`, `core.eol`, `core.safecrlf`, attributes files);
4. fresh isolated checkout bytes immediately after checkout, before npm/build commands;
5. bytes and `git status` after `npm ci`;
6. bytes and `git status` after `npm run build`;
7. bytes and `git status` after `npm run plugin:validate`;
8. `git ls-files --eol` at every relevant checkpoint;
9. package fingerprint and per-file SHA after each checkpoint where useful.

Use exact candidate `4e31dbd...` because it has a retained authoritative CI package proof and the `text eol=lf` experiment. Use `b081d55...` only as a diagnostic comparison for the later `-text` attempt.

The task may use isolated clones/worktrees and disposable indexes, including `git add --renormalize` as a diagnostic inside a disposable clone, but must not push source changes or mutate the live product.

## Runtime boundary

No installer, lifecycle command, live plugin/config mutation, Gateway restart, live SQLite mutation, provider/model substitution, Discord traffic, Release/tag/asset mutation, force push, or process workaround is authorized.

## Disposition

`ACCEPT_FAIL_CROSS_PLATFORM_DETERMINISM__DIST_REPAIR_PROVEN__STATIC_CHECKOUT_BOUNDARY_ADJUDICATION_REQUIRED`
