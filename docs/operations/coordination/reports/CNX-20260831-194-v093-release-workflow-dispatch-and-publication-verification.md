# CNX-20260831-194 — v0.9.3 Release Workflow Dispatch and Publication Verification

**Disposition:** `FAIL_RELEASE_WORKFLOW`

## Scope and authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Coordination branch: `agent/v0.9.3-full-stabilization`
- Release ref: `main`
- Frozen candidate SHA: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Workflow: `.github/workflows/release.yml`
- Requested version: `0.9.3`
- Executor: Hermes / authenticated GitHub operator
- Publication was dispatched exactly once.
- No source, runtime, plugin, test, installer, provider, or workflow change was made.
- No manual release, tag creation, force push, duplicate dispatch, or cleanup was performed.

## Fresh pre-dispatch authority checks

Executed against GitHub immediately before dispatch on 2026-08-31 UTC:

```text
gh auth status
gh api repos/funggier/CogentNexus-OpenClaw/git/ref/heads/main
gh pr view 26 --repo funggier/CogentNexus-OpenClaw --json state,mergedAt,mergeCommit,headRefName,baseRefName,url
gh api repos/funggier/CogentNexus-OpenClaw/git/ref/tags/v0.9.3
gh release view v0.9.3 --repo funggier/CogentNexus-OpenClaw --json tagName,isDraft,isPrerelease,url
gh run list --repo funggier/CogentNexus-OpenClaw --workflow release.yml --limit 30 --json databaseId,status,conclusion,event,headBranch,headSha,createdAt,displayTitle,url
```

Results:

- Authenticated GitHub account: `funggier`; required `repo` and `workflow` scopes were present.
- `main` was exactly `26ce64a624255278a3a0266ad38746e0e6ed2e31`.
- PR #26 was `MERGED`; merge SHA was exactly `26ce64a624255278a3a0266ad38746e0e6ed2e31`.
- Tag `v0.9.3`: GitHub API `404 Not Found`.
- Release `v0.9.3`: `release not found`.
- No existing/in-progress v0.9.3 Release workflow run was present.

## Exact dispatch

Command executed once:

```text
gh workflow run release.yml --repo funggier/CogentNexus-OpenClaw --ref main -f version=0.9.3 -f candidate_sha=26ce64a624255278a3a0266ad38746e0e6ed2e31
```

Dispatch observation:

- Dispatch request time: `2026-08-31T13:53:44Z` (local UTC capture)
- Run URL returned by GitHub: `https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33399493141`
- Run ID: `33399493141`
- Event: `workflow_dispatch`
- Ref/head branch: `main`
- Head SHA: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Run created: `2026-08-31T13:53:47Z`

No second dispatch was attempted.

## Workflow result

The run reached terminal state:

- Overall status: `completed`
- Overall conclusion: `failure`
- Updated: `2026-08-31T13:55:42Z`
- Run URL: `https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33399493141`

Jobs:

| Job | Job ID | Conclusion | URL |
|---|---:|---|---|
| `package` | `99512028016` | `success` | `https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33399493141/job/99512028016` |
| `publish` | `99512545570` | `failure` | `https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/33399493141/job/99512545570` |

The `package` job passed all listed validation, test, metadata, archive build, integrity, and artifact-staging steps. This included Python tests, npm tests/evaluation/audit/plugin validation, exact release metadata, and archive verification/staging.

The first failed step was:

```text
publish / Publish GitHub Release
```

Failure log captured with:

```text
gh run view 33399493141 --repo funggier/CogentNexus-OpenClaw --log-failed
```

Relevant exact failure output:

```text
2026-08-31T13:55:39.7099189Z failed to run git: fatal: not a git repository (or any of the parent directories): .git
2026-08-31T13:55:39.7100136Z
2026-08-31T13:55:39.7130607Z ##[error]Process completed with exit code 1.
```

The failed step had already validated:

```text
TAG: v0.9.3
CANDIDATE_SHA: 26ce64a624255278a3a0266ad38746e0e6ed2e31
```

The workflow's publish command was:

```text
gh release create "$tag" "${common[@]}" \
  --target "$CANDIDATE_SHA" \
  --notes-file "$notes" \
  --title "CogentNexus-OpenClaw $tag"
```

The workflow failure is therefore recorded as a workflow/publish failure. No repair was authorized under Task 194.

## Post-failure publication verification

Fresh GitHub checks after terminal failure:

```text
gh api repos/funggier/CogentNexus-OpenClaw/git/ref/heads/main
gh api repos/funggier/CogentNexus-OpenClaw/git/ref/tags/v0.9.3
gh release view v0.9.3 --repo funggier/CogentNexus-OpenClaw --json tagName,name,isDraft,isPrerelease,createdAt,publishedAt,targetCommitish,url,assets
gh run view 33399493141 --repo funggier/CogentNexus-OpenClaw --json databaseId,status,conclusion,event,headBranch,headSha,createdAt,updatedAt,url,displayTitle
```

Results:

- `main` remained exactly `26ce64a624255278a3a0266ad38746e0e6ed2e31`.
- Tag `v0.9.3` remained absent (`404 Not Found`).
- Release `v0.9.3` remained absent (`release not found`).
- No public release assets existed, so independent downloads, archive listing, and SHA-256 verification could not be performed.
- No evidence of a partial tag/release publication was found.

## Anomalies

1. The `package` job passed and staged validated release assets.
2. The `publish` job downloaded the artifact successfully but `Publish GitHub Release` failed because the GitHub CLI attempted to run git outside a Git repository, returning exit code `1`.
3. GitHub Actions emitted Node.js 20 deprecation annotations for `actions/upload-artifact@v4` and `actions/download-artifact@v5`, but these were warnings and not the failure cause.
4. No workflow or product repair was attempted because Task 194 explicitly forbids repairs under the publication boundary.

## Final disposition

```text
FAIL_RELEASE_WORKFLOW
```

Task 194 stops here. Further release attempts, workflow repairs, tag/release manipulation, or product changes require a separate explicitly authorized task.
