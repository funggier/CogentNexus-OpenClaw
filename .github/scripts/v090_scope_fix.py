from pathlib import Path

p = Path('plugins/cogentnexus-rotation/src/v090.ts')
s = p.read_text(encoding='utf-8')

recover_start = s.index('  TicketStore.prototype.recoverUndeliveredDirect=')
recover_end = s.index('  TicketStore.prototype.promotePendingDirectForSession=', recover_start)
recover = s[recover_start:recover_end]
wrong = '''    db.prepare("UPDATE tickets SET failure_class=NULL WHERE status='cancelled' AND failure_class IS NOT NULL").run();
    cancelledOutboxSuppressed=Number(db.prepare("DELETE FROM ticket_outbox WHERE delivery_status='pending' AND ticket_id IN (SELECT ticket_id FROM tickets WHERE status='cancelled')").run().changes);
    terminalRecoverySuppressed=Number(db.prepare("UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=COALESCE(last_error,'terminal ticket fence'),updated_at=? WHERE state<>'cancelled' AND ticket_id IN (SELECT ticket_id FROM tickets WHERE status IN ('completed','failed','cancelled'))").run(stamp).changes);
'''
if wrong not in recover:
    raise SystemExit('mis-scoped terminal fence block not found in recoverUndeliveredDirect')
recover = recover.replace(wrong, '', 1)
s = s[:recover_start] + recover + s[recover_end:]

prepare_start = s.index('export function prepareV090RecoveryState(')
prepare_end = s.index('\nfunction resetStale(', prepare_start)
prepare = s[prepare_start:prepare_end]
needle = '  try{db.exec("BEGIN IMMEDIATE");const rows=db.prepare('
replacement = '''  try{db.exec("BEGIN IMMEDIATE");
    db.prepare("UPDATE tickets SET failure_class=NULL WHERE status='cancelled' AND failure_class IS NOT NULL").run();
    cancelledOutboxSuppressed=Number(db.prepare("DELETE FROM ticket_outbox WHERE delivery_status='pending' AND ticket_id IN (SELECT ticket_id FROM tickets WHERE status='cancelled')").run().changes);
    terminalRecoverySuppressed=Number(db.prepare("UPDATE cnx_direct_recovery SET state='cancelled',active_run_id=NULL,next_attempt_at=NULL,last_error=COALESCE(last_error,'terminal ticket fence'),updated_at=? WHERE state<>'cancelled' AND ticket_id IN (SELECT ticket_id FROM tickets WHERE status IN ('completed','failed','cancelled'))").run(stamp).changes);
    const rows=db.prepare('''
if needle not in prepare:
    raise SystemExit('prepareV090RecoveryState transaction marker not found')
prepare = prepare.replace(needle, replacement, 1)
s = s[:prepare_start] + prepare + s[prepare_end:]

p.write_text(s, encoding='utf-8')
