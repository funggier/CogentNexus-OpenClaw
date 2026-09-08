export type CloudPassThroughInput = {
  hostMode: string;
  providerId: string;
  modelRef: string;
};

export type CloudPassThroughPolicy = {
  mode: "passthrough";
  providerId: string;
  modelRef: string;
  authOwner: "openclaw";
  lifecycleOwner: "openclaw";
  probePolicy: "gateway-only";
  recoveryOwner: "openclaw";
  durableWorkflow: "unsupported";
};

/**
 * Describe the deliberately narrow Cloud-provider boundary. OpenClaw owns the
 * configured route, authentication, provider lifecycle, and provider recovery;
 * CogentNexus-OpenClaw may only preserve the opaque route identity and its own delivery
 * continuity. No credential or endpoint is accepted here.
 */
export function cloudPassThroughPolicy(input: CloudPassThroughInput): CloudPassThroughPolicy {
  if (input.hostMode !== "passthrough") {
    throw new Error("Cloud provider pass-through requires PASSTHROUGH host mode");
  }
  const providerId = input.providerId.trim();
  const modelRef = input.modelRef.trim();
  if (!providerId) throw new Error("Cloud provider route requires a provider id");
  if (!modelRef) throw new Error("Cloud provider route requires an exact model route");
  if (providerId.toLowerCase() === "ollama" || modelRef.toLowerCase().startsWith("ollama/")) {
    throw new Error("Ollama is managed and cannot use Cloud provider pass-through");
  }
  if (/api[_-]?key|authorization|bearer|token|secret|password/i.test(`${providerId} ${modelRef}`)) {
    throw new Error("Cloud provider route must not contain credentials");
  }
  return {
    mode: "passthrough",
    providerId,
    modelRef,
    authOwner: "openclaw",
    lifecycleOwner: "openclaw",
    probePolicy: "gateway-only",
    recoveryOwner: "openclaw",
    durableWorkflow: "unsupported",
  };
}
