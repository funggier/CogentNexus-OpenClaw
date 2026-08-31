# Independent Review — CNX-20260828-118 POSIX Installer Provider-Neutrality Alignment

## Verdict

`REJECTED FOR CANDIDATE ADVANCEMENT — CODE REPAIR ACCEPTED; CANONICAL INSTALL DOCUMENTATION/AUTHORITY REMAINS INCONSISTENT`

Task 118 correctly removed provider ownership from `scripts/install.sh`, but the exact candidate `9dfa979e745dbbfeb3e5ea1a584f5285d4fb1852` must not advance to real-Windows lifecycle acceptance yet because the user-facing installation contract and its automated authority test do not yet describe the same responsibility boundary as the implementation.

## Accepted work

The Task-118 TDD sequence is materially valid:

- tests-only RED: `94ae5edfe2f39feae8b16d57beca3585dd7d76dd`;
- production repair: `9dfa979e745dbbfeb3e5ea1a584f5285d4fb1852`;
- `scripts/install.sh` no longer defines/defaults/validates a provider;
- no `--provider` installer API remains;
- no direct Ollama prerequisite remains in the POSIX installer;
- provider-specific install/success text was removed;
- lifecycle handoff is generic `enable` with no provider argument;
- Task-117 PowerShell provider-neutral repair remains intact;
- runtime/provider modules were not broadened or redesigned;
- Task-118 report records full validation, exact-SHA CI, and a new package-proof artifact;
- no live Windows/POSIX mutation or Task-116 replay occurred.

The source implementation therefore now satisfies the responsibility-local installer boundary on both PowerShell and POSIX entry points.

## Blocking finding 1 — canonical installation documentation still mixes installer and runtime responsibilities

At candidate `9dfa979e745dbbfeb3e5ea1a584f5285d4fb1852`, `docs/INSTALL.md` still presents `Ollama installed` as a general installation requirement and states that the installer performs `provider/Gateway preflight`. `docs/INSTALL.th.md` carries the same structure and claim.

Those statements are no longer accurate as installer-owned requirements after Tasks 117/118. Provider runtime requirements may still be documented where runtime readiness is discussed, because current v0.9.3 runtime policy remains provider-aware, but they must not be represented as data/dependencies owned by the installer itself.

The documentation needs a clean distinction such as:

- installer prerequisites: tools actually required by installation itself;
- runtime readiness/current supported provider: provider-specific requirements checked/owned by runtime after generic installation/lifecycle handoff.

This is exactly the responsibility-locality rule recorded in `docs/operations/ROADMAP.md`.

## Blocking finding 2 — canonical POSIX invocation is not established in user-facing install docs

Task 118 reports the provider-free canonical command:

```sh
./scripts/install.sh --workspace "$HOME/.openclaw/workspace"
```

However, current `docs/INSTALL.md` contains only the PowerShell development-candidate installation example. The POSIX canonical invocation is not established there as a user-facing installation contract.

The newly added test initially attempted to find the command in `scripts/install.sh`; during the production repair it was changed to read the Task-118 coordination task document instead. A coordination task is not canonical consumer installation documentation and must not serve as the permanent authority for the public install command.

Therefore the test can currently pass even while the user-facing installation guide lacks the POSIX command it claims to protect.

## Required successor

Open a source-safe documentation/contract task before any live acceptance retry.

The successor should:

1. add a tests-only RED that reads canonical user-facing installation docs, not coordination task files;
2. require provider-neutral PowerShell and POSIX install command shapes;
3. separate installer prerequisites from runtime/provider readiness requirements;
4. remove claims that installer itself performs provider selection/provider-specific preflight;
5. preserve accurate runtime documentation that v0.9.3 currently supports/owns provider policy in the runtime layer;
6. keep both installers unchanged unless a newly demonstrated implementation defect appears;
7. run focused/full validation and exact-SHA CI/package proof again because documentation is part of the candidate identity;
8. stop for independent review before opening a real-Windows lifecycle retry.

## Live boundary

Task 116 remains the latest authoritative live-machine state. No live mutation is authorized by this review.

Do not replay Task 116, do not clean/normalize live residue, and do not send a Dashboard semantic message.
