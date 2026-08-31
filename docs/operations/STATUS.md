# Current Project Status

**Updated:** 2026-08-31  
**Release line:** v0.9.3  
**Current branch:** `agent/v0.9.3-full-stabilization`  
**Frozen accepted product candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`  
**Validated OpenClaw:** `2026.7.1-2 (0790d9f)`  
**Managed provider:** **Ollama only**  
**Latest published release:** v0.9.2  
**Task-187 disposition in progress:** `BLOCKED — fingerprint-sensitive documentation convergence requires a new candidate/requalification`

## What is already accepted

The exact frozen candidate completed the bounded real-Windows acceptance sequence:

- Task 182 — install-over/provenance reacceptance;
- Task 183 — reset/fresh-state reacceptance;
- Task 184 — uninstall/external-preservation acceptance;
- Task 185 — fresh reinstall/post-install acceptance;
- Task 186 — final Dashboard semantic/durable-delivery acceptance.

Task 186 proved one human Send produced exactly one Ticket, one session/run, one Ollama model call, one durable assistant delivery, and one logical Dashboard assistant result, with no retry/recovery/duplicate semantic work/outbox residue.

## Why publication is blocked

Task 187 audited release/current documentation before merge/tag/publication and proved that some stale current guidance is part of the accepted installed/payload surface:

1. `plugins/cogentnexus-openclaw/README.md` is listed in `plugins/cogentnexus-openclaw/package.json.files`; payload-v2 fingerprinting hashes `package.json` plus every declared package file. Editing the README therefore changes the accepted plugin fingerprint `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`.
2. `skills/cogentnexus-openclaw/SKILL.md` and its references are copied wholesale by the installer into the live workspace skill tree. Current wording still contains pre-acceptance status; `references/architecture.md` also labels the architecture as current v0.9.1.
3. Correcting those files is required for full living-documentation convergence, but the corrected artifact would no longer be the exact artifact accepted by Tasks 182–186.

The Task-187 hard fence therefore forbids continuing to merge/tag/release while pretending the previous Windows acceptance applies unchanged.

## Safe documentation convergence

Repository documentation outside the installed/product payload may be updated to describe the true current state. Those changes must remain documentation-only and must not modify production/runtime/plugin executable source, tests, dependencies, or workflow behavior.

Historical release notes, completed coordination reports, and old accepted evidence remain historical and are not rewritten.

## Release topology

- default branch: `main`;
- current `main` opening HEAD for Task 187: `874dd8f8ce9c1ca5595b29207281430a86c074de`;
- `v0.9.3` tag/release did not exist at Task-187 inspection;
- PR #24 is an older Draft from `agent/v0.9.3-recovery-reality-tests` to `release/v0.9.2` and is not the current release path;
- `.github/workflows/release.yml` remains the required exact-SHA publication gate once a corrected candidate is requalified.

## Next priority

Open a narrowly scoped documentation-payload repair/requalification task:

1. correct stale plugin/skill current guidance only;
2. prove executable/runtime/plugin executable bytes remain unchanged from the accepted product candidate;
3. compute the new plugin fingerprint and skill-tree identity;
4. rerun exact-candidate repository/package validation;
5. perform the minimum Windows requalification justified by the changed surface, including install-over/provenance and final semantic/durable-delivery validation when the installed instruction surface changed;
6. after acceptance, create the correct current PR to `main`, merge only on green gates, freeze exact merged SHA, and dispatch Release workflow with `version=0.9.3` + that exact SHA.

## Safety boundary

Do not force push. Do not publish v0.9.3 from the Task-187 branch after a material payload/product identity change unless the corrected candidate receives the required requalification. Do not repeat reset/uninstall/fresh-reinstall/semantic side effects merely because documentation work is blocked; requalification scope must be proportional to the actual changed artifact surface.
