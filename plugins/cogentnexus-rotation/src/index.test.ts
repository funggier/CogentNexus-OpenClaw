import { describe, expect, it } from "vitest";
import entry, { autoResumeTag, isResumableInterruption, rotationIdentity, scheduleInterruptedResume } from "./index.js";
import { assessSession, selectActiveDescendant } from "./context-guard.js";
import { getToolPluginMetadata } from "openclaw/plugin-sdk/tool-plugin";

describe("cogentnexus-rotation", () => {
  it("declares the rotation tool", () => {
    expect(getToolPluginMetadata(entry)?.tools.map((tool) => tool.name)).toEqual(["cogent_rotation"]);
  });

  it("uses a deterministic generation-fenced identity", () => {
    expect(rotationIdentity("CNX-PHASE4-001", 3)).toEqual({
      runId: "cogent-rotate-cnx-phase4-001-3",
      childSessionKey: "agent:main:cogent-rotate-cnx-phase4-001-3",
    });
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
});
