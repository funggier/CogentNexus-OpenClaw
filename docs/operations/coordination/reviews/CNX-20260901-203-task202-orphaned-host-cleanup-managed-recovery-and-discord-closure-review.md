# CNX-20260901-203 Review — Orphaned Host Cleanup / Stale Reset Blocker

Disposition: `ACCEPT_FAIL_PRE_ENABLE_HEALTH__STALE_RESET_FOLLOWUP_REQUIRED`

## Accepted Task-203 result

Task 203 correctly terminated only the exact Task-200/202 orphaned PowerShell root PID `11704` after identity and idle/no-execution-descendant revalidation. The associated console host disappeared as a consequence. No installer replay, broad process kill, enable, reset, uninstall, reinstall, provider change, source mutation, Release mutation, or Discord Send occurred.

The post-cleanup pre-enable gate then found an independent historical lifecycle tree:

- PID `9840`: product-owned Python, `host_control_v092.py --root ... reset --provider ollama`
- child PID `17360`: base/underlying Python, same reset command line

Because this lifecycle tree targets the same CogentNexus state root, Task 203 correctly stopped before the one authorized `enable` and before Discord traffic. Final disposition `FAIL_PRE_ENABLE_HEALTH` is accepted.

## Timing and lineage review

The reset tree creation time reported by Task 203 is `1788186963.6185184`, equivalent to `2026-08-31T14:36:03.618518Z` / `2026-08-31 21:36:03 ICT`.

This predates:

- repaired Task-198 candidate commit `9f4eaa429b2540540e7d6f6c2af99067960e45fb` at `2026-08-31T16:23:31Z`;
- the later Task-200/202 orphan PowerShell root creation by about 1h55m.

Therefore the reset tree is not a child or consequence of the Task-200 install-over.

It is also not the accepted Task-183 reset. Task 183 ran much earlier, exited `0`, emitted `COGENTNEXUS-OPENCLAW RESET: PASS`, completed in about 225 seconds, reached fresh-install MANAGED state, and its post-scan proved no lifecycle residue.

The current evidence is consistent with a separate historical/manual reset invocation. The exact historical human/executor origin and exact internal wait point remain to be adjudicated before cleanup; no stronger causal claim is accepted yet.

## Reset source semantics relevant to follow-up

The reset implementation performs read-only preflight and then blocks on explicit interactive `Continue? [y/N]:` before its destructive mutation sequence. A stale reset process may therefore be waiting before mutation, but Task 203 did not capture its stdin/prompt state, so prompt-wait is a hypothesis rather than a proven fact.

The two-Python shape is not treated as proof of two reset invocations. The product-owned virtual-environment interpreter may delegate to its underlying/base Python; follow-up must classify the tree as one or more logical invocations from command line, creation time, ancestry, and parent/session evidence rather than by process count alone.

## Frozen authorities

- repaired product candidate: `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- installed repaired fingerprint: `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`
- published `v0.9.3` target: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Discord Send budget remains `0 / 1` consumed.

## Successor boundary

A successor task may:

1. revalidate the exact stale reset tree and parent/session lineage read-only;
2. sample CPU/thread/handle and relevant state-file progress;
3. if the exact tree remains stale/idle and no lifecycle progress is occurring, terminate only the identity-fenced reset tree;
4. verify no lifecycle residue remains;
5. invoke installed `cnxclaw.cmd enable` exactly once;
6. only after managed convergence, perform the still-unused single human Discord Send and durable correlation.

It must not rerun reset or installer, terminate by broad process name, mutate product source, or touch the published Release.
