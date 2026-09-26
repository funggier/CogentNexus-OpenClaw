import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";

import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV091DashboardVerifiedDelivery } from "./v091-dashboard-verified-delivery.js";

type Hook = (event: any, ctx: any) => unknown;

function setup(label: string) {
  const root = mkdtempSync(join(tmpdir(), `cnx448-${label}-`));
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
      } catch {}
    },
  };
}

function acceptDirect(path: string, runId: string, sessionKey: string) {
  expect(sessionAuthority(path, sessionKey)).toMatchObject({ state: "active", generation: 0 });
  const store = new TicketStore(path);
  const ticket = store.accept({ runId, ownerSessionKey: sessionKey, prompt: "CNX-448 native terminal-boundary prompt" });
  store.route(ticket.ticketId, false);
  return ticket;
}

function state(path: string, ticketId: string) {
  const db = new DatabaseSync(path, { readOnly: true });
  try {
    return {
      ticket: db.prepare(
        "SELECT status,response_ready_at,delivery_confirmed_at FROM tickets WHERE ticket_id=?",
      ).get(ticketId),
      deliveries: db.prepare(
        "SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND kind='direct_result'",
      ).get(ticketId),
    };
  } finally {
    db.close();
  }
}

function nativeMessage(input: {
  runId: string;
  text: string;
  stopReason: string;
  errorMessage?: string;
  toolCalls?: number;
}) {
  return {
    role: "assistant",
    provider: "ollama",
    model: "qwen3.8:27b",
    stopReason: input.stopReason,
    ...(input.errorMessage ? { errorMessage: input.errorMessage } : {}),
    content: [
      { type: "text", text: input.text },
      ...Array.from({ length: input.toolCalls ?? 0 }, (_, i) => ({
        type: "toolCall",
        id: `call-${i + 1}`,
        name: i === 0 ? "read" : "memory_search",
        arguments: {},
      })),
    ],
    __openclaw: { runId: input.runId },
  };
}

describe("CNX-448 native Ollama terminal authority", () => {
  it("keeps the live toolUse topology non-terminal", () => {
    const s = setup("tool-use");
    try {
      const runId = "189e1a24-8230-4d50-90fc-d24d25ca1acc";
      const sessionKey = "agent:main:dashboard:4e97d1d4-2007-43d0-838d-0a929f1e8140";
      const ticket = acceptDirect(s.path, runId, sessionKey);
      const write = s.hooks.get("before_message_write");
      const message = nativeMessage({
        runId,
        text: "I will inspect the skill and memory before answering. </think>",
        stopReason: "toolUse",
        toolCalls: 2,
      });

      expect(write?.({ message }, { sessionKey, agentId: "main" })).toBeUndefined();
      expect(state(s.path, ticket.ticketId)).toEqual({
        ticket: { status: "accepted", response_ready_at: null, delivery_confirmed_at: null },
        deliveries: { n: 0 },
      });
    } finally {
      s.cleanup();
    }
  });

  it("does not allow a native terminal message for another exact run to capture the Ticket", () => {
    const s = setup("wrong-run");
    try {
      const runId = "cnx448-owned-run";
      const sessionKey = "agent:main:dashboard:cnx448-wrong-run";
      const ticket = acceptDirect(s.path, runId, sessionKey);
      const write = s.hooks.get("before_message_write");
      const message = nativeMessage({
        runId: "cnx448-other-run",
        text: "UNRELATED_NATIVE_FINAL",
        stopReason: "stop",
      });

      expect(write?.({ message }, { sessionKey, agentId: "main" })).toBeUndefined();
      expect(state(s.path, ticket.ticketId)).toEqual({
        ticket: { status: "accepted", response_ready_at: null, delivery_confirmed_at: null },
        deliveries: { n: 0 },
      });
    } finally {
      s.cleanup();
    }
  });

  it("does not settle aborted/error native output as success", () => {
    const s = setup("aborted");
    try {
      const runId = "cnx448-aborted-run";
      const sessionKey = "agent:main:dashboard:cnx448-aborted";
      const ticket = acceptDirect(s.path, runId, sessionKey);
      const write = s.hooks.get("before_message_write");
      const message = nativeMessage({
        runId,
        text: "partial output",
        stopReason: "aborted",
        errorMessage: "request timed out",
      });

      expect(write?.({ message }, { sessionKey, agentId: "main" })).toBeUndefined();
      expect(state(s.path, ticket.ticketId)).toEqual({
        ticket: { status: "accepted", response_ready_at: null, delivery_confirmed_at: null },
        deliveries: { n: 0 },
      });
    } finally {
      s.cleanup();
    }
  });

  it("still settles an exact native terminal success exactly once", () => {
    const s = setup("terminal");
    try {
      const runId = "cnx448-native-final";
      const sessionKey = "agent:main:dashboard:cnx448-terminal";
      const ticket = acceptDirect(s.path, runId, sessionKey);
      const write = s.hooks.get("before_message_write");
      const message = nativeMessage({
        runId,
        text: "CNX448_NATIVE_FINAL",
        stopReason: "stop",
      });

      const result = write?.({ message }, { sessionKey, agentId: "main" }) as any;
      const persisted = result?.message ?? message;
      expect(persisted.content[0].text).toContain("cogentnexus-openclaw-delivery:");

      s.transcriptUpdate()?.({
        sessionKey,
        sessionFile: join(s.root, "native-session.jsonl"),
        message: persisted,
        messageId: "cnx448-native-final-message",
        messageSeq: 1,
        agentId: "main",
        sessionId: "cnx448-native-final-session",
      });

      const db = new DatabaseSync(s.path, { readOnly: true });
      try {
        expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(ticket.ticketId))
          .toEqual({ status: "completed" });
        expect(db.prepare(
          "SELECT count(*) AS n FROM cnx_assistant_delivery WHERE ticket_id=? AND status='delivered'",
        ).get(ticket.ticketId)).toEqual({ n: 1 });
        expect(db.prepare(
          "SELECT count(*) AS n FROM ticket_events WHERE ticket_id=? AND event_type='delivery_confirmed'",
        ).get(ticket.ticketId)).toEqual({ n: 1 });
      } finally {
        db.close();
      }
    } finally {
      s.cleanup();
    }
  });
});
