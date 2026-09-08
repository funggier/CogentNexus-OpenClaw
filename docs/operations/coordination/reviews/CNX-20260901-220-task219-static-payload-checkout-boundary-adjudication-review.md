# Independent Review — CNX-20260901-220 Static Payload Checkout-Boundary Adjudication

## Verdict

`ACCEPT_PARTIAL__STATIC_DIVERGENCE_PRE_NPM_PROVEN__EXACT_FIRST_CHECKOUT_CONTROL_REQUIRED`

Task 220 materially narrows the remaining package-identity mismatch: the three static payload files are already CRLF at the first measured working-tree checkpoint and remain byte-stable through `npm ci`, `npm run build`, and `npm run plugin:validate`. The repository objects at `4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0` are LF-only. Therefore npm/build/validation are not the first source of the remaining static divergence.

The report's stronger disposition `PASS_CHECKOUT_CONFIG_ROOT_CAUSE_PROVEN` is not yet accepted as final root-cause closure because the checkout experiment is two-stage:

```text
git clone <branch HEAD>
git checkout --detach 4e31dbd...
```

At the time of Task 220, branch ancestry already contained `b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5`, whose `.gitattributes` marks the four static package paths `-text`. The only committed difference from `4e31dbd...` to `b081d55...` is `.gitattributes`; the static payload files themselves are unchanged. A checkout from a later attributes state to an earlier attributes state can preserve existing working-tree bytes for unchanged blobs unless the files are explicitly rematerialized. Task 220 therefore does not yet distinguish:

1. direct materialization of exact `4e31dbd...` under `core.autocrlf=true`; from
2. carry-over of working-tree bytes produced by a prior checkout/attribute state.

This ambiguity is especially important because Task 220 simultaneously reports `git check-attr` at `4e31dbd...` as `text eol=lf` while `git ls-files --eol` reports `w/crlf` for three paths. That is a real observation, but not by itself proof that `core.autocrlf=true` overrides an exact first checkout with `eol=lf`.

## Accepted facts

- repository object bytes for `README.md`, `openclaw.plugin.json`, `scripts/bootstrap-ticket-db.mjs`, and `package.json` at `4e31dbd...` are LF-only;
- Task-220 D0 already contained CRLF in the first three files and LF in `package.json`;
- D1/D2/D3 after npm/build/validation did not change those bytes;
- `core.autocrlf=false` control yielded LF-only working-tree bytes;
- the later `-text` experiment is not an accepted deterministic-package repair;
- generated `dist` determinism remains separately solved by the Task-219 bounded canonicalizer lineage;
- no live runtime/install/Discord mutation occurred.

## Required successor

Open a diagnostic-only Task 221 that makes the exact target commit the **first-ever working-tree materialization**.

Use a no-checkout topology such as:

```text
git clone --no-checkout ...
# or git init + remote + fetch exact SHA
set local core.autocrlf control
checkout/materialize exact 4e31dbd... once
```

Required controls:

- first materialization of exact `4e31dbd...` with inherited/default `core.autocrlf=true`;
- first materialization with explicit local `core.autocrlf=true`;
- first materialization with explicit local `core.autocrlf=false`;
- capture `git config --show-origin --get-regexp core\.(autocrlf|eol|safecrlf)`, `git check-attr -a`, `git ls-files --eol`, exact object/worktree hashes and CRLF/LF counts, and status immediately after materialization;
- separate two-stage reproduction `branch HEAD -> 4e31dbd...` for comparison;
- if two-stage and first-materialization differ, test an explicit forced rematerialization (`git checkout-index -f`, equivalent safe index/worktree refresh, or a new no-checkout worktree) without editing source;
- no product/source fix during Task 221.

Only after this closes should a repair choose between repository attribute/blob normalization, build/package staging canonicalization, or execution-environment checkout policy.

## Runtime boundary

No installer, lifecycle command, live plugin/config mutation, Gateway restart, SQLite write, provider/model change, Discord traffic, Release/tag mutation, history rewrite, or product source edit is authorized.

## Disposition

`ACCEPT_PARTIAL__STATIC_DIVERGENCE_PRE_NPM_PROVEN__EXACT_FIRST_CHECKOUT_CONTROL_REQUIRED`
