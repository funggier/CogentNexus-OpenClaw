import { mkdtempSync, rmSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { deleteSessionByKey, finalizeSessionDeletion, reactivateSessionForLifecycle } from "./v090.js";
import { installV091DashboardVerifiedDelivery, stageDashboardDirectResult, settleDashboardNativeDelivery } from "./v091-dashboard-verified-delivery.js";

type HookMap = Map<string, ((event: any, ctx: any) => any)[]>;

function setup(root: string) {
  const path = join(root, "tickets.sqlite3");
  const hooks: HookMap = new Map();
  const logs: string[] = [];
  const api: any = {
    on: (name: string, handler: any) => hooks.set(name, [...(hooks.get(name) ?? []), handler]),
    logger: { info: (message: string) => logs.push(message), warn: () => {}, error: () => {} },
    runtime: { events: {} },
  };
  installV091DashboardVerifiedDelivery(api, { workspaceDir: root, ticketDatabasePath: path });
  return { path, hooks, logs };
}

function hook(hooks: HookMap, name: string) { return hooks.get(name)?.[0]!; }

function readTicket(path: string, runId: string) {
  const db = new DatabaseSync(path, { readOnly: true });
  try { return db.prepare("SELECT ticket_id,status,delivery_confirmed_at FROM tickets WHERE run_id=?").get(runId) as any; }
  finally { db.close(); }
}

describe("Task275 Discord Direct owner-context and stale-settlement proof", () => {
  it("rejects a wrong consume-time owner and still stages for the exact owner", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-task275-owner-context-"));
    try {
      const { path, hooks } = setup(root);
      const ownerA = "agent:main:discord:channel:275001";
      const ownerB = "agent:main:discord:channel:275002";
      const runId = "task275-owner-run";
      const store = new TicketStore(path);
      const ticket = store.accept({ runId, ownerSessionKey: ownerA, prompt: "owner context" });
      store.route(ticket.ticketId, false);
      const dispatch = hook(hooks, "reply_dispatch");
      const sending = hook(hooks, "reply_payload_sending");
      const dispatcher = {
        getQueuedCounts: () => ({ final: 1 }),
        waitForIdle: async () => {},
        getFailedCounts: () => ({ final: 0 }),
        getCancelledCounts: () => ({ final: 0 }),
      };
      dispatch({}, { runId, sessionKey: ownerA, channel: "discord", messageProvider: "discord", dispatcher });
      const wrong = await sending({ kind: "final", payload: { text: "wrong owner" } }, { runId, sessionKey: ownerB, channel: "discord", messageProvider: "discord" });
      expect(wrong).toBeUndefined();
      expect(readTicket(path, runId)).toMatchObject({ status: "accepted", delivery_confirmed_at: null });
      const correct = await sending({ kind: "final", payload: { text: "exact owner" } }, { runId, sessionKey: ownerA, channel: "discord", messageProvider: "discord" });
      expect(correct?.payload?.text).toContain("exact owner");
      await new Promise<void>((resolve) => setImmediate(resolve));
      expect(readTicket(path, runId).status).toBe("completed");
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("releases a stale public-hook waiter after deletion without settling the old generation", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-task275-stale-waiter-"));
    try {
      const { path, hooks } = setup(root);
      const key = "agent:main:discord:channel:275003";
      const runId = "task275-stale-run";
      const store = new TicketStore(path);
      const ticket = store.accept({ runId, ownerSessionKey: key, prompt: "stale waiter" });
      store.route(ticket.ticketId, false);
      let release!: () => void;
      const idle = new Promise<void>((resolve) => { release = resolve; });
      const dispatcher = { getQueuedCounts: () => ({ final: 1 }), waitForIdle: () => idle, getFailedCounts: () => ({ final: 0 }), getCancelledCounts: () => ({ final: 0 }) };
      hook(hooks, "reply_dispatch")({}, { runId, sessionKey: key, channel: "discord", messageProvider: "discord", dispatcher });
      const staged = await hook(hooks, "reply_payload_sending")({ kind: "final", payload: { text: "old final" } }, { runId, sessionKey: key, channel: "discord", messageProvider: "discord" });
      expect(staged?.payload?.text).toContain("old final");
      await Promise.resolve();
      expect(deleteSessionByKey(path, { sessionKey: key, message: "Task275 stale waiter" }).assistantSuppressed).toBe(1);
      finalizeSessionDeletion(path, key, "Task275 stale waiter");
      release();
      await new Promise<void>((resolve) => setImmediate(resolve));
      await new Promise<void>((resolve) => setTimeout(resolve, 20));
      expect(readTicket(path, runId).status).not.toBe("completed");
      const newSession = reactivateSessionForLifecycle(path, { sessionKey: key, sessionId: "task275-new-session" });
      expect(newSession.accepted).toBe(true);
      const fresh = store.accept({ runId: "task275-fresh-run", ownerSessionKey: key, prompt: "fresh generation" });
      store.route(fresh.ticketId, false);
      const freshStaged = stageDashboardDirectResult(path, { runId: "task275-fresh-run", text: "fresh final", ownerSessionKey: key, ingressSurface: "discord" });
      expect(freshStaged.staged).toBe(true);
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("settles a timeout-surviving durable final exactly once", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-task275-exact-settlement-"));
    try {
      const { path } = setup(root);
      const key = "agent:main:discord:channel:275004";
      const store = new TicketStore(path);
      const ticket = store.accept({ runId: "task275-exact-run", ownerSessionKey: key, prompt: "exact settlement" });
      store.route(ticket.ticketId, false);
      expect(stageDashboardDirectResult(path, { runId: "task275-exact-run", text: "durable exact", ownerSessionKey: key, ingressSurface: "discord", now: new Date("2026-09-06T00:00:00.000Z") }).staged).toBe(true);
      expect(store.recoverUndeliveredDirect({ now: new Date("2026-09-06T01:00:00.000Z"), olderThanMs: 1000 })).toEqual([]);
      const pending = new DatabaseSync(path, { readOnly: true });
      expect(pending.prepare("SELECT status FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId)).toEqual({ status: "pending" });
      pending.close();
      expect(settleDashboardNativeDelivery(path, "task275-exact-run", new Date("2026-09-06T01:00:01.000Z"))).toBe(true);
      expect(settleDashboardNativeDelivery(path, "task275-exact-run", new Date("2026-09-06T01:00:02.000Z"))).toBe(false);
      expect(readTicket(path, "task275-exact-run")).toMatchObject({ status: "completed", delivery_confirmed_at: "2026-09-06T01:00:01.000Z" });
      const db = new DatabaseSync(path, { readOnly: true });
      try {
        expect(db.prepare("SELECT status FROM cnx_assistant_delivery WHERE ticket_id=?").get(ticket.ticketId)).toEqual({ status: "delivered" });
        expect(db.prepare("SELECT event_type FROM ticket_events WHERE ticket_id=? AND event_type IN ('delivery_confirmed','completed')").all(ticket.ticketId)).toHaveLength(2);
      } finally { db.close(); }
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});
