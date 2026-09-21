import { afterEach, describe, expect, it, vi } from "vitest";
import { DatabaseSync } from "node:sqlite";
import { join } from "node:path";
import { existsSync, mkdirSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { replyDispatchNativeCommandExcluded } from "./ticket-admission-kernel.js";
import {
  enforceOwnerSessionFollowupQueue,
  ownerConversationSessionEligible,
} from "./v095-session-serialization.js";
import { cancelDirectOwnerSessionForAuthoritativeUserStop, isAuthoritativeUserStop, readHostRunTerminalEvidence, resolveHostAgentDatabasePath, scheduleHostRunTerminalReconcile, waitForHostRunTerminalEvidence } from "./v095-host-terminal-evidence.js";
import { TicketStore } from "./ticket-store.js";
import { retireHistoricalNativeCommandTickets } from "./v095-native-command-retirement.js";
import entry from "./index.js";

afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks(); });

function ensureCommandRetirementEvidenceTables(db: DatabaseSync) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS cnx_direct_model_call(
      call_id TEXT PRIMARY KEY,
      ticket_id TEXT
    );
    CREATE TABLE IF NOT EXISTS cnx_inference_attempt(
      attempt_id TEXT PRIMARY KEY,
      ticket_id TEXT
    );
    CREATE TABLE IF NOT EXISTS cnx_assistant_delivery(
      delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_id TEXT,
      status TEXT
    );
    CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY,
      mode TEXT,
      state TEXT
    );
  `);
}

function bestEffortRemove(path: string) {
  try { rmSync(path, { recursive: true, force: true, maxRetries: 10, retryDelay: 50 }); } catch { /* Windows may retain SQLite handles until worker exit. */ }
}

describe("CNX-442 session serialization and terminal truth", () => {
  it.each([
    ["discord", "agent:main:discord:channel:1391855033993138217"],
    ["dashboard", "agent:main:dashboard:main"],
    ["webchat/generic", "agent:main:webchat:conversation-1"],
  ])("bypasses host-native /context before Ticket admission on %s", (_surface, sessionKey) => {
    const cfg = { commands: { native: "auto" } };
    const event = {
      sessionKey,
      ctx: {
        SessionKey: sessionKey,
        InboundEventKind: "slash-command",
        CommandAuthorized: true,
        CommandBody: "/context",
        BodyForAgent: "/context",
        RawBody: "/context",
      },
    };
    expect(replyDispatchNativeCommandExcluded(event, { cfg })).toBe(true);
  });

  it("binds the provisional ingress Ticket at before_agent_run when the host gate precedes reply_dispatch", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-agent-gate-before-reply-dispatch-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const hooks = new Map<string, Array<{ callback:any; options:any }>>();
      const api:any = {
        config:{},
        pluginConfig:{
          ticketFirst:true,
          preInferenceAdmission:true,
          ticketDatabasePath:databasePath,
          autoWorkflowCompletion:false,
          discordActiveTyping:false,
        },
        registerTool:()=>{},
        registerService:()=>{},
        on:(name:string,callback:any,options?:any) => hooks.set(name,[...(hooks.get(name) ?? []),{callback,options:options ?? {}}]),
        logger:{warn:()=>{},error:()=>{},info:()=>{}},
        session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async()=>{}}},
        runtime:{tasks:{managedFlows:{}}},
      };
      entry.register?.(api);

      const beforeDispatch = hooks.get("before_dispatch")?.find((item)=>item.options?.registrationId==="cogentnexus-openclaw-pre-dispatch-ticket-intake")?.callback;
      expect(beforeDispatch).toBeTypeOf("function");
      const sessionKey="agent:main:discord:channel:agent-gate-order";
      const prompt="@Ce first live turn";
      await beforeDispatch({
        messageId:"msg-agent-gate-order",
        content:prompt,
        body:prompt,
        channel:"discord",
        sessionKey,
        senderId:"owner",
      },{
        messageId:"msg-agent-gate-order",
        channelId:"discord",
        accountId:"default",
        conversationId:"agent-gate-order",
        sessionKey,
        senderId:"owner",
      });

      const runId="run-agent-gate-order";
      const beforeAgent = [...(hooks.get("before_agent_run") ?? [])]
        .sort((a,b)=>Number(b.options?.priority ?? 0)-Number(a.options?.priority ?? 0));
      expect(beforeAgent.length).toBeGreaterThan(0);
      let gateResult:any;
      for (const item of beforeAgent) {
        const result=await item.callback({
          prompt,
          messages:[],
          accountId:"default",
          channelId:"discord",
          senderId:"owner",
          senderIsOwner:true,
        },{
          runId,
          sessionKey,
          sessionId:"physical-agent-gate-order",
          workspaceDir:root,
          channel:"discord",
          accountId:"default",
          senderId:"owner",
          inputProvenance:{kind:"external_user",sourceChannel:"discord"},
        });
        if (result?.outcome==="block") { gateResult={...result,priority:item.options?.priority,registrationId:item.options?.registrationId}; break; }
      }
      expect(gateResult).toBeUndefined();

      let db=new DatabaseSync(databasePath,{readOnly:true});
      expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({n:1});
      const row=db.prepare("SELECT ticket_id,run_id,status FROM tickets").get() as any;
      expect(row).toMatchObject({run_id:runId,status:"accepted"});
      expect(db.prepare("SELECT bound_run_id FROM ticket_ingress_claims WHERE ticket_id=?").get(row.ticket_id)).toEqual({bound_run_id:runId});
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='ingress_run_bound'").get(row.ticket_id)).toEqual({n:1});
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='routed'").get(row.ticket_id)).toEqual({n:1});
      db.close();

      const replyDispatch = hooks.get("reply_dispatch")?.find((item)=>item.options?.registrationId==="cogentnexus-openclaw-ticket-first-admission")?.callback;
      expect(replyDispatch).toBeTypeOf("function");
      await replyDispatch({
        runId,
        sessionKey,
        ctx:{
          SessionKey:sessionKey,
          MessageSidFull:"msg-agent-gate-order",
          OriginatingChannel:"discord",
          AccountId:"default",
          BodyForAgent:prompt,
          RawBody:prompt,
          InboundAccessAuthorized:true,
        },
      },{cfg:{},dispatchKind:"agent",dispatcher:{}});

      db=new DatabaseSync(databasePath,{readOnly:true});
      expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({n:1});
      expect(db.prepare("SELECT run_id FROM tickets").get()).toEqual({run_id:runId});
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });


  it("holds a later ingress before Host queue admission until the older direct Ticket is fully completed", async () => {
    const root=mkdtempSync(join(tmpdir(),"cnx442-predispatch-fifo-hold-"));
    try {
      const databasePath=join(root,"tickets.sqlite3");
      const store=new TicketStore(databasePath);
      store.snapshot();
      const sessionKey="agent:main:discord:channel:predispatch-fifo";
      const sessionId="physical-predispatch-fifo";
      const stamp=new Date().toISOString();
      let db=new DatabaseSync(databasePath);
      db.exec("CREATE TABLE IF NOT EXISTS cnx_sessions(session_key TEXT PRIMARY KEY,state TEXT NOT NULL DEFAULT 'active',generation INTEGER NOT NULL DEFAULT 0,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,deleted_at TEXT,delete_reason TEXT,session_id TEXT);");
      db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at,session_id) VALUES (?,'active',4,?,?,?)")
        .run(sessionKey,stamp,stamp,sessionId);
      db.close();

      const hooks=new Map<string,Array<{callback:any;options:any}>>();
      const api:any={
        config:{},
        pluginConfig:{
          ticketFirst:true,
          preInferenceAdmission:true,
          ticketDatabasePath:databasePath,
          autoWorkflowCompletion:false,
          discordActiveTyping:false,
        },
        registerTool:()=>{},
        registerService:()=>{},
        on:(name:string,callback:any,options?:any)=>hooks.set(name,[...(hooks.get(name)??[]),{callback,options:options??{}}]),
        logger:{warn:()=>{},error:()=>{},info:()=>{}},
        session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async()=>{}}},
        runtime:{tasks:{managedFlows:{}}},
      };
      entry.register?.(api);
      const registration=hooks.get("before_dispatch")?.find((item)=>item.options?.registrationId==="cogentnexus-openclaw-pre-dispatch-ticket-intake");
      expect(registration?.callback).toBeTypeOf("function");

      const firstPrompt="@Ce FIFO FIRST";
      await registration!.callback({
        messageId:"msg-fifo-first",content:firstPrompt,body:firstPrompt,channel:"discord",sessionKey,senderId:"owner",
      },{
        messageId:"msg-fifo-first",channelId:"discord",accountId:"default",conversationId:"predispatch-fifo",sessionKey,senderId:"owner",
      });
      db=new DatabaseSync(databasePath,{readOnly:true});
      const firstTicket=(db.prepare("SELECT ticket_id FROM tickets ORDER BY created_at LIMIT 1").get() as any).ticket_id;
      db.close();
      expect(store.bindPendingIngressRun({
        ownerSessionKey:sessionKey,ownerSessionId:sessionId,runId:"run-fifo-first",prompt:firstPrompt,sourceChannel:"discord",
      })).toMatchObject({state:"bound",ticketId:firstTicket});
      store.route(firstTicket,false);

      let settled=false;
      const secondPrompt="@Ce FIFO SECOND";
      const secondPromise=Promise.resolve(registration!.callback({
        messageId:"msg-fifo-second",content:secondPrompt,body:secondPrompt,channel:"discord",sessionKey,senderId:"owner",
      },{
        messageId:"msg-fifo-second",channelId:"discord",accountId:"default",conversationId:"predispatch-fifo",sessionKey,senderId:"owner",
      })).then((result:any)=>{settled=true;return result;});

      await new Promise((resolve)=>setTimeout(resolve,40));
      expect(settled).toBe(false);

      db=new DatabaseSync(databasePath,{readOnly:true});
      const second=db.prepare("SELECT t.ticket_id,t.status,c.bound_run_id,c.owner_generation FROM tickets t JOIN ticket_ingress_claims c ON c.ticket_id=t.ticket_id WHERE c.source_message_id='msg-fifo-second'").get() as any;
      expect(second).toMatchObject({status:"accepted",bound_run_id:null,owner_generation:4});
      db.close();

      expect(store.finalizeDirectRun({
        runId:"run-fifo-first",success:true,interrupted:false,expectsDelivery:false,
      })).toBe("completed");

      await expect(secondPromise).resolves.toBeUndefined();
      db=new DatabaseSync(databasePath,{readOnly:true});
      expect(db.prepare("SELECT bound_run_id FROM ticket_ingress_claims WHERE ticket_id=?").get(second.ticket_id))
        .toEqual({bound_run_id:null});
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });


  it("consumes a held later ingress silently at before_dispatch when authoritative Stop cancels its owner generation", async () => {
    const root=mkdtempSync(join(tmpdir(),"cnx442-predispatch-stop-consume-"));
    try {
      const databasePath=join(root,"tickets.sqlite3");
      const store=new TicketStore(databasePath);
      store.snapshot();
      const sessionKey="agent:main:discord:channel:predispatch-stop";
      const sessionId="physical-predispatch-stop";
      const stamp=new Date().toISOString();
      let db=new DatabaseSync(databasePath);
      db.exec("CREATE TABLE IF NOT EXISTS cnx_sessions(session_key TEXT PRIMARY KEY,state TEXT NOT NULL DEFAULT 'active',generation INTEGER NOT NULL DEFAULT 0,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,deleted_at TEXT,delete_reason TEXT,session_id TEXT);");
      db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at,session_id) VALUES (?,'active',8,?,?,?)")
        .run(sessionKey,stamp,stamp,sessionId);
      db.close();

      const hooks=new Map<string,Array<{callback:any;options:any}>>();
      const api:any={
        config:{},
        pluginConfig:{ticketFirst:true,preInferenceAdmission:true,ticketDatabasePath:databasePath,autoWorkflowCompletion:false,discordActiveTyping:false},
        registerTool:()=>{},
        registerService:()=>{},
        on:(name:string,callback:any,options?:any)=>hooks.set(name,[...(hooks.get(name)??[]),{callback,options:options??{}}]),
        logger:{warn:()=>{},error:()=>{},info:()=>{}},
        session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async()=>{}}},
        runtime:{tasks:{managedFlows:{}}},
      };
      entry.register?.(api);
      const registration=hooks.get("before_dispatch")?.find((item)=>item.options?.registrationId==="cogentnexus-openclaw-pre-dispatch-ticket-intake");
      expect(registration?.callback).toBeTypeOf("function");
      expect(registration?.options?.timeoutMs).toBeUndefined();

      const firstPrompt="@Ce STOP HOLD FIRST";
      await registration!.callback({
        messageId:"msg-stop-hold-first",content:firstPrompt,body:firstPrompt,channel:"discord",sessionKey,senderId:"owner",
      },{
        messageId:"msg-stop-hold-first",channelId:"discord",accountId:"default",conversationId:"predispatch-stop",sessionKey,senderId:"owner",
      });
      db=new DatabaseSync(databasePath,{readOnly:true});
      const firstTicket=(db.prepare("SELECT ticket_id FROM tickets ORDER BY rowid LIMIT 1").get() as any).ticket_id;
      db.close();
      expect(store.bindPendingIngressRun({
        ownerSessionKey:sessionKey,ownerSessionId:sessionId,runId:"run-stop-hold-first",prompt:firstPrompt,sourceChannel:"discord",
      })).toMatchObject({state:"bound",ticketId:firstTicket});
      store.route(firstTicket,false);

      let settled=false;
      const secondPrompt="@Ce STOP HOLD SECOND";
      const secondPromise=Promise.resolve(registration!.callback({
        messageId:"msg-stop-hold-second",content:secondPrompt,body:secondPrompt,channel:"discord",sessionKey,senderId:"owner",
      },{
        messageId:"msg-stop-hold-second",channelId:"discord",accountId:"default",conversationId:"predispatch-stop",sessionKey,senderId:"owner",
      })).then((result:any)=>{settled=true;return result;});

      await new Promise((resolve)=>setTimeout(resolve,40));
      expect(settled).toBe(false);

      const stop:any={state:"terminal",runId:"run-stop-hold-first",status:"interrupted",stopReason:"aborted",aborted:true,externalAbort:true,timedOut:false};
      const cancelled=cancelDirectOwnerSessionForAuthoritativeUserStop({ticketDatabasePath:databasePath,sessionKey,evidence:stop});
      expect(cancelled.state).toBe("cancelled");
      expect(cancelled.generation).toBe(9);

      await expect(secondPromise).resolves.toMatchObject({handled:true});

      db=new DatabaseSync(databasePath,{readOnly:true});
      const rows=db.prepare("SELECT t.ticket_id,t.status,c.source_message_id,c.bound_run_id,c.owner_generation FROM tickets t JOIN ticket_ingress_claims c ON c.ticket_id=t.ticket_id ORDER BY c.rowid").all() as any[];
      expect(rows).toHaveLength(2);
      expect(rows[0]).toMatchObject({status:"cancelled",source_message_id:"msg-stop-hold-first",owner_generation:8});
      expect(rows[1]).toMatchObject({status:"cancelled",source_message_id:"msg-stop-hold-second",bound_run_id:null,owner_generation:8});
      expect(db.prepare("SELECT generation FROM cnx_sessions WHERE session_key=?").get(sessionKey)).toEqual({generation:9});
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("suppresses a cancelled queued ingress at before_agent_run even after Stop advances the owner generation", async () => {
    const root=mkdtempSync(join(tmpdir(),"cnx442-stop-before-agent-run-"));
    try {
      const databasePath=join(root,"tickets.sqlite3");
      const hooks=new Map<string,Array<{callback:any;options:any}>>();
      const api:any={
        config:{},
        pluginConfig:{
          ticketFirst:true,
          preInferenceAdmission:true,
          ticketDatabasePath:databasePath,
          autoWorkflowCompletion:false,
          discordActiveTyping:false,
        },
        registerTool:()=>{},
        registerService:()=>{},
        on:(name:string,callback:any,options?:any)=>hooks.set(name,[...(hooks.get(name)??[]),{callback,options:options??{}}]),
        logger:{warn:()=>{},error:()=>{},info:()=>{}},
        session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async()=>{}}},
        runtime:{tasks:{managedFlows:{}}},
      };
      entry.register?.(api);

      const sessionKey="agent:main:discord:channel:stop-before-agent";
      const sessionId="physical-stop-before-agent";
      {
        const db=new DatabaseSync(databasePath);
        new TicketStore(databasePath).snapshot();
        db.exec(`
          CREATE TABLE IF NOT EXISTS cnx_sessions(
            session_key TEXT PRIMARY KEY,
            state TEXT NOT NULL DEFAULT 'active',
            generation INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            deleted_at TEXT,
            delete_reason TEXT,
            session_id TEXT
          );
        `);
        db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at,session_id) VALUES (?,'active',9,?,?,?)")
          .run(sessionKey,new Date().toISOString(),new Date().toISOString(),sessionId);
        db.close();
      }

      const beforeDispatch=hooks.get("before_dispatch")?.find((item)=>item.options?.registrationId==="cogentnexus-openclaw-pre-dispatch-ticket-intake")?.callback;
      expect(beforeDispatch).toBeTypeOf("function");
      const prompt="@Ce queued work that must be cancelled";
      await beforeDispatch({
        messageId:"msg-stop-before-agent",
        content:prompt,
        body:prompt,
        channel:"discord",
        sessionKey,
        senderId:"owner",
      },{
        messageId:"msg-stop-before-agent",
        channelId:"discord",
        accountId:"default",
        conversationId:"stop-before-agent",
        sessionKey,
        senderId:"owner",
      });

      {
        const db=new DatabaseSync(databasePath);
        const ticket=db.prepare("SELECT ticket_id FROM tickets").get() as any;
        db.prepare("UPDATE tickets SET status='cancelled',failure_message=?,updated_at=? WHERE ticket_id=?")
          .run("Reply operation aborted by user",new Date().toISOString(),ticket.ticket_id);
        db.prepare("UPDATE cnx_sessions SET generation=10,updated_at=? WHERE session_key=?")
          .run(new Date().toISOString(),sessionKey);
        db.close();
      }

      const runId="run-must-not-reach-model";
      const beforeAgent=[...(hooks.get("before_agent_run")??[])]
        .sort((a,b)=>Number(b.options?.priority??0)-Number(a.options?.priority??0));
      let gateResult:any;
      for(const item of beforeAgent){
        const result=await item.callback({
          prompt,
          messages:[],
          accountId:"default",
          channelId:"discord",
          senderId:"owner",
          senderIsOwner:true,
        },{
          runId,
          sessionKey,
          sessionId,
          workspaceDir:root,
          channel:"discord",
          accountId:"default",
          senderId:"owner",
          inputProvenance:{kind:"external_user",sourceChannel:"discord"},
        });
        if(result?.outcome==="block"){gateResult={...result,priority:item.options?.priority};break;}
      }
      expect(gateResult).toMatchObject({outcome:"block",category:"cnxclaw_cancelled_ingress",priority:2000});

      const db=new DatabaseSync(databasePath,{readOnly:true});
      expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({n:1});
      const ticket=db.prepare("SELECT ticket_id,status FROM tickets").get() as any;
      expect(ticket.status).toBe("cancelled");
      expect(db.prepare("SELECT bound_run_id,owner_session_id FROM ticket_ingress_claims WHERE ticket_id=?").get(ticket.ticket_id))
        .toEqual({bound_run_id:runId,owner_session_id:sessionId});
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='ingress_run_suppressed'").get(ticket.ticket_id)).toEqual({n:1});
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("persists a provisional Ticket at before_dispatch and atomically binds it to the actual run at reply_dispatch", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-predispatch-durable-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const hooks = new Map<string, any[]>();
      const api: any = {
        config: {},
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);

      const beforeDispatch = hooks.get("before_dispatch")?.[0];
      expect(beforeDispatch).toBeTypeOf("function");
      const sessionKey = "agent:main:discord:channel:42";
      await beforeDispatch({
        messageId:"msg-queued-42",
        content:"@Ce queued followup",
        body:"@Ce queued followup",
        channel:"discord",
        sessionKey,
        senderId:"owner-42",
        isGroup:true,
      }, {
        messageId:"msg-queued-42",
        channelId:"discord",
        accountId:"default",
        conversationId:"42",
        sessionKey,
        senderId:"owner-42",
      });

      let db = new DatabaseSync(databasePath, { readOnly:true });
      const first = db.prepare("SELECT ticket_id,run_id,owner_session_key,prompt,status FROM tickets").get() as any;
      expect(first).toMatchObject({ owner_session_key:sessionKey, prompt:"@Ce queued followup", status:"accepted" });
      expect(first.run_id).toMatch(/^ingress:/u);
      expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({n:1});
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='routed'").get(first.ticket_id)).toEqual({n:0});
      db.close();

      const replyDispatch = hooks.get("reply_dispatch")?.[0];
      expect(replyDispatch).toBeTypeOf("function");
      const actualRunId = "run-followup-queued";
      await replyDispatch({
        runId:actualRunId,
        sessionKey,
        ctx: {
          SessionKey:sessionKey,
          MessageSidFull:"msg-queued-42",
          OriginatingChannel:"discord",
          AccountId:"default",
          BodyForAgent:"@Ce queued followup",
          RawBody:"@Ce queued followup",
          InboundAccessAuthorized:true,
        },
      }, { cfg:{}, dispatchKind:"agent", dispatcher:{} });

      db = new DatabaseSync(databasePath, { readOnly:true });
      expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({n:1});
      expect(db.prepare("SELECT ticket_id,run_id FROM tickets").get()).toEqual({ticket_id:first.ticket_id,run_id:actualRunId});
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='ingress_run_bound'").get(first.ticket_id)).toEqual({n:1});
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='routed'").get(first.ticket_id)).toEqual({n:1});
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("suppresses a dequeued followup whose provisional Ticket was cancelled before execution", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-cancelled-before-dequeue-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const hooks = new Map<string, any[]>();
      const api: any = {
        config: {},
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const beforeDispatch = hooks.get("before_dispatch")?.[0];
      const replyDispatch = hooks.get("reply_dispatch")?.[0];
      expect(beforeDispatch).toBeTypeOf("function");
      expect(replyDispatch).toBeTypeOf("function");

      const sessionKey="agent:main:discord:channel:stop-queue";
      await beforeDispatch({
        messageId:"msg-stop-queued",
        content:"@Ce queued then stopped",
        body:"@Ce queued then stopped",
        channel:"discord",
        sessionKey,
        senderId:"owner",
      }, {
        messageId:"msg-stop-queued",
        channelId:"discord",
        accountId:"default",
        conversationId:"stop-queue",
        sessionKey,
        senderId:"owner",
      });

      let db=new DatabaseSync(databasePath);
      const provisional=db.prepare("SELECT ticket_id FROM tickets").get() as any;
      db.prepare("UPDATE tickets SET status='cancelled',failure_message='Reply operation aborted by user' WHERE ticket_id=?")
        .run(provisional.ticket_id);
      db.close();

      const result=await replyDispatch({
        runId:"actual-run-after-stop",
        sessionKey,
        ctx:{
          SessionKey:sessionKey,
          MessageSidFull:"msg-stop-queued",
          OriginatingChannel:"discord",
          AccountId:"default",
          BodyForAgent:"@Ce queued then stopped",
          RawBody:"@Ce queued then stopped",
          InboundAccessAuthorized:true,
        },
      }, {cfg:{},dispatchKind:"agent",dispatcher:{}});
      expect(result).toMatchObject({handled:true,queuedFinal:false});

      db=new DatabaseSync(databasePath,{readOnly:true});
      expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({n:1});
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(provisional.ticket_id)).toEqual({status:"cancelled"});
      expect(db.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='ingress_run_suppressed'").get(provisional.ticket_id)).toEqual({n:1});
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("pre-dispatch intake bypasses recognized native commands and requires a stable source message identity", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-predispatch-bypass-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const hooks = new Map<string, any[]>();
      const api: any = {
        config: { commands:{ native:"auto" } },
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const beforeDispatch = hooks.get("before_dispatch")?.[0];
      expect(beforeDispatch).toBeTypeOf("function");

      await beforeDispatch({
        messageId:"msg-native",
        content:"/context",
        body:"/context",
        channel:"discord",
        sessionKey:"agent:main:discord:channel:1",
        senderId:"owner-42",
      }, { channelId:"discord", sessionKey:"agent:main:discord:channel:1", messageId:"msg-native", senderId:"owner-42" });

      await beforeDispatch({
        content:"ordinary message with no source id",
        body:"ordinary message with no source id",
        channel:"webchat",
        sessionKey:"agent:main:webchat:1",
      }, { channelId:"webchat", sessionKey:"agent:main:webchat:1" });

      if (existsSync(databasePath)) {
        const db = new DatabaseSync(databasePath, { readOnly:true });
        expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({n:0});
        db.close();
      }
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not create a Ticket when reply_dispatch receives an authorized native command", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-command-bypass-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const hooks = new Map<string, any[]>();
      const api: any = {
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const admission = hooks.get("reply_dispatch")?.[0];
      expect(admission).toBeTypeOf("function");
      const sessionKey = "agent:main:dashboard:main";
      await admission({
        runId: "command-run",
        sessionKey,
        ctx: {
          SessionKey: sessionKey,
          InboundEventKind: "slash-command",
          CommandAuthorized: true,
          CommandBody: "/context",
          BodyForAgent: "/context",
          RawBody: "/context",
          InboundAccessAuthorized: true,
        },
      }, { cfg: {}, dispatchKind: "agent", dispatcher: {} });
      if (existsSync(databasePath)) {
        const db = new DatabaseSync(databasePath, { readOnly: true });
        expect(db.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({ n: 0 });
        db.close();
      }
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not treat unknown slash-looking conversational text as a native command without host command facts", () => {
    const event = {
      sessionKey: "agent:main:dashboard:main",
      ctx: {
        SessionKey: "agent:main:dashboard:main",
        InboundEventKind: "message",
        CommandAuthorized: false,
        BodyForAgent: "/this-is-user-text please explain it",
        RawBody: "/this-is-user-text please explain it",
      },
    };
    expect(replyDispatchNativeCommandExcluded(event, { cfg: {} })).toBe(false);
  });

  it("applies followup queue policy through the supported OpenClaw session API without channel special-casing", async () => {
    const entries = new Map<string, any>([
      ["agent:main:discord:channel:1", { sessionId: "d1", queueMode: "steer" }],
      ["agent:main:dashboard:main", { sessionId: "w1" }],
      ["agent:main:webchat:conversation-1", { sessionId: "x1", queueMode: "collect" }],
    ]);
    const patches: string[] = [];
    const sessionApi = {
      resolveStorePath: (_store?: string, opts?: { agentId?: string }) => `/state/agents/${opts?.agentId}/agent/openclaw-agent.sqlite`,
      getSessionEntry: ({ sessionKey }: { sessionKey: string }) => entries.get(sessionKey),
      patchSessionEntry: async ({ sessionKey, update }: any) => {
        const current = entries.get(sessionKey);
        const patch = await update(current, { existingEntry: current });
        entries.set(sessionKey, { ...current, ...patch });
        patches.push(sessionKey);
        return entries.get(sessionKey);
      },
    };
    const api: any = { runtime: { agent: { session: sessionApi } } };

    for (const key of entries.keys()) {
      expect(ownerConversationSessionEligible(key)).toBe(true);
      await expect(enforceOwnerSessionFollowupQueue(api, key)).resolves.toMatchObject({ state: "updated", queueMode: "followup" });
      expect(entries.get(key).queueMode).toBe("followup");
    }
    expect(patches).toEqual([...entries.keys()]);
  });

  it("does not apply owner followup serialization to subagent/internal session keys", () => {
    expect(ownerConversationSessionEligible("agent:main:subagent:worker-1")).toBe(false);
    expect(ownerConversationSessionEligible("agent:main:cron:job-1")).toBe(false);
    expect(ownerConversationSessionEligible("agent:main:cogent-rotate-task")).toBe(false);
  });

  it("retires only stranded historical native-command Tickets with zero execution or delivery evidence", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-native-retirement-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const old = new Date("2026-09-20T07:36:00Z");
      const a = store.accept({ runId:"run-context", ownerSessionKey:"agent:main:discord:channel:1", prompt:"/context" });
      store.route(a.ticketId, false, old);
      const b = store.accept({ runId:"run-context-detail", ownerSessionKey:"agent:main:dashboard:main", prompt:"/context detail" });
      store.route(b.ticketId, false, old);
      const ordinary = store.accept({ runId:"run-ordinary", ownerSessionKey:"agent:main:webchat:1", prompt:"/this-is-user-text please explain it" });
      store.route(ordinary.ticketId, false, old);

      const db = new DatabaseSync(databasePath);
      ensureCommandRetirementEvidenceTables(db);
      db.prepare("UPDATE tickets SET created_at=?,updated_at=? WHERE ticket_id IN (?,?,?)")
        .run(old.toISOString(),old.toISOString(),a.ticketId,b.ticketId,ordinary.ticketId);
      db.close();

      const result = retireHistoricalNativeCommandTickets({
        ticketDatabasePath: databasePath,
        cfg: { commands:{ native:"auto" } },
        now: new Date("2026-09-20T07:40:00Z"),
        minAgeMs: 60_000,
      });
      expect(result).toMatchObject({ retired:2, skippedForEvidence:0, schemaReady:true });

      const check = new DatabaseSync(databasePath, { readOnly:true });
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(a.ticketId)).toEqual({status:"cancelled"});
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(b.ticketId)).toEqual({status:"cancelled"});
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ordinary.ticketId)).toEqual({status:"accepted"});
      expect(check.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE event_type='native_command_ticket_retired'").get()).toEqual({n:2});
      check.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not retire a native-command Ticket once execution evidence exists", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-native-evidence-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const old = new Date("2026-09-20T07:36:00Z");
      const ticket = store.accept({ runId:"run-context-evidence", ownerSessionKey:"agent:main:discord:channel:1", prompt:"/context" });
      store.route(ticket.ticketId, false, old);

      const db = new DatabaseSync(databasePath);
      ensureCommandRetirementEvidenceTables(db);
      db.prepare("UPDATE tickets SET created_at=?,updated_at=? WHERE ticket_id=?")
        .run(old.toISOString(),old.toISOString(),ticket.ticketId);
      db.prepare("INSERT INTO cnx_direct_model_call(call_id,ticket_id) VALUES (?,?)").run("call-1",ticket.ticketId);
      db.close();

      const result = retireHistoricalNativeCommandTickets({
        ticketDatabasePath: databasePath,
        cfg: {},
        now: new Date("2026-09-20T07:40:00Z"),
      });
      expect(result).toMatchObject({ retired:0, skippedForEvidence:1, schemaReady:true });

      const check = new DatabaseSync(databasePath, { readOnly:true });
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId)).toEqual({status:"accepted"});
      check.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not retire a fresh native-command Ticket inside the bounded migration age", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-native-fresh-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const store = new TicketStore(databasePath);
      const fresh = new Date("2026-09-20T07:39:30Z");
      const ticket = store.accept({ runId:"run-context-fresh", ownerSessionKey:"agent:main:dashboard:main", prompt:"/context" });
      store.route(ticket.ticketId, false, fresh);
      const db = new DatabaseSync(databasePath);
      ensureCommandRetirementEvidenceTables(db);
      db.prepare("UPDATE tickets SET created_at=?,updated_at=? WHERE ticket_id=?")
        .run(fresh.toISOString(),fresh.toISOString(),ticket.ticketId);
      db.close();

      const result = retireHistoricalNativeCommandTickets({
        ticketDatabasePath: databasePath,
        cfg: {},
        now: new Date("2026-09-20T07:40:00Z"),
        minAgeMs: 60_000,
      });
      expect(result).toMatchObject({ retired:0, schemaReady:true });

      const check = new DatabaseSync(databasePath, { readOnly:true });
      expect(check.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId)).toEqual({status:"accepted"});
      check.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("cancels current and queued direct Tickets from authoritative external user abort before the queued turn can execute", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx442-authoritative-user-stop-"));
    try {
      const databasePath=join(root,"tickets.sqlite3");
      const store=new TicketStore(databasePath);
      store.snapshot();
      const sessionKey="agent:main:discord:channel:authoritative-stop";
      const sessionId="physical-authoritative-stop";
      const db=new DatabaseSync(databasePath);
      const now="2026-09-20T16:32:48.781Z";
      db.exec(`
        CREATE TABLE IF NOT EXISTS cnx_sessions(
          session_key TEXT PRIMARY KEY,
          state TEXT NOT NULL DEFAULT 'active',
          generation INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          deleted_at TEXT,
          delete_reason TEXT,
          session_id TEXT
        );
        CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
          ticket_id TEXT PRIMARY KEY,
          mode TEXT NOT NULL DEFAULT 'resume',
          state TEXT NOT NULL DEFAULT 'pending',
          attempt_count INTEGER NOT NULL DEFAULT 0,
          active_run_id TEXT,
          next_attempt_at TEXT,
          last_error TEXT,
          owner_generation INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
      `);
      db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at,session_id) VALUES (?,'active',11,?,?,?)")
        .run(sessionKey,now,now,sessionId);
      db.close();

      const first=store.acceptIngress({
        sourceKey:"source-stop-1",
        sourceChannel:"discord",
        sourceMessageId:"msg-stop-1",
        ownerSessionKey:sessionKey,
        prompt:"@Ce STOP 1",
      });
      expect(store.bindPendingIngressRun({
        ownerSessionKey:sessionKey,
        ownerSessionId:sessionId,
        runId:"run-stop-1",
        prompt:"@Ce STOP 1",
        sourceChannel:"discord",
      }).state).toBe("bound");
      store.route(first.ticketId,false);

      const second=store.acceptIngress({
        sourceKey:"source-stop-2",
        sourceChannel:"discord",
        sourceMessageId:"msg-stop-2",
        ownerSessionKey:sessionKey,
        prompt:"@Ce STOP 2",
      });

      let mutate=new DatabaseSync(databasePath);
      mutate.prepare("UPDATE tickets SET status='failed',failure_class='permanent',failure_message='' WHERE ticket_id=?")
        .run(first.ticketId);
      mutate.prepare(`
        INSERT INTO cnx_direct_recovery(ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,owner_generation,created_at,updated_at)
        VALUES (?,'resume','pending',0,NULL,?,?,11,?,?)
      `).run(second.ticketId,now,"queued",now,now);
      mutate.close();

      const evidence:any={
        state:"terminal",
        runId:"run-stop-1",
        status:"interrupted",
        stopReason:"aborted",
        aborted:true,
        externalAbort:true,
        timedOut:false,
      };
      expect(isAuthoritativeUserStop(evidence)).toBe(true);
      const result=cancelDirectOwnerSessionForAuthoritativeUserStop({
        ticketDatabasePath:databasePath,
        sessionKey,
        evidence,
        now:new Date("2026-09-20T16:32:48.900Z"),
      });
      expect(result.state).toBe("cancelled");
      expect(new Set(result.cancelled)).toEqual(new Set([first.ticketId,second.ticketId]));
      expect(result.generation).toBe(12);
      const duplicate=cancelDirectOwnerSessionForAuthoritativeUserStop({
        ticketDatabasePath:databasePath,
        sessionKey,
        evidence,
        now:new Date("2026-09-20T16:32:49.000Z"),
      });
      expect(duplicate).toEqual({state:"unchanged",cancelled:[]});

      let check=new DatabaseSync(databasePath,{readOnly:true});
      expect(check.prepare("SELECT ticket_id,status FROM tickets ORDER BY created_at").all()).toEqual([
        {ticket_id:first.ticketId,status:"cancelled"},
        {ticket_id:second.ticketId,status:"cancelled"},
      ]);
      expect(check.prepare("SELECT generation,state FROM cnx_sessions WHERE session_key=?").get(sessionKey))
        .toEqual({generation:12,state:"active"});
      expect(check.prepare("SELECT state,active_run_id,next_attempt_at FROM cnx_direct_recovery WHERE ticket_id=?").get(second.ticketId))
        .toEqual({state:"cancelled",active_run_id:null,next_attempt_at:null});
      expect(check.prepare("SELECT COUNT(*) AS n FROM ticket_events WHERE event_type='cancelled_by_user' AND ticket_id IN (?,?)").get(first.ticketId,second.ticketId))
        .toEqual({n:2});
      check.close();

      const dequeue=store.bindPendingIngressRun({
        ownerSessionKey:sessionKey,
        ownerSessionId:sessionId,
        runId:"run-stop-2-after-host-dequeue",
        prompt:"@Ce STOP 2",
        sourceChannel:"discord",
      });
      expect(dequeue).toMatchObject({state:"cancelled",ticketId:second.ticketId});

      check=new DatabaseSync(databasePath,{readOnly:true});
      expect(check.prepare("SELECT COUNT(*) AS n FROM tickets").get()).toEqual({n:2});
      expect(check.prepare("SELECT bound_run_id FROM ticket_ingress_claims WHERE ticket_id=?").get(second.ticketId))
        .toEqual({bound_run_id:"run-stop-2-after-host-dequeue"});
      check.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not advance the Stop generation twice when an earlier UI Stop already advanced the owner barrier", () => {
    const root=mkdtempSync(join(tmpdir(),"cnx442-stop-generation-convergence-"));
    try {
      const databasePath=join(root,"tickets.sqlite3");
      const store=new TicketStore(databasePath);
      store.snapshot();
      const sessionKey="agent:main:discord:channel:stop-generation-convergence";
      const sessionId="physical-stop-generation-convergence";
      const now="2026-09-21T01:03:28.900Z";
      let db=new DatabaseSync(databasePath);
      db.exec(`
        CREATE TABLE IF NOT EXISTS cnx_sessions(
          session_key TEXT PRIMARY KEY,
          state TEXT NOT NULL DEFAULT 'active',
          generation INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          deleted_at TEXT,
          delete_reason TEXT,
          session_id TEXT
        );
        CREATE TABLE IF NOT EXISTS cnx_direct_recovery(
          ticket_id TEXT PRIMARY KEY,
          mode TEXT NOT NULL DEFAULT 'resume',
          state TEXT NOT NULL DEFAULT 'pending',
          attempt_count INTEGER NOT NULL DEFAULT 0,
          active_run_id TEXT,
          next_attempt_at TEXT,
          last_error TEXT,
          owner_generation INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
      `);
      db.prepare("INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at,session_id) VALUES (?,'active',11,?,?,?)")
        .run(sessionKey,now,now,sessionId);
      db.close();

      const first=store.acceptIngress({
        sourceKey:"source-converge-1",
        sourceChannel:"discord",
        sourceMessageId:"msg-converge-1",
        ownerSessionKey:sessionKey,
        prompt:"@Ce STOP CONVERGE 1",
      });
      expect(store.bindPendingIngressRun({
        ownerSessionKey:sessionKey,
        ownerSessionId:sessionId,
        runId:"run-converge-1",
        prompt:"@Ce STOP CONVERGE 1",
        sourceChannel:"discord",
      }).state).toBe("bound");
      store.route(first.ticketId,false);
      const second=store.acceptIngress({
        sourceKey:"source-converge-2",
        sourceChannel:"discord",
        sourceMessageId:"msg-converge-2",
        ownerSessionKey:sessionKey,
        prompt:"@Ce STOP CONVERGE 2",
      });

      db=new DatabaseSync(databasePath);
      db.prepare("UPDATE tickets SET status='failed',failure_class='permanent',failure_message='' WHERE ticket_id=?").run(first.ticketId);
      db.prepare("UPDATE tickets SET status='cancelled',failure_class=NULL,failure_message='Reply operation aborted by user' WHERE ticket_id=?").run(second.ticketId);
      db.prepare("UPDATE cnx_sessions SET generation=12,updated_at=? WHERE session_key=?").run(now,sessionKey);
      db.close();

      const evidence:any={
        state:"terminal",
        runId:"run-converge-1",
        status:"interrupted",
        stopReason:"aborted",
        aborted:true,
        externalAbort:true,
        timedOut:false,
      };
      const result=cancelDirectOwnerSessionForAuthoritativeUserStop({
        ticketDatabasePath:databasePath,
        sessionKey,
        evidence,
        now:new Date("2026-09-21T01:03:29.100Z"),
      });
      expect(result.state).toBe("cancelled");
      expect(result.cancelled).toEqual([first.ticketId]);
      expect(result.generation).toBe(12);

      const check=new DatabaseSync(databasePath,{readOnly:true});
      expect(check.prepare("SELECT generation,state FROM cnx_sessions WHERE session_key=?").get(sessionKey))
        .toEqual({generation:12,state:"active"});
      expect(check.prepare("SELECT ticket_id,status FROM tickets WHERE ticket_id IN (?,?) ORDER BY created_at").all(first.ticketId,second.ticketId))
        .toEqual([
          {ticket_id:first.ticketId,status:"cancelled"},
          {ticket_id:second.ticketId,status:"cancelled"},
        ]);
      expect(check.prepare("SELECT owner_generation FROM ticket_ingress_claims WHERE ticket_id=?").get(first.ticketId))
        .toEqual({owner_generation:11});
      check.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("waits boundedly for a delayed authoritative user-stop terminal event", async () => {
    const root=mkdtempSync(join(tmpdir(),"cnx442-delayed-stop-terminal-"));
    try {
      const agentDir=join(root,"agents","main","agent");
      mkdirSync(agentDir,{recursive:true});
      const dbPath=join(agentDir,"openclaw-agent.sqlite");
      const db=new DatabaseSync(dbPath);
      db.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL,
          PRIMARY KEY(session_id,seq)
        );
      `);
      db.close();

      const api:any={
        config:{},
        runtime:{agent:{resolveAgentDir:()=>agentDir}},
      };
      const timer=setTimeout(()=>{
        const write=new DatabaseSync(dbPath);
        write.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES (?,?,?,?,?)")
          .run(
            "physical-stop",
            1,
            "run-delayed-stop",
            JSON.stringify({
              type:"session.ended",
              runId:"run-delayed-stop",
              data:{
                status:"interrupted",
                aborted:true,
                externalAbort:true,
                timedOut:false,
                stopReason:"aborted",
                promptError:"agent run aborted | OPENCLAW_DIRECT_ABORT",
              },
            }),
            Date.now(),
          );
        write.close();
      },40);

      const started=Date.now();
      const evidence=await waitForHostRunTerminalEvidence({
        api,
        sessionKey:"agent:main:discord:channel:42",
        runId:"run-delayed-stop",
        timeoutMs:500,
        pollMs:10,
      });
      clearTimeout(timer);
      expect(Date.now()-started).toBeLessThan(500);
      expect(evidence).toMatchObject({
        state:"terminal",
        runId:"run-delayed-stop",
        status:"interrupted",
        aborted:true,
        externalAbort:true,
        timedOut:false,
        stopReason:"aborted",
        promptError:"agent run aborted | OPENCLAW_DIRECT_ABORT",
      });
      expect(evidence.state==="terminal" && isAuthoritativeUserStop(evidence)).toBe(true);
    } finally {
      bestEffortRemove(root);
    }
  });

  it("does not classify restart or supersession aborts as an authoritative user Stop", () => {
    for (const stopReason of ["restart","superseded"]) {
      expect(isAuthoritativeUserStop({
        state:"terminal",
        runId:`run-${stopReason}`,
        status:"interrupted",
        aborted:true,
        externalAbort:true,
        timedOut:false,
        stopReason,
      })).toBe(false);
    }
  });

  it("reads authoritative host terminal error evidence by exact run id", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-host-terminal-"));
    try {
      const dbPath = join(root, "openclaw-agent.sqlite");
      const db = new DatabaseSync(dbPath);
      db.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL
        );
      `);
      db.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES(?,?,?,?,?)").run(
        "session-1",
        9,
        "run-failed",
        JSON.stringify({
          type: "session.ended",
          runId: "run-failed",
          data: { status: "error", stopReason: "error", aborted: false, externalAbort: false, timedOut: false },
        }),
        1,
      );
      db.close();

      expect(readHostRunTerminalEvidence({ databasePath: dbPath, runId: "run-failed" })).toMatchObject({
        state: "terminal",
        status: "error",
        runId: "run-failed",
      });
      expect(readHostRunTerminalEvidence({ databasePath: dbPath, runId: "other-run" })).toEqual({ state: "pending" });
    } finally {
      bestEffortRemove(root);
    }
  });

  it("resolves terminal evidence from openclaw-agent.sqlite rather than the legacy sessions.json store", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-host-db-path-"));
    try {
      const dbPath = join(root, "openclaw-agent.sqlite");
      new DatabaseSync(dbPath).close();
      const api: any = {
        config: {},
        runtime: { agent: {
          resolveAgentDir: () => root,
          session: { resolveStorePath: () => join(root, "sessions.json") },
        } },
      };
      expect(resolveHostAgentDatabasePath(api, "agent:main:dashboard:main")).toBe(dbPath);
    } finally {
      bestEffortRemove(root);
    }
  });

  it("schedules host terminal reconciliation after agent_end can return", async () => {
    vi.useFakeTimers();
    const root = mkdtempSync(join(tmpdir(), "cnx442-host-reconcile-"));
    try {
      const dbPath = join(root, "openclaw-agent.sqlite");
      const db = new DatabaseSync(dbPath);
      db.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL
        );
      `);
      db.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES(?,?,?,?,?)").run(
        "session-2",
        1,
        "run-error",
        JSON.stringify({ type: "session.ended", runId: "run-error", data: { status: "error", stopReason: "error" } }),
        2,
      );
      db.close();

      const onTerminal = vi.fn();
      const api: any = {
        config: {},
        runtime: { agent: {
          resolveAgentDir: () => root,
          session: { resolveStorePath: () => join(root, "sessions.json") },
        } },
      };
      const scheduled = scheduleHostRunTerminalReconcile({
        api,
        sessionKey: "agent:main:dashboard:main",
        runId: "run-error",
        delayMs: 100,
        pollMs: 50,
        maxAttempts: 2,
        onTerminal,
      });
      expect(scheduled.scheduled).toBe(true);
      await vi.advanceTimersByTimeAsync(100);
      expect(onTerminal).toHaveBeenCalledTimes(1);
      expect(onTerminal.mock.calls[0][0]).toMatchObject({ state: "terminal", status: "error", runId: "run-error" });
      scheduled.cancel();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("settles a silent direct Ticket only after authoritative Host success", async () => {
    vi.useFakeTimers();
    const root = mkdtempSync(join(tmpdir(), "cnx442-silent-success-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const agentDir = join(root, "agent");
      const dbPath = join(agentDir, "openclaw-agent.sqlite");
      mkdirSync(agentDir, { recursive: true });
      const host = new DatabaseSync(dbPath);
      host.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL
        );
      `);
      host.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES(?,?,?,?,?)").run(
        "session-success", 1, "run-silent",
        JSON.stringify({ type:"session.ended", runId:"run-silent", data:{ status:"success", stopReason:"stop" } }),
        1,
      );
      host.close();

      const hooks = new Map<string, any[]>();
      const api: any = {
        config: {},
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { agent:{ resolveAgentDir:()=>agentDir }, tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const owner = { sessionKey: "agent:main:dashboard:silent", runId: "run-silent", workspaceDir: root };
      expect(await hooks.get("before_agent_run")?.[0]({ prompt: "silent user turn", senderIsOwner: true }, owner)).toEqual({ outcome: "pass" });
      await hooks.get("agent_end")?.[0]({ runId: owner.runId, success: true, messages: [] }, owner);

      let db = new DatabaseSync(databasePath, { readOnly: true });
      expect(db.prepare("SELECT status,delivery_confirmed_at FROM tickets WHERE run_id=?").get(owner.runId)).toEqual({
        status:"accepted", delivery_confirmed_at:null,
      });
      db.close();

      await vi.advanceTimersByTimeAsync(150);

      db = new DatabaseSync(databasePath, { readOnly: true });
      const row = db.prepare("SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE run_id=?").get(owner.runId) as any;
      expect(row.status).toBe("completed");
      expect(row.response_ready_at).toEqual(expect.any(String));
      expect(row.delivery_confirmed_at).toEqual(expect.any(String));
      const events=(db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=(SELECT ticket_id FROM tickets WHERE run_id=?) ORDER BY event_id").all(owner.runId) as any[]).map(x=>x.event_type);
      expect(events).toEqual(["accepted","routed","response_ready","delivery_confirmed","completed"]);
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("retracts response_ready and promotes recovery when authoritative Host terminal is error", async () => {
    vi.useFakeTimers();
    const root = mkdtempSync(join(tmpdir(), "cnx442-host-error-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const agentDir = join(root, "agent");
      const dbPath = join(agentDir, "openclaw-agent.sqlite");
      mkdirSync(agentDir, { recursive: true });
      const host = new DatabaseSync(dbPath);
      host.exec(`
        CREATE TABLE trajectory_runtime_events(
          session_id TEXT NOT NULL,
          seq INTEGER NOT NULL,
          run_id TEXT,
          event_json TEXT NOT NULL,
          created_at INTEGER NOT NULL
        );
      `);
      host.prepare("INSERT INTO trajectory_runtime_events(session_id,seq,run_id,event_json,created_at) VALUES(?,?,?,?,?)").run(
        "session-error", 1, "run-host-error",
        JSON.stringify({ type:"session.ended", runId:"run-host-error", data:{ status:"error", stopReason:"error" } }),
        1,
      );
      host.close();

      const hooks = new Map<string, any[]>();
      const api: any = {
        config: {},
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { agent:{ resolveAgentDir:()=>agentDir }, tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const owner = { sessionKey: "agent:main:dashboard:error", runId: "run-host-error", workspaceDir: root };
      expect(await hooks.get("before_agent_run")?.[0]({ prompt: "user turn", senderIsOwner: true }, owner)).toEqual({ outcome: "pass" });
      await hooks.get("agent_end")?.[0]({ runId: owner.runId, success: true, messages: [] }, owner);
      await vi.advanceTimersByTimeAsync(150);

      const db = new DatabaseSync(databasePath, { readOnly: true });
      const row = db.prepare("SELECT status,workflow_eligible,response_ready_at,delivery_confirmed_at,failure_class FROM tickets WHERE run_id=?").get(owner.runId) as any;
      expect(row.status).not.toBe("completed");
      expect(row.response_ready_at).toBeNull();
      expect(row.delivery_confirmed_at).toBeNull();
      expect(row.failure_class).toBe("interrupted");
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });

  it("never completes a ticketed conversational run merely because agent_end had no visible output", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx442-terminal-ticket-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const hooks = new Map<string, any[]>();
      const api: any = {
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const owner = { sessionKey: "agent:main:dashboard:main", runId: "run-race", workspaceDir: root };
      expect(await hooks.get("before_agent_run")?.[0]({ prompt: "user turn", senderIsOwner: true }, owner)).toEqual({ outcome: "pass" });
      await hooks.get("agent_end")?.[0]({ runId: owner.runId, success: true, messages: [] }, owner);

      const db = new DatabaseSync(databasePath, { readOnly: true });
      const row = db.prepare("SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE run_id=?").get(owner.runId) as any;
      expect(row.status).toBe("accepted");
      expect(row.response_ready_at).toEqual(expect.any(String));
      expect(row.delivery_confirmed_at).toBeNull();
      expect((db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=(SELECT ticket_id FROM tickets WHERE run_id=?) ORDER BY event_id").all(owner.runId) as any[]).map(x=>x.event_type))
        .toEqual(["accepted","routed","response_ready"]);
      db.close();
    } finally {
      bestEffortRemove(root);
    }
  });
});