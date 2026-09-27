# Current Project Status

**Updated:** 2026-09-28
**Active task:** none
**Latest completed task:** `CNX-20260927-456-v0.9.9-release.md`
**GitHub issue:** `#48` — completed
**Current classification:** `CNX456_V099_RELEASE_MAIN_CONVERGENCE_GREEN`

## Current accepted position

CogentNexus-OpenClaw v0.9.9 is published, independently verified, physically installed on OpenClaw 2026.9.6, and converged to `main` by fast-forward only. The immutable public tag targets exact release candidate `ea3b454815378dc1d45b2db621662744ddcd9936`.

**Current source/release line:** v0.9.9 (published accepted baseline)
**Latest published release:** v0.9.9
**Accepted release/tag SHA:** `ea3b454815378dc1d45b2db621662744ddcd9936`
**Post-release main convergence SHA:** `bdcf8180204a79aea9dbadc4d436241378612043`
**Release workflow:** `36335012227` — SUCCESS
**Validated OpenClaw runtime:** `2026.9.6`
**Managed Host:** active / MANAGED / generation 56
**Default local model:** `ollama/qwen3.8:27b`
**Local context:** `24576`
**Ollama keep-alive:** `6h`
**Managed provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through
**License:** MIT

## Qualification

- exact-candidate Validate `36333858334`: SUCCESS;
- exact-candidate PS5.1 Acceptance Smoke `36333858304`: SUCCESS;
- exact-candidate Windows Installer Pack Smoke `36333858298`: SUCCESS;
- Release `36335012227`: SUCCESS;
- post-release main Validate `36336713410`: SUCCESS;
- post-release main PS5.1 Acceptance Smoke `36336713372`: SUCCESS;
- post-release main Windows Installer Pack Smoke `36336713419`: SUCCESS;
- local full Python: `764 passed, 5 skipped, 38 subtests passed`;
- local Vitest: `96 files / 448 tests` PASS;
- evaluation: PASS;
- production `npm audit --omit=dev`: 0 vulnerabilities;
- plugin validation: PASS / 300 packed files.

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

Historical v0.9.6/v0.9.7/v0.9.8 tags/releases remain immutable.
