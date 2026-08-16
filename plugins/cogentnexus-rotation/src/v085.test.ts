import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  boundedOwnerContext,
  directRecoveryBackoffMs,
  executeCompatibilityWake,
  launchRecovery,
  patchTicketStore,
  prepareV085RecoveryState,
} from "./v085.js";

describe("CogentNexus v0.8.5 hidden Direct recovery", () => {
  patchTicketStore();

  function directTicket(path: string, runId: string, prompt = "สวัสดีครับ") {
    const store = new TicketStore(path);
    const ticket = store.accept({
      runId,
      ownerSessionKey: "agent:main:dashboard:test",
      prompt,
    });
    store.route(ticket.ticketId, false);
    return { store, ticket };
  }

  it("treats the exact OpenClaw user-abort wording as recoverable even when interrupted=false", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v085-abort-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const { store, ticket } = directTicket(path, "abort-run");
      expect(store.finalizeDirectRun({
        runId: "abort-run",
        success: false,
        interrupted: false,
        message: "Reply operation aborted by user",
      })).toBe("waiting");
      const db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status: "accepted", workflow_eligible: 0, failure_class: "interrupted" });
      expect(db.prepare("SELECT state FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ state: "pending" });
      db.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("moves a waitForRun timeout back to pending immediately instead of leaving running", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v085-timeout-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const { store, ticket } = directTicket(path, "timeout-run");
      store.finalizeDirectRun({ runId: "timeout-run", success: false, interrupted: true, message: "timed out" });
      const recovery = new DatabaseSync(path, { readOnly: true })
        .prepare(`SELECT r.ticket_id,t.owner_session_key,t.prompt,r.mode,r.attempt_count
          FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id WHERE r.ticket_id=?`)
        .get(ticket.ticketId) as any;
      let launchedSession = "";
      const api = { runtime: { subagent: {
        getSessionMessages: async ({ sessionKey }: any) => ({
          messages: sessionKey === "agent:main:dashboard:test"
            ? [{ role: "user", content: "สวัสดีครับ" }]
            : [],
        }),
        run: async (input: any) => {
          launchedSession = input.sessionKey;
          return { runId: "hidden-timeout-run" };
        },
        waitForRun: async () => ({ status: "timeout" }),
        deleteSession: async () => {},
      } } };
      await launchRecovery(api, path, root, recovery, { ticketDatabasePath: path, timeoutSeconds: 60 });
      expect(launchedSession).not.toBe("agent:main:dashboard:test");
      expect(launchedSession).toContain(":subagent:");
      const verify = new DatabaseSync(path, { readOnly: true });
      const state = verify.prepare("SELECT state,attempt_count,active_run_id,next_attempt_at,last_error FROM cnx_direct_recovery WHERE ticket_id=?")
        .get(ticket.ticketId) as any;
      expect(state.state).toBe("pending");
      expect(state.attempt_count).toBe(1);
      expect(state.active_run_id).toBeNull();
      expect(state.next_attempt_at).toBeTruthy();
      expect(state.last_error).toBe("Direct recovery run timed out");
      verify.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("queues hidden-worker assistant output for Host delivery without completing before injection", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v085-result-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const { store, ticket } = directTicket(path, "result-run", "ทำต่อรับ");
      store.finalizeDirectRun({ runId: "result-run", success: false, interrupted: true, message: "interrupted" });
      const recoveryDb = new DatabaseSync(path, { readOnly: true });
      const recovery = recoveryDb.prepare(`SELECT r.ticket_id,t.owner_session_key,t.prompt,r.mode,r.attempt_count
        FROM cnx_direct_recovery r JOIN tickets t ON t.ticket_id=r.ticket_id WHERE r.ticket_id=?`)
        .get(ticket.ticketId) as any;
      recoveryDb.close();
      let childKey = "";
      const api = { runtime: { subagent: {
        getSessionMessages: async ({ sessionKey }: any) => {
          if (sessionKey === "agent:main:dashboard:test") {
            return { messages: [
              { role: "user", content: "ก่อนหน้านี้" },
              { role: "assistant", content: "บริบทเดิม" },
              { role: "user", content: "#cogent-direct\nold internal prompt" },
            ] };
          }
          return { messages: [{ role: "assistant", content: "คำตอบที่กู้คืนสำเร็จ" }] };
        },
        run: async (input: any) => {
          childKey = input.sessionKey;
          expect(input.deliver).toBe(false);
          return { runId: "hidden-success-run" };
        },
        waitForRun: async () => ({ status: "ok" }),
        deleteSession: async () => {},
      } } };
      await launchRecovery(api, path, root, recovery, { ticketDatabasePath: path, timeoutSeconds: 60 });
      expect(childKey).toContain(":subagent:");
      const verify = new DatabaseSync(path, { readOnly: true });
      const ticketState = verify.prepare("SELECT status,workflow_eligible,response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?")
        .get(ticket.ticketId) as any;
      expect(ticketState.status).toBe("accepted");
      expect(ticketState.workflow_eligible).toBe(0);
      expect(ticketState.response_ready_at).toBeTruthy();
      expect(ticketState.delivery_confirmed_at).toBeNull();
      expect(verify.prepare("SELECT state FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ state: "awaiting_delivery" });
      const rows = verify.prepare("SELECT kind,text,status,target_json FROM cnx_assistant_delivery ORDER BY delivery_id").all() as any[];
      expect(rows.some((row) => row.kind === "recovery_status" && row.status === "pending")).toBe(true);
      const result = rows.find((row) => row.kind === "direct_result");
      expect(result.text).toBe("คำตอบที่กู้คืนสำเร็จ");
      expect(JSON.parse(result.target_json).kind).toBe("direct");
      verify.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("supersedes orphan Direct recovery rows once a workflow or terminal Ticket owns the intent", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v085-orphan-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const { store, ticket } = directTicket(path, "orphan-run");
      store.finalizeDirectRun({ runId: "orphan-run", success: false, interrupted: true, message: "interrupted" });
      const db = new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='failed',workflow_eligible=1,workflow_id='CNX-AUTO-test',failure_class='capability' WHERE ticket_id=?")
        .run(ticket.ticketId);
      db.close();
      const prepared = prepareV085RecoveryState(root, { ticketDatabasePath: path });
      expect(prepared.superseded).toBe(1);
      const verify = new DatabaseSync(path, { readOnly: true });
      const row = verify.prepare("SELECT state,active_run_id,next_attempt_at,last_error FROM cnx_direct_recovery WHERE ticket_id=?")
        .get(ticket.ticketId) as any;
      expect(row.state).toBe("done");
      expect(row.active_run_id).toBeNull();
      expect(row.next_attempt_at).toBeNull();
      expect(row.last_error).toContain("superseded");
      verify.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("filters old CogentNexus synthetic user turns out of bounded recovery context", () => {
    const context = boundedOwnerContext([
      { role: "user", content: "คำสั่งจริง" },
      { role: "assistant", content: "คำตอบเดิม" },
      { role: "user", content: "#cogent-direct\n[CogentNexus Direct Recovery: X]" },
      { role: "user", content: "[CogentNexus Delivery: ticket:1]\ninternal" },
    ]);
    expect(context).toContain("คำสั่งจริง");
    expect(context).toContain("คำตอบเดิม");
    expect(context).not.toContain("#cogent-direct");
    expect(context).not.toContain("CogentNexus Delivery");
  });

  it("routes terminal compatibility work through a hidden session and queues assistant delivery", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v085-compat-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "terminal", ownerSessionKey: "agent:main:dashboard:test", prompt: "work" });
      store.route(ticket.ticketId, true);
      const lease = store.claim({ ticketId: ticket.ticketId, workerId: "worker", leaseMs: 5000 })!;
      store.complete({ ...lease, result: { ok: true } });
      const outbox = store.pendingOutbox()[0];
      store.markOutboxScheduled(outbox.outboxId);
      let launchedKey = "";
      const api = { logger: { warn: () => {} }, runtime: { subagent: {
        getSessionMessages: async ({ sessionKey }: any) => sessionKey === "agent:main:dashboard:test"
          ? { messages: [{ role: "user", content: "work" }] }
          : { messages: [{ role: "assistant", content: "งานเสร็จแล้วตามผลที่ตรวจสอบได้" }] },
        run: async (input: any) => { launchedKey = input.sessionKey; return { runId: "hidden-delivery" }; },
        waitForRun: async () => ({ status: "ok" }),
        deleteSession: async () => {},
      } } };
      const result = await executeCompatibilityWake(api, { workspaceDir: root, ticketDatabasePath: path }, {
        sessionKey: "agent:main:dashboard:test",
        delayMs: 0,
        deleteAfterRun: true,
        deliveryMode: "announce",
        name: "delivery",
        tag: `cogent-ticket-result-${ticket.ticketId}`,
        message: `[CogentNexus Delivery: ticket:${outbox.outboxId}]\nReport the committed result.`,
      });
      expect(result.queued).toBe(true);
      expect(launchedKey).toContain(":subagent:");
      expect(launchedKey).not.toBe("agent:main:dashboard:test");
      expect(store.pendingOutbox()).toHaveLength(1);
      const db = new DatabaseSync(path, { readOnly: true });
      const queued = db.prepare("SELECT owner_session_key,text,target_json,status FROM cnx_assistant_delivery WHERE kind='compatibility_result'").get() as any;
      expect(queued.owner_session_key).toBe("agent:main:dashboard:test");
      expect(queued.text).toContain("งานเสร็จแล้ว");
      expect(JSON.parse(queued.target_json)).toEqual({ kind: "ticket", outboxId: outbox.outboxId });
      expect(queued.status).toBe("pending");
      db.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("keeps bounded retry timing", () => {
    expect([1,2,3,4,5,6,99].map(directRecoveryBackoffMs))
      .toEqual([5000,15000,30000,60000,120000,300000,300000]);
  });
});
