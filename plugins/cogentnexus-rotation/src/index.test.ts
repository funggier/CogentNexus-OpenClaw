import { describe, expect, it } from "vitest";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import entry, { autoResumeTag, completionMessage, deliverWorkflowCompletion, isResumableInterruption, pendingWorkflowCompletions, rotationCandidates, rotationIdentity, scheduleInterruptedResume, workflowCompletionTag } from "./index.js";
import { assessSession, selectActiveDescendant } from "./context-guard.js";
import { getToolPluginMetadata } from "openclaw/plugin-sdk/tool-plugin";

describe("cogentnexus-rotation", () => {
  it("declares the rotation tool", () => {
    expect(getToolPluginMetadata(entry)?.tools.map((tool) => tool.name)).toEqual(["cogent_rotation", "cogent_workflow_start"]);
  });

  it("uses a deterministic generation-fenced identity", () => {
    expect(rotationIdentity("CNX-PHASE4-001", 3)).toEqual({
      runId: "cogent-rotate-cnx-phase4-001-3",
      childSessionKey: "agent:main:cogent-rotate-cnx-phase4-001-3",
    });
  });

  it("selects only verified rotation observations for the current owner session", () => {
    const output = JSON.stringify({ observations: [
      { taskId: "T1", sessionKey: "owner", status: "observed", rotationRequired: true },
      { taskId: "T2", sessionKey: "other", status: "observed", rotationRequired: true },
      { taskId: "T3", sessionKey: "owner", status: "observed", rotationRequired: false },
    ] });
    expect(rotationCandidates(output, "owner")).toEqual(["T1"]);
  });

  it("rotates before token pressure when the raw transcript is large", () => {
    expect(assessSession({
      key: "old",
      totalTokens: 128231,
      totalTokensFresh: true,
      contextTokens: 372000,
      transcriptBytes: 7_973_463,
    }).action).toBe("ROTATE");
  });

  it("rotates immediately after context overflow or repeated compaction", () => {
    expect(assessSession({ key: "s", contextLengthExceeded: true }).action).toBe("ROTATE");
    expect(assessSession({ key: "s", compactionCount: 2 }).action).toBe("ROTATE");
  });

  it("follows the newest running descendant instead of a completed binding", () => {
    const selected = selectActiveDescendant("owner", [
      { key: "owner", status: "done", updatedAt: 1 },
      { key: "child-1", parentSessionKey: "owner", status: "done", updatedAt: 2 },
      { key: "child-2", parentSessionKey: "child-1", status: "running", updatedAt: 3 },
    ]);
    expect(selected?.key).toBe("child-2");
  });

  it("classifies only resumable terminal failures", () => {
    expect(isResumableInterruption(false, "CLI transcript compaction failed: context_length_exceeded")).toBe(true);
    expect(isResumableInterruption(false, "Interrupted while waiting on model work")).toBe(true);
    expect(isResumableInterruption(true, "Interrupted")).toBe(false);
    expect(isResumableInterruption(false, "permission denied")).toBe(false);
  });

  it("builds a scheduler-safe deterministic resume tag", () => {
    expect(autoResumeTag("run:abc/123")).toBe("cogent-resume-run-abc-123");
  });

  it("schedules exactly one continuation turn for an interrupted run", async () => {
    const unscheduled: unknown[] = [];
    const scheduled: Array<Record<string, unknown>> = [];
    const scheduledRuns = new Set<string>();
    const workflow = {
      async unscheduleSessionTurnsByTag(input: unknown) { unscheduled.push(input); },
      async scheduleSessionTurn(input: Record<string, unknown>) { scheduled.push(input); },
    };
    const input = {
      success: false,
      error: "Interrupted while waiting on model work",
      runId: "run:fixture/1",
      sessionKey: "agent:main:fixture",
      workflow,
      scheduledRuns,
    };
    await expect(scheduleInterruptedResume(input)).resolves.toBe(true);
    await expect(scheduleInterruptedResume(input)).resolves.toBe(false);
    expect(unscheduled).toHaveLength(1);
    expect(scheduled).toHaveLength(1);
    expect(scheduled[0]).toMatchObject({
      sessionKey: "agent:main:fixture",
      deleteAfterRun: true,
      deliveryMode: "announce",
      tag: "cogent-resume-run-fixture-1",
    });
  });

  it("discovers only pending terminal workflow outboxes", () => {
    const root = mkdtempSync(join(tmpdir(), "cogent-completion-"));
    try {
      const base = join(root, ".cogent", "workflows", "WF-1");
      mkdirSync(base, { recursive: true });
      const notice = {schemaVersion:1,taskId:"WF-1",ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:7,createdAt:new Date().toISOString(),deliveryStatus:"pending"};
      writeFileSync(join(base,"completion.json"), JSON.stringify(notice));
      const found = pendingWorkflowCompletions(root);
      expect(found).toHaveLength(1);
      expect(workflowCompletionTag(found[0].notice)).toBe("cogent-workflow-result-WF-1-7");
      expect(completionMessage(found[0].notice)).toContain("terminal status completed");
    } finally { rmSync(root, { recursive:true, force:true }); }
  });

  it("finishes TaskFlow, schedules the owner once by tag, and commits delivery", async () => {
    const root = mkdtempSync(join(tmpdir(), "cogent-delivery-"));
    try {
      const path = join(root,"completion.json");
      const notice = {schemaVersion:1,taskId:"WF-2",ownerSessionKey:"agent:main:owner",workflowStatus:"completed",stateRevision:9,createdAt:new Date().toISOString(),deliveryStatus:"pending"};
      writeFileSync(path, JSON.stringify(notice));
      const scheduled: any[] = [], finished: any[] = [];
      const flow = {flowId:"flow-1",syncMode:"managed",revision:1};
      const taskFlow = {list:()=>[],createManaged:()=>flow,get:()=>flow,finish:(value:any)=>finished.push(value),fail:()=>{ throw new Error("unexpected fail"); }};
      const api = {runtime:{tasks:{managedFlows:{bindSession:()=>taskFlow}}},session:{workflow:{unscheduleSessionTurnsByTag:async()=>{},scheduleSessionTurn:async(value:any)=>scheduled.push(value)}}};
      await deliverWorkflowCompletion(api,path,notice);
      expect(finished).toHaveLength(1);
      expect(scheduled[0]).toMatchObject({sessionKey:"agent:main:owner",tag:"cogent-workflow-result-WF-2-9",deliveryMode:"announce"});
      expect(JSON.parse(readFileSync(path,"utf8")).deliveryStatus).toBe("delivered");
    } finally { rmSync(root, { recursive:true, force:true }); }
  });
});
