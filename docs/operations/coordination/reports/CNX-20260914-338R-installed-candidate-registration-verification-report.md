# CNX-20260914-338R — Installed Candidate Registration Verification Report

**Date:** 2026-09-14 (Asia/Bangkok)
**Verdict:** `BLOCKED`
**Failure classification:** `CONTROLLER_MUTATION`

## Scope and safety fence

This gate was stopped during precondition verification. No runtime registration test was started. No Dashboard request, model inference, intentional Ticket, recovery, fallback, retry, duplicate-delivery test, or delivery action was performed by this gate.

## Fixed provenance

| Item | Required / observed |
|---|---|
| Repository | `funggier/CogentNexus-OpenClaw` |
| Candidate branch | `agent/v0.9.6-schema-authority-repair` |
| Candidate source HEAD | `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7` |
| Repair commit | `3efb971eeed55f0d48908281974577fdbed48612` |
| CNX-338A report commit | `328d6f83ad0c4612de29d71a7496e141a1315df4` |
| Installed entry | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` |
| Installed artifact SHA-256 | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| Observed installed artifact SHA-256 | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` |
| v0.9.5 tag | `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` (observed exact match) |

The artifact provenance and immutable v0.9.5 tag preconditions passed.

## Preconditions

### Plugin load

Direct `openclaw plugins list` inspection reported:

- `CogentNexus-OpenClaw Bridge`
- ID `cogentnexus-openclaw`
- Status `enabled`
- Source `global:cogentnexus-openclaw/dist/v091-release-entry.js`
- Version `0.9.5`

The plugin-load precondition passed. This command is observational only; it does not exercise registration.

### Controller state — failed precondition

The live controller file was read before any registration attempt:

`C:\Users\CDQ-P\.openclaw\workspace\host\controller.json`

- Observed SHA-256: `14ac439bfc74511cf326507810ec2aff772fdec7114654b1e57f978c06c1d77c`
- Observed bytes: 193
- Observed JSON: `{"schemaVersion":1,"mode":"passthrough","desiredGateway":"running","desiredProvider":"unchanged","generation":1,"updatedAt":"2026-08-29T01:36:31.541994+00:00"}`

Required state was:

- `schemaVersion=2`
- `cnxMode=active`
- `generation=101`

Observed state is schema 1 with legacy `mode=passthrough`, has no `cnxMode`, and has `generation=1`. This is a provenance/precondition deviation. Per the task safety fence, registration testing was not attempted.

### Provider/model and timeouts

The live OpenClaw configuration read showed:

- Provider/model: `ollama/qwen3.8:27b`
- Agent timeout: `2700` seconds
- Ollama provider timeout: `2700` seconds

These match the requested provider/model and timeout values (the task's provider/model spelling is preserved as supplied).

## Registration evidence

No registration invocation was performed because the controller precondition failed.

| Required evidence | Result |
|---|---|
| Host authority `AUTHORIZED` | **Not tested** |
| Observed schema-2 `cnxMode=active` authorization | **Not available** |
| Translated downstream mode | **Not available** |
| `legacyEntry.register(runtimeApi)` reached | **Not tested / no proof** |
| Registered hooks/events/services/tools | **Not tested / no proof** |
| `before_agent_run` present | **Not tested / no proof** |
| Duplicate owner/hook check | **Not tested** |
| Partial-registration check | **Not tested** |

Because the required registration boundary was not exercised, this report does not infer PASS from the plugin-list load result.

## Controller pre/post integrity

There was no registration attempt, so there is no post-registration mutation. The only available controller measurement is the pre-test observation above. A post-test comparison was intentionally not fabricated because the registration gate did not run.

The observed pre-test controller itself fails the required baseline (`schemaVersion=2`, `cnxMode=active`, `generation=101`); therefore this gate cannot establish controller-integrity success for the requested schema-2 registration test.

## Semantic-traffic gate

This gate performed no registration test and no semantic operation. There is no gate-generated evidence of:

- Dashboard traffic
- model inference
- intentional Ticket
- recovery
- fallback
- retry experiment
- duplicate-delivery test
- delivery action

The gate stopped before the operation that would have generated registration evidence.

## Final verdict

`BLOCKED`

**Exact failure classification:** `CONTROLLER_MUTATION`

The live controller does not satisfy the required schema-2/active/generation-101 precondition. The installed artifact SHA and plugin load status are correct, but Host authority acceptance, legacy registration reachability, and hook registration remain unproven. CNX-339 is not authorized by this report.
