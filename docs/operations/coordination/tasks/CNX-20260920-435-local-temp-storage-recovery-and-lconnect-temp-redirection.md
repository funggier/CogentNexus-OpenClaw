# CNX-20260920-435 — Local Temp Storage Recovery and LConnect Temp Redirection

Status: `COMPLETE`

Parent: `CNX-20260920-434`

## Trigger

The operator identified severe C: pressure under:

`C:\Users\CDQ-P\AppData\Local\Temp`

WinDirStat showed approximately:

- physical size: `111.47 GiB`;
- logical size: `106.32 GiB`;
- files: more than `3.3 million`.

A fresh LConnect disk probe shortly before cleanup showed C: free space had fallen to:

`18,948,087,808 bytes`

## Read-only inventory

A junction-safe scan was run before mutation.

Result:

- Temp logical size: `109.576 GiB`;
- files: `3,403,807`.

Category attribution:

- `openclaw-plugin-build-*`: `32.4537 GiB`;
- `openclaw-model-catalog-*`: `9.9465 GiB`;
- other `openclaw-*`: `1.0139 GiB`;
- random-dot directories: `33.2369 GiB`;
- other: `32.9196 GiB`.

The random-dot and unrelated Temp groups were not classified as CNX-owned and were deliberately left untouched.

A second exact inventory selected only top-level names beginning with:

- `cnx`
- `openclaw-`

while explicitly excluding the active `Temp\openclaw` log/runtime root.

Exact cleanup inventory:

- top-level entries: `1,408`;
- logical size: `73.275 GiB`;
- files: `3,039,244`.

Inventory artifact:

`T:\CogentNexus\CogentNexus-OpenClaw\diagnostics\TEMP-SPACE-20260920\cnx-openclaw-cleanup-inventory.json`

## Process safety gate

Before deletion, structured process checks found no active:

- node.exe;
- python.exe / pythonw.exe;
- cmd.exe;
- git.exe;

whose command line referenced:

- `C:\Users\CDQ-P\AppData\Local\Temp\cnx*`
- `C:\Users\CDQ-P\AppData\Local\Temp\openclaw-*`

PowerShell matches were confirmed to be self-matches from the LConnect query process itself.

The supported installer had already reached a terminal state and was not using these paths.

## Cleanup

Only inventory-authorized Temp paths were removed.

Guards:

- path must be one direct child of the user Temp root;
- name must begin with `cnx` or `openclaw-`;
- exact `openclaw` root is protected;
- top-level reparse points are rejected;
- no force-killing of processes;
- unrelated Temp trees are not touched.

Result:

- success: `1,408 / 1,408`;
- failures: `0`;
- skipped: `0`;
- estimated logical bytes removed: `73.275 GiB`;
- elapsed: approximately `280.5s`.

Cleanup report:

`T:\CogentNexus\CogentNexus-OpenClaw\diagnostics\TEMP-SPACE-20260920\cnx-openclaw-cleanup-report.json`

## Free-space proof

Before cleanup:

`C: free = 18,948,087,808 bytes`

After cleanup:

`C: free = 103,925,612,544 bytes`

Observed free-space recovery:

approximately `84.98 GB` decimal.

The difference between logical inventory size and physical free-space recovery is expected because NTFS allocation, sparse/compressed data, hard-link/reparse behavior, and concurrent Temp changes need not equal logical byte totals exactly.

Post-cleanup recheck:

- `Temp\cnx*`: `0`
- `Temp\openclaw-*`: `0`

No immediate recreation loop was observed.

## Prevention for the current LConnect work session

Created:

`T:\CogentNexus\CogentNexus-OpenClaw\temp\lconnect`

LConnect process-scope environment now uses:

- `TEMP=T:\CogentNexus\CogentNexus-OpenClaw\temp\lconnect`
- `TMP=T:\CogentNexus\CogentNexus-OpenClaw\temp\lconnect`

This is intentionally process-scoped:

- it affects LConnect and child processes launched after the change;
- it does not modify Windows user or machine TEMP;
- it does not affect unrelated applications.

## Classification

`CNX_OPENCLAW_TEMP_STORAGE_RECOVERY_GREEN`
