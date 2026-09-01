# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK221_EXACT_FIRST_CHECKOUT_CONTROL_ADJUDICATION`  
**Updated:** 2026-09-01 ICT  
**Transport:** GitHub repository + isolated Windows Git materialization evidence through Hermes  
**Active task:** `CNX-20260901-221`  
**Parent:** `CNX-20260901-220`  
**Repair parent:** `CNX-20260831-198`  
**Parent umbrella:** `CNX-20260831-188`  
**Completed publication:** `CNX-20260831-197`  
**Disposition:** `TASK220_STATIC_PRE_NPM_DIVERGENCE_PROVEN__TASK221_EXACT_FIRST_CHECKOUT_CONTROL_READY`

## Publication authority

Published `v0.9.3` remains untouched at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Accepted generated-output boundary

Task 219 successfully established the genuine RED for generated output and the bounded `dist` canonicalizer lineage. The remaining determinism failure is not in generated `dist`; Task-219 evidence reduced it to three static package files.

## Task 220 reviewed boundary

Task-220 report disposition:

`PASS_CHECKOUT_CONFIG_ROOT_CAUSE_PROVEN`

Independent review accepts only the narrower disposition:

`ACCEPT_PARTIAL__STATIC_DIVERGENCE_PRE_NPM_PROVEN__EXACT_FIRST_CHECKOUT_CONTROL_REQUIRED`

Accepted Task-220 evidence:

- repository object bytes at exact `4e31dbd...` are LF-only;
- three static working-tree files are CRLF at the first measured D0 checkpoint;
- npm/build/plugin validation do not create the divergence;
- an explicit `core.autocrlf=false` control yields LF-only working-tree bytes;
- `-text` does not establish deterministic CI-equivalent bytes.

Remaining ambiguity:

Task 220 cloned current branch HEAD before detaching to `4e31dbd...`. Branch ancestry already contained `b081d55...`, which changes only `.gitattributes` from `text eol=lf` to `-text`; the static blobs are unchanged. The evidence therefore does not yet isolate direct first-checkout behavior from working-tree/attribute-state carry-over.

## Active Task 221

Hermes must execute:

`docs/operations/coordination/tasks/CNX-20260901-221-task220-exact-first-checkout-control-adjudication.md`

Required outcome:

- exact `4e31dbd...` is the first working-tree materialization in independent no-checkout/init+fetch repositories;
- test inherited/default, explicit `core.autocrlf=true`, and explicit `core.autocrlf=false` before first checkout;
- record object/worktree hashes, CRLF/LF counts, effective attributes, `git ls-files --eol`, status, and config origins immediately after checkout;
- separately reproduce Task-220 two-stage topology;
- if needed, test one safe explicit Git rematerialization in the disposable tree;
- identify whether root cause is direct checkout policy, two-stage attribute carry-over, or a mixed materialization effect;
- publish report and stop.

A Task-221 PASS is diagnostic closure only. A separate repair task remains required before installer requalification.

## Runtime / Discord boundary

`0 Discord Sends`.

No installer/install-over, lifecycle action, live OpenClaw plugin/config mutation, Gateway restart, live SQLite/ownership/transaction write, provider/model substitution, product/source/test/workflow edit, Release/tag mutation, or force push is authorized.
