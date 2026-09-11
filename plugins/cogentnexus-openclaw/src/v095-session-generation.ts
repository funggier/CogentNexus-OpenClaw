export type SessionGenerationCause =
  | "delete"
  | "replace"
  | "rotate"
  | "provider_change"
  | "model_change"
  | "compaction"
  | "gateway_restart";

/**
 * Return whether an event represents a physical ownership boundary that must
 * advance the durable CNX session generation.
 *
 * Provider/model/runtime events never advance generation on their own. A
 * delete/replace/rotate only advances generation when the physical OpenClaw
 * session is actually changing.
 */
export function shouldAdvanceSessionGeneration(
  cause: SessionGenerationCause,
  samePhysicalSession: boolean,
): boolean {
  if (cause === "delete" || cause === "replace" || cause === "rotate") {
    return !samePhysicalSession;
  }
  return false;
}
