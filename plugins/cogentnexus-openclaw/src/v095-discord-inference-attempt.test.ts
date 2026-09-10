import { mkdtempSync, rmSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { TicketStore } from "./ticket-store.js";
import { installV095InferenceHookBridge } from "./v095-inference-hook-bridge.js";

describe("v0.9.5 Discord inference identity fence", () => {
  it("keeps concurrent Discord runs distinct and never lets a duplicate start create a second attempt", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-discord-inference-"));
    try {
      const databasePath = join(root, "tickets.sqlite3");
      const sessionKey = "agent:main:discord:channel:095001";
      const store = new TicketStore(databasePath);
      store.accept({ runId: "discord-run-a", ownerSessionKey: sessionKey, prompt: "A" });
      store.accept({ runId: "discord-run-b", ownerSessionKey: sessionKey, prompt: "B" });
      store.route(store.snapshot().ticketIds?.[0] ?? "", false);

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
      started({ runId: "discord-run-b", callId: "call-b", provider: "ollama", model: "m2" }, { runId: "discord-run-b", sessionKey, workspaceDir: root });
      ended({ runId: "discord-run-a", callId: "call-a", outcome: "error" }, { runId: "discord-run-a", sessionKey, workspaceDir: root });
      ended({ runId: "discord-run-b", callId: "call-b", outcome: "completed" }, { runId: "discord-run-b", sessionKey, workspaceDir: root });

      const db = new DatabaseSync(databasePath, { readOnly: true });
      try {
        const rows = db.prepare("SELECT run_id,session_key,session_generation,provider,model,state,outcome FROM cnx_inference_attempt WHERE run_id IN (?,?) ORDER BY run_id").all("discord-run-a", "discord-run-b") as any[];
        expect(rows).toEqual([
          { run_id: "discord-run-a", session_key: sessionKey, session_generation: 0, provider: "openai", model: "m1", state: "ended", outcome: "error" },
          { run_id: "discord-run-b", session_key: sessionKey, session_generation: 0, provider: "ollama", model: "m2", state: "ended", outcome: "completed" },
        ]);
      } finally {
        db.close();
      }
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
