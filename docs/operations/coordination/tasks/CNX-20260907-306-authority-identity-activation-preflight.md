# CNX-20260907-306 — Full-authority identity and activation preflight

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-305`
Executor: `Hermes`
Evidence audit: independent isolated read-only agent; not attributed to ChatGPT approval.

## Authority provenance

The operator explicitly instructed Hermes in the current desktop conversation to complete the project through release, decide technical/operational details, create successor tasks and update coordination, perform supported installation/activation/requalification, and release only after all acceptance gates pass. The remote full-authority handoff at `4506d6219f9e20a0d043d6561f86d945d0a0ba5a` records the same prospective authority. This is not a bare continuation and not a claim that ChatGPT accepted Task305. Historical reports/fences remain unchanged. This task records the smallest safe next phase under that newer operator authority.

## Scope and procedure

1. Fresh-read GitHub HEAD, ACTIVE, STATUS, Task305/304/301/302 and Task272-related chain. Independently audit Task305 retained evidence; distinguish reported facts from verified facts.
2. Validate source SHA literals before lookup. Resolve any handoff discrepancy explicitly from Git objects, historical reports and installed payload provenance; never normalize an invalid or nonexistent source identifier.
3. Read installed launcher and derive exact controller/state/runtime roots. Collect read-only recovery-preflight/ownership and file hashes, plugin identity, Host mode, quiescence lease, process/scheduler health, Gateway/Ollama health and SQLite schema/integrity/metadata. Do not read payload bodies or credentials when metadata suffices.
4. Bind target `CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc`, owner `agent:main:discord:channel:1391855033993138217`, generation `2`, idempotency key `cnxclaw-direct-result:CNXT-87fc2030-884f-4943-bb6e-864cc621d5dc:g2`. Determine pending recovery/delivery executable predicates without invoking them.
5. Trace supported enable, config transaction and lease implementation. Prove no competing writer, no protected-state exposure and no unapproved replay before any activation successor. An ambiguous pending delivery blocks activation, not safe offline diagnosis.
6. Inspect exact-SHA Actions, current version/tag/release workflow and release acceptance requirements read-only. Existing v0.9.3 is not permission to overwrite a tag/release.
7. Publish evidence-rich report and the smallest bounded successor based on findings. No live activation occurs within this preflight task. Source repair requires a named successor with genuine RED before implementation.

## Hard fences

Live installer/enable/lifecycle/scheduler mutation budget: 0. Semantic Send/Delete/cancel/replay/redelivery/disposition budget: 0. Manual SQLite/Ticket/session/transcript/config mutation: 0. Release/tag/default-branch promotion: 0. Force push: 0. Protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and owner `agent:main:discord:channel:1531199905673252946` must not be mutated. Preserve prior sacrificial lineage. Read-only metadata comparisons are preservation proof, not authorization to change it.

## Outcomes

`PASS_PREFLIGHT_READY_FOR_BOUNDED_ACTIVATION`, `BLOCKED_IDENTITY`, `BLOCKED_PENDING_DELIVERY_SAFETY`, `REWORK_SOURCE_CONTRACT`, or `BLOCKED_EVIDENCE`. Record each evidence lane independently, every harness error, timestamps, paths/hashes, exact run results and unperformed phases. Final release remains gated; no success claim from staging/health alone.

Report: `docs/operations/coordination/reports/CNX-20260907-306-authority-identity-activation-preflight.md`
