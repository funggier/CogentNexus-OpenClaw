# CNX-20260831-191 — NO_REPLY Direct Dashboard Semantic Repair

- **Disposition:** `READY_FOR_WINDOWS_REQUALIFICATION`
- **Date:** 2026-08-31 ICT
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Working branch:** `agent/v0.9.3-full-stabilization`
- **Parent umbrella:** `CNX-20260831-188`
- **Triggered by:** `CNX-20260831-190`
- **Repository repair candidate:** `050ab53f4b593ab538143084d6bbdbf7e1672e34`

## Result

Repository-side repair is complete and exact-candidate CI is green. Task 191 is **not** final PASS yet because the executable plugin behavior change still requires proportional requalification on the accepted real Windows host.

The previous product candidate `604569c286e930f1a596362ab926b065b56d486e` is retained only as Task-189/190 historical evidence and is no longer release-eligible.

## Triggering failure

Task 190 proved a healthy, exactly-once durable chain but the logical assistant content was wrong:

- exactly one genuine human Dashboard Send;
- one new Ticket;
- one correlated run/model call;
- one durable `direct_result` delivery;
- one logical Dashboard assistant bubble;
- no direct recovery, retry, regeneration, injection, duplicate Ticket/model-call/delivery, or pending terminal outbox residue;
- durable assistant text = `NO_REPLY`;
- visible Dashboard assistant text = `NO_REPLY`;
- requested nonce acknowledgement absent.

Task 190 correctly classified this as `FAIL_SEMANTIC_DURABLE_DELIVERY`.

## Root cause

Two facts interact at the boundary:

1. OpenClaw uses bare `NO_REPLY` as a silent/suppression sentinel and local/small models can still emit it on a direct human turn on the accepted OpenClaw baseline.
2. CogentNexus Dashboard verified delivery treated any non-empty final assistant text as durable visible content, staged it, then appended its delivery marker before native persistence.

For a bare sentinel, marker injection changed the payload from exact `NO_REPLY` into a non-bare text payload. That defeated exact-token silent suppression and made the sentinel durable and visible.

The repair therefore belongs at the CogentNexus integration boundary rather than by fabricating a user answer or replaying the lifecycle.

## TDD — RED

Test-only commit:

`94872464781e19d934877ac3346714e3061bd140`

Added:

`plugins/cogentnexus-openclaw/src/v191-no-reply-direct-dashboard.test.ts`

Validate run:

`33390068431`

Expected RED was observed before production edit:

- existing suite: `273` tests passed;
- Task-191 regression: `2` tests failed;
- bare `NO_REPLY` was actually staged (`staged:true`) instead of returning `silent-reply`;
- `before_agent_finalize` returned `undefined` instead of one bounded `revise` decision.

This isolated the defect without setup, syntax, Python, packaging, or unrelated plugin failures.

## Minimal production repair

Repair commit / exact candidate:

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

Parent:

`94872464781e19d934877ac3346714e3061bd140`

Production file changed:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

Production diff from the test-only commit:

- exactly one production file;
- `+17 / -2` lines;
- no dependency, workflow, durable-schema, provider, installer, lifecycle, or unrelated runtime change.

Fixed source Git blob:

`aa97d7a5411f799c612cd0aeece050085298a8bb`

Behavior:

1. Added exact bare-sentinel predicate after trim, case-insensitive:
   `^NO_REPLY$`.
2. `stageDashboardDirectResult` now returns `staged:false, reason:'silent-reply'` before any durable delivery staging when the result is bare `NO_REPLY` / `no_reply`.
3. Mixed substantive content mentioning the token remains ordinary visible content.
4. `before_agent_finalize` now returns one same-run OpenClaw revision decision only when:
   - run/session correlation exists;
   - an accepted direct Dashboard Ticket exists for the run;
   - natural final assistant text is exactly the bare silent sentinel.
5. Revision contract:
   - `action='revise'`;
   - idempotency key `cnxclaw-dashboard-visible-final:<runId>`;
   - `maxAttempts=1`;
   - instruction requires a visible answer to the current direct user request and forbids `NO_REPLY/no_reply` for that turn.
6. CogentNexus does not synthesize or derive the user-visible answer itself.
7. A second bare sentinel cannot be marker-staged because the common durable staging fence rejects it.

## GREEN verification

Exact-candidate Validate:

- run `33390552591`;
- exact head SHA `050ab53f4b593ab538143084d6bbdbf7e1672e34`;
- final status `completed/success`.

All jobs completed successfully:

- package dry-run;
- Ubuntu Python 3.11;
- Ubuntu Python 3.14;
- macOS Python 3.11;
- macOS Python 3.14;
- Windows Python 3.11;
- Windows Python 3.14.

Fresh plugin evidence from the exact-candidate run:

- Task-191 regression: `2/2` tests passed;
- plugin suite: `54` test files, `275` tests passed;
- Python suite: `474 passed`, `33 skipped`, `4 subtests passed` on the inspected Ubuntu 3.11 matrix job;
- evaluation passed;
- production npm audit passed with zero production vulnerabilities;
- plugin validation passed.

Additional exact-candidate gates:

- PS5.1 Acceptance Smoke `33390552613`: `completed/success`;
- Windows Installer Pack Smoke `33390552545`: `completed/success`.

## Repaired candidate identities

Exact repaired product candidate:

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

Root Git tree:

`1c10a631b58e1609fc76168e76a26dbe72444e6c`

Plugin tree (`plugins/cogentnexus-openclaw`):

`eeab5fb8c67e5c16284d5df49ec413a53c251a13`

Installed skill tree (`skills/cogentnexus-openclaw`) remains:

`a1e873ba404205507a1623961b49f1b1a0689f9f`

Executable skill scripts-tree remains:

`3d9d323ba19443d46e970b87cef52ce878da274f`

`cnxclaw.py` Git blob remains:

`879083d6186589d4b2774b8fd87fa93692dd2dfc`

Previously accepted Windows facade SHA-256 remains the expected live identity and must be re-proved by Windows Task 192:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

## Package proof

Version:

`0.9.3`

Payload-v2:

`b1ca9f3b42009cf4b1ae0a04f0e75add8d2ff9bd5dc97fce4040dc4753562d93`

Payload file count:

`186`

Dry-run tar:

- `cogentnexus-openclaw-v0.9.3.tar.gz`
- SHA-256 `7ed09e96163bd1e3fb3977abe30439728e93fb0a54ea2104286de8ece7cb4950`

Dry-run zip:

- `cogentnexus-openclaw-v0.9.3.zip`
- SHA-256 `d4c478365475ed7dd064168a89caf9bce89c5486d4238947cd048de0c4070c6a`

Package-proof artifact:

- ID `9757273396`
- name `cogentnexus-openclaw-v0.9.3-package-proof-050ab53f4b593ab538143084d6bbdbf7e1672e34`
- size `5,307,533` bytes
- artifact ZIP digest `7bfa3d16ed12ab0ee380ad62f7ac512381252c90c35618970038b4efa61d86cc`

These remain CI proof artifacts, not published GitHub Release assets.

## Scope review

No reset, uninstall, fresh reinstall, state deletion, provider replacement, durable schema change, dependency change, release PR/merge/tag/release action, or force push occurred during repository repair.

Because executable plugin behavior changed, a bounded real-Windows requalification is required before Task 191 or Task 188 can be accepted for release.

## Next boundary

Task 192 must use exact product candidate:

`050ab53f4b593ab538143084d6bbdbf7e1672e34`

Later coordination-only commits do not redefine that product candidate.

Default real-Windows scope:

1. read-only live baseline;
2. exactly one supported install-over of exact candidate;
3. installed plugin/package/source provenance and unchanged facade/runtime identity proof;
4. OpenClaw/Gateway/managed Ollama/delivery/recovery/SQLite health;
5. exactly one genuine human Dashboard semantic turn orchestrated by Hermes;
6. accept one same-run OpenClaw finalization revision only if the first natural final is a bare `NO_REPLY` sentinel;
7. prove one Ticket and one durable visible assistant delivery with no external direct recovery or duplicate output;
8. final health/provenance report.

No reset/uninstall/fresh reinstall is authorized by default.
