import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("v0.9.5 provider-independent capabilities", () => {
  const sourcePath = resolve(process.cwd(), "src", "index.ts");
  const source = readFileSync(sourcePath, "utf8");

  it("does not turn providerMode pass-through into a durable-admission capability gate", () => {
    expect(source).not.toContain('if (config.providerMode === "passthrough" && decision.lane === "durable")');
    expect(source).not.toContain('providerMode:"passthrough",durableWorkflow:"unsupported"');
  });

  it("keeps continuation hooks independent of providerMode", () => {
    expect(source).not.toContain('config.providerMode !== "passthrough" && config.autoResume !== false && config.ticketFirst === true');
    expect(source).not.toContain('config.providerMode !== "passthrough" && !internalDelivery && !ticketedDirect');
  });

  it("keeps terminal workflow completion and Ticket recovery services provider-independent", () => {
    expect(source).not.toContain('config.providerMode !== "passthrough" && config.autoWorkflowCompletion !== false');
    expect(source).not.toContain('config.providerMode !== "passthrough" && config.ticketFirst === true');
  });

  it("retains providerMode as compatibility metadata", () => {
    expect(source).toContain('providerMode?: "managed" | "passthrough";');
    expect(source).toContain('providerMode: Type.Optional(Type.Union([Type.Literal("managed"), Type.Literal("passthrough")]');
  });
});
