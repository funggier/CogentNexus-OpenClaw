# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK223_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK222_ACCEPTED__PACKAGE_IDENTITY_EQUAL__WINDOWS_INSTALLER_REQUALIFICATION_AUTHORIZED`
Task ID: `CNX-20260902-223`
Parent task: `CNX-20260901-222`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-02 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted installer candidate

Exact source candidate:

`a812f27815b3c87b7ca748dc2dea88f987601f70`

Accepted package identity:

```text
artifact ID: 9810139538
artifact digest: sha256:3164b7770e7d8991691d7bbedced092866c208add72b0c03b4aa3d39d1b50ff0
payload files: 192
payload fingerprint: e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
tar.gz: 88f1c81d5c68da11e7420388a215bf8b72c55a30e7924f24cf6a83b8912a7494
zip: 011aaff51462c47440d973a348b938b12a3c2aadcbbe436acf5d54d9f2ad003d
```

Exact candidate CI:

```text
Validate 33532084137: success
Windows Installer Pack Smoke 33532084225: success
PS5.1 Acceptance Smoke 33532084092: success
```

Task-222 report:

`reports/CNX-20260901-222-static-payload-byte-guard-and-candidate-requalification.md`

Task-222 review:

`reviews/CNX-20260901-222-static-payload-byte-guard-and-candidate-requalification-review.md`

Accepted disposition:

`ACCEPT_PASS_STATIC_BYTE_GUARD__CI_WINDOWS_PAYLOAD_IDENTITY_EQUAL__WINDOWS_INSTALLER_REQUALIFICATION_AUTHORIZED`

Accepted facts:

- genuine fail-open RED commit `31d8383d3340cda1e175045da7f554f102d44fc9` proved static CRLF contamination previously passed package validation;
- final candidate restores guarded package paths to `text eol=lf` and rejects noncanonical static bytes without rewriting them;
- Task-219 generated-`dist` canonicalization remains bounded/generated-only;
- byte-exact fingerprint semantics remain unchanged;
- fresh Windows exact-first build and CI both produced 192 files, zero byte differences, and exact fingerprint `e3bcce04...`;
- tracked Windows status remained clean;
- no live runtime mutation occurred during Task 222.

## Active Task 223

Hermes must execute:

`tasks/CNX-20260902-223-task222-exact-candidate-windows-install-over-requalification.md`

Required high-level boundary:

1. fresh preflight and prove Task-205 recovery remains inert;
2. materialize exact candidate before first working-tree checkout; never materialize branch HEAD then detach backward;
3. reprove exact candidate fingerprint `e3bcce04...` and clean package validation;
4. register one uniquely named temporary Scheduled Task using the direct PowerShell topology qualified by Task 215;
5. configure at least 30 minutes execution time, one-shot/no retry;
6. invoke candidate `scripts/install.ps1` exactly once;
7. observe without interrupting until terminal Task Scheduler evidence;
8. require installer success/complete stage evidence and `LastTaskResult=0` or proven equivalent;
9. clean only the temporary Task-223 task;
10. prove installed fingerprint/source exact candidate and healthy controller/startup/Gateway/Ollama/delivery/recovery/SQLite state;
11. report and stop for independent review.

Do not use the failed detached `Popen` topology from Tasks 212–213.

## Runtime / Discord boundary

Task 223 authorizes exactly one installer invocation and `0 Discord Sends`.

No installer retry, reset/uninstall/fresh reinstall, manual lifecycle repair, manual Gateway restart, manual live plugin/config/SQLite mutation, provider/model substitution, unrelated process kill, source/product edit, Release/tag mutation, or force push is authorized.
