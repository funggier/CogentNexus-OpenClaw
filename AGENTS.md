# CogentNexus-OpenClaw Agent Instructions

Use this file as the compact repository entry point. Current operational truth lives under `docs/`.

## Project identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Current source/release line: `v0.9.8` (published accepted baseline; release/tag SHA `4f9b07d6e29e2051a44d2681cce0f8ecf5f47037`)
- Current working branch: read from remote coordination `ACTIVE.md` / `STATUS.md`; do not hard-code an older branch
- License: MIT

## Coordination

When using the GitHub coordination workflow, read:

1. `docs/operations/coordination/README.md`
2. `docs/operations/coordination/ACTIVE.md`
3. `docs/operations/coordination/STATUS.md`
4. the task linked by `ACTIVE.md`

ChatGPT should execute repository/source/documentation/review work directly when current tools permit. Hermes is primarily for bounded local/live work that requires the user's machine.

The old Codex `legacy coordination watch` automation was retired and removed. Do not recreate it from historical task/report text.

## Minimal signals

- `ต่อ` — synchronize current durable authority and continue the exact assigned task.
- `สถานะ` — read/report state only.
- `หยุด` — do not begin a new coordination task.

Historical READY/WAITING tokens remain meaningful in old evidence but are not substitutes for reading current authority.

## Safety

- Task-specific safety gates are mandatory.
- Never force-push unless the operator explicitly gives separate, unmistakable authority requiring it.
- Protect unknown local work.
- Do not repeat completed external side effects after matching terminal evidence.
- Do not infer destructive/live/semantic authority from repository access.
- Historical tasks/reports/releases remain historical evidence.

## Technical truth

Accepted technical claims require code/tests/evidence/release gates. Current-facing documentation must distinguish:

- latest physical runtime acceptance from regression dependency pins;
- published release identity from an in-progress source/release line;
- historical compatibility code names from the current package version.
