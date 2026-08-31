import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";

const roots:string[]=[];
afterEach(()=>{for(const root of roots.splice(0)) rmSync(root,{recursive:true,force:true});});

function store(){const root=mkdtempSync(join(tmpdir(),"cnx-session-successor-"));roots.push(root);return new TicketStore(join(root,"tickets.sqlite3"));}

describe("session succession",()=>{
  it("rebinds unfinished tickets and pending terminal delivery to the trusted successor",()=>{
    const tickets=store();
    const accepted=tickets.accept({runId:"run-old",ownerSessionKey:"agent:main:main",prompt:"continue this"});
    const db=new DatabaseSync(tickets.databasePath);
    db.prepare(`INSERT INTO ticket_outbox(ticket_id,owner_session_key,terminal_status,payload_json,delivery_status,delivery_attempts,created_at) VALUES (?,?,?,?,'pending',0,?)`)
      .run(accepted.ticketId,"agent:main:main","completed","{}",new Date().toISOString());
    db.close();
    const rebound=tickets.rebindSessionOwner({fromSessionKey:"agent:main:main",toSessionKey:"agent:main:dashboard:new"});
    expect(rebound.ticketIds).toEqual([accepted.ticketId]);
    expect(rebound.outboxCount).toBe(1);
    expect(tickets.get(accepted.ticketId)?.ownerSessionKey).toBe("agent:main:dashboard:new");
    const verify=new DatabaseSync(tickets.databasePath);
    expect((verify.prepare("SELECT owner_session_key FROM ticket_outbox WHERE ticket_id=?").get(accepted.ticketId) as any).owner_session_key).toBe("agent:main:dashboard:new");
    expect((verify.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id DESC LIMIT 1").get(accepted.ticketId) as any).event_type).toBe("owner_session_rebound");
    verify.close();
  });

  it("does not move a different owner",()=>{
    const tickets=store();
    const accepted=tickets.accept({runId:"run-other",ownerSessionKey:"agent:other:main",prompt:"leave this"});
    const rebound=tickets.rebindSessionOwner({fromSessionKey:"agent:main:main",toSessionKey:"agent:main:dashboard:new"});
    expect(rebound.ticketIds).toEqual([]);
    expect(tickets.get(accepted.ticketId)?.ownerSessionKey).toBe("agent:other:main");
  });
});
