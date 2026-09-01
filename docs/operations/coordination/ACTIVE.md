# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK217_TASK216_CROSS_PLATFORM_PLUGIN_FINGERPRINT_PROVENANCE_ADJUDICATION`
Current disposition: `TASK216_BLOCKED_AUTHORITY_ACCEPTED__CROSS_PLATFORM_PAYLOAD_FINGERPRINT_ADJUDICATION_REQUIRED`
Task ID: `CNX-20260901-217`
Parent task: `CNX-20260901-216`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Task-207 source under adjudication

Exact source commit:

`27fe0181b3b65d555a3a0266ad38746e0e6ed2e31`

Correction / authoritative Task-207 source commit:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Accepted Ubuntu CI payload fingerprint:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

Fresh Windows build fingerprint from Task 216:

`3b86b13f6d39996f18687510ab65aa4bba46bdf8d80b1aaeef14fe8d199eb3ed`

Known preserved old live generation remains:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

## Task 216 reviewed result

Report:

`reports/CNX-20260901-216-task215-direct-scheduled-task-task207-installer-requalification.md`

Review:

`reviews/CNX-20260901-216-task215-direct-scheduled-task-task207-installer-requalification-review.md`

Accepted disposition:

`ACCEPT_BLOCKED_AUTHORITY__CROSS_PLATFORM_PAYLOAD_FINGERPRINT_ADJUDICATION_REQUIRED`

Accepted facts:

- fresh exact `27fe0181...` checkout was clean;
- installer and Task-207 production source hashes matched the candidate;
- Windows `npm ci` and `npm run plugin:validate` passed with packed file count 192;
- Windows repository-supported fingerprint was `3b86b13f...`, not accepted Ubuntu package-proof `d0677581...`;
- no Scheduled Task registration, installer invocation, lifecycle workaround, live SQLite mutation, Gateway restart or Discord traffic occurred;
- Task-207 CI artifact `9790881384` remains available, bound to exact head SHA `27fe0181...`, digest `sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34`, expiring 2026-09-15.

Independent source inspection shows the byte-exact payload fingerprint includes generated `dist/`; package dry-run establishes `d067...` on Ubuntu; Task 216 builds on Windows; `tsconfig.json` does not explicitly define TypeScript `newLine`. Cross-platform generated-byte variance is therefore the active hypothesis, not yet a concluded root cause.

## Active Task 217

Hermes must execute:

`tasks/CNX-20260901-217-task216-cross-platform-plugin-fingerprint-provenance-adjudication.md`

Task 217 is diagnostic/build-only and must:

1. preserve live product state read-only;
2. retrieve/verify retained package-proof artifact `9790881384` and reproduce CI extracted payload fingerprint `d067...` / file count 192;
3. reproduce fresh Windows-default exact-commit fingerprint `3b86...`;
4. compare exact payload path sets and file SHA-256 values file-by-file;
5. perform CRLF/LF byte-normalization analysis for every difference;
6. in an isolated copy, build exact source with explicit TypeScript `--newLine lf` and compute payload identity;
7. determine whether explicit LF makes the Windows payload byte-identical to retained CI `d067...`;
8. publish report and stop.

If newline nondeterminism is proven, a separate TDD Task 218 will canonicalize build output and establish a new repaired candidate before installer requalification resumes.

## Discord budget

Task 217 authorizes `0 Discord Sends`.

## Hard fence

No installer/install-over, no lifecycle command, no OpenClaw plugin/config mutation, no Gateway restart, no ownership/staging/transaction/SQLite mutation, no provider/model substitution, no product source/test/workflow commit, no Release/tag mutation, no force push, and no Discord traffic. Isolated exact-commit build experiments and CI-artifact extraction only.
