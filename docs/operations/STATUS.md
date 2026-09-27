# Current Project Status

**Updated:** 2026-09-27
**Active task:** `CNX-20260927-456-v0.9.9-release.md`
**Working branch:** `cnx-456-v0.9.9-release`
**GitHub issue:** `#48`
**Current classification:** `CNX456_V099_PUBLISHED_MAIN_CONVERGENCE_PENDING`

## Current accepted position

CogentNexus-OpenClaw v0.9.9 is published, independently verified, and physically installed on OpenClaw 2026.9.6. The immutable public tag targets exact candidate `ea3b454815378dc1d45b2db621662744ddcd9936`.

**Current source/release line:** v0.9.9 (published accepted baseline)
**Latest published release:** v0.9.9
**Accepted release/tag SHA:** `ea3b454815378dc1d45b2db621662744ddcd9936`
**Release workflow:** `36335012227` — SUCCESS
**Validated OpenClaw runtime:** `2026.9.6`
**Managed Host:** active / MANAGED / generation 56
**Default local model:** `ollama/qwen3.8:27b`
**Local context:** `24576`
**Ollama keep-alive:** `6h`
**Managed provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through
**License:** MIT

## Exact-SHA qualification

- Validate `36333858334`: SUCCESS;
- PS5.1 Acceptance Smoke `36333858304`: SUCCESS;
- Windows Installer Pack Smoke `36333858298`: SUCCESS;
- Release `36335012227`: SUCCESS;
- local full Python: `764 passed, 5 skipped, 38 subtests passed`;
- Vitest: 96 files / 448 tests PASS;
- production audit: 0 vulnerabilities.

## Physical install-over

- installer exit 0;
- MANAGED generation `55 -> 56`;
- native OpenClaw restart: `134873 ms`, inside 180-second budget;
- Gateway/OpenClaw 2026.9.6 healthy;
- Ollama healthy;
- skill source/installed parity: 97/97 equal;
- installed plugin package: 300/300 package files equal to source counterparts;
- durable Ticket state preserved; pending outbox 0.

## Published asset hashes

- TAR.GZ: `e93d27a1c180a409a1ecd678482919582336699d0095c624835b69cd1f59966a`;
- ZIP: `1a26d2305cd0ccb65d6688ebfc63535b0419caffa784d67da0f2784d52e40d1d`;
- documentation ZIP: `c0f7ae4a4570026b21dec8c9993e7006d8e2aa54bc2254151d6fa7f26b483c1e`;
- SHA256SUMS: `72abd0a17e4d68458f266e3d84fddf6f40e53df5d861a7241121736c332a9637`.

Independent public downloads match `SHA256SUMS.txt` and GitHub asset digests. Documentation ZIP contains 59 bounded documentation entries and no coordination internals.

## Remaining closeout

Fast-forward `main` to the post-release current-document convergence commit, verify remote main, then mark CNX-456 COMPLETE / coordination IDLE and close Issue #48.

Historical v0.9.6/v0.9.7/v0.9.8 tags/releases remain immutable.
