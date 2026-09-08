# CNX-20260905-255 — Independent Review

## Verdict

`ACCEPT_BLOCKED_PREFLIGHT_DRIFT__FAIL_CLOSED_CORRECT__IDENTITY_CONTRACT_DEFECT_CANONICAL_VS_CRLF_PROVEN__SUCCESSOR_AUTHORIZED_SEPARATELY`

The executor's `BLOCKED_PREFLIGHT_DRIFT` disposition is accepted. The one-shot
installer was correctly never started. One diagnostic sentence in the report is
rejected and corrected below: the mismatch **is** precisely an LF-vs-CRLF
line-ending variance, proven by exact in-memory reproduction.

## Reviewed authority

- Task: `docs/operations/coordination/tasks/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification.md`
- Report: `docs/operations/coordination/reports/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification.md`
- Report HEAD: `df2cf38b27dbb1c5beefcde6f46739d3cb37f7b9`
- Opening remote HEAD for the task: `7cd240d04f6e4ec6017ca314b7c4c36bdbaf05ee`
- Exact candidate: `6822af464fe7a5cb3f93305d0263dfc86b56ac68`
- Reviewer checkout: fresh isolated clone, `LOCAL_HEAD == REMOTE_HEAD == df2cf38`, clean worktree.

## Independent verification

1. Ancestry: `6822af4` is an ancestor of `df2cf38` (`merge-base --is-ancestor` = true).
   Task254 TDD lineage preserved: `cc4d062 -> e09c2e8 (RED) -> 6822af4 (repair)
   -> 6fe7e19 (report) -> 04cfa3e (review) -> 1da7174/25e54ac/7cd240d (Task255
   open/activate/align) -> df2cf38 (Task255 report)`.
2. Canonical installer identity, reproduced independently from the reviewer clone:
   `git show 6822af4:scripts/install.ps1 | sha256sum`
   = `9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b`.
3. Runner identity: `git show 6822af4:scripts/manifest-streaming-runner.ps1`
   = `729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e`,
   matching the Task255 requirement.
4. Raw GitHub bytes at the exact commit fetched independently
   (`raw.githubusercontent.com/.../6822af4.../scripts/install.ps1`):
   length `31983`, LF-only, SHA-256 `9d53a427...e17b57b`. Matches (2).
5. CRLF-materialization reproduction, in memory, against the exact canonical bytes:
   canonical `31983` bytes, `585` LF lines, zero CR; CRLF conversion
   `b.replace(b'\n', b'\r\n')` yields `32568` bytes (`31983 + 585`) with SHA-256
   exactly `c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`
   — byte-for-byte the Task255 "required" hash. Root cause is therefore proven,
   not hypothesized: the contract hash is the Windows materialized (CRLF) form
   of the same file whose canonical Git form is `9d53a427...`.
6. The report's sentence "This is a real candidate-content mismatch, not a
   line-ending conversion artifact" is factually incorrect and is superseded by
   (5). The fail-closed outcome it supported remains correct; only the
   characterization is corrected. There is no product content drift in
   `scripts/install.ps1` between `e09c2e8` and `6822af4` (empty diff; both hash
   to `9d53a427...`).
7. Exact-candidate CI, re-queried via Checks API for `6822af4`: all nine
   check-runs terminal `success` (`npm-pack 101247485728`, `package dry-run
   101247485892`, `serializer 101247485787`, `validate macos 3.11 101247486008`,
   `macos 3.14 101247486052`, `ubuntu 3.11 101247486003`, `ubuntu 3.14
   101247486019`, `windows 3.11 101247486029`, `windows 3.14 101247486055`).
   HEAD workflows (`33946606241/240/253`) are terminal `success`.
8. Publication integrity: `df2cf38` adds exactly one file at the matching report
   path (`128` insertions, no source/test changes). No release/tag mutation:
   `v0.9.3` remains `26ce64a624255278a3a0266ad38746e0e6ed2e31`.
9. Cardinality / hard fences: `registrations = 0`, `starts = 0`,
   `scripts/install.ps1 starts = 0`, `retries = 0`, `semantic sends = 0`,
   `TaskPresent=False` pre-registration, no manifest frozen for execution. No
   second registration or compensating direct installer start occurred. No
   force-push in the recent coordination chain; no production repair was
   performed inside the executor task.

## Provenance of `c0779d...` (root-cause first)

- First introduction: `8cbbe2d` ("docs: publish task 247 powershell stderr
  repair") recorded "Production file SHA-256: `c0779d...`" — bytes taken from a
  Windows materialized working tree (CRLF), not canonical Git bytes.
- Forwarded without canonical re-proof through Task248 / Task250 / Task252-254
  reports, tasks, and the Task254 independent review (which accepted `c0779d...`
  as the installer identity), into `ACTIVE.md` / `STATUS.md` and the Task255
  contract (`Required installer SHA-256 = c0779d...`).
- The Task254 streaming-runner repair itself (`6822af4`, runner-only diff) never
  touched `scripts/install.ps1`; canonical bytes were stable throughout.

## Contract correction (no hash-swap pass)

- The canonical Git object is the sole installer authority:
  `9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b`.
- `c0779d...` is retained in coordination records only as the known
  CRLF-materialized digest for diagnosis — never as a gate.
- A successor task must require `core.autocrlf=false`, triple proof
  (`git show` + detached working tree + raw GitHub bytes), and dual recording
  of both digests. Simply rewriting the expected hash to `9d53...` without this
  provenance record is forbidden.
- No retry from Task255 is authorized. The successor below is a new authority
  with reconciled identity, not a continuation of the consumed Task255 preflight.

## Successor authorization boundary

Successor `CNX-20260905-256` (new task file in this same publication) may perform
the single exact-candidate install-over with the reconciled canonical gate. It
inherits the Task255 topology, `PT45M` / `AllowHardTerminate=true` contract,
`<=1 / <=1 / <=1 / retry 0 / semantic 0` budget, and fail-closed branches. Even
on installer PASS, semantic acceptance remains a further separate task.

## Effect ledger adjudication

Reviewer performed read-only verification plus four coordination-doc writes
(review + successor task + ACTIVE + STATUS) in one report-only publication
commit. No installer execution, scheduler mutation, lifecycle/DB mutation,
semantic send, replay, release/tag mutation, or force-push was performed or
authorized by this review.
