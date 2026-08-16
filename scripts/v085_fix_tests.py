from pathlib import Path

root = Path(__file__).resolve().parents[1]
test_path = root / "plugins" / "cogentnexus-rotation" / "src" / "v085.test.ts"
host_delivery_path = root / "skills" / "cogentnexus" / "scripts" / "host_delivery.py"

test = test_path.read_text(encoding="utf-8")
old = '''      const recovery = new DatabaseSync(path, { readOnly: true })
        .prepare(`SELECT r.ticket_id,t.owner_session_key,t.prompt,r.mode,r.attempt_count
          FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id WHERE r.ticket_id=?`)
        .get(ticket.ticketId) as any;
'''
new = '''      const recoveryDb = new DatabaseSync(path, { readOnly: true });
      const recovery = recoveryDb
        .prepare(`SELECT r.ticket_id,t.owner_session_key,t.prompt,r.mode,r.attempt_count
          FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id WHERE r.ticket_id=?`)
        .get(ticket.ticketId) as any;
      recoveryDb.close();
'''
if old not in test:
    raise SystemExit("timeout recovery handle pattern not found")
test = test.replace(old, new, 1)
old = '''      expect(store.pendingOutbox()).toHaveLength(1);
      const db = new DatabaseSync(path, { readOnly: true });
      const queued = db.prepare("SELECT owner_session_key,text,target_json,status FROM cnx_assistant_delivery WHERE kind='compatibility_result'").get() as any;
'''
new = '''      const db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT delivery_status FROM ticket_outbox WHERE outbox_id=?").get(outbox.outboxId))
        .toEqual({ delivery_status: "pending" });
      const queued = db.prepare("SELECT owner_session_key,text,target_json,status FROM cnx_assistant_delivery WHERE kind='compatibility_result'").get() as any;
'''
if old not in test:
    raise SystemExit("scheduled outbox assertion pattern not found")
test = test.replace(old, new, 1)
test_path.write_text(test, encoding="utf-8", newline="\n")

host = host_delivery_path.read_text(encoding="utf-8")
old = '''        except Exception as error:
            mark_failed(root, delivery_id, str(error))
            failed.append({"deliveryId": delivery_id, "error": str(error)})
    return {"delivered": delivered, "failed": failed, "pending": len(pending_deliveries(root, 200))}
'''
new = '''        except Exception as error:
            mark_failed(root, delivery_id, str(error))
            failed.append({"deliveryId": delivery_id, "error": str(error)})
            # Preserve transcript ordering. A later result must not overtake an
            # earlier recovery/status delivery for the same durable queue.
            break
    return {"delivered": delivered, "failed": failed, "pending": len(pending_deliveries(root, 200))}
'''
if old not in host:
    raise SystemExit("Host delivery failure loop pattern not found")
host = host.replace(old, new, 1)
host_delivery_path.write_text(host, encoding="utf-8", newline="\n")
