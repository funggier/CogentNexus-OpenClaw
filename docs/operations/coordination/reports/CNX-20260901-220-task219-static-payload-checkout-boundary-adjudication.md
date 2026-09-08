# CNX-20260901-220 — Task-219 Static Payload Checkout-Boundary Adjudication

Date: 2026-09-01 ICT  
Parent: `CNX-20260901-219`  
Execution mode: `TASK220_STATIC_PAYLOAD_CHECKOUT_BOUNDARY_ADJUDICATION`  
Executor: Hermes / authenticated Windows repository operator  
Coordinator / final reviewer: ChatGPT

## Final disposition

`PASS_CHECKOUT_CONFIG_ROOT_CAUSE_PROVEN`

This is diagnostic closure only. It does not authorize installer execution, lifecycle mutation, or Discord traffic.

## Authority

Fresh remote authority before execution:

```text
REMOTE_HEAD=cf798d98f978a2744596b28964483cf1cf31fbbf
Task ID=CNX-20260901-220
Status=READY_FOR_HERMES
```

Primary candidate under adjudication:

```text
4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0
```

Later `-text` experiment:

```text
b081d55c4ffa5fcb03931dc320d39bdcf92a6cf5
```

## Repository-object truth

Exact Git object SHA-1 values at `4e31dbd…`:

```text
plugins/cogentnexus-openclaw/package.json
object: 383d2c30dfc603b66140f177ee4e37ccadb6f422

plugins/cogentnexus-openclaw/README.md
object: eabd610eb876ef9bb165e0af9c02de474e711fb8

plugins/cogentnexus-openclaw/openclaw.plugin.json
object: fa2b8322bd08f0d6f684e15113530ff2bc0b6e7a

plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs
object: 7b7b067a11ba3a21d222355aa2d864e43fe7d2df

.gitattributes
object: 8fd0a11f8c001fc493fa7e4dfde1eb68e55d0d53
```

The repository object bytes for all four static paths are LF-only. The object truth was obtained from Git object identity and byte metrics in the disposable evidence tree; ordinary console rendering was not used as the object-byte authority.

## Default Windows checkout and checkpoint trace

The default fresh checkout used the system Git configuration:

```text
checkout: git clone --no-tags https://github.com/funggier/CogentNexus-OpenClaw.git <evidence>/default
git checkout --detach 4e31dbd79cd4c0a7eb161888c14221f0ae03bcc0
config origin: file:C:/Program Files/Git/etc/gitconfig
core.autocrlf=true
```

D0 immediately after exact checkout, before npm:

| Path | Bytes | CRLF | LF-only | Status |
|---|---:|---:|---:|---|
| `package.json` | 1051 | 0 | 36 | clean |
| `README.md` | 4088 | 66 | 0 | clean |
| `openclaw.plugin.json` | 8230 | 68 | 0 | clean |
| `scripts/bootstrap-ticket-db.mjs` | 4375 | 106 | 0 | clean |

`git ls-files --eol` at D0 reported:

```text
i/lf    w/crlf  attr/text eol=lf      plugins/cogentnexus-openclaw/README.md
i/lf    w/crlf  attr/text eol=lf      plugins/cogentnexus-openclaw/openclaw.plugin.json
i/lf    w/lf    attr/text eol=lf      plugins/cogentnexus-openclaw/package.json
i/lf    w/crlf  attr/text eol=lf      plugins/cogentnexus-openclaw/scripts/bootstrap-ticket-db.mjs
```

D1 after `npm ci --ignore-scripts`, D2 after `npm run build`, and D3 after `npm run plugin:validate` retained the exact same hashes, byte sizes, and newline counts. Status remained clean at each checkpoint. No first divergence occurred after checkout: the static CRLF was already present at D0.

The normal isolated build/validation sequence completed successfully. It did not create the static-byte divergence; it preserved the bytes introduced by checkout.

## Git policy controls

Three immediate-checkout controls were compared:

### Default inherited config

```text
file:C:/Program Files/Git/etc/gitconfig core.autocrlf true
```

Results:

```text
README.md: CRLF=66, LF-only=0
openclaw.plugin.json: CRLF=68, LF-only=0
bootstrap-ticket-db.mjs: CRLF=106, LF-only=0
package.json: CRLF=0, LF-only=36
```

### Explicit `core.autocrlf=false`

```text
file:C:/Program Files/Git/etc/gitconfig core.autocrlf true
file:<clone>/.git/config core.autocrlf false
```

All four static paths were LF-only:

```text
README.md: CRLF=0, LF-only=66
openclaw.plugin.json: CRLF=0, LF-only=68
bootstrap-ticket-db.mjs: CRLF=0, LF-only=106
package.json: CRLF=0, LF-only=36
```

### Explicit `core.autocrlf=true`

```text
file:C:/Program Files/Git/etc/gitconfig core.autocrlf true
file:<clone>/.git/config core.autocrlf true
```

The result matched the default checkout: the same three static files were CRLF and `package.json` remained LF-only.

This isolates the root cause to checkout policy. The repository objects are LF-only, and the first byte transition occurs during checkout under `core.autocrlf=true`.

## Attributes and renormalization interpretation

For `4e31dbd…`, `git check-attr -a` reported `text` and `eol=lf` for all four paths. Nevertheless, with the inherited system `core.autocrlf=true`, the working tree showed `w/crlf` for three files. The control with `core.autocrlf=false` produced LF-only working-tree bytes.

The disposable renormalization diagnostic did not produce a repository fix and was not committed. It was used only to inspect index/object normalization behavior. No Task-220 source/product commit was made.

The later `b081d55…` `-text` experiment produced:

```text
core.autocrlf=true
text: unset for the three paths
working-tree bytes: still CRLF for all three
status: clean because Git treated them as non-text/binary
```

Therefore `-text` suppresses conversion/status detection but does not produce the CI LF bytes or establish payload identity. It is not accepted as the repair.

## Root-cause conclusion

The three remaining static payload differences are introduced at the Windows checkout boundary by the inherited system-level setting:

```text
core.autocrlf=true
origin: C:/Program Files/Git/etc/gitconfig
```

The evidence rules out:

- repository object CRLF;
- `npm ci` as the first mutation;
- `npm run build` as the first mutation;
- `npm run plugin:validate` as the first mutation;
- generated `dist` output as the remaining cause for this task;
- `-text` as a byte-identity repair.

Primary classification:

```text
PASS_CHECKOUT_CONFIG_ROOT_CAUSE_PROVEN
```

## Live preservation and mutation ledger

Task 220 was diagnostic-only:

```text
installer/install-over: 0
cnxclaw lifecycle actions: 0
live plugin/config mutation: 0
Gateway restart: 0
live ownership/staging/transaction/SQLite writes: 0
provider/model substitution: 0
Discord Sends: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
product/source/test/workflow commits: 0
isolated clones/builds: yes
```

No live product state was changed. This report does not authorize installation. A later repair task must choose and prove a deterministic static-payload strategy, then rerun CI and fresh Windows exact fingerprint/byte equality.
