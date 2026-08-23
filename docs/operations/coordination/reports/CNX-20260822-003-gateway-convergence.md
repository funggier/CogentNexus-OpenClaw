# CNX-20260822-003 — Gateway Baseline Convergence Report

- Task ID: `CNX-20260822-003`
- Status: `PASS`
- Executed: 2026-08-22 21:09–21:11 ICT
- Repository path: `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260822-003-gateway-baseline`
- Branch: `codex/CNX-20260822-003`
- Execution HEAD: `648c7adc660c0e5fd71369613d70b5b38b34e7cd`
Report base HEAD: `c1441966586729fca32774234cd887a35dd4c95a`

## Source and isolation gates

- A new dedicated worktree was created for this task. The dirty primary checkout and all predecessor worktrees, including the protected `cogentnexus-v093-test` worktree, were left untouched.
- `git status --short` was empty before runtime actions.
- Required ancestor `306b091352a652a898c353aa49323c8d6a389106` was present (`git merge-base --is-ancestor` exit 0).
- Diagnostic blob matched `fdaa7c49c49e529e791b3ac3db482cd3758ec470`.
- OpenClaw: `2026.7.1-2 (0790d9f)`.
- Ollama: `0.32.13`.

## Read-only baseline classification

The previously reported recovery-verdict/Gateway-health mismatch was no longer present. Before injection:

- `cnx status` reported mode `managed`, desired Gateway/provider `running`, selected provider `ollama`, Gateway `healthy: true`, and runtime running on PID `26384`.
- `cnx provider status --json` reported Ollama selected, reachable, healthy, and ready.
- `cnx check recovery --json` returned verdict `READY`, exit code 0, with no maintenance marker or active provider incident.
- Gateway listened on `127.0.0.1:18789` as `node.exe` PID `26384` with an OpenClaw Gateway command line.
- Ollama listened on `127.0.0.1:11434` as `ollama.exe` PID `12640`.
- Windows `Get-ScheduledTask` displayed `OpenClaw Gateway` adapter state `Ready`; independently, `cnx status` runtime detection reported `running`, connectivity probe `ok`, and the listener/process identity was healthy. Thus recovery verdict `READY` agreed with actual Gateway health.

The authorized pre-injection `cnx start` was not used because the baseline was already healthy.

## Diagnostic execution and result

Executed exactly from the isolated worktree, with `y` supplied only to its explicit confirmation:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-gateway-convergence-windows.ps1 -RunDisruptive
```

- Diagnostic exit code: 0.
- Diagnostic JSON result: `PASS`.
- The target was validated as exact OpenClaw Gateway `node.exe` PID `26384`; the harness PID was `25556`, and the target was not the harness or an ancestor.
- Injection used `Stop-Process -Id 26384 -Force` for that exact PID only. No process-tree kill was used.
- A replacement Gateway listener appeared as a different `node.exe` PID `39108` on port 18789.
- No manual `cnx start`, `cnx stop`, `cnx restart`, or other runtime intervention was issued after injection.
- The first recovery observation was `READY_WITH_WARNINGS` while the intentional maintenance marker was active.
- Natural durable convergence reached `READY` after 8 observations in 14.769 seconds.
- Final state remained MANAGED with Ollama selected; Gateway PID `39108` and Ollama PID `12640` were listening and healthy.

## Evidence

- TXT: `C:\Users\CDQ-P\Downloads\CNX_V093_GATEWAY_CONVERGENCE_20260822-211011.txt`
  - SHA256: `64B8F607461A2B953E9DCAD9112D736EEA141788BBCFC1ABFE553568B45A8713`
- JSON: `C:\Users\CDQ-P\Downloads\CNX_V093_GATEWAY_CONVERGENCE_20260822-211011.json`
  - SHA256: `7C88DDDC18AB23FFD31542A44843B44C628D2C7461C31A29DEEA0C354C673307`

## Cleanup and safety notes

The diagnostic left tracked-file deletion residue in this dedicated worktree. Only this newly created worktree was restored from its unchanged execution HEAD, after validating its absolute path; `git status --short` was then empty. No runtime/source/configuration file was modified, no software was installed or removed, and no unrelated checkout was cleaned, reset, stashed, or altered.

Nothing required by Task 003 remains unproven. Recommended next step: ChatGPT review this PASS report and decide the next coordination state.
