# CNX-20260831-196 — Review

Status: `REVIEWED__FAIL_RELEASE_WORKFLOW`
Date: 2026-08-31 ICT
Reviewer: ChatGPT
Parent: `CNX-20260831-188`

## Accepted evidence

Task 196 is accepted as an accurate failure report.

- Release workflow run `33406148890` was dispatched exactly once from repaired `main` `c70552801ddbb9dc0a49c9cfc64368b9f4820f07`.
- Requested `candidate_sha` remained `26ce64a624255278a3a0266ad38746e0e6ed2e31`.
- Package job passed and staged validated release assets.
- Publish job reached the GitHub Releases API with the expected repository/tag/candidate values.
- Publication failed with `HTTP 403: Resource not accessible by integration`.
- No `v0.9.3` tag or GitHub Release was created and no retry/manual publication occurred.

## Root-cause refinement

The current release workflow already grants `contents: write` to the `publish` job and uses explicit `GH_REPO` context.

The frozen candidate `26ce64a624255278a3a0266ad38746e0e6ed2e31` differs from the current default branch `main = c70552801ddbb9dc0a49c9cfc64368b9f4820f07` in `.github/workflows/release.yml` because Task 195 repaired the release workflow after the product candidate had already been frozen.

GitHub's Create-a-release authorization rules require a credential with workflow-write authority when the selected target commit changes workflow files relative to the default branch. The Actions `GITHUB_TOKEN` cannot be granted that additional workflow authorization for this edge case. Therefore another `GITHUB_TOKEN` workflow retry targeting `26ce64a...` is not an appropriate repair.

## Publication decision

Preserve the frozen release target `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

Use the already validated Task-196 Actions artifact under a narrowly bounded publication task with an authenticated user/GitHub-App credential that can create a release targeting this workflow-divergent commit. Do not rebuild or retarget merely to avoid the permission boundary.

## Discord evidence review

The Discord evidence is accepted as a separate defect signal, not as publication success/failure evidence.

Observed:

- prior Discord session `agent:main:discord:channel:1531201432861282405` was blocked before agent execution with `missing-run-correlation` / missing delivery-observer prerequisites;
- newer session `agent:main:discord:channel:1531199905673252946` created one Ticket/run/model call, completed without recovery, and produced a user-visible Discord response;
- the completed Ticket had no corresponding `cnx_assistant_delivery` row;
- a `missing-run-correlation` observer skip still appeared around the newer session.

This is sufficient to open a dedicated session/correlation durability investigation. It is not sufficient to claim a root cause yet.

## Disposition

`TASK196_ACCEPTED_AS_FAILURE__OPEN_TASK197_PUBLICATION_FALLBACK__QUEUE_TASK198_DISCORD_SESSION_INVESTIGATION`
