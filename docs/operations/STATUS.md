# Current Project Status

**Updated:** 2026-09-25
**Active task:** CNX-447 — v0.9.8 release preparation and publication
**Current source line:** v0.9.8 (release candidate; not yet published)
**Latest published release:** v0.9.7
**Accepted release/tag SHA:** `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`
**Release workflow:** `35948011186` — SUCCESS
**Latest physical OpenClaw acceptance:** `2026.9.5 (ec9c1a1)`
**Regression/dev OpenClaw pin:** `2026.7.1-2`
**Managed provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through
**License:** MIT

## Current accepted runtime position

CNX-446 is COMPLETE/GREEN and supplies the accepted v0.9.8 production behavior before release metadata. Production-code authority `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec` passed exact-SHA GitHub CI, real Windows install-over, installed/source parity, Gateway/runtime/supervisor checks, fresh Codex progress -> tool -> terminal acceptance, and native Ollama control acceptance.

CNX-447 is now preparing the exact v0.9.8 release candidate. v0.9.7 remains the latest published accepted release and its release proof below is immutable historical evidence.

The final physical Ticket was `CNXT-52baf1dc-c5b9-4971-b8d0-db0f6d27abde`. Its active Direct model call and exact canonical inference attempt were both closed with `host-gateway-interruption-authorized`; one recovery ran with `attempt_count=1`; one result was delivered; and the dedicated transcript contained exactly one assistant result with no native OpenClaw restart duplicate.

The accepted route remained `ollama/qwen3.8:27b`. Provider/model/auth routing remains OpenClaw-owned.

## Release proof

- tag: `v0.9.7`;
- exact SHA: `43f970895e3b6fe5de6d2f11ffe6bf544fcd2026`;
- Validate: `35944572696` — SUCCESS;
- PS5.1 Acceptance Smoke: `35944572682` — SUCCESS;
- Windows Installer Pack Smoke: `35944572655` — SUCCESS;
- Release: `35948011186` — SUCCESS;
- release state: public, non-draft, non-prerelease;
- ZIP SHA-256: `190b1224fc23f45a662e6e66d15a4e651313e13ee2782ccc2ad8df48674bee12`;
- TAR.GZ SHA-256: `6af5d0d23606ebd2bfe5f2974d0c237c001fd5e6ec8e0f6867ba24068c65c9bf`;
- checksum file SHA-256: `4e9fdda8c43373366cf3ba18704a8fe0831f77412c1819185407af29771b5485`;
- independent downloaded-asset verification: PASS.

## Coordination model

The retired one-minute Codex `legacy coordination watch` automation remains retired. Do not recreate it.

Current durable authority is the published release/tag plus the coordination final report. Historical tasks/reports/reviews remain evidence for the states they recorded.

## Known boundaries still outside full production proof

- long high-concurrency soak;
- disk-full / DB-corruption hardening;
- universal exactly-once external side effects;
- arbitrary future OpenClaw versions beyond explicitly tested evidence.
