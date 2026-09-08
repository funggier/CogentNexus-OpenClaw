# CNX-20260901-221 — Task-220 Exact First-Checkout Control Adjudication

Date: 2026-09-01 ICT  
Parent: `CNX-20260901-220`  
Execution mode: `TASK221_EXACT_FIRST_CHECKOUT_CONTROL_ADJUDICATION`  
Executor: Hermes / authenticated Windows repository operator  
Coordinator / final reviewer: ChatGPT

## Final disposition

`PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN`

This is diagnostic closure only. It does not authorize installer execution, lifecycle mutation, or Discord traffic.

## Fresh authority

```text
Fresh authority branch before execution:
3f51f2c77311ca7828125647da3f4be037ee8e4e

Task ID:
CNX-20260901-221

Status:
READY_FOR_HERMES

Target commit under control:
4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0
```

Public `v0.9.3` remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

## Git version and policy

The disposable controls used the installed Windows Git. The inherited policy was:

```text
origin: file:C:/Program Files/Git/etc/gitconfig
core.autocrlf=true
```

No live or repository source configuration was changed by Task 221.

## Repository-object baseline

For target `4e31dbd…`, the exact repository object sizes were:

```text
plugins/cogentnexus-openclaw/package.json
object: 383d2c30dfc603b66140f177ee4e37ccadb6f422
size: 1051 bytes

plugins/cogentnexus-openclaw/README.md
object: eabd610eb876ef9bb165e0af9c02de474e711fb8
size: 4022 bytes

plugins/cogentnexus-openclaw/openclaw.plugin.json
object: fa2b8322bd08f0d6f684e15113530ff2bc0b6e7a
size: 8162 bytes

plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs
object: 7b7b067a11ba3a21d222355aa2d864e43fe7d2df
size: 4269 bytes

.gitattributes
object: 8fd0a11f8c001fc493fa7e4dfde1eb68e55d0d53
size: 240 bytes
```

The target repository objects are the LF-only baseline. The static payload blobs did not change between `4e31dbd…` and the later `b081d55…` experiment; only `.gitattributes` changed between those commits.

## Exact first-materialization controls

Each control used an independent disposable repository with no working tree populated before target selection:

```text
git clone --no-tags --no-checkout https://github.com/funggier/CogentNexus-OpenClaw.git <dir>
[set local core.autocrlf for C2/C3]
git checkout --detach 4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0
```

### C1 — inherited/default

```text
core.autocrlf=true
```

All four static paths were LF-only immediately after first materialization, with clean status:

```text
package.json:              CRLF=0, LF-only=36, status clean
aREADME.md:                CRLF=0, LF-only=66, status clean
openclaw.plugin.json:      CRLF=0, LF-only=68, status clean
bootstrap-ticket-db.mjs:   CRLF=0, LF-only=106, status clean
```

(`README.md` is named `README.md` in the path above; no file was renamed.)

`git ls-files --eol` reported `i/lf w/lf attr/text eol=lf` for all four paths.

### C2 — explicit true

```text
core.autocrlf=true
```

C2 matched C1 exactly: all four paths were LF-only, target HEAD was `4e31dbd…`, and status was clean immediately after first materialization.

### C3 — explicit false

```text
core.autocrlf=false
```

C3 also produced LF-only bytes for all four paths, target HEAD was `4e31dbd…`, and status was clean immediately after first materialization.

### First-materialization result

The direct first-materialization controls did **not** reproduce the CRLF result previously observed in the two-stage topology. In particular, inherited `core.autocrlf=true` alone was insufficient to produce CRLF when the target commit was selected before any working-tree materialization.

## D — two-stage reproduction

The two-stage control used:

```text
git clone --no-tags https://github.com/funggier/CogentNexus-OpenClaw.git <dir>
git checkout --detach 4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0
```

The initial clone materialized the current branch state before switching to the older target. Immediately after the subsequent target checkout, the result was:

```text
package.json:              CRLF=0, LF-only=36, status clean
README.md:                 CRLF=66, LF-only=0, status clean
openclaw.plugin.json:      CRLF=68, LF-only=0, status clean
bootstrap-ticket-db.mjs:   CRLF=106, LF-only=0, status clean
```

`git ls-files --eol` reported `i/lf w/crlf attr/text eol=lf` for the three affected paths and `i/lf w/lf` for `package.json`.

## Exact boundary and classification

The first materialization controls C1/C2/C3 prove that exact target-first checkout yields LF-only bytes, including under inherited `core.autocrlf=true`.

The two-stage D control proves that cloning/materializing a newer branch state before detaching to `4e31dbd…` carries an attribute/index/worktree state that produces CRLF for the three static paths during the target switch.

Therefore the refined root cause is:

```text
Two-stage checkout / attribute-state carry-over before switching to the older target commit,
under the Windows Git environment, introduces the static CRLF working-tree bytes.
```

Primary classification:

```text
PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN
```

This supersedes the less precise direct-`core.autocrlf` hypothesis from Task 220. `core.autocrlf=true` is part of the environment, but it does not explain C1/C2; the materialization topology is necessary for the observed divergence.

## Mutation ledger

Task 221 was diagnostic-only:

```text
product/source/test/workflow edits: 0
repository product commits: 0
installer/install-over: 0
cnxclaw lifecycle actions: 0
live plugin/config mutation: 0
Gateway restart: 0
live SQLite/ownership/transaction mutation: 0
provider/model substitution: 0
Discord Sends/API traffic: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
isolated clone/control work: yes
```

All evidence was collected under disposable temporary roots. No npm command was required for the primary classification, and no live product state was touched.

## Decision

`PASS_TWO_STAGE_ATTRIBUTE_CARRYOVER_ROOT_CAUSE_PROVEN`

Diagnostic closure only. A later repair task must choose a deterministic checkout/build strategy that avoids two-stage carry-over or otherwise establishes exact static payload bytes, then rerun package proof and fresh Windows identity verification. Installer requalification remains unauthorized.
