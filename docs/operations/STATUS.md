# Current Project Status

**Updated:** 2026-08-24  
**Development line:** v0.9.3 implementation and v1.0.0 acceptance preparation  
**Release target:** v1.0.0 after complete real-Windows lifecycle acceptance  
**Active PR:** #24 — `v0.9.3: Ollama-only recovery reality and provider simplification`  
**Branch:** `agent/v0.9.3-recovery-reality-tests`  
**Status:** Task 042 implementing CogentNexus-OpenClaw v0.9.3 namespace isolation and release metadata; PR remains Draft

## Current priority

The operator accepted Task 041 bounded non-recurrence evidence without claiming a root cause and redirected implementation to prevent collisions with the future CogentNexus-HermesAgent product.

Task `CNX-20260824-042` sets `VERSION` to `0.9.3`, adds v0.9.3 release notes describing the explicit naming contract, and changes every current operational namespace from generic CogentNexus-OpenClaw/CNX surfaces to explicit CogentNexus-OpenClaw surfaces.

The required Windows launcher is `cnxclaw.cmd`; the skill, plugin, state root, package/tool identifiers, tasks/services, logs/backups, migration, reset, uninstall, documentation, tests, and release packages must be isolated accordingly.

Fresh install must create only the new namespace. Installation over the legacy generic deployment must migrate transactionally, use the old launcher only for the pre-mutation PASSTHROUGH handoff, and leave no permanent generic alias.

Reset and uninstall must be bounded by a product ownership manifest and must preserve future CogentNexus-HermesAgent state byte-for-byte.

## Task 041 retained evidence

The authorized exact Task 027 restore and 600-second Procmon trace completed safely. No destructive post-restore event was observed and the bounded poststate was fully materialized. No actor was attributed. Do not repeat Task 041 or discard its retained artifacts.

## Safety

Task 042 is repository-only. It must not perform a live install, runtime action, reset, uninstall, worktree cleanup, Procmon action, merge, tag, or release.
