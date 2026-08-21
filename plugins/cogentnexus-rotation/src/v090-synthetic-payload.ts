import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { relative, resolve } from "node:path";

export type SyntheticPayloadConfig = {
  syntheticPromptInlineChars?: number;
  syntheticPromptChunkChars?: number;
};

export type SyntheticPayloadBundle = {
  message:string;
  externalized:boolean;
  rootPath?:string;
  manifestPath?:string;
  sha256?:string;
  chunkCount?:number;
};

function safeRelative(workspace:string,path:string) {
  return relative(workspace,path).replace(/\\/g,"/");
}

function boundedExcerpt(text:string,maxChars:number) {
  if(text.length<=maxChars)return text;
  const half=Math.max(256,Math.floor(maxChars/2));
  return `${text.slice(0,half)}\n\n...[exact middle omitted from inline prompt; read durable chunks]...\n\n${text.slice(-half)}`;
}

export function externalizeOversizedSyntheticPayload(input:{
  workspaceDir:string;
  sessionKey:string;
  message:string;
  config?:SyntheticPayloadConfig;
}):SyntheticPayloadBundle {
  const inlineLimit=Math.max(4_000,Math.min(Math.floor(input.config?.syntheticPromptInlineChars ?? 12_000),48_000));
  if(input.message.length<=inlineLimit)return {message:input.message,externalized:false};

  const chunkSize=Math.max(2_000,Math.min(Math.floor(input.config?.syntheticPromptChunkChars ?? 8_000),24_000));
  const sha256=createHash("sha256").update(input.message,"utf8").digest("hex");
  const sessionHash=createHash("sha256").update(input.sessionKey,"utf8").digest("hex").slice(0,16);
  const root=resolve(input.workspaceDir,".cogent","context","synthetic-input",sessionHash,sha256.slice(0,24));
  mkdirSync(root,{recursive:true});
  const fullPath=resolve(root,"payload.txt");
  writeFileSync(fullPath,input.message,"utf8");

  const chunks:Array<{index:number;path:string;startChar:number;endChar:number;sha256:string}>=[];
  for(let start=0,index=0;start<input.message.length;start+=chunkSize,index++){
    const text=input.message.slice(start,Math.min(input.message.length,start+chunkSize));
    const path=resolve(root,`chunk-${String(index+1).padStart(4,"0")}.txt`);
    writeFileSync(path,text,"utf8");
    chunks.push({
      index:index+1,
      path:safeRelative(input.workspaceDir,path),
      startChar:start,
      endChar:start+text.length,
      sha256:createHash("sha256").update(text,"utf8").digest("hex"),
    });
  }
  const manifestPath=resolve(root,"manifest.json");
  writeFileSync(manifestPath,`${JSON.stringify({
    schemaVersion:1,
    kind:"cogentnexus-synthetic-payload",
    createdAt:new Date().toISOString(),
    ownerSessionKeyHash:sessionHash,
    totalChars:input.message.length,
    chunkChars:chunkSize,
    sha256,
    fullPath:safeRelative(input.workspaceDir,fullPath),
    chunks,
    rule:"payload.txt is exact authoritative content; chunks are deterministic contiguous slices in index order",
  },null,2)}\n`,`utf8`);

  const manifest=safeRelative(input.workspaceDir,manifestPath);
  const full=safeRelative(input.workspaceDir,fullPath);
  const excerpt=boundedExcerpt(input.message,Math.min(inlineLimit-1500,8_000));
  const message=[
    "[CogentNexus Internal Payload Reference]",
    "The exact internal task payload is larger than the safe inline context budget.",
    "Do NOT treat the excerpt below as the complete instruction.",
    "The exact payload is durably preserved in the workspace and is authoritative.",
    `Manifest: ${manifest}`,
    `Exact payload: ${full}`,
    `SHA-256: ${sha256}`,
    `Chunks: ${chunks.length} contiguous files of at most ${chunkSize} characters each.`,
    "Read manifest.json first. Inspect chunk files incrementally with file/read tools as needed; do not concatenate every chunk into one model turn.",
    "Preserve all constraints from the exact payload. Use CN-002 style incremental execution and commit intermediate findings/artifacts rather than retaining the whole payload in context.",
    "",
    "Bounded orientation excerpt (non-authoritative if it differs from the exact files):",
    excerpt,
  ].join("\n");
  return {message,externalized:true,rootPath:safeRelative(input.workspaceDir,root),manifestPath:manifest,sha256,chunkCount:chunks.length};
}
