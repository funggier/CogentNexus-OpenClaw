import { describe, expect, it } from "vitest";
import { admissionTraceFields } from "./index.js";

describe("CNX-359 admission trace diagnostics", () => {
  it("exposes a non-secret correlated trace record", () => {
    const record = admissionTraceFields({
      state: "admission.trace.started",
      traceId: "trace-1",
      runId: "run-1",
      sessionKey: "agent:main:dashboard:test",
      sessionId: "session-1",
      senderIsOwner: true,
      dashboardNamespaceMatch: true,
      ticketFirst: true,
      ticketIntakeEligible: true,
    });
    expect(record).toMatchObject({
      state: "admission.trace.started",
      traceId: "trace-1",
      runId: "run-1",
      sessionKey: "agent:main:dashboard:test",
      sessionId: "session-1",
    });
    expect(record).not.toHaveProperty("prompt");
  });
});
