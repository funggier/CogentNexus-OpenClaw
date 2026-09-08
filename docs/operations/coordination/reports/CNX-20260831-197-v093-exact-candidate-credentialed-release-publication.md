# CNX-20260831-197 — v0.9.3 Exact-Candidate Credentialed Release Publication

- Date: 2026-08-31 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Executor: Hermes
- Coordinator / final reviewer: ChatGPT
- Parent: `CNX-20260831-188`
- Predecessor: `CNX-20260831-196`
- Final disposition: `PASS`

## Result

v0.9.3 was published successfully using exactly one authenticated Release creation attempt. The already-validated Actions artifact was used without rebuild or modification. The resulting tag and Release target the frozen candidate exactly, and all three public assets independently match the pre-publication artifact and published checksum file.

## Locked identities

- Repaired workflow execution `main` SHA:
  `c70552801ddbb9dc0a49c9cfc64368b9f4820f07`
- Frozen v0.9.3 release target:
  `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Validated workflow run: `33406148890`
- Workflow URL: https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33406148890
- Validated Actions artifact ID: `9763253683`
- Artifact name: `release-assets-0.9.3-26ce64a624255278a3a0266ad38746e0e6ed2e31`
- GitHub artifact digest:
  `sha256:5ca5bf8579754888c355c0976a86fd03c3c79eeed2ecd52293a0d6e5fa24b65d`

The artifact came from the successful `package` job of run `33406148890`; no workflow redispatch or archive rebuild was performed.

## Pre-publication authority and credential gate

Fresh checks before the single publication attempt showed:

- `main = c70552801ddbb9dc0a49c9cfc64368b9f4820f07`;
- tag `v0.9.3` absent;
- Release `v0.9.3` absent;
- validated run and artifact present;
- no other v0.9.3 publication observed;
- authenticated GitHub account: `funggier`;
- authentication scopes visible without exposing credentials: `repo`, `workflow`, `gist`, `read:org`.

No token, password, key, or connection string was recorded in this report.

One initial preflight query requested an unsupported `gh run view --json artifacts` field. The installed `gh` CLI rejected that field before any publication action. This was corrected by using the GitHub REST artifact endpoint and is recorded as a harness/query issue, not as product or publication evidence.

## Artifact download and independent validation

The exact artifact was downloaded from run `33406148890` into an external evidence directory. The release files were not rebuilt or altered.

| File | Pre-publication size | Pre-publication SHA-256 |
|---|---:|---|
| `cogentnexus-openclaw-v0.9.3.tar.gz` | 3,161,708 bytes | `1c452706cf823391243819dbb3bf5c18275ed8351264b99006573da2780011e5` |
| `cogentnexus-openclaw-v0.9.3.zip` | 4,160,823 bytes | `1682a962302b7439002e3f53f652af1ddd325705d5ddbc72cf634a9c7c2ea137` |
| `SHA256SUMS.txt` | 199 bytes | `57b8ef5e17c3d7ec09e91f4f13fec76e25205023306d124cc2dca039abf4f633` |

Published checksum file contents:

```text
1c452706cf823391243819dbb3bf5c18275ed8351264b99006573da2780011e5  cogentnexus-openclaw-v0.9.3.tar.gz
1682a962302b7439002e3f53f652af1ddd325705d5ddbc72cf634a9c7c2ea137  cogentnexus-openclaw-v0.9.3.zip
```

Independent verification before publication:

- tar archive opened and listed successfully: `1290` members;
- zip archive opened and listed successfully: `1290` members;
- both archives contained the expected `skills/cogentnexus-openclaw` payload;
- both computed archive hashes matched `SHA256SUMS.txt`.

## Single authenticated publication action

After a second fresh absence check, exactly one authenticated Release creation command/action was executed with:

- repository: `funggier/CogentNexus-OpenClaw`;
- tag: `v0.9.3`;
- target: `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- title: `CogentNexus-OpenClaw v0.9.3`;
- notes: exact `RELEASE_NOTES.md` from the validated artifact;
- assets: the exact tar.gz, zip, and `SHA256SUMS.txt` files above.

The command returned the Release URL and exit code `0`:

https://github.com/funggier/CogentNexus-OpenClaw/releases/tag/v0.9.3

Publication mutation count: `1 / 1 consumed`.

## Post-publication authority verification

### Tag

Fresh GitHub API readback:

```text
refs/tags/v0.9.3
object type: commit
object SHA: 26ce64a624255278a3a0266ad38746e0e6ed2e31
```

The tag target is exactly the frozen candidate.

### Release metadata

- URL: https://github.com/funggier/CogentNexus-OpenClaw/releases/tag/v0.9.3
- Tag: `v0.9.3`
- Name: `CogentNexus-OpenClaw v0.9.3`
- Target commitish: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Draft: `false`
- Prerelease: `false`
- Published: `2026-08-31T15:24:55Z`

Exactly these three public assets were present:

| Asset | Published size | Public URL |
|---|---:|---|
| `cogentnexus-openclaw-v0.9.3.tar.gz` | 3,161,708 bytes | https://github.com/funggier/CogentNexus-OpenClaw/releases/download/v0.9.3/cogentnexus-openclaw-v0.9.3.tar.gz |
| `cogentnexus-openclaw-v0.9.3.zip` | 4,160,823 bytes | https://github.com/funggier/CogentNexus-OpenClaw/releases/download/v0.9.3/cogentnexus-openclaw-v0.9.3.zip |
| `SHA256SUMS.txt` | 199 bytes | https://github.com/funggier/CogentNexus-OpenClaw/releases/download/v0.9.3/SHA256SUMS.txt |

No duplicate or unexpected v0.9.3 tag/Release was observed.

## Public asset verification

All three public assets were downloaded again from the published Release. The public downloads were byte-identical to the pre-publication files:

| File | Public size | Public SHA-256 | Pre/public bytes equal | Checksum file match |
|---|---:|---|---|---|
| `cogentnexus-openclaw-v0.9.3.tar.gz` | 3,161,708 | `1c452706cf823391243819dbb3bf5c18275ed8351264b99006573da2780011e5` | `true` | `true` |
| `cogentnexus-openclaw-v0.9.3.zip` | 4,160,823 | `1682a962302b7439002e3f53f652af1ddd325705d5ddbc72cf634a9c7c2ea137` | `true` | `true` |
| `SHA256SUMS.txt` | 199 | `57b8ef5e17c3d7ec09e91f4f13fec76e25205023306d124cc2dca039abf4f633` | `true` | not applicable |

The publicly downloaded tar and zip archives opened and listed successfully, each with `1290` members.

## Scope and hard-fence confirmation

The following were not performed under Task 197:

- no workflow redispatch;
- no automatic retry after the Task 196 workflow failure;
- no candidate retarget;
- no archive rebuild or alteration;
- no manual tag creation before Release creation;
- no product/runtime/plugin/installer/provider/package mutation;
- no reset, uninstall, reinstall, or install-over;
- no force push.

Task 198 Discord/session investigation remains queued separately. Task 196's Discord evidence is not reinterpreted by this publication task and no additional Discord send was performed.

## Final disposition

```text
PASS
```

The exact candidate was published once through an authorized credential, the tag target is exact, the Release is public, exactly the required assets are present, and independent public-download checksum/archive verification passed.

Task 197 is complete and stops here for ChatGPT review.
