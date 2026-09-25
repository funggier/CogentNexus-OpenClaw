import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";

import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

type Hook = (event: any, ctx: any) => unknown;

function assistantMessage(
  text: string,
  meta?: { runId?: string; mirrorOrigin?: string; runTerminal?: boolean },
) {
  return {
    role: "assistant",
    content: [{ type: "text", text }],
    stopReason: "stop",
    ...(meta
      ? {
          __openclaw: {
            ...(meta.runId ? { runId: meta.runId } : {}),
            ...(meta.mirrorOrigin ? { mirrorOrigin: meta.mirrorOrigin } : {}),
            ...(meta.runTerminal === true ? { runTerminal: true } : {}),
          },
        }
      : {}),
  };
}

function messageText(message: any): string {
  return (Array.isArray(message?.content) ? message.content : [])
    .filter((part: any) => part?.type === "text" && typeof part?.text === "string")
    .map((part: any) => part.text)
    .join("\n");
}

function setup(label: string) {
  const root = mkdtempSync(join(tmpdir(), `cnx446-${label}-`));
  const path = join(root, "tickets.sqlite3");
  const hooks = new Map<string, Hook>();
  let transcriptUpdate: ((event: any) => void) | undefined;

  installV091DashboardVerifiedDelivery(
    {
      on(name: string, handler: Hook) {
        hooks.set(name, handler);
      },
      runtime: {
        events: {
          onSessionTranscriptUpdate(handler: (event: any) => void) {
            transcriptUpdate = handler;
            return () => undefined;
          },
        },
      },
      logger: {},
    },
    { workspaceDir: root, ticketDatabasePath: path },
  );

  return {
    root,
    path,
    hooks,
    transcriptUpdate: () => transcriptUpdate,
    cleanup() {
      try {
        rmSync(root, { recursive: true, force: true, maxRetries: 5, retryDelay: 20 });
      } catch {
        // Windows can release SQLite handles just after the assertion completes.
      }
    },
  };
}

function acceptDirect(path: string, runId: string, sessionKey: string) {
  // Bootstrap the same v0.9 session + assistant-delivery schema used by production.
  expect(sessionAuthority(path, sessionKey)).toMatchObject({ state: "active", generation: 0 });
  const store = new TicketStore(path);
  const ticket = store.accept({ runId, ownerSessionKey: sessionKey, prompt: "CNX-446 production-topology prompt" });
  store.route(ticket.ticketId, false);
  return ticket;
}

function ticketState(path: string, ticketId: string) {
  const db = new DatabaseSync(path, { readOnly: true });
  try {
    const ticket = db.prepare(
      "SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?",
    ).get(ticketId);
    const deliveryCount = db.prepare(
      "SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'",
    ).get(ticketId);
    return { ticket, deliveryCount };
  } finally {
    db.close();
  }
}

describe("CNX-446 Dashboard Direct terminal-final boundary", () => {
  it("rejects mirrored progress with stopReason=stop when runTerminal is absent", () => {
    const s = setup("progress");
    try {
      const runId = "63bb6787-a016-426b-9ba0-d84ac15ff555";
      const sessionKey = "agent:main:dashboard:6090e8c3-88fc-420d-8ee8-1f498b9146f6";
      const ticket = acceptDirect(s.path, runId, sessionKey);
      const beforeMessageWrite = s.hooks.get("before_message_write");
      expect(beforeMessageWrite).toBeTypeOf("function");

      const progress = assistantMessage(
        "I will inspect the workspace first, then provide the final architecture answer.",
        { runId, mirrorOrigin: "codex-app-server" },
      );

      const result = beforeMessageWrite?.(
        { message: progress },
        { sessionKey, agentId: "main" },
      ) as any;

      expect(result).toBeUndefined();
      expect(messageText(result?.message ?? progress)).not.toContain("cogentnexus-openclaw-delivery:");

      const state = ticketState(s.path, ticket.ticketId) as any;
      expect(state.ticket).toEqual({
        status: "accepted",
        response_ready_at: null,
        delivery_confirmed_at: null,
      });
      expect(state.deliveryCount).toEqual({ n: 0 });
    } finally {
      s.cleanup();
    }
  });

  it("accepts the later exact mirrored terminal write and settles only that payload", () => {
    const s = setup("terminal");
    try {
      const runId = "cnx446-terminal-run";
      const sessionKey = "agent:main:dashboard:cnx446-terminal";
      const ticket = acceptDirect(s.path, runId, sessionKey);
      const beforeMessageWrite = s.hooks.get("before_message_write");
      const terminal = assistantMessage(
        "CNX446_TRUE_TERMINAL_RESULT",
        { runId, mirrorOrigin: "codex-app-server", runTerminal: true },
      );

      const writeResult = beforeMessageWrite?.(
        { message: terminal },
        { sessionKey, agentId: "main" },
      ) as any;
      const persisted = writeResult?.message ?? terminal;
      expect(messageText(persisted)).toContain("CNX446_TRUE_TERMINAL_RESULT");
      expect(messageText(persisted)).toContain("<!-- cogentnexus-openclaw-delivery:");

      s.transcriptUpdate()?.({
        sessionKey,
        sessionFile: join(s.root, "session.jsonl"),
        message: persisted,
        messageId: "cnx446-terminal-message",
        messageSeq: 4,
        agentId: "main",
        sessionId: "cnx446-terminal-session",
      });

      const db = new DatabaseSync(s.path, { readOnly: true });
      try {
        expect(db.prepare(
          "SELECT status,delivery_confirmed_at FROM tickets WHERE ticket_id=?",
        ).get(ticket.ticketId)).toMatchObject({ status: "completed" });
        expect(db.prepare(
          "SELECT text,status FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'",
        ).get(ticket.ticketId)).toEqual({
          text: "CNX446_TRUE_TERMINAL_RESULT",
          status: "delivered",
        });
      } finally {
        db.close();
      }
    } finally {
      s.cleanup();
    }
  });

  it("rejects mirrored terminal metadata for a different run", () => {
    const s = setup("wrong-run");
    try {
      const runId = "cnx446-owned-run";
      const sessionKey = "agent:main:dashboard:cnx446-wrong-run";
      const ticket = acceptDirect(s.path, runId, sessionKey);
      const beforeMessageWrite = s.hooks.get("before_message_write");
      const unrelated = assistantMessage(
        "UNRELATED_TERMINAL",
        { runId: "cnx446-other-run", mirrorOrigin: "codex-app-server", runTerminal: true },
      );

      const result = beforeMessageWrite?.(
        { message: unrelated },
        { sessionKey, agentId: "main" },
      ) as any;

      expect(result).toBeUndefined();
      const state = ticketState(s.path, ticket.ticketId) as any;
      expect(state.ticket).toEqual({
        status: "accepted",
        response_ready_at: null,
        delivery_confirmed_at: null,
      });
      expect(state.deliveryCount).toEqual({ n: 0 });
    } finally {
      s.cleanup();
    }
  });

  it("preserves the proven native fallback when OpenClaw does not provide mirrored runTerminal metadata", () => {
    const s = setup("native");
    try {
      const runId = "cnx446-native-ollama-run";
      const sessionKey = "agent:main:dashboard:cnx446-native";
      const ticket = acceptDirect(s.path, runId, sessionKey);
      const beforeMessageWrite = s.hooks.get("before_message_write");
      const nativeTerminal = assistantMessage("CNX446_NATIVE_TERMINAL");

      const writeResult = beforeMessageWrite?.(
        { message: nativeTerminal },
        { sessionKey, agentId: "main" },
      ) as any;
      const persisted = writeResult?.message ?? nativeTerminal;
      expect(messageText(persisted)).toContain("<!-- cogentnexus-openclaw-delivery:");

      s.transcriptUpdate()?.({
        sessionKey,
        sessionFile: join(s.root, "native-session.jsonl"),
        message: persisted,
        messageId: "cnx446-native-message",
        messageSeq: 1,
        agentId: "main",
        sessionId: "cnx446-native-session",
      });

      const db = new DatabaseSync(s.path, { readOnly: true });
      try {
        expect(db.prepare(
          "SELECT status FROM tickets WHERE ticket_id=?",
        ).get(ticket.ticketId)).toEqual({ status: "completed" });
        expect(db.prepare(
          "SELECT text,status FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'",
        ).get(ticket.ticketId)).toEqual({
          text: "CNX446_NATIVE_TERMINAL",
          status: "delivered",
        });
      } finally {
        db.close();
      }
    } finally {
      s.cleanup();
    }
  });
});
