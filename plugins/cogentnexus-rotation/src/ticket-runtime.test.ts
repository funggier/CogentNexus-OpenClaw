import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketDispatcher } from "./ticket-dispatcher.js";
import { TicketStore } from "./ticket-store.js";

describe("Ticket runtime", () => {
  it("migrates a Phase 0 database without losing its accepted Ticket", () => {
    const root = mkdtempSync(join(tmpdir(),"cnx-migrate-"));
    const path = join(root,"tickets.sqlite3");
    const db = new DatabaseSync(path);
    db.exec(`CREATE TABLE schema_migrations(version INTEGER PRIMARY KEY,applied_at TEXT NOT NULL);
      CREATE TABLE tickets(ticket_id TEXT PRIMARY KEY,request_key TEXT NOT NULL UNIQUE,run_id TEXT NOT NULL,owner_session_key TEXT NOT NULL,
      prompt TEXT NOT NULL,prompt_sha256 TEXT NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
      CREATE TABLE ticket_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT,ticket_id TEXT NOT NULL,event_type TEXT NOT NULL,payload_json TEXT NOT NULL,created_at TEXT NOT NULL);`);
    db.prepare("INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?)").run("OLD-1","key","run","owner","prompt","hash","accepted","2026-01-01","2026-01-01");
    db.close();
    const store = new TicketStore(path);
    store.route("OLD-1",true);
    expect(store.ready()).toEqual([{ticketId:"OLD-1",attemptCount:0,maxAttempts:3}]);
    const check = new DatabaseSync(path,{readOnly:true});
    expect((check.prepare("SELECT version FROM schema_migrations ORDER BY version").all() as any[]).map(x=>x.version)).toEqual([1,2,3,4]);
    check.close();
    rmSync(root,{recursive:true,force:true});
  });

  it("dispatches no more than the configured bound", () => {
    const root = mkdtempSync(join(tmpdir(),"cnx-dispatch-"));
    const store = new TicketStore(join(root,"tickets.sqlite3"));
    for (let i=0;i<3;i++) { const ticket=store.accept({runId:`run-${i}`,ownerSessionKey:"owner",prompt:`work-${i}`}); store.route(ticket.ticketId,true); }
    const launched:string[] = [];
    const claims = new TicketDispatcher(store).dispatch({limit:1,leaseMs:5000,launch:(lease)=>launched.push(lease.ticketId)});
    expect(claims).toHaveLength(1);
    expect(launched).toHaveLength(1);
    expect(store.snapshot().tickets).toMatchObject({accepted:2,running:1});
    rmSync(root,{recursive:true,force:true});
  });

  it("dispatches nothing for a zero or invalid limit and enforces the hard ceiling of 32", () => {
    const root = mkdtempSync(join(tmpdir(),"cnx-dispatch-ceiling-"));
    const store = new TicketStore(join(root,"tickets.sqlite3"));
    for (let i=0;i<35;i++) { const ticket=store.accept({runId:`ceiling-${i}`,ownerSessionKey:"owner",prompt:`work-${i}`}); store.route(ticket.ticketId,true); }
    const dispatcher = new TicketDispatcher(store);
    const launched:string[] = [];
    expect(dispatcher.dispatch({limit:0,leaseMs:5000,launch:(lease)=>launched.push(lease.ticketId)})).toEqual([]);
    expect(dispatcher.dispatch({limit:Number.NaN,leaseMs:5000,launch:(lease)=>launched.push(lease.ticketId)})).toEqual([]);
    expect(dispatcher.dispatch({limit:100,leaseMs:5000,launch:(lease)=>launched.push(lease.ticketId)})).toHaveLength(32);
    expect(launched).toHaveLength(32);
    expect(store.snapshot().tickets).toMatchObject({accepted:3,running:32});
    rmSync(root,{recursive:true,force:true});
  }, 20_000);

  it("requeues launch failures and stops at the retry ceiling", () => {
    const root = mkdtempSync(join(tmpdir(),"cnx-retry-"));
    const store = new TicketStore(join(root,"tickets.sqlite3"));
    const ticket = store.accept({runId:"retry",ownerSessionKey:"owner",prompt:"work",maxAttempts:2});
    store.route(ticket.ticketId,true);
    const dispatcher = new TicketDispatcher(store);
    expect(dispatcher.dispatch({limit:1,leaseMs:5000,launch:()=>{throw new Error("offline")}})).toEqual([]);
    expect(store.snapshot().tickets.waiting).toBe(1);
    expect(dispatcher.dispatch({limit:1,leaseMs:5000,launch:()=>{throw new Error("offline")}})).toEqual([]);
    expect(store.snapshot().tickets.failed).toBe(1);
    const outbox = store.pendingOutbox();
    expect(outbox).toHaveLength(1);
    expect(outbox[0]).toMatchObject({ticketId:ticket.ticketId,terminalStatus:"failed",deliveryAttempts:0});
    rmSync(root,{recursive:true,force:true});
  });

  it.each(["authorization","permanent"] as const)("fails %s errors immediately without retry", (classification) => {
    const root = mkdtempSync(join(tmpdir(),`cnx-${classification}-`));
    const store = new TicketStore(join(root,"tickets.sqlite3"));
    const ticket = store.accept({runId:classification,ownerSessionKey:"owner",prompt:"work",maxAttempts:3});
    store.route(ticket.ticketId,true);
    const lease = store.claim({ticketId:ticket.ticketId,workerId:"worker",leaseMs:5000})!;
    expect(store.failAttempt({...lease,classification,message:"do not retry"})).toBe("failed");
    expect(store.snapshot()).toMatchObject({tickets:{failed:1},pendingOutbox:1});
    expect(store.ready()).toEqual([]);
    expect(store.pendingOutbox()[0]).toMatchObject({ticketId:ticket.ticketId,terminalStatus:"failed",payload:{classification,message:"do not retry"}});
    rmSync(root,{recursive:true,force:true});
  });

  it("creates one idempotent completion outbox and tracks delivery", () => {
    const root = mkdtempSync(join(tmpdir(),"cnx-outbox-"));
    const store = new TicketStore(join(root,"tickets.sqlite3"));
    const ticket = store.accept({runId:"done",ownerSessionKey:"owner",prompt:"work"});
    const lease = store.claim({ticketId:ticket.ticketId,workerId:"worker",leaseMs:5000})!;
    store.complete({...lease,result:{artifact:"ok"}});
    const outbox = store.pendingOutbox();
    expect(outbox).toHaveLength(1);
    expect(outbox[0]).toMatchObject({ticketId:ticket.ticketId,ownerSessionKey:"owner",terminalStatus:"completed",payload:{artifact:"ok"}});
    expect(store.markOutboxFailed(outbox[0].outboxId,"gateway unavailable")).toBe(true);
    expect(store.pendingOutbox()[0].deliveryAttempts).toBe(1);
    expect(store.markOutboxDelivered(outbox[0].outboxId)).toBe(true);
    expect(store.markOutboxDelivered(outbox[0].outboxId)).toBe(false);
    expect(store.snapshot()).toMatchObject({tickets:{completed:1},expiredRunning:0,pendingOutbox:0});
    rmSync(root,{recursive:true,force:true});
  });

  it("rolls back terminal state and evidence when the atomic outbox write fails", () => {
    const root = mkdtempSync(join(tmpdir(),"cnx-outbox-atomic-"));
    const path = join(root,"tickets.sqlite3");
    const store = new TicketStore(path);
    const ticket = store.accept({runId:"atomic",ownerSessionKey:"owner",prompt:"work"});
    const lease = store.claim({ticketId:ticket.ticketId,workerId:"worker",leaseMs:5000})!;
    const db = new DatabaseSync(path);
    db.exec("CREATE TRIGGER reject_terminal_outbox BEFORE INSERT ON ticket_outbox BEGIN SELECT RAISE(ABORT, 'outbox unavailable'); END;");
    db.close();
    expect(() => store.complete({...lease,result:{artifact:"must-not-commit"}})).toThrow(/outbox unavailable/);
    const check = new DatabaseSync(path,{readOnly:true});
    expect(check.prepare("SELECT status,result_json FROM tickets WHERE ticket_id=?").get(ticket.ticketId)).toEqual({status:"running",result_json:null});
    expect((check.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? ORDER BY event_id").all(ticket.ticketId) as any[]).map(x=>x.event_type)).toEqual(["accepted","claimed"]);
    expect(check.prepare("SELECT count(*) AS count FROM ticket_outbox").get()).toEqual({count:0});
    check.close();
    rmSync(root,{recursive:true,force:true});
  });

  it("reports expired running leases in the deterministic operations snapshot", () => {
    const root = mkdtempSync(join(tmpdir(),"cnx-status-"));
    const store = new TicketStore(join(root,"tickets.sqlite3"));
    const ticket = store.accept({runId:"status",ownerSessionKey:"owner",prompt:"work"});
    store.claim({ticketId:ticket.ticketId,workerId:"worker",leaseMs:1000,now:new Date("2026-08-13T00:00:00.000Z")});
    expect(store.snapshot(new Date("2026-08-13T00:00:02.000Z"))).toMatchObject({tickets:{running:1},expiredRunning:1,pendingOutbox:0});
    rmSync(root,{recursive:true,force:true});
  });
});
