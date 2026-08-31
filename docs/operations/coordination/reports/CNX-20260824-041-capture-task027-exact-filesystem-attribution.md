# CNX-20260824-041 — Capture Task027 Exact Filesystem Attribution

Status: `BLOCKED_NO_DELETE_EVENT_OBSERVED`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Fetched start HEAD: `68b1a9d23b7a3a4845a22869bfd28e7813bbff66`
Target: `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`
Evidence directory: `C:\Users\CDQ-P\AppData\Local\Temp\cnx041-procmon\20260823T231558Z`

## Preflight

- Matching-report duplicate check: exit 128, absent.
- All target Git queries used `GIT_OPTIONAL_LOCKS=0`.
- Target registered/detached at `748b6e7accb22b6bb4a5503c9ac04265f153f9e5`, common repository `C:\Users\CDQ-P\.openclaw\workspace\.git`.
- Prestate: 387 tracked / 5 present / 382 absent; status consisted of 382 `.D` entries only; no staged/non-deletion modified/untracked/sparse/operation/process state.
- Present allowlist: `.gitignore`, `AGENTS.md`, `README.md`, `requirements-dev.txt`, `VERSION`.
- Canonical absent-list SHA256: `6A078DA7D54615B67E0020D978A065171E803B0A0DFE134CE978BB2616B91FB8`.
- Procmon64 SHA256 `78D7148EF5E1472BBCEC02CFD655F5AA789006B65D9990862DD8546ECF6C9AF1`, version 4.1, Authenticode Valid, Microsoft Corporation.
- PMC: 2,051 bytes, SHA256 `61F3BBB57B65F8DC708E66BC15B5B808AB44E9DC770799E8C32ED40724AE6CBC`; bounded structural indicators for exact Task027 path, `FilterRules`, and `DestructiveFilter` were present.
- Zero pre-existing Procmon process/driver/service and no Task041 PML/CSV.

A culture-aware PowerShell `Sort-Object` check initially produced a noncanonical hash; no state changed. Recomputing in Git path order reproduced the accepted canonical hash before any capture or restore.

## Evidence and capture

- Exact NUL pathspec: 382 paths, 21,133 bytes, SHA256 `B98921CDF052AB0048AB6377D284192918B4F52953AB0D5D8DA12E26DDF4DC50`.
- Prestate artifact SHA256 `CB42CE6F89D65721E7D17A822DFE0EAF870AB618C3C6E1AA0FA2A38EC1D6E310`.
- Procmon launch start `2026-08-23T23:16:08.3924827Z`, task-owned PID 49412, ordinary UAC approved by operator.
- Arguments: `/AcceptEula /Quiet /Minimized /LoadConfig <exact-PMC> /BackingFile <exact-PML> /Runtime 600`.
- Capture-active proof: PID 49412 matched the launched elevated process and the exact backing PML initialized to 134,217,728 bytes before restore.
- No `/Terminate`, force termination, process-tree action, or runtime extension occurred. Procmon stopped automatically; zero Procmon processes and zero matching drivers/services were observed after runtime. PML final write `2026-08-23T23:26:13.3498289Z`; the configured runtime was 600 seconds and the later write is the close/finalization boundary.

## Exactly one materialization

The authorized exact command was run once only:

`git -C <Task027> restore --source=HEAD --worktree --pathspec-from-file=<exact-NUL-pathspec> --pathspec-file-nul`

- start `2026-08-23T23:18:28.9625102Z`
- end `2026-08-23T23:18:29.1726988Z`
- exit 0; stdout/stderr empty
- transcript SHA256 `D6685801BC56E904BD6C6FBC883E0B2FD3CE39CE8120923CAA80FDDCE5D3958A`
- restore invocation count: exactly 1

After restore, Task027 was not queried/opened/enumerated until capture and export had fully stopped.

## Offline export and attribution

PML was exported offline with the verified executable using `/NoConnect /OpenLog <PML> /SaveAs <CSV>`. Export ended with zero Procmon processes and no capture driver/service.

- PML: 37,773,040 bytes, SHA256 `CBB00E41ACCF168A14342F9279C0BE354002A033AE18759DFB5E770AA7C8C83F`.
- CSV: 1,669,344 bytes, SHA256 `56C2491BF3AECF7D3ECB586CE9C1628C357DABC00B9E513F048A8473DA9A9B11`.
- Parsed events: 6,906.
- Filter escapes outside exact Task027 root: 0.
- Restore process: `git.exe`, PID 43544, with restore/create/write activity beginning around local `06:18:29`.
- Successful delete/disposition/rename/move-away events: 0.
- Post-restore rows: 1,946, all attributed to `System` PID 4 and limited to write/mapping/flush operations; none was a qualifying destructive operation.
- Event range: local `06:16:10` through `06:20:22`; no relevant filesystem event occurred for the remainder of the bounded capture.
- Attribution summary SHA256 `59AC97E070FD969EF4EBB6E1D83EDAA2AB629349B0476E66CB3C5BAE651305D6`.

No actor can be attributed because the trace contains no successful post-restore destructive event. Presence or timing alone was not converted into causation.

## Poststate

One bounded post-capture target query with `GIT_OPTIONAL_LOCKS=0` at `2026-08-23T23:33:27.6777932Z` found:

- 387 tracked / 387 present / 0 absent;
- present-list SHA256 `8B83307B564F0D14910C61BF351CA071BCF7D9C54323374F3648BB1DACF0BE36`;
- empty absent-list SHA256 `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`;
- porcelain status count 1 (the previously observed stat-cache anomaly class was not further queried because the task permits only one bounded poststate query);
- zero Procmon process and zero matching driver/service.

## Result boundary and safety

Proven: exact filtered capture, no filter escape, exactly one authorized materialization, complete poststate materialization, and absence of any successful destructive event during the 600-second observation.

Unproven: the actor/mechanism that caused earlier mass loss, whether loss recurs outside the bounded window, and the exact meaning of the single poststate status record.

No Task038 access; no second restore; no broad capture; no PMC change; no target stimulation beyond the one authorized restore; no worktree creation/removal/repair/prune; no watcher/Supervisor/task/config change; no retained-evidence cleanup; no CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action; no force action. No external side effect was repeated.

Human decision required: NO.