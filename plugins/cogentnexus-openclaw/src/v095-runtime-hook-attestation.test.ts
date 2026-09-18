import { describe, expect, it } from "vitest";
import {
  classifyRuntimeHookAttestation,
  registerRuntimeHookAttestation,
  type RuntimeHookAttestation,
} from "./v095-runtime-hook-attestation.js";

function snapshot(overrides: Partial<RuntimeHookAttestation> = {}): RuntimeHookAttestation {
  return {
    schemaVersion: 1,
    pluginId: "cogentnexus-openclaw",
    hookName: "before_agent_run",
    runnerReady: true,
    globalHookCount: 1,
    latestRegistryPluginHookCount: 1,
    classification: "PRESENT",
    ...overrides,
  };
}

describe("v0.9.5 runtime hook attestation", () => {
  it("classifies unavailable, absent, present, and ambiguous states conservatively", () => {
    expect(classifyRuntimeHookAttestation({
      runnerReady: false,
      globalHookCount: 0,
      latestRegistryPluginHookCount: null,
    })).toBe("RUNNER_UNAVAILABLE");

    expect(classifyRuntimeHookAttestation({
      runnerReady: true,
      globalHookCount: 0,
      latestRegistryPluginHookCount: 0,
    })).toBe("ABSENT");

    expect(classifyRuntimeHookAttestation({
      runnerReady: true,
      globalHookCount: 2,
      latestRegistryPluginHookCount: 1,
    })).toBe("PRESENT");

    expect(classifyRuntimeHookAttestation({
      runnerReady: true,
      globalHookCount: 2,
      latestRegistryPluginHookCount: 0,
    })).toBe("AMBIGUOUS");

    expect(classifyRuntimeHookAttestation({
      runnerReady: true,
      globalHookCount: 2,
      latestRegistryPluginHookCount: null,
    })).toBe("AMBIGUOUS");
  });

  it("registers a read-only Gateway RPC and returns only the supplied attestation snapshot", async () => {
    const registrations: Array<{
      method: string;
      handler: (ctx: { respond: (ok: boolean, payload: unknown) => void }) => unknown;
      options?: { scope?: string };
    }> = [];
    const expected = snapshot();

    registerRuntimeHookAttestation({
      registerGatewayMethod(method: string, handler: any, options?: { scope?: string }) {
        registrations.push({ method, handler, options });
      },
    } as any, () => expected);

    expect(registrations).toHaveLength(1);
    expect(registrations[0]?.method).toBe("cogentnexus.runtimeAttestation");
    expect(registrations[0]?.options).toEqual({ scope: "operator.read" });

    let response: { ok: boolean; payload: unknown } | undefined;
    await registrations[0]!.handler({
      respond(ok, payload) {
        response = { ok, payload };
      },
    });

    expect(response).toEqual({ ok: true, payload: expected });
  });

  it("does not upgrade a global hook owned by another registry/plugin into CogentNexus PRESENT", () => {
    expect(classifyRuntimeHookAttestation({
      runnerReady: true,
      globalHookCount: 1,
      latestRegistryPluginHookCount: 0,
    })).toBe("AMBIGUOUS");
  });
});
