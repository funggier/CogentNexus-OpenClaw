# CNX-20260918-402 — Production Artifact Identity and Registry-Lineage Reconciliation Report

## Classification

`PRODUCTION_ARTIFACT_IDENTITY_RECONCILED`

The discrepancy is reconciled as a CNX-401 report-local production-identity error, not a production artifact replacement. The established production entry remains `v091-release-entry.js` with SHA-256 `2841b704...c2d95`. `v091-dashboard-verified-delivery.js` exists on disk but is a different 39,760-byte artifact, is not the extension entry declared by the installed package manifest, and has no direct evidence tying it to the Gateway process. CNX-401's OpenClaw mechanism proof remains valid; its production-application metadata required correction.

## Authority and starting identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-402`
- Exact authoritative starting HEAD verified from GitHub: `71a9e2773b3c3f26ca93519f52e35fab1ceea369`
- Expected task starting HEAD: `fe07c5660f765360ace580eb768362908de71b07`
- Discrepancy: the live remote had already advanced by the reviewer-created CNX-402 task and authority updates; local checkout was fast-forwarded to the live tip before investigation.
- Starting gate: `READY_FOR_HERMES`

ACTIVE and STATUS at the live starting tip identify CNX-402 as `READY_FOR_HERMES`. CNX-401, CNX-400, CNX-399, and CNX-398 through CNX-391 were read. No historical report from CNX-360 through CNX-400 was edited.

## Direct production artifact evidence

Read-only hashes and sizes from the installed extension directory:

| Path | SHA-256 | Size | Result |
|---|---|---:|---|
| `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` | `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95` | 8,596 bytes | Established production entry |
| `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-dashboard-verified-delivery.js` | `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98` | 39,760 bytes | Exists, different artifact; not manifest-selected |

A byte comparison returned `cmp_exit=1`; the files are not identical.

The installed package manifest directly declares:

```json
"openclaw": {
  "extensions": ["./dist/v091-release-entry.js"]
}
```

A targeted read-only search found no package/manifest extension reference selecting `v091-dashboard-verified-delivery.js`. The dashboard file therefore cannot be treated as the effective production entry merely because it exists beside the declared entry.

## Historical provenance reconciliation

CNX-360 through CNX-399 consistently identify `dist/v091-release-entry.js` as the installed/effective artifact, with the accepted current baseline hash `2841b704...c2d95` in CNX-375 and subsequent lifecycle/source reports. CNX-400 is the first report in this chain to identify `v091-dashboard-verified-delivery.js` / `1276bd...` as the effective production artifact. CNX-401 copied that CNX-400 identity into its own artifact section.

The direct evidence supports this correction:

- `v091-release-entry.js` is the manifest-selected extension entry.
- `v091-dashboard-verified-delivery.js` is a distinct file and hash.
- No authorized production replacement, rename, copy-over, or deploy was performed in CNX-401.
- No evidence shows that the Gateway process loaded the dashboard file.
- The dashboard filename matches a CogentNexus source/build naming family, but filename similarity is not runtime provenance.

Therefore `1276bd...` is retained as an observed alternate on-disk artifact identity, not reclassified as production. The evidence does not establish when or why that file was present.

## Runtime/PID correlation

Read-only process inspection found PID `27372`:

- Executable: `C:\Program Files\nodejs\node.exe`
- Creation date raw WMI value: `1789596828606`
- Command line: `"C:\Program Files\nodejs\node.exe" C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`

The command line identifies the OpenClaw Gateway launcher but does not expose the loaded extension module path. No debugger, inspector, injection, restart, or mutation was used. Thus the PID evidence is consistent with the established manifest-selected release entry but does not independently expose Node's in-memory module filename. The direct manifest and prior accepted artifact evidence are the authoritative identity mapping available under the fence.

## Correction applied

A minimal correction was applied to the CNX-401 report only:

- The CNX-401 artifact section now identifies `v091-release-entry.js` / `2841b704...c2d95` as the established production artifact.
- It records `v091-dashboard-verified-delivery.js` / `1276bd...` as a distinct observed on-disk artifact whose production use is unproven.
- No OpenClaw source, CogentNexus source, production file, configuration, historical CNX-360–CNX-400 report, main branch, tag, release, or runtime state was changed.

## Impact on CNX-401

The CNX-401 mechanism classification remains unchanged: `REGISTRY_REPLACEMENT_MECHANISM_PROVEN`. Its source proof is based on exact OpenClaw module hashes and is independent of the CogentNexus production entry filename.

The production-application statements are now bounded correctly:

- The registry replacement/cache mechanism is source-proven for the inspected OpenClaw runtime.
- The repeated production `hook-registered` chronology remains inherited from CNX-400, but the CNX-400/CNX-401 artifact identity assertion involving `v091-dashboard-verified-delivery.js` was not supported as the effective manifest-selected production entry.
- The corrected production baseline is `v091-release-entry.js` / `2841b704...c2d95`.
- Registry identity, cache hit/miss, and historical active-object replacement in PID 27372 remain unproven.

No production causality claim should use the dashboard artifact as the runtime identity. CNX-401's mechanism evidence may be used independently; its production correlation must use the corrected release-entry identity and retain the remaining observability gap.

## Direct evidence versus inference

**Direct:** live GitHub starting HEAD; both files' exact hashes and sizes; byte inequality; installed package manifest selecting `v091-release-entry.js`; historical report assertions through CNX-399; PID 27372 executable and command line; and the absence of an authorized production replacement in the CNX-401 execution record.

**Inference/limitation:** the dashboard file may be an alternate, stale, test, or unselected build artifact. Its presence and source-like name do not establish production loading. The PID command line does not reveal Node's loaded extension module path.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production artifact replacement/deploy/rename/copy-over: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair: `0`
- Debugger/inspector attachment: `0`
- Permanent instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-400 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-403 created/started: `0`

## Closeout

After publication, ACTIVE.md and STATUS.md are set to `WAITING_FOR_CHATGPT_REVIEW`. No successor task was created or started.
