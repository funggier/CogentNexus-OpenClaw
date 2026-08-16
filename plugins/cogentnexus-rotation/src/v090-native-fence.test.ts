import { describe, expect, it } from "vitest";
import { shouldFenceNativeCnxTask } from "./v090-entry.js";

describe("v0.9 native OpenClaw task fence", () => {
  const failed = new Map([["CNXT-failed-1", "failed"]]);
  const cancelled = new Map([["CNXT-cancelled-1", "cancelled"]]);
  const completed = new Map([["CNXT-completed-1", "completed"]]);
  const waiting = new Map([["CNXT-waiting-1", "waiting"]]);

  it("fences a running CNX failed-ticket delivery", () => {
    expect(shouldFenceNativeCnxTask({
      id:"task-1",
      label:"plugin:cogentnexus-rotation",
      runId:"cnx-scheduled-deadbeef",
      status:"running",
      title:"[CogentNexus Delivery: ticket:5]\nCogentNexus Ticket CNXT-failed-1 reached terminal status failed.",
    }, failed)).toBe(true);
  });

  it("fences a running CNX cancelled ticket even without the delivery status line", () => {
    expect(shouldFenceNativeCnxTask({
      id:"task-2",
      label:"plugin:cogentnexus-rotation",
      runId:"cnx-direct-CNXT-cancelled-1-3-abcdef",
      status:"running",
      title:"Resume CogentNexus Ticket CNXT-cancelled-1",
    }, cancelled)).toBe(true);
  });

  it("does not fence completed or recoverable tickets", () => {
    const completedTask = {
      id:"task-3",
      label:"plugin:cogentnexus-rotation",
      runId:"cnx-direct-CNXT-completed-1-1-abcdef",
      status:"running",
      title:"Resume CogentNexus Ticket CNXT-completed-1",
    };
    const waitingTask = {
      id:"task-4",
      label:"plugin:cogentnexus-rotation",
      runId:"cnx-direct-CNXT-waiting-1-1-abcdef",
      status:"running",
      title:"Resume CogentNexus Ticket CNXT-waiting-1",
    };
    expect(shouldFenceNativeCnxTask(completedTask, completed)).toBe(false);
    expect(shouldFenceNativeCnxTask(waitingTask, waiting)).toBe(false);
  });

  it("does not touch unrelated OpenClaw tasks", () => {
    expect(shouldFenceNativeCnxTask({
      id:"task-5",
      label:"plugin:other",
      runId:"other-run",
      status:"running",
      title:"CogentNexus Ticket CNXT-failed-1 reached terminal status failed.",
    }, failed)).toBe(false);
  });

  it("fences blocked workflow delivery but not successful workflow completion", () => {
    expect(shouldFenceNativeCnxTask({
      id:"task-6",
      label:"plugin:cogentnexus-rotation",
      sourceId:"cnx-scheduled-workflow-blocked",
      status:"queued",
      title:"[CogentNexus Delivery: workflow:CNX-AUTO-test:12]\nCogentNexus workflow CNX-AUTO-test reached terminal status blocked.",
    }, new Map())).toBe(true);
    expect(shouldFenceNativeCnxTask({
      id:"task-7",
      label:"plugin:cogentnexus-rotation",
      sourceId:"cnx-scheduled-workflow-complete",
      status:"queued",
      title:"[CogentNexus Delivery: workflow:CNX-AUTO-test:13]\nCogentNexus workflow CNX-AUTO-test reached terminal status completed.",
    }, new Map())).toBe(false);
  });

  it("ignores already-terminal native task records", () => {
    expect(shouldFenceNativeCnxTask({
      id:"task-8",
      label:"plugin:cogentnexus-rotation",
      runId:"cnx-scheduled-deadbeef",
      status:"cancelled",
      title:"[CogentNexus Delivery: ticket:5]\nCogentNexus Ticket CNXT-failed-1 reached terminal status failed.",
    }, failed)).toBe(false);
  });
});
