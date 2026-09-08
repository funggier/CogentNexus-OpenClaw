# CNX-20260831-196 — v0.9.3 Second Release Dispatch and Publication Verification

- Date: 2026-08-31 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Executor: Hermes
- Coordinator / final reviewer: ChatGPT
- Parent: `CNX-20260831-188`
- First publication attempt: Task 194, run `33399493141`
- Repair: Task 195, PR #27
- Final disposition: `FAIL_RELEASE_WORKFLOW`

## Executive result

The exactly-authorized second Release workflow dispatch was performed once from the repaired `main` commit. The package job passed, including the repository-context repair and all validation/test/archive steps. The publish job reached GitHub with the expected repository, tag, and candidate values, but GitHub rejected release creation with:

```text
HTTP 403: Resource not accessible by integration
```

The workflow therefore ended `completed/failure`. No tag, GitHub Release, or public release assets were created. The workflow was not retried, and no tag/release was created manually.

## Authority and pre-dispatch gate

Fresh authority was read from GitHub on the authoritative branch `agent/v0.9.3-full-stabilization` before dispatch.

| Check | Evidence | Result |
|---|---|---|
| Repaired workflow execution ref | `main = c70552801ddbb9dc0a49c9cfc64368b9f4820f07` | PASS |
| PR #27 | Merged | PASS |
| v0.9.3 tag absent | GitHub ref lookup returned 404 Not Found | PASS |
| v0.9.3 Release absent | `gh release view` returned `release not found` | PASS |
| No successful second publication already present | No prior successful second run found before dispatch | PASS |
| Repository-explicit publish context | `GH_REPO: ${{ github.repository }}` present in `release.yml` on repaired `main` | PASS |

The frozen release candidate was preserved exactly and was not replaced by the repaired workflow SHA:

```text
candidate_sha = 26ce64a624255278a3a0266ad38746e0e6ed2e31
```

## Authorized dispatch

Exactly one dispatch was performed:

- Workflow: `.github/workflows/release.yml`
- Ref: `main`
- Version: `0.9.3`
- Candidate SHA input: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Dispatch count: `1`
- Workflow run: `33406148890`
- URL: https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33406148890
- Event: `workflow_dispatch`
- Workflow execution head SHA: `c70552801ddbb9dc0a49c9cfc64368b9f4820f07`
- Created: `2026-08-31T15:02:38Z`
- Completed: `2026-08-31T15:04:17Z`
- Overall status/conclusion: `completed / failure`

No retry, rerun, manual publication, candidate retargeting, force push, reset, uninstall, reinstall, or install-over was performed.

## Workflow verification

### Package job

- Job ID: `99534121902`
- URL: https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33406148890/job/99534121902
- Conclusion: `success`
- Duration: approximately 1m19s

The following groups passed:

- exact request and checked-out candidate identity validation;
- CogentNexus-OpenClaw namespace isolation;
- Python setup and dependency installation;
- baseline consistency check;
- Cogent, runtime, and workflow self-tests;
- Python compilation;
- `python -m pytest -q`;
- plugin path migration helper;
- `npm ci`;
- `npm test`;
- `npm run evaluation`;
- `npm audit --omit=dev`;
- `npm run plugin:validate`;
- exact release metadata and release identity checks;
- release archive build and verification;
- validated release asset staging.

### Publish job

- Job ID: `99534579993`
- URL: https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33406148890/job/99534579993
- Conclusion: `failure`
- `Download validated release assets`: success
- `Publish GitHub Release`: failure

The publish log proves that the repaired repository context was active and that the expected values were passed:

```text
GH_REPO: funggier/CogentNexus-OpenClaw
TAG: v0.9.3
CANDIDATE_SHA: 26ce64a624255278a3a0266ad38746e0e6ed2e31
```

The exact failure was:

```text
HTTP 403: Resource not accessible by integration (https://api.github.com/repos/funggier/CogentNexus-OpenClaw/releases)
```

This is different from Task 194's earlier failure:

```text
failed to run git: fatal: not a git repository
(or any of the parent directories): .git
```

## Publication verification

Because the publish step failed, the required public publication checks could not pass:

| Required item | Fresh GitHub result |
|---|---|
| Tag `v0.9.3` exists | No; ref lookup returned 404 |
| Tag target equals candidate | Not applicable; tag absent |
| GitHub Release `v0.9.3` published | No; release not found |
| Required public assets | Not published |
| Download published assets | Not possible |
| Published `SHA256SUMS.txt` contents | Not available |
| Independent archive SHA-256 comparison | Not possible against a published release |
| Archive open/list verification from public release | Not applicable |
| Duplicate/unexpected second v0.9.3 publication | None observed |

The workflow did produce one retained Actions artifact for the failed run, but it is not a published Release asset and must not be treated as publication success:

- Artifact: `release-assets-0.9.3-26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Artifact ID: `9763253683`
- Size: `7,021,277` bytes
- Digest reported by GitHub: `sha256:5ca5bf8579754888c355c0976a86fd03c3c79eeed2ecd52293a0d6e5fa24b65d`
- Expiration: `2026-09-07T15:04:00Z`

This artifact was not downloaded or used as a substitute for the required published-release verification.

## Post-dispatch authority state

Fresh GitHub checks after the failed run showed:

- `main` remained exactly `c70552801ddbb9dc0a49c9cfc64368b9f4820f07`;
- tag `v0.9.3` remained absent;
- Release `v0.9.3` remained absent;
- no partial tag/release publication was observed.

## Discord session test evidence requested by the user

This section records the latest user-driven Discord test separately from the release workflow result. The user sent the message from Discord; Hermes did not send, press Enter, retry, regenerate, inject, or recover the request.

### Previous failing Discord session

The earlier Discord-origin session was:

```text
agent:main:discord:channel:1531201432861282405
```

Its requests were blocked before the agent ran. The relevant log pattern was:

```text
handler-skip: missing-run-correlation
before_agent_run hook failed; blocking request
handler-skip: missing-append-before-deliver
```

That session did not provide evidence of a durable Ticket/model-call/delivery path for the blocked requests. It must not be conflated with the later room test.

### New Discord session and user-visible result

The user sent once from a different Discord room. The new session was:

```text
agent:main:discord:channel:1531199905673252946
```

The backend records were:

- Ticket: `CNXT-50d93e89-a04b-421d-bad2-b2c747f646da`
- Run: `65f3abad-9817-4c7a-aeb7-1feeafda5213`
- Model call: `65f3abad-9817-4c7a-aeb7-1feeafda5213:model:1`
- Provider/model: `ollama / qwen3.5:9b`
- Prompt: `@Ce สวัสดีครับ`

The observed event chain was:

```text
accepted
→ routed
→ direct_model_call_started
→ direct_model_call_ended
→ response_ready
→ delivery_confirmed
→ completed
```

Authoritative SQLite values after completion:

- Ticket status: `completed`
- Model call state/outcome: `ended / completed`
- Model duration: `912602 ms` (approximately 15m 12.602s)
- `response_ready_at`: `2026-08-31T14:56:33.668Z`
- `delivery_confirmed_at`: `2026-08-31T14:56:49.816Z`
- `attempt_count`: `0`
- `recovery_attempt_count`: `0`
- `ticket_outbox`: `0` rows for this Ticket
- `cnx_direct_recovery`: `0` rows for this Ticket
- SQLite integrity: `ok`

The user independently confirmed that the response was visibly present in Discord. Therefore the latest room test is:

```text
Discord user-visible delivery: PASS (user-confirmed)
Backend processing and model completion: PASS
```

### Discord anomaly and interpretation

The same Ticket had no row in `cnx_assistant_delivery`, even though the Ticket contained `delivery_confirmed_at` and terminal `delivery_confirmed → completed` events. This is an internal evidence inconsistency, not evidence that the user did not see the response.

The log still contained a `missing-run-correlation` observer skip around the new-session request. The latest test therefore demonstrates a behavioral difference between Discord sessions:

1. the old session was blocked at `before_agent_run` because correlation/delivery-observer prerequisites were missing;
2. the new session passed pre-agent, created a Ticket, started and completed a model call, and reached terminal completion;
3. the user saw the resulting Discord response;
4. the durable assistant-delivery table did not record a corresponding row.

The evidence supports the conclusion that Discord transport is not uniformly blocked across rooms. It does **not** prove the root cause of the session-to-session divergence, and it does not prove that the durable delivery-record anomaly is harmless. A likely hypothesis is that session/run correlation and the durable delivery-observer path are not applied consistently across Discord session lifecycles, but this remains a hypothesis because no source/config mutation or controlled repeat test was authorized in this task.

The long model duration also explains why an intermediate observer showed the call as `active` for an extended period. It was not a model failure: the call eventually completed, with no recovery attempt. The earlier `long_running` diagnostic should be recorded as an operational warning, not as the cause of the final Discord result.

## Problems, provenance, predictions, and analysis

### Problem history

- Task 194 proved that the original publish job failed locally in the runner because it lacked a Git repository context.
- Task 195 repaired the workflow with repository-explicit context and merged PR #27.
- Task 196 tested that repaired workflow exactly once.
- The repair was exercised: the old local Git-repository error did not recur.
- The remaining failure is GitHub API authorization (`HTTP 403`) during release creation.

### Pre-dispatch prediction

Before dispatch, the expected outcome was that the repository-context repair would allow `gh release create` to reach the GitHub API and that publication could succeed if the workflow token had sufficient release-write permission. The first half was confirmed; the second was disproven by the 403 response.

### Analysis

The package job and all release preparation stages passed, so the candidate validation and archive construction path was not the failing boundary. The publish job received the correct `GH_REPO`, tag, and candidate values, proving the Task 195 repair addressed the Task 194 checkout/context failure. The failure occurred specifically when the Actions integration attempted `POST /repos/funggier/CogentNexus-OpenClaw/releases` and was denied by GitHub. This points to workflow-token permission/policy or repository Actions authorization, not candidate identity or archive generation. The exact permission/policy cause was not changed or independently proven in this task.

For Discord, the user-visible confirmation proves the new-room response reached the user, while SQLite proves the backend lifecycle completed. The missing `cnx_assistant_delivery` row and residual correlation-skip log limit the scope of the acceptance claim and should remain open for a separate diagnosis task.

## Final disposition

```text
FAIL_RELEASE_WORKFLOW
```

Reason: the exactly-authorized second dispatch completed with `package=success` but `publish=failure` due to GitHub `HTTP 403: Resource not accessible by integration`; no public v0.9.3 Release was created. Task 196 is stopped here for ChatGPT review. No retry or manual publication was performed.
