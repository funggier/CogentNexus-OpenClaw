# Current Project Status

**Updated:** 2026-09-22
**Active task:** CNX-444 — v0.9.7 exact Gateway-interruption Direct recovery
**Current source line:** v0.9.7 (development)
**Latest published release:** v0.9.6
**Working branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`
**Latest physical OpenClaw acceptance:** `2026.9.5 (ec9c1a1)`
**Regression/dev OpenClaw pin:** `2026.7.1-2`
**Managed provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through
**License:** MIT

## Current accepted runtime position

CNX-443 / v0.9.6 remains the immutable published predecessor. Its authoritative Stop/session FIFO and four-stage physical lifecycle acceptance remain GREEN.

CNX-444 was opened from a production Discord incident on OpenClaw 2026.9.5. The request was correctly routed to `ollama/qwen3.8:27b`, but the Gateway was confirmed unresponsive and restarted while the model call was active. Because the old process disappeared before terminal model-call hooks ran, the CNX row remained `active` and no Direct Recovery authority was created.

OpenClaw subsequently waited its configured whole-run timeout of about 2700 seconds. This proves the repair is not "increase timeout".

## Current task: CNX-444

Required v0.9.7 semantics:

1. preserve the 15-minute CNX model-call deadline as observational only;
2. treat a confirmed Gateway process replacement as exact interruption evidence;
3. quiesce Gateway inference before authorizing replacement inference;
4. persist pending Direct Recovery before starting the replacement Gateway;
5. preserve response/delivery/terminal/cancellation/generation fences;
6. remain provider-neutral and preserve OpenClaw routing authority;
7. restore Gateway if classification fails after stop;
8. fully requalify repository, package, Windows lifecycle and live behavior before release.

## Current evidence

TDD:

- initial RED: missing gateway-interruption classifier + opaque `lifecycle restart` reproduced;
- focused repaired suite: `24/24 PASS`;
- expanded Host/provider/recovery regression: `112/112 PASS`;
- Python syntax: PASS;
- `git diff --check`: PASS.

The repair is not release-complete yet. Full local Python/plugin/package qualification is GREEN; exact-SHA CI, physical Windows lifecycle, and live interruption/recovery acceptance remain pending.

## Coordination model

The retired one-minute Codex `legacy coordination watch` automation remains retired. Do not recreate it.

Current execution model:

- ChatGPT performs repository/documentation/review work directly when tools permit.
- LConnect is used for bounded local Windows execution and evidence.
- `ACTIVE.md` / `STATUS.md` carry current durable coordination authority.
- Historical watcher/baton documents remain evidence only.

## Release topology

Release publication uses `.github/workflows/release.yml` with an exact validated candidate SHA.

No force push. v0.9.7 publication must fail closed if:

- source/version metadata disagree;
- required release notes are absent;
- repository/plugin/live acceptance is incomplete;
- exact candidate validation is not acceptable;
- tag/release already exists;
- package/checksum verification fails.

## Known boundaries still outside full production proof

- long high-concurrency soak;
- disk-full / DB-corruption hardening;
- universal exactly-once external side effects;
- arbitrary future OpenClaw versions beyond explicitly tested evidence.

Historical evidence remains in coordination tasks/reports/reviews and release notes; it is not rewritten merely to make old wording look current.
