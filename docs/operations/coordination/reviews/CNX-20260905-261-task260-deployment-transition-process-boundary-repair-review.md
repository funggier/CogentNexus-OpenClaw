# CNX-20260905-261 — Independent Review

## Verdict

`ACCEPT_REPAIR__CI_GREEN_VERIFIED__LIVE_SUCCESSOR_ESCALATION`

Task261 is accepted as a correct, minimal, honestly-reported
deployment-transition process-boundary repair. Durable CI PASS is verified
on the exact publication SHA. No live install-over, Gateway restart,
recovery disposition, or semantic send is authorized by this review; the
live successor decision is escalated.

## Exact authority and publication

- Branch: `agent/v0.9.3-full-stabilization`
- Reviewed report commit: `d7cf125393994444178644732d50ffbfb3cb8e03`
- Repair lineage (linear, no rewrite): `5a40a21` (RED test) ->
  `0a03686` (minimal fix) -> `a87c393` (fixture correction) -> `d7cf125`
  (report + coordination state)
- Report blob: `bd656f25a59637c6156b1a9f80970ba1a534d8b6`
- Report raw SHA-256 (LF bytes): `8dd2f786001aee0cd4270c84ab7ee290ce5a7de28e271a24bf4fbb207f6a11f2`
- Public tag: `v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31` (unchanged)
- New source candidate: `a87c3930651eecf4563d5d8bafe897e058bbdfe0`
  (publication tree `d7cf125` adds coordination docs only; source identical)

## CI gate (independently verified via GitHub API)

Publication SHA `d7cf125` is terminal success:

- `PS5.1 Acceptance Smoke` run `33960828088`: success
- `Windows Installer Pack Smoke` run `33960828097`: success
- `Validate` run `33960828083`: success
- 9/9 check-runs `completed success` (npm-pack, package dry-run,
  serializer + six validate matrix jobs).

Failure accounting (honest, no blind rerun): the first `Validate` attempt
failed one job (`windows-latest, 3.14`) with a vitest worker timeout in
`ticket-runtime.test.ts` (285/286 passed) — a harness flake in a file
untouched by this repair, on a tree that was 9/9 green at `a87c393`.
Exactly one bounded rerun of the failed job was executed
(`job 101296144134`, attempt 2, completed success). No other job was
rerun. The conditional review hold is released by this evidence.

## Independent critical-claim checks

1. `host_v091.enable()` calls `runtime_boundary.activate_current_config()`
   immediately after `lifecycle start --provider`, fails closed when the
   boundary is unverified, and returns boundary evidence in the enable
   result. Placement is on the success path, after replacement.
2. `scripts/install.ps1` computes `$expectedPluginFingerprint` from the
   candidate source (`:182/:197-198`, format-validated, fail-closed) and
   enforces case-insensitive equality of the installed fingerprint before
   ownership creation (`:506`). The guard chain is complete.
3. Fixture correction `a87c393` is a single mock line for the new boundary
   dependency — minimal and correctly separated from the product fix.
4. TDD topology is genuine: test-only `5a40a21`, fix `0a03686`,
   fixture fix after authoritative failure, report `d7cf125`.
5. Hard-fence ledger accepted: repair commits touch only tests plus
   `host_v091.py`/`install.ps1`; the report commit touches only
   ACTIVE/STATUS/report. Zero installer starts, Gateway mutations, DB or
   recovery mutations, dispose/replay/redeliver/resend, semantic sends,
   release/tag mutations, or force-push.
6. Candidate consequence accepted: Task259 `d153140...` is reference-only;
   the `a87c393`/`d7cf125` tree is the new candidate. Nothing was copied
   into the live installation.

## Successor boundary and escalation

The repair is complete and reviewed, but no standing authority permits a
live install-over (installer execution, Gateway restart, production
recovery exposure). Per the baton protocol this is a genuine
decision/authority boundary: a live/destructive side effect would exceed
existing explicit authority. This review therefore sets
`WAITING_FOR_CHATGPT` with the decision packet in ACTIVE/STATUS and opens
no live successor.

The pending subject row `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
remains untouched: under the new candidate it is non-due/non-waking by
the 15-minute fence, so deployment alone emits nothing.
