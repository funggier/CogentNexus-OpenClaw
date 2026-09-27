# Current Project Status

**Updated:** 2026-09-27
**Active task:** none
**Working branch:** `cnx-455-openclaw-2026.9.6-upgrade`
**Latest completed task:** `CNX-20260927-455-openclaw-2026.9.6-upgrade.md`
**GitHub issue:** `#47`
**Current classification:** `CNX455_OPENCLAW_2026_9_6_UPGRADE_GREEN_WITH_BOUNDED_RESTART_COMPATIBILITY_REPAIR`

## Current accepted position

CogentNexus-OpenClaw v0.9.8 remains the immutable published baseline, now physically qualified on OpenClaw `2026.9.6`.

**Current source/release line:** v0.9.8 (published accepted baseline)
**Latest published release:** v0.9.8
**Accepted release/tag SHA:** `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`
**Release workflow:** `36159455993` — SUCCESS
**Latest physical OpenClaw acceptance:** `2026.9.6`
**Regression/dev OpenClaw pin:** `2026.7.1-2`
**Managed provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through
**License:** MIT

## CNX-455 acceptance

- OpenClaw CLI/Gateway: `2026.9.6`.
- CogentNexus Host: MANAGED / active, generation `54`.
- Provider/model/auth ownership: OpenClaw.
- Default model: `ollama/qwen3.8:27b`.
- Ollama context: `24576`.
- Ollama keep-alive: `6h`, physically active.
- GPT-6 Astra: PASS, no fallback.
- GPT-6 Sol: PASS, no fallback.
- GPT-6 Luna: PASS, no fallback.
- Focused restart-timeout regression: `1 passed`.
- Runtime self-test: PASS.
- Full Python suite: `755 passed, 5 skipped, 38 subtests passed`.
- Final Gateway/CogentNexus/Discord/supervisor health: GREEN.

OpenClaw 2026.9.6 exposed one bounded lifecycle compatibility gap: the native Gateway restart can take longer than the previous 60-second inner subprocess budget. Commit `deec8efbd78c540defa5c1104415454b158af0d4` raises only that restart-command budget to 180 seconds while preserving transactional authority ordering and fail-closed rollback. A qualifying restart completed in `128801 ms`.

## Non-blocking observations

- OpenClaw 2026.9.6 runtime inspector reports `hookNames=[]` while also reporting `hookCount=47` and populated `typedHooks`; physical behavior is GREEN.
- Archive provenance metadata reports `trust.reason=provenance-invalid` for the retained old archive source path, while runtime status is loaded/activated, diagnostics are empty, and dependencies are installed.
- Windows Gateway Scheduled Task may display `Last Result=267009` while Running; the task is Enabled and Gateway connectivity is healthy.

## Release proof retained

- tag: `v0.9.8`;
- exact SHA: `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`;
- Validate: `36144053827` — SUCCESS;
- PS5.1 Acceptance Smoke: `36144053553` — SUCCESS;
- Windows Installer Pack Smoke: `36144053896` — SUCCESS;
- Release: `36159455993` — SUCCESS.

Historical v0.9.6/v0.9.7/v0.9.8 release evidence and OpenClaw 2026.9.5-specific compatibility comments remain immutable historical records.
