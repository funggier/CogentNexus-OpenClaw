# Current Project Status

**Updated:** 2026-08-28  
**Development line:** v0.9.3 repository stabilization and v1.0.0 acceptance preparation  
**Release target:** v1.0.0 only after exact-candidate freeze, bounded real-Windows lifecycle acceptance, and explicit human release review  
**Current stabilization branch:** `agent/v0.9.3-full-stabilization`  
**Existing Draft PR:** #24 — `v0.9.3: Ollama-only recovery reality and provider simplification` remains open on the older `agent/v0.9.3-recovery-reality-tests` branch; it is not the current stabilization branch  
**Status:** Phase I — Living Documentation Cleanup

## Accepted repository boundary

- v0.9.2 remains the frozen historical Golden Baseline.
- v0.9.3 is the current development candidate.
- The validated OpenClaw compatibility baseline is `2026.7.1-2`.
- The v0.9.3 managed provider surface is **Ollama only**.
- Repository stabilization phases A through H have completed their current evidence gates.
- The latest full pre-Phase-I validation evidence is GitHub Actions Validate run `33124732652` (run 2508), which completed successfully on commit `1111aa34e2f4d2ea5d27573c6ed080016feb1ae7` across Ubuntu, macOS, and Windows Python 3.11/3.14 plus the package dry-run.
- Release publication is no longer reachable from an ordinary branch/tag push. The publication workflow requires an explicit manual dispatch with exact requested version and candidate SHA; no v0.9.3 publication has been dispatched.

## Current priority

Phase I keeps living documentation aligned with the current repository state while preserving historical evidence unchanged. The immediate work is:

1. keep `STATUS.md`, `ROADMAP.md`, and `DECISIONS.md` current;
2. keep clean-reinstall documentation aligned with the implementation-owned external backup boundary;
3. programmatically verify current user-facing `cnxclaw.cmd` command examples against the v0.9.3 facade and delegated Host command surface.

After Phase I, continue with:

- Phase J — security and repository hygiene sweep;
- Phase K — final repository audit, exact candidate identity/provenance verification, and candidate freeze;
- only then, a separately bounded real-Windows lifecycle/semantic acceptance task.

## Safety boundary

Repository stabilization remains non-live. Until Phase K freezes the exact candidate, do **not** perform live install, install-over, reset, uninstall, Gateway/Ollama/Supervisor restart, live SQLite/config/session mutation, or Dashboard semantic acceptance work.

Do not merge, tag, or publish a release from the stabilization loop. Release publication remains a separate explicit human-controlled action.
