import { mkdtempSync, rmSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { sessionAuthority } from "./v090.js";
import { installV095InferenceHookBridge } from "./v095-inference-hook-bridge.js";

describe("v0.9.5 Discord inference identity fence", () => {
  it("keeps concurrent Discord runs distinct and preserves separate failover attempts inside one run", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-discord-inference-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:discord:channel:095001";
      const store = new TicketStore(databasePath);
      sessionAuthority(databasePath, sessionKey);
      const ticketA = store.accept({ runId: "discord-run-a", ownerSessionKey: sessionKey, prompt: "A" });
      const ticketB = store.accept({ runId: "discord-run-b", ownerSessionKey: sessionKey, prompt: "B" });
      store.route(ticketA.ticketId, false);
      store.route(ticketB.ticketId, false);

      const hooks = new Map<string, (event: any, ctx: any) => unknown>();
      const api: any = {
        pluginConfig: { ticketDatabasePath: databasePath, workspaceDir: root },
        on: (name: string, handler: any) => hooks.set(name, handler),
        logger: { warn: () => {} },
      };
      installV095InferenceHookBridge(api);
      const started = hooks.get("model_call_started")!;
      const ended = hooks.get("model_call_ended")!;

      started({ runId: "discord-run-a", callId: "call-a", provider: "openai", model: "m1" }, { runId: "discord-run-a", sessionKey, workspaceDir: root });
      started({ runId: "discord-run-a", callId: "call-a", provider: "openai", model: "m1" }, { runId: "discord-run-a", sessionKey, workspaceDir: root });
      started({ runId: "discord-run-a", callId: "call-a-failover", provider: "anthropic", model: "m2" }, { runId: "discord-run-a", sessionKey, workspaceDir: root });
      started({ runId: "discord-run-b", callId: "call-b", provider: "ollama", model: "m3" }, { runId: "discord-run-b", sessionKey, workspaceDir: root });
      ended({ runId: "discord-run-a", callId: "call-a", outcome: "error" }, { runId: "discord-run-a", sessionKey, workspaceDir: root });
      ended({ runId: "discord-run-a", callId: "call-a-failover", outcome: "completed" }, { runId: "discord-run-a", sessionKey, workspaceDir: root });
      ended({ runId: "discord-run-b", callId: "call-b", outcome: "completed" }, { runId: "discord-run-b", sessionKey, workspaceDir: root });

      const db = new DatabaseSync(databasePath, { readOnly: true });
      try {
        const rows = db.prepare("SELECT run_id,call_id,session_key,session_generation,provider,model,state,outcome FROM cnx_inference_attempt WHERE run_id IN (?,?) ORDER BY run_id,call_id").all("discord-run-a", "discord-run-b") as any[];
        expect(rows).toEqual([
          { run_id: "discord-run-a", call_id: "call-a", session_key: sessionKey, session_generation: 0, provider: "openai", model: "m1", state: "ended", outcome: "error" },
          { run_id: "discord-run-a", call_id: "call-a-failover", session_key: sessionKey, session_generation: 0, provider: "anthropic", model: "m2", state: "ended", outcome: "completed" },
          { run_id: "discord-run-b", call_id: "call-b", session_key: sessionKey, session_generation: 0, provider: "ollama", model: "m3", state: "ended", outcome: "completed" },
        ]);
      } finally {
        db.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
