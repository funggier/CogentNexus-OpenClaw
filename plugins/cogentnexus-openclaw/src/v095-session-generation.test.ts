import { describe, expect, it } from "vitest";
import { shouldAdvanceSessionGeneration, type SessionGenerationCause } from "./v095-session-generation.js";

describe("v0.9.5 physical session generation rule", () => {
  it("does not advance generation for provider/model or runtime events", () => {
    const nonPhysical: SessionGenerationCause[] = [
      "provider_change",
      "model_change",
      "compaction",
      "gateway_restart",
    ];

    for (const cause of nonPhysical) {
      expect(shouldAdvanceSessionGeneration(cause, true)).toBe(false);
      expect(shouldAdvanceSessionGeneration(cause, false)).toBe(false);
    }
  });

  it("advances only when a physical lifecycle boundary replaces the session", () => {
    const physical: SessionGenerationCause[] = ["delete", "replace", "rotate"];

    for (const cause of physical) {
      expect(shouldAdvanceSessionGeneration(cause, true)).toBe(false);
      expect(shouldAdvanceSessionGeneration(cause, false)).toBe(true);
    }
  });
});
