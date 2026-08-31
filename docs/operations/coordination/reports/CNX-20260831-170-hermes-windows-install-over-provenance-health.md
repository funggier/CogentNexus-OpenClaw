# CNX-20260831-170 — Windows Install-Over Provenance and Health

## 1. Disposition

**PASS** — The accepted Task-167 repair was installed once through the supported Windows installer path. The installed OpenClaw plugin fingerprint exactly equals the candidate fingerprint computed before installation, OpenClaw remains pinned at `2026.7.1-2`, and independent post-install checks show healthy managed controller, Gateway, Ollama provider, startup adapter, recovery/ownership, delivery, plugin, and SQLite state.

The task hard fence was respected: no semantic Dashboard Send, `chat.inject`, intentional inference/regeneration, manual durable-state mutation, second installer attempt, uninstall/reinstall/reset, or OpenClaw upgrade occurred.

## 2. Objective and acceptance contract

- **Task:** `CNX-20260831-170`
- **Task path:** `docs/operations/coordination/tasks/CNX-20260831-170-hermes-windows-install-over-provenance-health.md`
- **Objective:** Install the accepted Task-167 repair candidate over the existing Windows instance exactly once, then prove package/plugin provenance and healthy post-install state.
- **Active authority:** `WINDOWS_TASK167_ACCEPTED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`
- **Accepted candidate:** `231761fca24c315e90536955d3e384f55e2e232e`
- **Pinned OpenClaw:** `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` / `2026.7.1-2`

Hard fences applied: exactly one supported install-over; no semantic acceptance; no Dashboard Send; no model inference; no manual ticket/result/outbox/delivery/database/transcript mutation; no upgrade, reset, uninstall, clean reinstall, production repair, release/promotion, default/release merge, or force push.

## 3. Authority and starting state

| Item | Evidence |
|---|---|
| Repository | `funggier/CogentNexus-OpenClaw` |
| Branch | `agent/v0.9.3-full-stabilization` |
| Fresh remote HEAD before side effect | `4b336b34117ae08878d510199347fee83c8ad4ff` |
| Fresh remote HEAD verification | `git ls-remote` at `2026-08-30T22:39:08Z` and again immediately before publication; unchanged |
| Active task | `CNX-20260831-170`, read from fresh remote `ACTIVE.md`/`STATUS.md` |
| Report replay fence | Matching Task-170 report absent at remote HEAD before installation |
| Accepted candidate checkout | Fresh isolated checkout, detached at `231761fca24c315e90536955d3e384f55e2e232e` |
| Candidate remote relation | Candidate fetched from GitHub and verified as accepted repair ancestor of coordination tip |
| Local evidence root | `C:\Users\CDQ-P\AppData\Local\Temp\cnx170-evidence-20260830T222719Z` |
| Installed OpenClaw before action | `2026.7.1-2` |
| Installed pre-action fingerprint | `5b23040f26ab1148c44647429cc5eff0ef89505e2f068b72d41d9a5fb0ee02e5` |
| Pre-action controller/provider | managed/running, selected provider `ollama`, provider ready, Gateway reachable |
| Pre-action database | `integrity_check=ok`; tickets `3`; outbox `0`; direct recovery `0`; assistant delivery `0` |

The matching report was still absent at the final pre-publication remote read. No remote race occurred during the install observation.

## 4. Candidate and package provenance

The candidate source checkout was created independently from the live coordination checkout. Candidate product diff from its parent was limited to the accepted repair source/test paths plus the already-authorized coordination report:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts` — modified
- `plugins/cogentnexus-openclaw/src/v167-native-delivery-staging-order.test.ts` — added
- `docs/operations/coordination/reports/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md` — added historical report

Source/package validation:

- `npm ci`: exit `0`
- `npm run plugin:validate`: exit `0`
- `npm pack --json`: valid structured record, filename/version/size validated
- Package: `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`
- Package size: `205860` bytes
- Package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- npm shasum: `ba4b7b5bdca37ded4d29813b0a6bac68b6a57371`
- npm integrity: `sha512-y1LrJGHmuzeW9FkI87Lg3pU6bv1vPw2EgidVAfuXYfHWO1NFk71u/d3QACRwWBhD+N4Wd7qaE355fakkQcQxVg==`
- Packed file count: `184`
- Candidate plugin fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Candidate package copy was retained outside the source/installer deletion roots.

The supported installer regenerated the same package from the frozen checkout. The post-install ownership transaction recorded `expectedReplacementFingerprint` equal to the candidate fingerprint, and the independent installed extension fingerprint matched it exactly. The installer does not retain its transient tarball after extraction, so a second post-extraction tarball byte hash is not available; the repository-supported fingerprint and transaction provenance are the authoritative installed-payload identity.

## 5. Exactly-one installer action

One and only one supported command was launched:

```text
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:\Users\CDQ-P\AppData\Local\Temp\cnx-live-20260830T222539Z\scripts\install.ps1" -Workspace "C:/Users/CDQ-P/.openclaw/workspace"
```

- Wrapper PID: `18088`
- Installer PID: `22052`
- Started: `2026-08-30T22:33:55.6861109Z`
- Installer PID terminated naturally: `2026-08-30T22:47:21.3430166Z`
- Final process observation: `present=false`, `timedOut=false`
- No installer retry, kill, rollback, uninstall, reinstall, reset, or workaround occurred.
- Installer direct parent exit code was not captured because the wrapper intentionally returned without waiting; it is reported as unavailable, not invented.

All seven installer stage starts had matching completes and zero child exit codes:

| Stage | Start UTC | Complete UTC | Exit |
|---|---|---|---:|
| `ticket-db-bootstrap` | `22:36:06.227062Z` | `22:36:06.282080Z` | 0 |
| `plugin-npm-pack` | `22:36:08.114257Z` | `22:36:08.738199Z` | 0 |
| `plugin-rollover-prepare` | `22:36:08.768785Z` | `22:43:23.209080Z` | 0 |
| `plugin-install-local-package` | `22:43:23.210080Z` | `22:43:47.672624Z` | 0 |
| `plugin-disable-post-install` | `22:43:47.674696Z` | `22:43:53.940509Z` | 0 |
| `plugin-rollover-finalize` | `22:43:58.895473Z` | `22:44:02.075118Z` | 0 |
| `owned-runtime-ensure` | `22:44:02.078119Z` | `22:44:02.226802Z` | 0 |

The installer backed up the prior skill generation, installed the package into the canonical extension path, finalized rollover, ensured the owned runtime, restored managed authority, and completed successfully.

## 6. Post-install health and provenance

Independent post-install plugin inventory reported:

- ID: `cogentnexus-openclaw`
- Version: `0.9.3`
- Source: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- `enabled=true`
- `status=loaded`
- `error=null` / no dependency missing
- Installed extension fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

The installed fingerprint equals the frozen candidate fingerprint exactly. OpenClaw CLI and Gateway both remained `2026.7.1-2`; no upstream upgrade was performed.

Post-install `cnxclaw check system`, `check provider ollama`, and Gateway status all exited `0`. System readiness was `READY`, with:

- controller mode `managed`, desired Gateway/provider `running`;
- Gateway reachable/listening on `127.0.0.1:18789`;
- Ollama reachable/healthy/ready, selected model `ollama/qwen3.5:9b`, four models visible;
- startup adapter installed, enabled, `State=Ready`, `LastTaskResult=0`;
- no maintenance marker, healthy supervisor snapshot, no provider recovery incident;
- no pending terminal deliveries and no pending outbox;
- ownership `OWNERSHIP_PRESENT`, expected five new paths, no legacy paths;
- recovery preflight exit `0` and ownership verification exit `0`;
- second 60-second read-only stability observation passed all five checks with exit `0`.

## 7. Durable-state reconciliation

Post-install SQLite read-only evidence:

- DB: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`
- `PRAGMA integrity_check`: `ok`
- Tables: `11`
- `tickets`: `3`
- `ticket_outbox`: `0`
- `cnx_assistant_delivery`: `0`
- `cnx_direct_recovery`: `0`
- `cnx_direct_model_call`: `3`
- `cnx_sessions`: `4`
- `ticket_events`: `21`
- `cnx_synthetic_runs`: `0`

The preflight key counts were tickets `3`, outbox `0`, direct recovery `0`, assistant delivery `0`; they remained unchanged. The installer executed no semantic operation and no manual database/state mutation. The three existing direct model-call rows were not increased by this task.

## 8. Logs, anomalies, and uncertainty

Raw installer streams were preserved separately:

- stdout: `93018` bytes, SHA-256 `5ecd217f2ed0cb8aa6eb492f8be76072b75e51672813785b5ad88e981792bc3e`
- stderr: `928` bytes, SHA-256 `a23ccfd64f36d329417b0182297d02c58d23b9732405b0fc098375666296f626`
- combined evidence construction: `93977` bytes, SHA-256 `737f607ffdb55ffa14aad0c00f8a202ba8545fbed3da76c8ba4b2861d84fb5b6`

Observed anomalies were bounded and non-blocking:

1. The first executor call timed out while the installer was still running. The same PID was polled afterward; it completed naturally. No retry was made.
2. Two initial postflight probes used incorrect subcommand syntax. They were corrected using installed `--help`; only the corrected read-only commands were used for the verdict. No live mutation occurred from either failed probe.
3. Installer stderr contained npm warnings (deprecated package, pending install-script approvals) and a pre-existing configuration warning about the plugin being disabled during the transition. Final inventory independently reported enabled/loaded.
4. Gateway logs contained transient startup WebSocket/Tailscale warnings and recurring external Discord command-cap errors. No CogentNexus-OpenClaw loader `ERROR/FATAL` attributable to this install-over remained; final Gateway and plugin checks were healthy. These external channel warnings are recorded but are not a Task-170 product-loader failure.

## 9. Acceptance matrix

| Criterion | Verdict | Evidence |
|---|---|---|
| Exact accepted candidate and package provenance established before installation | PASS | Candidate `231761f...`; package SHA-256 `8f6d0b...`; fingerprint `e7d7d6...`; `b03/b04/b05` evidence |
| Exactly one supported install-over executed | PASS | PID `22052`; one launch ledger; seven paired zero-exit stages; natural termination |
| No unauthorized retry or lifecycle workaround | PASS | Process observation `d04/d05`; no second installer/uninstall/reset/rollback |
| Installed fingerprint equals candidate fingerprint | PASS | Candidate and extension both `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19` |
| OpenClaw pin preserved | PASS | Gateway/CLI `2026.7.1-2`; pinned commit retained |
| Plugin ID/version enabled and loaded | PASS | Inventory: ID correct, `0.9.3`, `enabled=true`, `status=loaded`, no missing deps |
| Ownership/provenance and launcher/runtime health | PASS | `e14` verify exit 0; `e15` recovery/ownership exit 0; canonical paths and owned Python runtime |
| Controller/Gateway/provider/startup health | PASS | `e05-e10` and second observation `f01-f05`, all exit 0; managed/running/READY |
| Recovery/delivery pending-state proof | PASS | Recovery preflight clean; assistant delivery/outbox/pending terminal delivery all 0 |
| Storage integrity and durable-state reconciliation | PASS | SQLite read-only integrity `ok`; tickets/outbox/recovery/delivery reconciled |
| No semantic Send/model inference/manual semantic mutation | PASS | Hard-fence review; no semantic UI/API invocation; direct model-call count unchanged at 3 |
| No unexplained critical install-over error remains | PASS | Raw stream hashes, paired stage table, bounded log classification, independent healthy post-state |

## 10. Hard-fence compliance

- Authorized mutation performed: exactly one supported Windows install-over of the accepted candidate.
- Other authorized effects: installer-managed backup/rollover, plugin reload, owned runtime ensure, and managed startup restoration.
- Prohibited actions performed: **none**.
- Semantic Dashboard Sends/interactions: `0`.
- Intentional model inference/regeneration requests: `0`.
- Manual DB/state/ticket/result/outbox/transcript mutations: `0`.
- Installer attempts: `1`.
- Uninstall/reinstall/reset/upgrade/force push: `0`.

## 11. Residual unproven items

No required Task-170 criterion remains unproven within the repository-supported provenance/health contract. The transient npm tarball is not retained by the installer after extraction, so installed tarball bytes cannot be independently rehashed after extraction; the exact repository-supported installed fingerprint and rollover transaction expected fingerprint provide the authoritative payload-equivalence proof.

Semantic Dashboard delivery remains intentionally untested and is outside this task.

## 12. Reviewer Verification Packet

| # | Critical claim | Why it matters | Exact evidence | Suggested reviewer check |
|---:|---|---|---|---|
| 1 | Remote authority was Task-170 and report was absent before mutation | Prevents replaying stale authorization | Fresh remote HEAD `4b336b...`; `ACTIVE.md`/`STATUS.md`; report absence check | Read current branch files and confirm Task-170 authorization/report absence in pre-state |
| 2 | Candidate/package binding is exact | Prevents installing an unaccepted or drifted payload | Candidate SHA `231761f...`; package SHA `8f6d0b...`; fingerprint `e7d7d6...`; `b03-b05` | Recompute candidate fingerprint/package record from isolated checkout |
| 3 | Exactly one installer execution completed | Prevents hidden retry or ambiguous lifecycle mutation | `d01`, PID `22052`, `d04/d05`, seven-stage `d07` | Confirm one PID chain, natural termination, all stage pairs and zero exits |
| 4 | Installed payload equals candidate identity | Core provenance gate | `e02` fingerprint and rollover transaction `b96d...` expected fingerprint both `e7d7d6...` | Read installed extension fingerprint and transaction JSON |
| 5 | Plugin is actually loaded/enabled on pinned OpenClaw | Proves runtime compatibility, not just file copy | `e09` and stability `f04`: ID/version/path/enabled/loaded; Gateway `e10/f05` | Inspect the one matching plugin entry and Gateway version |
| 6 | Managed runtime and provider remain healthy | Prevents accepting a broken installation | `e06-e10`, `f01-f05`: system READY, Gateway healthy, Ollama ready, startup Ready | Re-run only read-only status/check commands if needed |
| 7 | Durable state was not manufactured/corrupted | Protects ticket/delivery correctness | Preflight key counts; `d08`: integrity `ok`, tickets 3, outbox/recovery/delivery 0, direct model calls 3 | Compare pre/post key counts and inspect DB only read-only |
| 8 | Hard fence was honored and anomalies are classified | Prevents accidental semantic acceptance | Raw stream hashes, no Send/inference/manual mutation, bounded log classification | Verify no semantic command/API and distinguish external Discord warnings |

## 13. Recommended successor

Stop at Task-170 `PASS` and await ChatGPT review. Do not perform a semantic Dashboard Send or open/execute a successor task from this report; any later semantic reacceptance requires a separate explicit authorization.

## 14. Publication state

- Execution HEAD before report publication: `4b336b34117ae08878d510199347fee83c8ad4ff`
- Report path: `docs/operations/coordination/reports/CNX-20260831-170-hermes-windows-install-over-provenance-health.md`
- Publication commit: to be filled after the report-only commit and verified remote readback.
- Changed-file fence: report path only.
