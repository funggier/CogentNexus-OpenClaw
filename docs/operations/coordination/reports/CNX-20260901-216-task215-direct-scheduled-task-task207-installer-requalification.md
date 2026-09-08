# CNX-20260901-216 — Task-207 Installer Requalification

## Disposition

`BLOCKED_AUTHORITY`

Task 216 stopped before any Scheduled Task registration or installer invocation because the fresh exact candidate checkout did not reproduce the candidate plugin fingerprint required by the live authority.

## Authority

- Task: `CNX-20260901-216`
- Parent: `CNX-20260901-215`
- Candidate commit required: `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`
- Authority candidate fingerprint required: `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`
- Evidence root: `C:/Users/CDQ-P/AppData/Local/Temp/cnx216-task215-installer-requalification-20260901T/`

## Fresh candidate preparation

A new isolated checkout was created and detached at the exact required commit:

```text
HEAD=27fe0181b3b65d555a3b0cc8354f6f7945c21c0b
WORKTREE_CLEAN=true
```

Source hash checks passed:

```text
scripts/install.ps1
8cb713b7ddfe5be113530298fe3195094c0055a78ff63cdb393a483debc47e56

plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts
157460ee24a37472830b30dd19fec06172e3245b0f25447ddc0db1280b43473a
```

The plugin manifest/package layout was present at:

```text
plugins/cogentnexus-openclaw/package.json
```

## Repository validation

The following commands were run in the fresh plugin checkout:

```text
npm ci                         PASS (18s, 352 packages added)
npm run plugin:validate        PASS
```

Validation output included:

```text
CogentNexus-OpenClaw mixed-plugin artifact verification: PASS (45 config properties, 5 tools)
CogentNexus-OpenClaw ticket DB bootstrap: PASS (9 required tables + v095 registration fence)
packedFileCount: 192
```

Observed npm warnings/advisories were retained as environment output: four high-severity audit findings and five blocked install scripts. They were not changed or suppressed.

## Blocking provenance mismatch

The repository-supported fingerprint command was run after validation:

```text
python skills/cogentnexus-openclaw/scripts/namespace_ownership.py \
  plugin-fingerprint \
  --plugin-root plugins/cogentnexus-openclaw \
  --version 0.9.3
```

Observed result:

```text
fingerprint=3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed
```

Required authority result:

```text
d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
```

The fresh source checkout therefore has a material candidate/provenance mismatch. Although source hashes, npm validation, and packed file count passed, the required exact plugin fingerprint did not. Per Task 216 Phase A, this is an authority ambiguity and requires `BLOCKED_AUTHORITY` with no task registration/start.

The earlier accepted artifact fingerprint `d067...` must not be inferred from the newly generated fresh checkout fingerprint `3b86...`; the two values are not interchangeable.

## Live mutation gate

Because Phase A failed, no live preflight mutation or installer task was attempted:

```text
Scheduled Task registration: 0
Scheduled Task start: 0
Installer invocation: 0
Installer retry: 0
Lifecycle workaround: 0
Plugin/OpenClaw mutation: 0
Gateway restart: 0
SQLite write: 0
Provider/model/config mutation: 0
Process termination: 0
Discord traffic: 0
Release/tag/asset mutation: 0
```

The fresh checkout's `npm ci` and validation touched only the isolated candidate tree. No live product path was used.

## Conclusion

Task-207 installer requalification cannot safely proceed until the coordinator resolves why the exact required commit and repository-supported fresh fingerprint produce `3b86...` while the accepted package authority requires `d067...`. No installer, enable, restart, or Discord acceptance was performed.
