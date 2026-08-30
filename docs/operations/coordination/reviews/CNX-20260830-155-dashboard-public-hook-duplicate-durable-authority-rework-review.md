# CNX-20260830-155 — Dashboard Public-Hook Duplicate Durable-Authority Rework Review

Disposition: `ACCEPT`
Reviewer: `ChatGPT self-review (operator-authorized; not independent)`

## Review scope

Review the Task-155 offline RED -> minimal GREEN -> exact-SHA verification repair that followed Task-154 disposition `REWORK`.

This review is performed under the accepted Task-156 GitHub coordination policy. Because ChatGPT also executed/reported Task 155, this checkpoint is explicitly a **self-review**, not an independent review. Technical evidence requirements are unchanged.

## Evidence reviewed

- Task-155 report:
  `docs/operations/coordination/reports/CNX-20260830-155-dashboard-public-hook-duplicate-durable-authority-rework.md`
- genuine RED commit:
  `232bc2ce3975e076de4214e4742f4a712a3966bb`
- RED Validate workflow:
  `33292884867`
- production repair:
  `1ec8cfc81b8a21a178200c33816427f9abfd31b9`
- report publication:
  `239d743dac82ee515ef9f7f2a8961e5130798506`
- exact-repair Validate:
  `33293037351`
- exact-repair PS5.1 Acceptance Smoke:
  `33293037346`
- exact-repair Windows Installer Pack Smoke:
  `33293037362`
- exact production delta `git diff --check`: exit `0`

## Findings

### 1. Genuine behavior-specific RED exists

The test-only RED proves both Task-154 review blockers against predecessor production behavior:

- repeated same-text public-hook final returned `undefined` instead of reasserting the durable marker-bearing native payload;
- repeated changed-text final returned without reaching the durable text mismatch failure.

The predecessor `v091-dashboard-verified-delivery` suite remained `11/11`, localizing the defect to duplicate public-hook re-observation semantics.

Result: `PASS`.

### 2. Production repair is minimal and correctly restores durable authority

The repair removes the already-owned early return from `reply_payload_sending`, routes every qualifying repeated final through `stageDashboardDirectResult(...)`, and guards first-ownership pulse/log side effects separately.

The pre-existing waiter gate remains single-shot.

Result: `PASS`.

### 3. Same-text duplicate semantics are safe

The strengthened regression proves the second same-text callback returns the same marker-bearing durable native text while keeping one durable direct-result row and one settlement waiter.

Result: `PASS`.

### 4. Changed-text duplicate fails closed

A repeated final with changed text for the same run/generation now re-enters durable authority and throws `durable Dashboard result changed`; the durable row remains singular.

Result: `PASS`.

### 5. Append-capable predecessor path is preserved

The production delta is confined to the public-hook fallback block. The append-capable `reply_dispatch` path was not changed, and its related predecessor delivery tests remain green.

Result: `PASS`.

### 6. Exact-SHA verification is sufficient for the offline repair

On repair SHA `1ec8cfc81b8a21a178200c33816427f9abfd31b9`:

- Task-155 regressions: `2/2` PASS;
- related delivery suite: `11/11` PASS;
- full plugin suite: `51/51` files, `271/271` tests PASS;
- representative Python suite: `469 passed, 33 skipped, 4 subtests passed`;
- TypeScript build/evaluation: PASS;
- `npm audit --omit=dev`: 0 vulnerabilities;
- plugin/schema/DB bootstrap/package-content validation: PASS;
- package dry-run/provenance verification: PASS;
- `git diff --check`: PASS;
- Validate, PS5.1 Acceptance Smoke, and Windows Installer Pack Smoke: all success.

Result: `PASS`.

### 7. Task fence was preserved

Task 155 performed no live Windows/runtime mutation, install/reset/uninstall/reinstall, Dashboard semantic Send, manual durable DB mutation, dependency upgrade, merge/tag/release, or force push.

Result: `PASS`.

## Disposition

`ACCEPT`

Task 155 repairs the Task-154 duplicate durable-authority blocker and is accepted as the repository candidate for the next Phase-P acceptance step.

This review does **not** itself accept Phase P and does not substitute for real-machine evidence that the remaining acceptance sequence may require. The successor must be selected from the current durable Phase-P coordination/operations requirements. If that successor requires actual Windows installation/runtime or Dashboard semantic side effects, it must move to the Hermes/Codex local/live execution lane under the standing escalation policy.
