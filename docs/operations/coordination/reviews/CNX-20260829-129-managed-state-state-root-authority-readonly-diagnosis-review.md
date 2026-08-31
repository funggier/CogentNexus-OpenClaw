# Independent Review — CNX-20260829-129 Managed-State / State-Root Authority Read-Only Diagnosis

## Verdict

**NEEDS EVIDENCE CLOSEOUT — the reported root-cause classification is technically credible and consistent with the installed-launcher contract, and Task 129 appears to have respected the read-only hard fence, but the published report does not contain enough of the evidence explicitly required by the Task-129 contract for independent acceptance. Do not mutate or normalize the live runtime; publish the retained forensic evidence first.**

## What is accepted from the current report

The report gives a coherent explanation for Task 128's false unsafe preflight:

- Task-128 probing used `--root C:\Users\CDQ-P\.openclaw\workspace`;
- the installed launcher targets `--root C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`;
- direct installed-launcher probes reportedly returned `managed`, selected provider `ollama`, desired provider `ollama`, and `check recovery` verdict `READY`;
- the authoritative SQLite database reportedly exists under the `.cogentnexus-openclaw` state root and `PRAGMA integrity_check` returned `ok` from a read-only URI connection;
- no lifecycle/recovery/provider/config/database mutation or Dashboard semantic Send is reported;
- Task-128 repaired-harness suite remains `0 / 1 launched`.

Those facts support the likely classification **LAUNCHER_OR_ROOT_MISMATCH**, with the Task-128 SQLite nonexistence result explained by the same wrong-root probe and therefore also a **SQLITE_PATH_OR_STATUS_PROBE_DEFECT** at the acceptance-probe layer rather than a missing authoritative database.

The Task-129 repository commit is report-only and has parent `c97c6f39468f7f4f27efe7a9b44e0761879b0924`, the exact Task-129 activation HEAD. No repository source/runtime change was inserted by the executor.

## Why this is not yet ACCEPTED PASS

Task 129 explicitly required the final report to publish enough evidence for independent review. The report references a local evidence root and artifact names, but omits several required facts from the report itself:

1. exact coordination HEAD observed at execution start;
2. launcher SHA256, size/timestamps, and complete launcher content/bytes;
3. installed `cnxclaw_v093.py`, `cnxclaw.py`, and relevant `host_control_v092.py` hashes/identity, including comparison to the accepted candidate/package where practical;
4. literal authoritative read-only command invocations and captured exit codes;
5. bounded competing-root inventory and which roots, if any, are actually referenced by installed launcher/task/service authority;
6. scheduled-task/service executable, arguments, working directory, state, and last-result authority;
7. relevant non-secret environment overrides affecting workspace/root/config resolution;
8. Task-125 cleanup state versus current controller generation/mode/provider/`updatedAt`, including whether generation advanced and whether any durable transition can be established;
9. detailed controller/runtime/ownership file metadata sufficient to show that the coherent state came from the exact parsed installed root rather than another retained extraction.

The report says these raw files exist locally, but an independent repository review cannot verify their contents from the report as published. The missing publication detail is material because Task 128 itself failed due to an incorrect root-selection probe; the review must therefore be able to trace root authority literally rather than accept another summarized assertion.

## Safety / ledger review

No evidence in the Task-129 repository commit indicates a live mutation. The reported ledger remains consistent with the hard fence:

- Task-128 repaired-harness recovery suite: `0 / 1 launched`;
- Task-129 lifecycle/recovery mutations: `0`;
- crash scenarios: `0`;
- confirmation input: `0`;
- Dashboard semantic Send: `0`.

Preserve those counts. Do not replay Task 128 or manufacture a managed precondition while closing this evidence gap.

## Required next step

Open a **read-only evidence-publication closeout** task. It should primarily consume the already-retained Task-129 evidence root and publish the missing authority chain in a new report. New live probing should be avoided unless a required fact was not retained; if strictly necessary, only deterministic read-only probes equivalent to Task 129 may be used. No lifecycle, recovery, provider, config, process, database-write, cleanup, or normalization action is justified.

If the closeout publishes the required evidence and it corroborates the current Task-129 findings, Task 129 may then be independently accepted and a new separately authorized recovery re-acceptance task may be considered. Until then, no disruptive recovery acceptance or Dashboard durable-delivery task should be opened.
