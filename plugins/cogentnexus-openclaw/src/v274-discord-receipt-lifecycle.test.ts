import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it, vi } from "vitest";
import { TicketStore } from "./ticket-store.js";
import entry from "./index.js";
import { stageDashboardDirectResult } from "./v091-dashboard-verified-delivery.js";
import { deleteSessionByKey, finalizeSessionDeletion, reactivateSessionForLifecycle } from "./v090.js";

describe("Task274 Discord Direct receipt lifecycle fence", () => {
  it("does not infer a same-session run from a runId-less message_sent receipt", async () => {
    vi.useFakeTimers();
    const root = mkdtempSync(join(tmpdir(), "cnx-task274-concurrent-receipt-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:discord:channel:274001";
      const hooks = new Map<string, any[]>();
      const logs: string[] = [];
      const api: any = {
        pluginConfig: { ticketFirst: true, preInferenceAdmission: true, directDeliverySettleMs: 1000, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
        registerTool: () => {}, registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, [...(hooks.get(name) ?? []), callback]),
        logger: { warn: () => {}, error: () => {}, info: (message: string) => logs.push(message) },
        session: { workflow: { unscheduleSessionTurnsByTag: async () => {}, scheduleSessionTurn: async () => {} } },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);
      const beforeRun = hooks.get("before_agent_run")?.[0];
      const messageSent = hooks.get("message_sent")?.[0];
      expect(beforeRun).toBeTypeOf("function");
      expect(messageSent).toBeTypeOf("function");

      const ownerA = { sessionKey, runId: "task274-run-a", workspaceDir: root, channel: "discord", messageProvider: "discord" };
      const ownerB = { sessionKey, runId: "task274-run-b", workspaceDir: root, channel: "discord", messageProvider: "discord" };
      expect(await beforeRun({ prompt: "ตอบกลับ A", senderIsOwner: true }, ownerA)).toEqual({ outcome: "pass" });
      expect(await beforeRun({ prompt: "ตอบกลับ B", senderIsOwner: true }, ownerB)).toEqual({ outcome: "pass" });
      const store = new TicketStore(databasePath);
      const ticketA = store.accept({ runId: ownerA.runId, ownerSessionKey: sessionKey, prompt: "ตอบกลับ A" });
      const ticketB = store.accept({ runId: ownerB.runId, ownerSessionKey: sessionKey, prompt: "ตอบกลับ B" });
      store.route(ticketA.ticketId, false);
      store.route(ticketB.ticketId, false);
      expect(new TicketStore(databasePath).snapshot()).toMatchObject({ tickets: { accepted: 2 } });
      expect(stageDashboardDirectResult(databasePath, { runId: ownerA.runId, text: "A final", ownerSessionKey: sessionKey, ingressSurface: "discord" }).staged).toBe(true);
      expect(stageDashboardDirectResult(databasePath, { runId: ownerB.runId, text: "B final", ownerSessionKey: sessionKey, ingressSurface: "discord" }).staged).toBe(true);

      // Installed OpenClaw may omit runId from outbound receipts. This receipt
      // has no safe per-turn identity and must not be attributed to B.
      await messageSent({ sessionKey, success: true }, ownerB);
      expect(logs.some((line) => line.includes("ambiguous Discord message_sent receipt"))).toBe(true);
      vi.advanceTimersByTime(1000);
      await Promise.resolve();

      const snapshot = new TicketStore(databasePath).snapshot();
      expect(snapshot.tickets).toMatchObject({ accepted: 2 });
      expect(snapshot.tickets.completed ?? 0).toBe(0);
    } finally {
      vi.useRealTimers();
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("does not let a deleted generation settle late and stages the recreated generation", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-task274-lifecycle-generation-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const key = "agent:main:discord:channel:274002";
      const store = new TicketStore(path);
      const old = store.accept({ runId: "task274-old", ownerSessionKey: key, prompt: "old direct" });
      store.route(old.ticketId, false);
      expect(stageDashboardDirectResult(path, { runId: "task274-old", text: "old final", ownerSessionKey: key, ingressSurface: "discord" })).toMatchObject({ staged: true, ownerGeneration: 0 });
      expect(deleteSessionByKey(path, { sessionKey: key, message: "Task274 lifecycle fence" }).assistantSuppressed).toBe(1);
      finalizeSessionDeletion(path, key, "Task274 lifecycle fence");
      expect(stageDashboardDirectResult(path, { runId: "task274-old", text: "late old final", ownerSessionKey: key, ingressSurface: "discord" })).toMatchObject({ staged: false });
      expect(reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "new-session-id" })).toMatchObject({ accepted: true, generation: 2 });
      const fresh = store.accept({ runId: "task274-new", ownerSessionKey: key, prompt: "new direct" });
      store.route(fresh.ticketId, false);
      expect(stageDashboardDirectResult(path, { runId: "task274-new", text: "new final", ownerSessionKey: key, ingressSurface: "discord" })).toMatchObject({ staged: true, ownerGeneration: 2 });
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("does not promote a durable Discord final during a later timeout scan", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-task274-timeout-fence-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const key = "agent:main:discord:channel:274003";
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "task274-timeout", ownerSessionKey: key, prompt: "timeout direct" });
      store.route(ticket.ticketId, false);
      expect(stageDashboardDirectResult(path, { runId: "task274-timeout", text: "durable final", ownerSessionKey: key, ingressSurface: "discord", now: new Date("2026-09-06T00:00:00.000Z") })).toMatchObject({ staged: true });
      expect(store.recoverUndeliveredDirect({ now: new Date("2026-09-06T01:00:00.000Z"), olderThanMs: 1000 })).toEqual([]);
      expect(store.snapshot()).toMatchObject({ tickets: { accepted: 1 }, pendingOutbox: 0 });
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});
