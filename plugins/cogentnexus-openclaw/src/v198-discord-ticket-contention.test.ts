import { spawn, type ChildProcess } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import entry from "./index.js";
import { TicketStore } from "./ticket-store.js";

function holdWriterLock(databasePath: string, holdMs: number): Promise<ChildProcess> {
  const script = [
    'import { DatabaseSync } from "node:sqlite";',
    'const db = new DatabaseSync(process.argv[1]);',
    'db.exec("PRAGMA busy_timeout=5000; BEGIN IMMEDIATE;");',
    'process.stdout.write("LOCKED\\n");',
    'setTimeout(() => { db.exec("ROLLBACK"); db.close(); process.exit(0); }, Number(process.argv[2]));',
  ].join("\n");
  const child = spawn(process.execPath, ["--input-type=module", "-e", script, databasePath, String(holdMs)], {
    stdio: ["ignore", "pipe", "pipe"],
  });
  return new Promise((resolve, reject) => {
    let stderr = "";
    child.stderr?.on("data", (chunk) => { stderr += String(chunk); });
    child.once("error", reject);
    child.once("exit", (code) => {
      reject(new Error(`SQLite lock helper exited before LOCKED (code=${code}): ${stderr}`));
    });
    child.stdout?.on("data", (chunk) => {
      if (String(chunk).includes("LOCKED")) resolve(child);
    });
  });
}

describe("Task 198 Discord Ticket-first contention", () => {
  it("does not turn transient SQLite writer contention into a fail-closed before_agent_run exception", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v198-discord-contention-"));
    let locker: ChildProcess | undefined;
    try {
      const databasePath = join(root, "tickets.sqlite3");
      new TicketStore(databasePath).snapshot();

      const hooks = new Map<string, any>();
      const api: any = {
        pluginConfig: {
          ticketFirst: true,
          preInferenceAdmission: true,
          ticketDatabasePath: databasePath,
          autoWorkflowCompletion: false,
        },
        registerTool: () => {},
        registerService: () => {},
        on: (name: string, callback: any) => hooks.set(name, callback),
        logger: { warn: () => {}, error: () => {}, info: () => {} },
        session: { workflow: {} },
        runtime: { tasks: { managedFlows: {} } },
      };
      entry.register?.(api);

      locker = await holdWriterLock(databasePath, 5_500);
      const hook = hooks.get("before_agent_run");
      expect(hook).toBeTypeOf("function");

      const sessionKey = "agent:main:discord:channel:1531201432861282405";
      const runId = "task198-discord-contention-run";
      const prompt = "@Ce สวัสดีครับ";

      await expect(Promise.resolve().then(() => hook(
        { prompt, senderIsOwner: true },
        { sessionKey, runId, workspaceDir: root },
      ))).resolves.toEqual({ outcome: "pass" });

      const ticket = new TicketStore(databasePath).get(
        new TicketStore(databasePath).accept({ runId, ownerSessionKey: sessionKey, prompt }).ticketId,
      );
      expect(ticket).toMatchObject({ runId, ownerSessionKey: sessionKey, prompt, workflowEligible: false });
    } finally {
      if (locker && locker.exitCode === null) locker.kill();
      rmSync(root, { recursive: true, force: true });
    }
  }, 15_000);
});
