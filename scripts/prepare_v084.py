from pathlib import Path
import json
import re

root = Path('.')
version = '0.8.4'
(root / 'VERSION').write_text(version + '\n', encoding='utf-8')

package_path = root / 'plugins/cogentnexus-rotation/package.json'
package = json.loads(package_path.read_text(encoding='utf-8'))
package['version'] = version
package_path.write_text(json.dumps(package, indent=2) + '\n', encoding='utf-8')

manifest_path = root / 'plugins/cogentnexus-rotation/openclaw.plugin.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['version'] = version
props = manifest.get('configSchema', {}).get('properties', {})
if 'autoResume' in props:
    props['autoResume']['description'] = 'Enable bounded Direct recovery after a resumable interruption.'
if 'postCompactionResumeDelayMs' in props:
    props['postCompactionResumeDelayMs']['description'] = 'Delay before the Direct Recovery Guard checks unfinished Direct work after successful compaction.'
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

lock_path = root / 'plugins/cogentnexus-rotation/package-lock.json'
lock = json.loads(lock_path.read_text(encoding='utf-8'))
lock['version'] = version
lock['packages']['']['version'] = version
lock_path.write_text(json.dumps(lock, indent=2) + '\n', encoding='utf-8')

v084_path = root / 'plugins/cogentnexus-rotation/src/v084.ts'
source = v084_path.read_text(encoding='utf-8')
old_query = "SELECT ticket_id,prompt,status FROM tickets WHERE status IN ('waiting','failed') AND workflow_eligible=1 AND workflow_id IS NULL AND failure_class='interrupted' ORDER BY created_at"
new_query = "SELECT ticket_id,prompt,status,workflow_eligible,failure_class,failure_message FROM tickets WHERE status IN ('waiting','failed') AND workflow_id IS NULL AND ((workflow_eligible=1 AND failure_class='interrupted') OR (status='failed' AND workflow_eligible=0 AND failure_class='permanent' AND failure_message='Reply operation aborted by user')) ORDER BY created_at"
if old_query not in source:
    raise SystemExit('v084 migration query anchor not found')
source = source.replace(old_query, new_query, 1)
old_update = "UPDATE tickets SET status='accepted',workflow_eligible=0,worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,response_ready_at=NULL,delivery_confirmed_at=NULL,updated_at=? WHERE ticket_id=? AND workflow_id IS NULL"
new_update = "UPDATE tickets SET status='accepted',workflow_eligible=0,worker_id=NULL,lease_token=NULL,lease_expires_at=NULL,heartbeat_at=NULL,response_ready_at=NULL,delivery_confirmed_at=NULL,delivery_last_error=NULL,result_json=NULL,failure_class='interrupted',updated_at=? WHERE ticket_id=? AND workflow_id IS NULL"
if old_update not in source:
    raise SystemExit('v084 migration update anchor not found')
source = source.replace(old_update, new_update, 1)
old_reason = 'queueRecovery(db,r.ticket_id,"resume",`v0.8.4 reopened ${r.status} Direct Ticket`,stamp);addEvent(db,r.ticket_id,"v084_direct_recovery_reopened",{previousStatus:r.status},stamp);'
new_reason = 'const legacyAbort=r.failure_class==="permanent"&&r.failure_message==="Reply operation aborted by user";const reason=legacyAbort?"v0.8.4 reopened legacy user-aborted Direct Ticket":`v0.8.4 reopened ${r.status} Direct Ticket`;queueRecovery(db,r.ticket_id,"resume",reason,stamp);addEvent(db,r.ticket_id,"v084_direct_recovery_reopened",{previousStatus:r.status,legacyAbort},stamp);'
if old_reason not in source:
    raise SystemExit('v084 migration reason anchor not found')
source = source.replace(old_reason, new_reason, 1)
v084_path.write_text(source, encoding='utf-8')

test_path = root / 'plugins/cogentnexus-rotation/src/v084.test.ts'
tests = test_path.read_text(encoding='utf-8')
anchor = '  it("settles a pending Ticket marker through runtime.subagent", async () => {'
if anchor not in tests:
    raise SystemExit('v084 test insertion anchor not found')
legacy_test = '''  it("reopens the exact v0.8.3 user-aborted Direct misclassification", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v084-legacy-abort-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "legacy-abort", ownerSessionKey: "agent:main:dashboard:test", prompt: "สวัสดี" });
      store.route(ticket.ticketId, false);
      const db = new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='failed',workflow_eligible=0,failure_class='permanent',failure_message='Reply operation aborted by user' WHERE ticket_id=?").run(ticket.ticketId);
      db.prepare("INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,'failed','{}','pending',3,?)")
        .run(ticket.ticketId, "agent:main:dashboard:test", new Date().toISOString());
      db.close();
      const prepared = prepareV084RecoveryState(root, { ticketDatabasePath: path });
      expect(prepared.reopened).toBe(1);
      const verify = new DatabaseSync(path, { readOnly: true });
      expect(verify.prepare("SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status: "accepted", workflow_eligible: 0, failure_class: "interrupted" });
      expect(verify.prepare("SELECT COUNT(*) AS count FROM ticket_outbox WHERE ticket_id=? AND delivery_status='pending'").get(ticket.ticketId))
        .toEqual({ count: 0 });
      expect(verify.prepare("SELECT mode,state,attempt_count FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ mode: "resume", state: "pending", attempt_count: 0 });
      verify.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

'''
if 'reopens the exact v0.8.3 user-aborted Direct misclassification' not in tests:
    tests = tests.replace(anchor, legacy_test + anchor, 1)
test_path.write_text(tests, encoding='utf-8')

baseline_path = root / 'docs/BASELINE.md'
baseline = baseline_path.read_text(encoding='utf-8')
replacement = '''### 8.1 Direct Recovery Guard

A resumable interruption does not, by itself, make lightweight DIRECT work a durable workflow. The original committed Ticket remains the authority for the user's intent.

For managed DIRECT work, aborts, successful compaction with unfinished work, failed delivery, and unconfirmed delivery use the same bounded recovery rule:

1. keep the same Ticket in `accepted` with `workflow_eligible=0` unless independent admission evidence requires STAGED execution;
2. classify the interruption as recoverable and persist retry state in the additive `cnx_direct_recovery` table;
3. wake the exact owner session through an OpenClaw runtime path available to external plugins rather than relying on bundled-only scheduler APIs;
4. use deterministic bounded backoff and idempotency so repeated recovery scans cannot create uncontrolled duplicate turns;
5. inspect the owner transcript/delivery evidence before declaring recovery successful;
6. for dashboard sessions, a fresh persisted assistant response in the bound session is durable delivery evidence; channel-bound sessions request normal OpenClaw delivery;
7. if completed response content is already durable, retry delivery only and do not repeat external side effects;
8. explicit cancellation is terminal and fences recovery from resurrecting abandoned work;
9. only escalate to STAGED/durable workflow execution when the request independently qualifies for it or bounded Direct recovery repeatedly proves insufficient.

Successful history compaction therefore schedules/checks Direct recovery for the same committed intent instead of automatically promoting a simple request into a heavyweight workflow. If the original run continues normally or the Ticket is already terminal, no duplicate recovery is created.

Legacy v0.8.3 Direct Tickets misclassified by the exact OpenClaw error `Reply operation aborted by user` are narrowly migrated back into this recoverable Direct path only when no workflow is linked and admission still classifies the original request as DIRECT.

'''
pattern = re.compile(r'### 8\.1 Post-Compaction Continuation Guard\n.*?(?=## 9\. Session cancellation)', re.S)
baseline, count = pattern.subn(replacement, baseline, count=1)
if count != 1:
    raise SystemExit('BASELINE section 8.1 anchor not found')
baseline = baseline.replace('- **Post-Compaction Continuation Guard** — delayed idempotent fallback that promotes an unfinished DIRECT Ticket into durable recovery only if the original turn becomes silent after successful compaction.', '- **Direct Recovery Guard** — bounded provider-agnostic retry/redelivery for interrupted DIRECT work that preserves the same committed intent before any escalation to STAGED execution.')
baseline_path.write_text(baseline, encoding='utf-8')

readme_path = root / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
readme = readme.replace('**Post-Compaction Continuation Guard** for successful compaction that leaves durable work pending;', '**Direct Recovery Guard** for interrupted, compacted, or delivery-uncertain DIRECT work without automatic promotion to a heavyweight workflow;')
readme_path.write_text(readme, encoding='utf-8')

release_path = root / 'docs/releases/v0.8.4.md'
release_path.write_text('''# CogentNexus v0.8.4

v0.8.4 fixes provider-agnostic DIRECT continuity and session wake failures discovered during real Windows/OpenClaw 2026.7.1 testing of v0.8.3.

## Fixed

- DIRECT interruption no longer automatically promotes a lightweight request into a resource-gated durable workflow.
- The exact OpenClaw failure `Reply operation aborted by user` is treated as recoverable for committed DIRECT work rather than as a permanent loss of intent.
- Recovery and terminal delivery no longer depend on OpenClaw session scheduler APIs that are restricted to bundled plugins; the external CogentNexus bridge uses session-bound runtime subagent execution instead.
- DIRECT retry/redelivery state is persisted in the additive `cnx_direct_recovery` table with deterministic bounded backoff and idempotent run binding.
- Dashboard recovery uses fresh persisted assistant transcript output as delivery evidence, while channel-bound sessions request normal OpenClaw delivery.
- Stale Ticket outbox and workflow completion schedule fences are reset when the Gateway starts so a dead previous process cannot suppress recovery indefinitely.
- Legacy v0.8.3 Tickets carrying the exact `Reply operation aborted by user` misclassification are narrowly reopened only when no workflow is linked and the original request still classifies as DIRECT.

## Validation hardening

- Added regression coverage for DIRECT interruption remaining in the DIRECT lane, legacy interrupted promotions, the exact v0.8.3 user-aborted misclassification, runtime-subagent terminal wake/delivery, dashboard delivery semantics, and deterministic recovery backoff.
- The Validate matrix covers Ubuntu, Windows, and macOS on Python 3.11 and 3.14, plus plugin tests, evaluation, production audit, and OpenClaw plugin validation.
- Windows workflow self-test handles the known detached-controller teardown race with one bounded retry without weakening runtime assertions.

## Compatibility

Existing `.cogent` state remains supported. `cnx_direct_recovery` is additive. Linked durable workflows are not downgraded, arbitrary permanent/authorization/validation failures are not reopened, and explicit cancellation remains terminal.
''', encoding='utf-8')
