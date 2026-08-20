import { existsSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { durableAdmissionEligible } from "./index.js";
import { withV095EphemeralEmbeddedSession } from "./v095-direct-recovery.js";
import { withV096InternalRecoveryAdmissionFence } from "./v096-direct-recovery.js";

describe("v0.9.6 Direct Recovery internal admission fence", () => {
  it("marks the ephemeral embedded recovery as an internal subagent-shaped session", async () => {
    let observed: any;
    const rawApi: any = {
      runtime: {
        agent: {
          async runEmbeddedAgent(input: any) {
            observed = input;
            expect(typeof input.sessionFile).toBe("string");
            expect(existsSync(input.sessionFile)).toBe(true);
            return { payloads: [{ text: "ok" }] };
          },
        },
      },
    };

    // Production composition: v096 wraps the real runtime first; v095 then
    // supplies the temporary sessionFile before invoking the wrapped runtime.
    const composed = withV095EphemeralEmbeddedSession(
      withV096InternalRecoveryAdmissionFence(rawApi),
    );
    await composed.runtime.agent.runEmbeddedAgent({
      sessionId: "cnx-direct-CNXT-fixture-1-g0",
      agentId: "main",
    });

    expect(observed.sessionKey).toBe("agent:main:subagent:cnx-recovery-cnx-direct-CNXT-fixture-1-g0");
    expect(observed.sessionKey).toContain(":subagent:");
    expect(durableAdmissionEligible({ sessionKey: observed.sessionKey, senderIsOwner: true })).toBe(false);
  });
});
