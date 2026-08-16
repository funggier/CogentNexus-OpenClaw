from pathlib import Path

p = Path('plugins/cogentnexus-rotation/src/v090.test.ts')
s = p.read_text(encoding='utf-8')
old = '''      const db=new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='cancelled',failure_class='interrupted' WHERE ticket_id=?").run(ticket.ticketId);
      db.prepare("INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,'cancelled','{}','pending',3,?)")
        .run(ticket.ticketId,"agent:main:dashboard:owner",new Date().toISOString());
      db.prepare("INSERT INTO cnx_direct_recovery(ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,created_at,updated_at) VALUES (?,'resume','pending',10,NULL,?,'connection refused',?,?)")
        .run(ticket.ticketId,new Date().toISOString(),new Date().toISOString(),new Date().toISOString());
      db.close();
'''
new = '''      expect(markDirectRecovery(path,{runId:"old-human",mode:"resume",message:"connection refused"})).toBe(true);
      const db=new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='cancelled',failure_class='interrupted' WHERE ticket_id=?").run(ticket.ticketId);
      db.prepare("INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,'cancelled','{}','pending',3,?)")
        .run(ticket.ticketId,"agent:main:dashboard:owner",new Date().toISOString());
      db.close();
'''
if old not in s:
    raise SystemExit('synthetic delivery fixture block not found')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
