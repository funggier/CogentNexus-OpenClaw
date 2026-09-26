# Current Project Status

**Updated:** 2026-09-26
**Active task:** CNX-453 — scheduled supervisor Direct-lease fence and Gateway recovery settlement
**Working branch:** `cnx-453-supervisor-direct-lease-fence`
**Task baseline:** `09eec4113b371d39334d90a332fa9a6455530db0` (CNX-451 candidate)
**GitHub issue:** `#45`
**Current classification:** `CNX453_LOCAL_GREEN_CI_PENDING`

## Active development position

CNX-451 soft-context-pressure repair is code/CI/install green but live acceptance is blocked by CNX-453. During a dedicated Ollama `qwen3.8:27b` live run, the scheduled Host stopped an unresponsive Gateway while the Direct model-call lease was still unexpired. Startup reconciliation restored the Gateway and generated an authorized recovery continuation without user resend, but the interrupted original model-call and canonical inference-attempt rows remained stale `active`. CNX-453 owns the destructive-restart lease fence and recovery-settlement repair.

**Current source/release line:** v0.9.8 (published accepted baseline)
**Latest published release:** v0.9.8
**Accepted release/tag SHA:** `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`
**Release workflow:** `36159455993` — SUCCESS
**Latest physical OpenClaw acceptance:** `2026.9.5 (ec9c1a1)`
**Regression/dev OpenClaw pin:** `2026.7.1-2`
**Managed provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through
**License:** MIT

## Current accepted runtime position

CNX-446 is COMPLETE/GREEN and supplies the accepted v0.9.8 production behavior before release metadata. Production-code authority `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec` passed exact-SHA GitHub CI, real Windows install-over, installed/source parity, Gateway/runtime/supervisor checks, fresh Codex progress -> tool -> terminal acceptance, and native Ollama control acceptance.

CNX-447 has published the exact v0.9.8 candidate `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`. Exact-SHA CI, real v0.9.7 -> v0.9.8 install-over, source/installed payload parity, fresh Codex progress -> tool -> terminal acceptance, Release workflow publication, and independent public asset verification are GREEN. v0.9.7 remains immutable historical evidence.

The final physical Ticket was `CNXT-52baf1dc-c5b9-4971-b8d0-db0f6d27abde`. Its active Direct model call and exact canonical inference attempt were both closed with `host-gateway-interruption-authorized`; one recovery ran with `attempt_count=1`; one result was delivered; and the dedicated transcript contained exactly one assistant result with no native OpenClaw restart duplicate.

The accepted route remained `ollama/qwen3.8:27b`. Provider/model/auth routing remains OpenClaw-owned.

## Release proof

- tag: `v0.9.8`;
- exact SHA: `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`;
- Validate: `36144053827` — SUCCESS;
- PS5.1 Acceptance Smoke: `36144053553` — SUCCESS;
- Windows Installer Pack Smoke: `36144053896` — SUCCESS;
- Release: `36159455993` — SUCCESS;
- release state: public, non-draft, non-prerelease;
- ZIP SHA-256: `2c9f9214feb7d90b9a1b3d89c71a4dcd4ecacfa425618baaeb8e8d97a2a1e4f3`;
- TAR.GZ SHA-256: `de2b4dcee696ca48cf9521e6844a350cd79f4f2336499bd5fc64c6fc0a551143`;
- checksum file SHA-256: `8693865c7d0feb91628e71c9e808392cb84dc65f662b6340f37a70ef7bcc0c61`;
- independent downloaded-asset verification: PASS.

## Coordination model

The retired one-minute Codex `legacy coordination watch` automation remains retired. Do not recreate it.

Current durable authority is the published release/tag plus the coordination final report. Historical tasks/reports/reviews remain evidence for the states they recorded.

## Known boundaries still outside full production proof

- long high-concurrency soak;
- disk-full / DB-corruption hardening;
- universal exactly-once external side effects;
- arbitrary future OpenClaw versions beyond explicitly tested evidence.