import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

function installHarness(root: string, path: string, logs: string[] = []) {
  let replyDispatch: ((event: any, ctx: any) => void) | undefined;
  installV091DashboardVerifiedDelivery({
    on: (name: string, handler: (event: any, ctx: any) => void) => {
      if (name === "reply_dispatch") replyDispatch = handler;
    },
    logger: { info: (message: string) => logs.push(String(message)) },
  }, { workspaceDir: root, ticketDatabasePath: path });
  expect(replyDispatch).toBeTypeOf("function");
  return replyDispatch!;
}

function throwingPayload(label: string) {
  const payload: Record<string, unknown> = {};
  Object.defineProperties(payload, {
    text: { enumerable: true, get: () => { throw new Error(`${label}:text-read`); } },
    mediaUrl: { enumerable: true, get: () => { throw new Error(`${label}:mediaUrl-read`); } },
    mediaUrls: { enumerable: true, get: () => { throw new Error(`${label}:mediaUrls-read`); } },
  });
  return payload;
}

describe("Task 104 behavior-neutral Dashboard observability", () => {
  it("returns non-final callbacks without reading payload or dispatcher state", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v104-non-final-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const replyDispatch = installHarness(root, path);
      let callback: ((payload: any, info: any) => any) | undefined;
      let queuedCountReads = 0;
      const dispatcher = {
        appendBeforeDeliver: (fn: any) => { callback = fn; },
        getQueuedCounts: () => { queuedCountReads += 1; throw new Error("non-final:queued-count-read"); },
      };
      replyDispatch({ runId: "secret-non-final-run" }, { dispatcher });
      expect(callback).toBeTypeOf("function");
      const payload = throwingPayload("non-final");
      expect(() => callback!(payload, { kind: "delta" })).not.toThrow();
      expect(callback!(Object.freeze({ opaque: true }), { kind: "delta" })).toEqual({ opaque: true });
      expect(queuedCountReads).toBe(0);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("returns an already-owned second final without reading the second payload or queued counts", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v104-owned-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const sessionKey = "agent:main:dashboard:v104-owned";
      sessionAuthority(path, sessionKey);
      const ticket = store.accept({ runId: "secret-owned-run", ownerSessionKey: sessionKey, prompt: "secret-owned-prompt" });
      store.route(ticket.ticketId, false);

      const replyDispatch = installHarness(root, path);
      let callback: ((payload: any, info: any) => any) | undefined;
      let queuedCountReads = 0;
      const dispatcher = {
        appendBeforeDeliver: (fn: any) => { callback = fn; },
        getQueuedCounts: () => {
          queuedCountReads += 1;
          if (queuedCountReads > 1) throw new Error("already-owned:queued-count-read");
          return { final: 1 };
        },
        waitForIdle: () => new Promise<void>(() => {}),
      };
      replyDispatch({ runId: "secret-owned-run" }, { dispatcher });
      expect(callback).toBeTypeOf("function");
      const first = callback!({ text: "first final" }, { kind: "final" });
      expect(first.text).toContain("first final");
      expect(queuedCountReads).toBe(1);
      const second = throwingPayload("already-owned");
      expect(() => callback!(second, { kind: "final" })).not.toThrow();
      expect(queuedCountReads).toBe(1);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("preserves predecessor semantic read order for the supported final path", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v104-order-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const sessionKey = "agent:main:dashboard:v104-order";
      sessionAuthority(path, sessionKey);
      const ticket = store.accept({ runId: "secret-order-run", ownerSessionKey: sessionKey, prompt: "secret-order-prompt" });
      store.route(ticket.ticketId, false);

      const replyDispatch = installHarness(root, path);
      let callback: ((payload: any, info: any) => any) | undefined;
      const order: string[] = [];
      const dispatcher = {
        appendBeforeDeliver: (fn: any) => { callback = fn; },
        getQueuedCounts: () => { order.push("queued-final-count"); return { final: 1 }; },
        waitForIdle: () => new Promise<void>(() => {}),
      };
      replyDispatch({ runId: "secret-order-run" }, { dispatcher });
      const payload: Record<string, unknown> = {};
      Object.defineProperties(payload, {
        text: { enumerable: true, get: () => { order.push("text"); return "ordered final"; } },
        mediaUrl: { enumerable: true, get: () => { order.push("mediaUrl"); return undefined; } },
        mediaUrls: { enumerable: true, get: () => { order.push("mediaUrls"); return undefined; } },
      });
      callback!(payload, { kind: "final" });
      expect(order.slice(0, 5)).toEqual(["text", "text", "queued-final-count", "mediaUrl", "mediaUrls"]);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});