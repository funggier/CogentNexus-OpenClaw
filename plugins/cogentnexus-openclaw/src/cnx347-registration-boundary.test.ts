import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, expect, it } from "vitest";
import releaseEntry from "./v091-release-entry.js";

describe("CNX-347 release-entry admission boundary", () => {
  it("registers exactly one effective before_agent_run admission owner at priority 2000 through the canonical release chain", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx347-registration-"));
    try {
      const controllerDir = join(root, ".cogentnexus-openclaw", "host");
      mkdirSync(controllerDir, { recursive: true });
      writeFileSync(join(controllerDir, "controller.json"), JSON.stringify({ schemaVersion: 2, cnxMode: "active", generation: 1 }));
      const registrations: Array<{ name: string; handler: Function; options?: { priority?: number } }> = [];
      const api: any = {
        pluginConfig: { workspaceDir: root, ticketFirst: true, preInferenceAdmission: true, autoWorkflowCompletion: false },
        config: { agents: { defaults: { workspace: root } } },
        logger: { info() {}, warn() {}, error() {}, debug() {} },
        on(name: string, handler: Function, options?: { priority?: number }) { registrations.push({ name, handler, options }); },
        registerService() {}, registerTool() {}, registerCommand() {}, registerCli() {}, registerGatewayMethod() {},
        session: { workflow: {} }, runtime: { tasks: { managedFlows: {} } },
      };

      await releaseEntry.register?.(api);

      const admission = registrations.filter((item) => item.name === "before_agent_run" && item.options?.priority === 2000);
      expect(admission).toHaveLength(1);
      const result = await admission[0].handler(
        { prompt: "PHASE 1\nA\nPHASE 2\nB\nPHASE 3\nC", senderIsOwner: true },
        { sessionKey: "agent:main:dashboard:cnx347", runId: "cnx347-run", workspaceDir: root },
      );
      expect(result).toMatchObject({ outcome: "block", category: "cnxclaw_ticket_admission" });
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});
