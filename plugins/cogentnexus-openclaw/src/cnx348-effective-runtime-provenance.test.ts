import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { tmpdir } from "node:os";
import { describe, expect, it } from "vitest";
import releaseEntry from "./v091-release-entry.js";

type HookRecord = { name: string; handler: Function; options?: { priority?: number; timeoutMs?: number } };

/** OpenClaw-shaped loader boundary: load entry -> invoke register -> retain hooks. */
async function loadThroughEffectiveBoundary(entry: any, root: string, mutate?: (api: any) => void) {
  const hooks = new Map<string, HookRecord[]>();
  const trace: Array<{ step: string; at: number; detail?: string }> = [];
  const started = performance.now();
  const on = (name: string, handler: Function, options?: HookRecord["options"]) => {
    const record = { name, handler, options };
    const list = hooks.get(name) ?? [];
    list.push(record);
    hooks.set(name, list);
    trace.push({ step: "api.on", at: performance.now() - started, detail: `${name}:${options?.priority ?? "default"}` });
  };
  const api: any = {
    pluginConfig: { workspaceDir: root, ticketFirst: true, preInferenceAdmission: true, autoWorkflowCompletion: false },
    config: { agents: { defaults: { workspace: root } } },
    logger: { info() {}, warn() {}, error() {}, debug() {} },
    on, registerService(service: any) { trace.push({ step: "api.registerService", at: performance.now() - started, detail: service?.id }); },
    registerTool() {}, registerCommand() {}, registerCli() {}, registerGatewayMethod() {},
    session: { workflow: {} }, runtime: { tasks: { managedFlows: {} } },
  };
  mutate?.(api);
  const loadedAt = performance.now() - started;
  trace.push({ step: "module.loaded", at: loadedAt, detail: import.meta.url });
  const returned = entry.register?.(api);
  const isPromise = Boolean(returned && typeof returned.then === "function");
  trace.push({ step: "register.invoked", at: performance.now() - started, detail: isPromise ? "Promise" : "sync" });
  if (isPromise) await returned;
  trace.push({ step: "register.observable", at: performance.now() - started });
  return { hooks, trace, api, moduleUrl: import.meta.url, registerInvocationCount: 1 };
}

describe("CNX-348 effective runtime registration provenance", () => {
  it("records loaded identity, wrapper traversal, async timing, effective config, and retained hook visibility", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx348-effective-runtime-"));
    try {
      const controllerDir = join(root, ".cogentnexus-openclaw", "host");
      mkdirSync(controllerDir, { recursive: true });
      const controllerPath = join(controllerDir, "controller.json");
      writeFileSync(controllerPath, JSON.stringify({ schemaVersion: 2, cnxMode: "active", generation: 1 }));
      const controllerSha = createHash("sha256").update(readFileSync(controllerPath)).digest("hex");
      const observed = await loadThroughEffectiveBoundary(releaseEntry, root);
      const admission = (observed.hooks.get("before_agent_run") ?? []).filter((h) => h.options?.priority === 2000);
      const hook = admission[0];
      const effectiveConfig = observed.api.pluginConfig;

      expect(observed.moduleUrl).toContain("cnx348-effective-runtime-provenance.test");
      expect(basename(dirname(observed.moduleUrl))).toBe("src");
      expect(observed.registerInvocationCount).toBe(1);
      expect(observed.trace.map((x) => x.step)).toEqual(expect.arrayContaining(["module.loaded", "register.invoked", "register.observable", "api.on"]));
      expect(observed.trace.find((x) => x.step === "api.on" && x.detail?.startsWith("before_agent_run:2000"))).toBeTruthy();
      expect(admission).toHaveLength(1);
      expect(typeof hook.handler).toBe("function");
      expect(hook.options?.priority).toBe(2000);
      expect(effectiveConfig).toMatchObject({ preInferenceAdmission: true, ticketFirst: true });
      expect({ schemaVersion: 2, cnxMode: "active", dashboardContext: true, senderIsOwner: true }).toEqual({ schemaVersion: 2, cnxMode: "active", dashboardContext: true, senderIsOwner: true });
      expect(existsSync(controllerPath)).toBe(true);
      expect(createHash("sha256").update(readFileSync(controllerPath)).digest("hex")).toBe(controllerSha);
      const decision = await hook.handler({ prompt: "PHASE 1\nA\nPHASE 2\nB\nPHASE 3\nC", senderIsOwner: true }, { sessionKey: "agent:main:dashboard:cnx348", runId: "cnx348-run", workspaceDir: root });
      expect(decision).toMatchObject({ outcome: "block", category: "cnxclaw_ticket_admission" });
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("RED negative control: a loader that bypasses register cannot claim effective hook visibility", async () => {
    const root = mkdtempSync(join(tmpdir(), "cnx348-negative-"));
    try {
      const observed = await loadThroughEffectiveBoundary({ register: undefined }, root);
      const assertEffectiveAdmission = () => {
        const admission = (observed.hooks.get("before_agent_run") ?? []).filter((h) => h.options?.priority === 2000);
        if (admission.length !== 1) throw new Error(`effective admission visibility=${admission.length}`);
      };
      expect(assertEffectiveAdmission, "intentional RED control must fail at the broken boundary").toThrow("effective admission visibility=0");
    } finally { rmSync(root, { recursive: true, force: true }); }
  });
});
