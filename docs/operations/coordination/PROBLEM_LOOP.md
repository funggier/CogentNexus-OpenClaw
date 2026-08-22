# Problem Resolution and Communication Loop

This contract prevents a safe execution stop from becoming a silent coordination dead end.

## Core rule

Stop an unsafe or unauthorized action, but continue the coordination loop through durable reporting, review, diagnosis, and the narrowest justified next task.

A `BLOCKED`, `FAIL`, or partial result is useful evidence. It is not permission to improvise, repeat side effects, or abandon the project without an explicit reviewed disposition.

## Required Codex problem report

When an authorized task starts but cannot complete, Codex must publish the matching report whenever repository publication is still possible.

The report must include:

- task ID, branch, start HEAD, and ACTIVE verification;
- exact status: `COMPLETED`, `PARTIAL`, `BLOCKED`, or `FAIL`;
- the exact failed precondition, command, check, or observed runtime condition;
- commands/actions actually executed and exit codes;
- evidence paths, hashes, timestamps, and relevant durable fields;
- state-changing or destructive actions that did and did not occur;
- gates proven, failed, skipped, or still unproven;
- whether the cause is a task/specification conflict, execution-environment issue, evidence gap, test/harness defect, product/runtime defect, or unknown;
- one or more narrow safe remediation options;
- the recommended next option and why;
- `Human decision required: YES|NO`, with the exact decision if `YES`;
- duplicate-execution and external-side-effect accounting.

Codex must not convert a recommendation into authority. It stops after publishing the report.

## Required ChatGPT response

When a new matching report has no review, ChatGPT must:

1. read the active task, report, immutable criteria, cited evidence, and current project records;
2. publish exactly one `ACCEPT`, `REWORK`, `BLOCKED`, or `SUPERSEDED` review;
3. state what evidence is accepted and what remains unproven;
4. classify the blocker;
5. choose exactly one disposition:
   - create the narrowest safe diagnostic task;
   - create the narrowest justified fix-and-validation task;
   - create a corrected replacement task for a specification/mechanical conflict;
   - set coordination state to blocked for an exact human decision;
   - close/supersede the path when evidence proves no further action is useful;
6. update `ACTIVE.md` and `STATUS.md` when the disposition changes the next step;
7. notify the human operator of the result, risk, and next action.

ChatGPT must not silently leave an actionable `BLOCKED` or `FAIL` report without a reviewed disposition.

## Remediation ladder

Use the smallest layer justified by evidence:

1. missing fields or ambiguous artifacts → read-only evidence extraction;
2. task/watcher/specification conflict → corrected replacement task;
3. checkout/environment problem → narrow validation or cleanup manifest before mutation;
4. test/harness defect → offline fix plus unit/parser/syntax/CI validation;
5. product/runtime defect → offline diagnosis, narrow fix, and CI before any new disruptive run;
6. destructive, architectural, dependency-removal, or user-data choice → block for human decision.

A disruptive scenario may be repeated only when the prior run did not execute that side effect, or a later exact task explicitly authorizes the repeat from reviewed evidence and retains all safety/duplicate fences.

## Human communication rule

The user-facing update must distinguish:

- what succeeded;
- what failed or blocked;
- what was not attempted;
- whether machine/runtime state changed;
- what task or human decision comes next.

No-op watch cycles may remain silent. Meaningful reports, reviews, blockers, fixes, and human-decision gates must be communicated.

## Durable conversation

GitHub coordination records are the primary Codex–ChatGPT conversation:

`task → report → review → next task or human decision`

Chat text may summarize this loop but must not replace the durable report/review/task records.
