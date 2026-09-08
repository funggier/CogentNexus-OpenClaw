# CNX-20260907-308 — Exact candidate install and managed activation requalification

## Disposition

`BLOCKED_REVIEW_DEFECT__LEASE_RELEASE_REPLACEMENT_RACE`

The bounded supported install and canonical enable both completed successfully, but the candidate is not accepted for release because an independent fail-closed review found a concrete race in the lease release primitive. No release/version/tag mutation is authorized by this result.

## Authority and exact lineage

- Remote authority before execution: `55b50a065760994cdd8f43681bbf60ae837b2649`
- Active task: `CNX-20260907-308`
- Source candidate: `853650ce7f59687fbce172bd96543a38f288e47a`
- Detached candidate: `C:\\Users\\CDQ-P\\AppData\\Local\\Temp\\cnx-release-20260907T134252Z\\task308-candidate-853650c`
- Candidate version: `0.9.3`
- Candidate plugin fingerprint: `9af4712dd3265afc577a233b4716279901b9eab1128ad6640c63e0ba846f0f33`
- Evidence root: `C:\\Users\\CDQ-P\\AppData\\Local\\Temp\\cnx-release-20260907T134252Z\\task308-evidence-20260907T152731Z`

Candidate CI was terminal-successful before execution:

- Validate `34137033103`
- PS5.1 Acceptance Smoke `34137033075`
- Windows Installer Pack Smoke `34137033014`

The publication coordination commit `55b50a065760994cdd8f43681bbf60ae837b2649` also passed Validate `34138119457`, PS5.1 `34138119383`, and Windows pack `34138119485`.

## Preflight

Fresh read-only preflight at `2026-09-07T15:30:02Z` recorded:

- competing installer/enable writers: `0`
- quiescence lease: absent
- Gateway/Ollama health: HTTP `200` / HTTP `200`
- SQLite integrity: `ok`
- promotion selection for protected Ticket: `false`
- promotion selection for stale target: `false`
- delivery due for protected Ticket: `false`
- delivery due for stale target: `false`
- preflight durable exact hash: `6779f2dcd573526e8aea67bc2499355d2096ab34805906e632cb23835bd42e1f`

The protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and owner session `agent:main:discord:channel:1531199905673252946` were not selected by the repaired predicates.

## Supported installer ledger

The repository-supported `scripts/install.ps1` was launched from the detached candidate exactly once through a file-based PowerShell runner:

- start: `2026-09-07T15:31:00.765Z`
- end: `2026-09-07T15:40:09.943Z`
- inner exit code: `0`
- runner PID: `25096`
- stdout SHA-256: retained in `installer-result.json`
- stderr SHA-256: retained in `installer-result.json`
- no retry or second installer invocation

Post-install identity was exact: installed plugin fingerprint `9af4712d…f0f33`, all seven owner files byte-exact, plugin remained disabled pending canonical enable, and no competing writer remained.

## Canonical enable ledger

The canonical `C:\\Users\\CDQ-P\\.openclaw\\workspace\\cnxclaw.cmd enable` was launched exactly once through a file-based PowerShell runner:

- start: `2026-09-07T15:45:00.621Z`
- end: `2026-09-07T15:47:53.390Z`
- runner PID: `25376`
- exit code: `0`
- invocation count: `1`
- enable stdout SHA-256: `cb2ba6984504016718b8f3e25e68d21f36514b22818ed9c224c2f46d48fca01e`
- enable stderr SHA-256: empty SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The lease observer captured one lease acquisition owned by the enable operation and observed the lease absent at completion. Token plaintext was not retained; only its SHA-256 was retained.

Enable output reported `mode=managed`, healthy Ollama, transactional completion, and protected/stale delivery held. The subsequent status snapshot showed managed generation `66`, Gateway/provider desired state `running`, and no maintenance marker.

## Post-enable and stabilization

Read-only post-enable and observation checks reported:

- plugin `cogentnexus-openclaw`: `enabled=true`, `status=loaded`
- installed fingerprint equals candidate: `9af4712d…f0f33`
- all seven owner files byte-exact
- Gateway health: HTTP `200`
- Ollama health: HTTP `200`
- delivery check: `READY`, pending terminal deliveries `0`
- recovery check: `READY`, maintenance marker absent
- namespace ownership verification: exit `0`
- quiescence lease: absent
- competing installer/enable writers: `0`
- SQLite integrity: `ok`
- durable exact hash remained `6779f2dcd573526e8aea67bc2499355d2096ab34805906e632cb23835bd42e1f`
- protected Ticket/session metadata and target pending-delivery metadata were unchanged
- protected and stale-target promotion/delivery predicates remained false

No semantic send, replay, redelivery, disposition, session cancel, manual SQLite mutation, or protected-state mutation occurred.

## Independent review blocker

The independent fail-closed reviewer returned `passed=false` with no security concerns but one remaining concrete logic error:

`supervisor_quiescence.release()` performs `_read_raw(path)`, validates owner/token, and then `path.unlink()` as separate operations without serializing against `acquire()`. After the old lease expires, another activation can replace the lease between validation and unlink; the old owner can then unlink the new owner's lease. This violates the required invariant that an enable exit releases only its own lease/token.

The reviewer also identified generation-0 and stale-at-promotion-time issues. Those two findings were corrected in the candidate with RED→GREEN coverage before this live run. The release replacement race was not covered and remains a candidate defect.

## Harness/tooling record

- An initial stabilization label `stabilized` was rejected by the retained snapshot script; the supported `observe` label was then run successfully. No live state was changed by the failed probe.
- One installer wait call hit the tool's 420-second wait limit while the installer continued; the original process was not killed or retried, and the runner later produced terminal exit `0` with complete evidence.
- An inactive cron wake record was removed after the local bounded observer completed; no lifecycle component was started to activate the scheduler.
- A read-only probe once used a wrong report filename and once ran `git ls-remote` outside the repository; both were corrected and are classified as harness errors, not product outcomes.

## Required successor

Create the smallest evidence-bound successor for a deterministic RED test of concurrent stale-lease replacement, then implement the minimal operation-lock/atomic ownership repair, run focused and full GREEN validation, obtain independent review, and repeat exact-SHA CI. Because this source candidate has already been installed, a new candidate must receive fresh supported install/enable authority and fresh postflight proof before release. Do not retry either consumed Task308 operation under this task.
