# CNX-20260831-197 — v0.9.3 Exact-Candidate Credentialed Release Publication Review

- Date: 2026-08-31 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Reviewed report: `docs/operations/coordination/reports/CNX-20260831-197-v093-exact-candidate-credentialed-release-publication.md`
- Coordinator / final reviewer: ChatGPT
- Final review disposition: `PASS_ACCEPTED`

## Review result

Task 197 is accepted as `PASS`.

Fresh GitHub authority independently confirms:

- tag `v0.9.3` exists;
- `refs/tags/v0.9.3` is a direct commit ref to `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- GitHub Release `v0.9.3` exists and is public (`draft=false`, `prerelease=false`);
- Release `target_commitish` is exactly `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- exactly three release assets are present:
  - `cogentnexus-openclaw-v0.9.3.tar.gz`
  - `cogentnexus-openclaw-v0.9.3.zip`
  - `SHA256SUMS.txt`
- GitHub-reported asset digests equal the Task-197 independently verified values:
  - tar.gz: `1c452706cf823391243819dbb3bf5c18275ed8351264b99006573da2780011e5`
  - zip: `1682a962302b7439002e3f53f652af1ddd325705d5ddbc72cf634a9c7c2ea137`
  - checksum file: `57b8ef5e17c3d7ec09e91f4f13fec76e25205023306d124cc2dca039abf4f633`

Task 197 also records pre-publication and post-publication archive opening/listing and byte/checksum equality against the retained validated Actions artifact from run `33406148890`; no rebuild or candidate retarget occurred.

## Candidate-lineage check

The public release target `26ce64a...` is the frozen publication candidate that was authoritative `main` when Task 194 first dispatched release publication. It descends from the repaired product candidate `050ab53f4b593ab538143084d6bbdbf7e1672e34`.

The compare from `050ab53f...` to `26ce64a...` contains documentation/coordination and workflow-level changes, but no runtime/plugin product-source mutation. Therefore the release-note reference to the Task-191/192 repaired product candidate and the public tag target to the later frozen publication candidate are compatible identities rather than product drift.

## Publication history

- Task 194: package passed; publish failed because `gh release create` ran without repository context.
- Task 195: repaired repository-explicit publish context.
- Task 196: package passed; publish reached GitHub API but failed at the workflow-token authorization boundary.
- Task 197: reused the exact validated artifact and performed one credential-capable publication attempt; publication and independent public-asset verification passed.

No additional release attempt is authorized or required for v0.9.3.

## Next task

Task 198 is now the active work item:

`docs/operations/coordination/tasks/CNX-20260831-198-discord-session-correlation-and-durable-delivery-investigation.md`

The Discord/session evidence from Task 196 remains a separate runtime defect investigation and does not invalidate the already published v0.9.3 artifact identity.
