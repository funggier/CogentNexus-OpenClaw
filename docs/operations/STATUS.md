# Current Project Status

**Updated:** 2026-09-27
**Active task:** `CNX-20260927-456-v0.9.9-release.md`
**Working branch:** `cnx-456-v0.9.9-release`
**GitHub issue:** `#48`
**Current classification:** `CNX456_V0_9_9_RELEASE_QUALIFICATION_ACTIVE`

## Current position

CogentNexus-OpenClaw v0.9.9 is the current source/release line. Publication is exact-SHA gated. v0.9.8 remains the immutable published predecessor.

**Target release:** v0.9.9
**Validated OpenClaw runtime:** `2026.9.6`
**Regression/dev OpenClaw pin:** `2026.7.1-2`
**Managed provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through
**License:** MIT

## Accepted predecessor evidence

CNX-455 physically qualified OpenClaw 2026.9.6 with CogentNexus-OpenClaw MANAGED at generation 54, default `ollama/qwen3.8:27b`, context `24576`, six-hour keep-alive, and GPT-6 Astra/Sol/Luna no-fallback PASS.

The 2026.9.6 Gateway restart compatibility repair uses a bounded 180-second restart command budget after a measured qualifying restart of `128801 ms`, while preserving transactional fail-closed rollback.

## CNX-456 release gates

- version/package/manifest/lock/doc convergence;
- deterministic `cogentnexus-openclaw-v0.9.9-document.zip` asset;
- SHA256/package provenance coverage for all three archives;
- source/plugin/package test suites;
- Windows package/install-over/reset qualification;
- exact-SHA CI workflows;
- physical post-install MANAGED runtime verification;
- exact GitHub Release/tag publication;
- downloaded public asset SHA-256 verification;
- post-release documentation/coordination closeout.

Historical v0.9.6/v0.9.7/v0.9.8 release evidence and OpenClaw 2026.9.5-specific compatibility comments remain immutable historical records.
