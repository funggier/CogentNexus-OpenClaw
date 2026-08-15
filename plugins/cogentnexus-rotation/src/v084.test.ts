import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  directRecoveryBackoffMs,
  executeCompatibilityWake,
  isDashboardSession,
  prepareV084RecoveryState,
  patchTicketStore,
} from "./v084.js";

describe("CogentNexus v0.8.4 recovery compatibility", () => {
  patchTicketStore();

  it("keeps interrupted Direct intent in the Direct lane", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v084-direct-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "direct-interrupt", ownerSessionKey: "agent:main:dashboard:test", prompt: "สวัสดีครับ" });
      store.route(ticket.ticketId, false);
      expect(store.finalizeDirectRun({ runId: "direct-interrupt", success: false, interrupted: true, message: "operation aborted" })).toBe("waiting");
      const db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT status,workflow_eligible,failure_class FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status: "accepted", workflow_eligible: 0, failure_class: "interrupted" });
      expect(db.prepare("SELECT mode,state,attempt_count FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ mode: "resume", state: "pending", attempt_count: 0 });
      db.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("reopens legacy interrupted Direct promotions before dispatch", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v084-migrate-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "legacy", ownerSessionKey: "agent:main:dashboard:test", prompt: "ช่วยทักทายสั้น ๆ" });
      store.route(ticket.ticketId, false);
      const db = new DatabaseSync(path);
      db.prepare("UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted' WHERE ticket_id=?").run(ticket.ticketId);
      db.close();
      const prepared = prepareV084RecoveryState(root, { ticketDatabasePath: path });
      expect(prepared.reopened).toBe(1);
      const verify = new DatabaseSync(path, { readOnly: true });
      expect(verify.prepare("SELECT status,workflow_eligible FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
        .toEqual({ status: "accepted", workflow_eligible: 0 });
      expect(verify.prepare("SELECT state FROM cnx_direct_recovery WHERE ticket_id=?").get(ticket.ticketId)).toEqual({ state: "pending" });
      verify.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("settles a pending Ticket marker through runtime.subagent", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v084-wake-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "terminal", ownerSessionKey: "agent:main:dashboard:test", prompt: "work" });
      store.route(ticket.ticketId, true);
      const lease = store.claim({ ticketId: ticket.ticketId, workerId: "worker", leaseMs: 5000 })!;
      store.complete({ ...lease, result: { ok: true } });
      const outbox = store.pendingOutbox()[0];
      store.markOutboxScheduled(outbox.outboxId);
      let reads = 0;
      const api = {
        logger: { warn: () => {} },
        runtime: { subagent: {
          getSessionMessages: async () => ({ messages: reads++ === 0
            ? [{ role: "assistant", content: "old" }]
            : [{ role: "assistant", content: "old" }, { role: "assistant", content: "new result" }] }),
          run: async (input: any) => {
            expect(input.sessionKey).toBe("agent:main:dashboard:test");
            expect(input.deliver).toBe(false);
            return { runId: "compat-run" };
          },
          waitForRun: async () => ({ status: "ok" }),
        } },
      };
      await executeCompatibilityWake(api, { workspaceDir: root, ticketDatabasePath: path }, {
        sessionKey: "agent:main:dashboard:test",
        delayMs: 0,
        deleteAfterRun: true,
        deliveryMode: "announce",
        name: "delivery",
        tag: `cogent-ticket-result-${ticket.ticketId}`,
        message: `[CogentNexus Delivery: ticket:${outbox.outboxId}]\nReport the committed result.`,
      });
      expect(store.pendingOutbox()).toEqual([]);
      const db = new DatabaseSync(path, { readOnly: true });
      expect(db.prepare("SELECT delivery_status FROM ticket_outbox WHERE outbox_id=?").get(outbox.outboxId))
        .toEqual({ delivery_status: "delivered" });
      db.close();
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("uses transcript delivery for dashboard sessions and bounded backoff", () => {
    expect(isDashboardSession("agent:main:dashboard:abc")).toBe(true);
    expect(isDashboardSession("agent:main:discord:abc")).toBe(false);
    expect([1, 2, 3, 4, 5, 6, 99].map(directRecoveryBackoffMs))
      .toEqual([5000, 15000, 30000, 60000, 120000, 300000, 300000]);
  });
});
