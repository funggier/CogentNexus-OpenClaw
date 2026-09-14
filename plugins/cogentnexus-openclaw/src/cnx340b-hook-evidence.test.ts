import { DatabaseSync } from "node:sqlite";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import releaseEntry from "./v091-release-entry.js";

describe("CNX-340B before_agent_run evidence qualification", () => {
  it("captures exactly one hook, invokes it once, and reaches TicketStore admission without provider traffic", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-340b-hook-evidence-"));
    const cogentRoot = join(root, ".cogentnexus-openclaw");
    const databasePath = join(cogentRoot, "runtime", "tickets.sqlite3");
    mkdirSync(join(cogentRoot, "host"), { recursive: true });
    writeFileSync(join(cogentRoot, "host", "controller.json"), JSON.stringify({ schemaVersion: 2, cnxMode: "active", generation: 1 }));
    const callbacks = new Map<string, Array<{ callback: any; stack: string }>>();
    const providerCalls: string[] = [];
    const api: any = {
      pluginConfig: { workspaceDir: root, cogentNexusOpenClawRoot: cogentRoot, ticketFirst: true, preInferenceAdmission: true, ticketDatabasePath: databasePath, autoWorkflowCompletion: false },
      on: (name: string, callback: any) => { const stack = new Error().stack ?? ""; callbacks.set(name, [...(callbacks.get(name) ?? []), { callback, stack }]); },
      registerTool: () => {}, registerService: () => {},
      logger: { warn: () => {}, error: () => {}, info: () => {} },
      session: { workflow: {} }, runtime: { tasks: { managedFlows: {} } },
      config: { agents: { defaults: { workspace: root } } },
      callProvider: () => { providerCalls.push("callProvider"); throw new Error("provider call forbidden"); },
      runModel: () => { providerCalls.push("runModel"); throw new Error("model call forbidden"); },
    };
    try {
      await releaseEntry.register(api);
      const owners = callbacks.get("before_agent_run") ?? [];
      const admissionOwners = owners.filter(({ stack }) => stack.includes("index.ts:730"));
      expect(admissionOwners).toHaveLength(1);
      const prompt = "CNX-340B synthetic eligible owner event";
      const context = { sessionKey: "agent:main:owner", runId: "cnx-340b-run", workspaceDir: root };
      const result = await admissionOwners[0].callback({ prompt, senderIsOwner: true }, context);
      expect(result).toEqual({ outcome: "pass" });
      expect(providerCalls).toEqual([]);
      const db = new DatabaseSync(databasePath);
      try {
        const ticket = db.prepare("SELECT run_id, owner_session_key, prompt, status FROM tickets").get() as any;
        expect(ticket).toMatchObject({ run_id: context.runId, owner_session_key: context.sessionKey, prompt, status: "accepted" });
        expect(db.prepare("SELECT event_type FROM ticket_events ORDER BY event_id").all().map((row: any) => row.event_type)).toEqual(["accepted", "routed"]);
      } finally { db.close(); }
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("retains the release bridge provenance to the legacy registration boundary", () => {
    const source = readFileSync(new URL("./v091-release-entry.ts", import.meta.url), "utf8");
    expect(source).toContain('import legacyEntry from "./v091-final-entry.js"');
    expect(source).toContain("legacyEntry");
    expect(source).toContain("register(runtimeApi)");
    expect(readFileSync(new URL("./index.ts", import.meta.url), "utf8")).toContain('api.on("before_agent_run"');
  });
});
