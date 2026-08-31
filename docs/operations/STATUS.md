# Current Project Status

**Updated:** 2026-08-31  
**Release line:** v0.9.3  
**Current branch:** `agent/v0.9.3-full-stabilization`  
**Previously accepted implementation candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`  
**Validated OpenClaw:** `2026.7.1-2 (0790d9f)`  
**Managed provider:** **Ollama only**  
**Task-188 package payload-v2:** `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / `184` files  
**Task-188 installed skill tree:** `a1e873ba404205507a1623961b49f1b1a0689f9f`  
**Executable scripts tree:** `3d9d323ba19443d46e970b87cef52ce878da274f` — unchanged

## What is already accepted

The exact implementation baseline completed the bounded real-Windows acceptance sequence:

- Task 182 — install-over/provenance reacceptance;
- Task 183 — reset/fresh-state reacceptance;
- Task 184 — uninstall/external-preservation acceptance;
- Task 185 — fresh reinstall/post-install acceptance;
- Task 186 — final Dashboard semantic/durable-delivery acceptance.

Task 186 proved one human Send produced exactly one Ticket, one session/run, one Ollama model call, one durable assistant delivery, and one logical Dashboard assistant result, with no retry/recovery/duplicate semantic work/outbox residue.

## Documentation-bearing candidate

Task 187 correctly stopped initial publication because stale current guidance existed inside package/installed product surfaces. Task 188 has now corrected that guidance in exactly these product documentation paths:

- `plugins/cogentnexus-openclaw/README.md`;
- `skills/cogentnexus-openclaw/SKILL.md`;
- `skills/cogentnexus-openclaw/references/architecture.md`;
- `skills/cogentnexus-openclaw/references/scheduler-adapters.md`.

The package README change produced payload-v2 `408167da...` / 184 files. The installed skill tree is now `a1e873ba...`. The executable scripts tree remains `3d9d323...`, including the unchanged accepted facade Git blob `879083d6186589d4b2774b8fd87fa93692dd2dfc`.

This is therefore a documentation/instruction identity change, not an executable/runtime behavior change.

## Qualification policy

The corrected artifact must receive proportional changed-surface requalification before publication:

1. exact-candidate repository/package CI;
2. one supported Windows install-over of the corrected candidate;
3. exact installed package/skill/facade provenance checks;
4. MANAGED + Ollama + Gateway + delivery/recovery + SQLite health;
5. one bounded Dashboard semantic/durable-delivery turn;
6. reset/uninstall/fresh-reinstall only if evidence from the corrected artifact gives a concrete lifecycle reason to repeat them.

The earlier destructive lifecycle evidence remains valid historical evidence for the implementation baseline and may support unchanged-surface claims only where byte identity is explicitly proven.

## Release topology

- default branch: `main`;
- Task-188 starting `main`: `874dd8f8ce9c1ca5595b29207281430a86c074de`;
- stale PR #24 is closed and not merged;
- `.github/workflows/release.yml` is the required exact-SHA publication gate;
- public release/tag state must be verified directly from GitHub Releases/tags rather than inferred from source prose.

## Publication path

After Task-188 requalification passes:

1. freeze the final exact candidate;
2. require exact-candidate CI/checks to be green;
3. create the current `agent/v0.9.3-full-stabilization` -> `main` release PR;
4. merge without force push only when topology/diff/checks are correct;
5. freeze exact merged `main` SHA;
6. dispatch `.github/workflows/release.yml` with `version=0.9.3` and that exact SHA;
7. verify Release workflow success, tag target, release notes, `.tar.gz`, `.zip`, `SHA256SUMS.txt`, and independent checksums.

## Safety boundary

Do not change production/runtime/plugin executable source, tests, dependencies, workflow behavior, provider/runtime semantics, or durable schema merely to obtain release success. Any need for such a change is a separate product defect and blocks publication. Do not force push.
