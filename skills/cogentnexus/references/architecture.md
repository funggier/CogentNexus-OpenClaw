# Architecture and Extension Contract

CogentNexus is a modular monolith: one discoverable OpenClaw skill and one `SKILL.md`.

## Directories

- `SKILL.md`: stable kernel, routing, invariants, validation command.
- `references/`: cognitive modules loaded only when routed.
- `scripts/`: deterministic state management and validation.
- `assets/`: non-executable templates.

## Adding a module

1. Give it one responsibility and a clear trigger.
2. Put detailed behavior in `references/<module>.md`.
3. Add exactly one routing bullet in `SKILL.md`.
4. Avoid duplicating Kernel invariants.
5. Add required-file checks to `scripts/validate.py`.
6. Run validation and an interruption/resume acceptance test.
7. Update the version only for material behavioral changes.

Do not add nested `SKILL.md` files. They would create separate discoverable skills and break the single-entry architecture.