# CNX-20260907-306 — Full-authority identity and activation preflight

## Disposition

`REWORK_SOURCE_CONTRACT`

Read-only preflight completed against coordination SHA `6dacb999715cd2b190dbc64da7242db9222e3220` and live state captured from `2026-09-07T13:46:04Z` through `2026-09-07T13:49:26Z`. No live activation, installer, lifecycle, scheduler, semantic, durable-state, protected-state, or release mutation occurred.

## Identity and prior staging adjudication

- Task305's five installed controller/Host files were independently hashed. Four matched candidate worktree bytes. `supervisor_quiescence.py` initially differed only because the Windows checkout materialized CRLF; the installed bytes matched the exact Git blob at candidate `113974b1ec28f50506b1fd2dcbd18d37d638f6d7`:
  - installed/Git-blob SHA-256 `d52f51a6aaa4fa8fd8361d684c1cf73462c93b3a083132f769374edcb4dd8d4a`
  - live equals Git blob: `true`
  - normalized worktree difference: CRLF only
- Installed ownership verification returned version `0.9.3` and canonical plugin root `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`.
- Installed plugin fingerprint is `79e9c2a32bea5eaade3a7b30efaeb2584b1e3a3972a4a8a93e8425ffc27160cc`, matching Task278/279's accepted fingerprint. Plugin inventory was `enabled=false`, `status=disabled`.
- The handoff literal `36cd4c800ded28bdb7165fcad6e0bfb48b4e9335` is valid 40-hex but GitHub returned no commit. The historical accepted literal `36cd4c800ded28bdb7165fcad6e0bfb48b4e933b` resolves to that exact commit. Both literals are preserved; the invalid lookup was not silently repaired.
- Task305's installer transcript/backup path was not retained in this session, so staging invocation count and backup creation remain report evidence rather than newly independent byte-level proof. This limitation does not authorize replay.

## Live read-only baseline

- launcher-derived state root: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`
- Host: `passthrough`, generation `62`, selected provider `ollama`
- Supervisor: registered, enabled, Ready, LastTaskResult `0`
- quiescence lease: absent
- Gateway HTTP `200`; Ollama HTTP `200`; Gateway process PID `22644`
- SQLite: one derived database, `pragma integrity_check=ok`
- public checks: delivery `READY`, recovery `READY`; these aggregate results do not override Ticket-specific rows
- live plugin/source owner files `host_v091.py`, `host_delivery.py`, `host_stall_v091.py`, `host_v092.py`, and `host_provider_v092.py` matched current candidate bytes exactly

## Exact durable predicates

Target:

- Ticket `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`
- owner `agent:main:discord:channel:1391855033993138217`, session active, generation `2`
- status `accepted`, response ready, no delivery confirmation
- exact `direct_result` delivery remains `pending`, attempt count `685`
- idempotency key `cnxclaw-direct-result:CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc:g2`
- recovery state `awaiting_delivery`; outbox count `0`

Protected state:

- Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- owner `agent:main:discord:channel:1531199905673252946`, active generation `1`, `session_id=null`
- Ticket `accepted`, `workflow_eligible=0`, `workflow_id=null`, `response_ready_at=null`
- recovery remains `pending/redeliver`; no delivery row

The exact read-only predicate copied from `host_v091.py:477-480` selects the protected Ticket (and a prior sacrificial Ticket) for post-enable `promote_interrupted_direct_v091()`. Thus canonical enable would mutate protected state. It was not invoked.

## Root-cause findings

1. **Global protected mutation on enable.** `host_authority_v091.py:229-234` invokes interrupted-Direct promotion and Supervisor execution after authority commit. `host_v091.py:477-502` has no session-liveness/identity fence and selects the protected row under its current live metadata.
2. **Product-generated redelivery exposure.** Plugin startup processes pending assistant deliveries globally. `host_delivery.py:247-269` may call `chat.inject` after a successful marker absence check. No manual redelivery is needed for this side effect; target attempt `685` is therefore an activation gate.
3. **Incomplete production quiescence.** `host.py:672-680` checks the lease, but composed production overlays do work first: `host_provider_v092.py:436-540` may mutate adapter/provider/recovery state and `host_stall_v091.py:335-358` may claim/recover calls before reaching the base guard.
4. **Lease exception gap.** `host_authority_v091.py:111-126` acquires the lease and runs reconcilers before entering the exception-protected transaction; release is not in an unconditional outer `finally`. A reconciler exception can retain the lease until expiry.

## CI and release gates

- Source candidate `113974b1ec28f50506b1fd2dcbd18d37d638f6d7`: Validate `34123277946`, Windows pack `34123277947`, PS5.1 `34123278045` all succeeded.
- Handoff SHA `4506d6219f9e20a0d043d6561f86d945d0a0ba5a`: Validate `34128750444` was cancelled; its smoke siblings succeeded. This is recorded, not upgraded to PASS.
- Task306 coordination SHA had Validate `34129169549` in progress at the final Task306 query; smoke siblings succeeded. Task306 does not treat pending CI as product acceptance.
- Public release `v0.9.3` already exists and its tag/release target is `26ce64a624255278a3a0266ad38746e0e6ed2e31`.
- `.github/workflows/release.yml` refuses an existing release. Current living docs and validation remain bound to version `0.9.3`; release cannot overwrite the tag and needs a separately resolved aligned version after runtime acceptance.
- Task272 durable lifecycle acceptance remains incomplete. Health and staging cannot close that gate.

## Evidence ledger

External retained root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx-release-20260907T134252Z`.

Critical evidence SHA-256:

- `a10-durable-metadata.json`: `fc21be796d9e592aaa46df1e62b1752219a1146dcc73be05d77f8d3d92a5a052`
- `a11-quiescence-byte-reconciliation.json`: `aefc1522bff5e458dab3b0cc3eeb36b2720e59e350edd55ec51116f56533c842`
- `a16-candidate-literals.json`: `68270f6c3dd880a175023765019ea8666060ca4ceac6bcbd0575f8a369d85405`
- `a17-enable-promotion-predicate.json`: `b5ed18e747fdacc353c94ffa3f125e5d3140ca3c5f7336c2cc104b19cd97090c`
- `a18-host-owner-identity.json`: `4b59ea4a2b4420390b411f79cb809a0653c1cf6e06117584729f13ac114426c8`

Independent auditor additionally reported one corrected read-only quoting error and two corrected missing-path reads; none affected product state.

## Issue register

| Issue | Classification | Product impact | Correction/consequence |
|---|---|---|---|
| candidate literal ending `9335` has no GitHub commit | authority discrepancy | blocks using that source identity | preserve literal; bind history to resolving `933b` only with explicit evidence |
| CRLF worktree hash differed for quiescence module | verifier/EOL issue | none | compared live bytes to Git blob; exact match |
| public health said READY while Ticket-level rows remain unsafe | evidence aggregation gap | blocks enable/release | schema-bound Ticket predicates take precedence |
| protected row selected by enable promotion | product safety failure | definite protected mutation if enable runs | source-only TDD repair required |
| production outer Supervisor not lease-fenced | product safety failure | concurrent writer remains possible | source-only composed-entry RED required |
| lease cleanup lacks unconditional coverage | product safety failure | stale lease possible on classifier error | source-only RED/finally repair required |
| pending target may auto-inject on activation | unresolved semantic side-effect | blocks enable | source-only eligibility fence/adjudication required |
| Task305 raw installer/backup artifacts unavailable | evidence limitation | no independent restaging proof | no retry; retain report-only evidence |
| existing `v0.9.3` release | release provenance conflict | overwrite forbidden | version successor only after acceptance |

## Mutation accounting

```text
read-only installed/live probes: performed
repository coordination writes: report/task/state only
installer/enable/lifecycle/scheduler mutation: 0
semantic send/Delete/cancel/replay/redelivery/disposition: 0
manual SQLite/Ticket/session/transcript/config mutation: 0
protected-state mutation: 0
release/tag/default-branch mutation: 0
force push: 0
```

## Successor

Task307 is a source-only strict-TDD repair for the three proven activation boundaries. It authorizes no live operation. A later activation task may be created only after exact-SHA tests/CI prove the repaired contracts and fresh read-only live predicates are safe.
