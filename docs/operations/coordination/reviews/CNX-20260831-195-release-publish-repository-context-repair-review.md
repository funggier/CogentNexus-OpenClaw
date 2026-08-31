# CNX-20260831-195 — Release Publish Repository-Context Repair Review

Disposition: `PASS`
Date: 2026-08-31 ICT
Reviewer: ChatGPT

## Review result

Accepted.

The Task 194 failure was isolated to GitHub CLI repository discovery in a publish job without a local checkout. Task 195 reproduced that defect with a focused RED regression test, applied a one-line repository-explicit fix, and returned the full validation surface to GREEN.

## Evidence accepted

- failed publication run `33399493141`;
- RED commit `7fc267dc15cb072079685790850ad57ca4574680`;
- RED Validate run `33403409766`;
- minimal fix commit `6d522806114d46f16a8efcc1c6722fa64ddd75e3`;
- RED-to-fix diff: only `.github/workflows/release.yml`, +1 line;
- GREEN Validate run `33403566461`;
- GREEN PS5.1 Acceptance run `33403566370`;
- GREEN Windows Installer Pack run `33403566408`.

## Release-target invariant

The accepted v0.9.3 candidate remains exactly:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

The forthcoming workflow-repair merge commit is not a replacement release candidate. It only provides the repaired workflow implementation used to execute a second, separately authorized publication attempt.

## Next gate

Create a fresh PR containing the workflow/test/coordination repair, review exact diff/checks, merge when GREEN, freeze repaired `main`, then create a separate publication task authorizing exactly one second Release dispatch with the original candidate SHA.
