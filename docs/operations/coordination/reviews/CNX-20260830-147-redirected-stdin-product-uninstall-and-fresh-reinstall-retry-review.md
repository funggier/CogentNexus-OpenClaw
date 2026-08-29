# CNX-20260830-147 — Independent Review

Disposition: **ACCEPT**

Reviewed: 2026-08-30 ICT
Reviewer: ChatGPT

## Scope

Independent review of:

- Task: `docs/operations/coordination/tasks/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md`
- Report: `docs/operations/coordination/reports/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md`
- Accepted production SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Report publication commit: `c934cd207252adf6a50d9f2fec108298c462e15c`

The publication commit changes only the matching Task-147 report. No product source, configuration, runtime authority, or coordination gate was modified by the executor while publishing the result.

## Findings

Task 147 satisfies the product uninstall + clean fresh-reinstall lifecycle acceptance contract.

1. The non-PTY redirected-stdin harness was qualified first on a harmless `input()` child. Exactly one `y` line was delivered, stdout/stderr were captured, and the child exited `0`.
2. The installed operator-facing `cnxclaw.cmd uninstall` was invoked exactly once. Exactly one lowercase `y` line was written, stdin was closed, the real prompt accepted it, and the process exited `0` with `COGENTNEXUS-OPENCLAW UNINSTALL: PASS`.
3. Product-owned Windows cleanup reached a clean CNX-absent boundary without manual deletion: launcher, CNX state root, workspace skill, plugin root, AppData root, and CNX supervisor task were absent.
4. Native OpenClaw remained installed and healthy and Ollama remained installed/healthy; Dashboard semantic Sends remained `0`.
5. A fresh detached checkout of exact accepted SHA `fb5781c1...` was used for one normal `scripts/install.ps1` invocation. It exited `0` with no retry or helper wrapper.
6. Post-install proof showed one canonical plugin, exact accepted fingerprint/helper hash, newly created ownership manifest, `MANAGED` controller, healthy Gateway/Ollama/recovery/delivery, pending `0`, and SQLite integrity `ok`.
7. The new live durable database contained no historical Task-145/146 records: all reported semantic table counts were `0`.
8. No reset, crash injection, manual semantic/database mutation, manual plugin/controller normalization, alternate installer, release/tag, or Dashboard semantic Send occurred.

## npm audit note

The installer transcript reported four high-severity findings while npm installed/audited the dependency tree. This does not invalidate the Task-147 lifecycle result. The accepted source's repository validation separately includes the production-dependency audit gate (`npm audit --omit=dev`) and had passed at the accepted candidate validation boundary. Treat any remaining audit output as a security-maintenance follow-up, not as evidence that uninstall/fresh reinstall failed.

## Accepted conclusion

The accepted candidate has now proven the real operator-facing clean lifecycle on Windows:

`installed MANAGED -> cnxclaw uninstall + y -> CNX absent/native OpenClaw healthy -> one fresh install -> fresh MANAGED`

Task 147 closes the uninstall + clean fresh-install acceptance gate.

## Still unproven

- real `cnxclaw.cmd reset` with explicit `y` and proof that only CNX state is recreated while program/plugin provenance remains installed;
- final start/stop/restart/disable/enable runtime lifecycle acceptance;
- final real Dashboard durable-delivery acceptance on the clean accepted runtime;
- final candidate freeze/release/distribution smoke.

## Next task

Open the narrowest successor: real Windows `reset` acceptance. Do not seed semantic Ticket/Dashboard data. Prove state recreation through pre/post state-file identity/timestamps and controller/runtime evidence while installed program/plugin provenance remains unchanged.
