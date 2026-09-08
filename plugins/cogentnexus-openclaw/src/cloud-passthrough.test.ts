import { describe, expect, it } from "vitest";
import {
  cloudPassThroughPolicy,
  type CloudPassThroughInput,
} from "./cloud-passthrough.js";

describe("Cloud provider pass-through policy", () => {
  it("keeps OpenClaw as auth and lifecycle owner for an exact native route", () => {
    const input: CloudPassThroughInput = {
      hostMode: "passthrough",
      modelRef: "openai/gpt-5.6-luna",
      providerId: "openai",
    };
    expect(cloudPassThroughPolicy(input)).toEqual({
      mode: "passthrough",
      providerId: "openai",
      modelRef: "openai/gpt-5.6-luna",
      authOwner: "openclaw",
      lifecycleOwner: "openclaw",
      probePolicy: "gateway-only",
      recoveryOwner: "openclaw",
      durableWorkflow: "unsupported",
    });
  });

  it("fails closed when passthrough has no exact model route", () => {
    expect(() => cloudPassThroughPolicy({
      hostMode: "passthrough",
      modelRef: "",
      providerId: "codex",
    })).toThrow(/model route/i);
  });

  it("rejects Ollama and credential-bearing route identities", () => {
    expect(() => cloudPassThroughPolicy({hostMode:"passthrough", providerId:"ollama", modelRef:"ollama/qwen"})).toThrow(/managed/i);
    expect(() => cloudPassThroughPolicy({hostMode:"passthrough", providerId:"openai", modelRef:"api-key/gpt"})).toThrow(/credentials/i);
  });
});
