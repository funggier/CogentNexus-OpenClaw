import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

export type AdmissionDecision = {
  lane: "direct" | "durable";
  score: number;
  reasons: string[];
  sections: Array<{ id: string; title: string; body: string }>;
};

const durableTerms = [
  /(?:until|จน)(?:\s|\S){0,24}(?:complete|finish|เสร็จ)/iu,
  /ห้าม(?:ข้าม|ลด)(?:\s|\S){0,40}(?:phase|ขั้น|ขอบเขต|จำนวน)/iu,
  /(?:dependency|validator|checkpoint|resume|disaster recovery|capacity planning)/iu,
  /(?:อย่างน้อย|at least)\s*\d+/iu,
];

function explicitSections(prompt: string) {
  const matches = [...prompt.matchAll(/^\s*(PHASE\s+\d+|ขั้น(?:ตอน)?ที่\s*\d+|STEP\s+\d+)\b[^\r\n]*/gimu)];
  return matches.map((match, index) => {
    const start = match.index ?? 0;
    const end = matches[index + 1]?.index ?? prompt.length;
    const title = match[0].trim();
    return { id: `component-${String(index + 1).padStart(2, "0")}`, title, body: prompt.slice(start, end).trim() };
  });
}

export function classifyDurableRequest(prompt: string, minimumScore = 5): AdmissionDecision {
  if (/\[(?:CogentNexus|Subagent) Context\]|cogent-workflow-result-|#cogent-direct\b/iu.test(prompt)) {
    return { lane: "direct", score: 0, reasons: ["internal-or-explicit-direct"], sections: [] };
  }
  const sections = explicitSections(prompt);
  let score = 0;
  const reasons: string[] = [];
  if (sections.length >= 3) { score += 6; reasons.push(`explicit-components:${sections.length}`); }
  if (prompt.length >= 1800) { score += 2; reasons.push("large-request"); }
  const matchedTerms = durableTerms.filter((pattern) => pattern.test(prompt)).length;
  if (matchedTerms >= 2) { score += 3; reasons.push(`durable-contract-signals:${matchedTerms}`); }
  const numericObligations = [...prompt.matchAll(/(?:อย่างน้อย|at least)\s*\d+|\b\d+\s+(?:services?|tables?|endpoints?|phases?|regions?)/giu)].length;
  if (numericObligations >= 3) { score += 3; reasons.push(`numeric-obligations:${numericObligations}`); }
  return { lane: score >= minimumScore ? "durable" : "direct", score, reasons, sections };
}

function safeId(value: string) {
  return value.replace(/[^A-Za-z0-9_-]/g, "-").replace(/-+/g, "-").slice(0, 72);
}

export function compileDurableIntake(input: {
  workspaceDir: string;
  prompt: string;
  runId: string;
  decision: AdmissionDecision;
  model: string;
}) {
  const taskId = `CNX-AUTO-${safeId(input.runId)}`;
  const relativeBase = `.cogent/intake/${taskId}`;
  const base = resolve(input.workspaceDir, relativeBase);
  mkdirSync(base, { recursive: true });
  writeFileSync(resolve(base, "request.txt"), input.prompt, "utf8");
  const sections = input.decision.sections.length > 0 ? input.decision.sections : [
    { id: "component-01", title: "Decompose and specify", body: "Produce a concrete dependency-aware execution specification." },
    { id: "component-02", title: "Execute", body: "Produce the requested deliverable from the verified specification." },
    { id: "component-03", title: "Verify and repair", body: "Check every stated obligation, repair failures, and report evidence." },
  ];
  const steps: any[] = [];
  const outputs: string[] = [];
  sections.forEach((section, index) => {
    const output = `${relativeBase}/artifacts/${section.id}.md`;
    const instruction = `${relativeBase}/prompts/${section.id}.txt`;
    mkdirSync(resolve(base, "prompts"), { recursive: true });
    writeFileSync(resolve(input.workspaceDir, instruction), [
      "Act as one bounded CogentNexus worker. Complete only the component below.",
      "Treat the full request appended by the controller as authoritative context.",
      "Produce a substantive artifact, state assumptions, and do not claim other components are complete.",
      `Component: ${section.title}`,
      section.body,
    ].join("\n\n"), "utf8");
    steps.push({
      id: section.id,
      dependsOn: index === 0 ? [] : [sections[index - 1].id],
      executor: { type: "ollama", model: input.model, promptFile: instruction, includeFiles: [`${relativeBase}/request.txt`], output, timeoutSeconds: 86400 },
      outputs: [output],
      outputMinimumBytes: 80,
      maximumAttempts: 2,
      idempotent: true,
    });
    outputs.push(output);
  });
  const assembled = `${relativeBase}/artifacts/assembled.md`;
  steps.push({
    id: "assemble",
    dependsOn: sections.map((section) => section.id),
    executor: { type: "concat", inputs: outputs, output: assembled },
    outputs: [assembled],
    outputMinimumBytes: 200,
    maximumAttempts: 1,
    idempotent: true,
  });
  const manifest = { schemaVersion: 1, taskId, goal: "Complete an automatically admitted durable request through bounded verified components", admission: { score: input.decision.score, reasons: input.decision.reasons }, steps };
  const manifestPath = `${relativeBase}/manifest.json`;
  writeFileSync(resolve(input.workspaceDir, manifestPath), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  return { taskId, manifestPath, componentCount: sections.length, assembledOutput: assembled };
}
