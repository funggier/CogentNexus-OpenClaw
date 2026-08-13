import { randomUUID } from "node:crypto";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";

export type ExperienceKind = "attempt" | "failure" | "correction" | "validator_outcome";
export type LessonStatus = "hypothesis" | "verified" | "contradicted" | "retired";
export type ApplicationOutcome = "success" | "failure" | "neutral";

export type LessonRecord = {
  lessonId: string;
  status: LessonStatus;
  summary: string;
  guidance: string;
  confidence: number;
  provenance: Array<{ evidenceRef: string; relation: string }>;
  createdAt: string;
  updatedAt: string;
};

const KNOWLEDGE_SCHEMA = `
CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY,
  applied_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS experiences (
  experience_id TEXT PRIMARY KEY,
  ticket_id TEXT,
  kind TEXT NOT NULL CHECK (kind IN ('attempt','failure','correction','validator_outcome')),
  summary TEXT NOT NULL,
  evidence_ref TEXT NOT NULL,
  outcome_json TEXT,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_experiences_ticket_created ON experiences(ticket_id,created_at);
CREATE TABLE IF NOT EXISTS lessons (
  lesson_id TEXT PRIMARY KEY,
  status TEXT NOT NULL CHECK (status IN ('hypothesis','verified','contradicted','retired')),
  summary TEXT NOT NULL,
  guidance TEXT NOT NULL,
  confidence REAL NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS lesson_evidence (
  lesson_id TEXT NOT NULL REFERENCES lessons(lesson_id) ON DELETE CASCADE,
  evidence_ref TEXT NOT NULL,
  relation TEXT NOT NULL CHECK (relation IN ('supports','contradicts','retires')),
  created_at TEXT NOT NULL,
  PRIMARY KEY (lesson_id,evidence_ref,relation)
);
CREATE TABLE IF NOT EXISTS lesson_applications (
  application_id TEXT PRIMARY KEY,
  lesson_id TEXT NOT NULL REFERENCES lessons(lesson_id) ON DELETE CASCADE,
  ticket_id TEXT,
  outcome TEXT NOT NULL CHECK (outcome IN ('success','failure','neutral')),
  evidence_ref TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_lesson_applications_lesson ON lesson_applications(lesson_id,created_at);
CREATE VIRTUAL TABLE IF NOT EXISTS lessons_fts USING fts5(lesson_id UNINDEXED,summary,guidance,tokenize='unicode61');
`;

function boundedText(value: string, name: string, maximum = 4000) {
  const clean = value.trim();
  if (!clean) throw new Error(`${name} is required`);
  return clean.slice(0, maximum);
}

function confidence(value: number) {
  if (!Number.isFinite(value) || value < 0 || value > 1) throw new Error("confidence must be between 0 and 1");
  return value;
}

function ftsQuery(value: string) {
  const tokens = value.normalize("NFKC").match(/[\p{L}\p{N}_-]+/gu) ?? [];
  return tokens.slice(0, 20).map((token) => `"${token.replaceAll('"', '""')}"`).join(" OR ");
}

export class KnowledgeStore {
  readonly databasePath: string;

  constructor(databasePath: string) { this.databasePath = resolve(databasePath); }

  private open() {
    mkdirSync(dirname(this.databasePath), { recursive: true });
    const db = new DatabaseSync(this.databasePath);
    try {
      db.exec("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;");
      db.exec(KNOWLEDGE_SCHEMA);
      const applied = new Date().toISOString();
      for (const version of [5,6]) db.prepare("INSERT OR IGNORE INTO schema_migrations(version,applied_at) VALUES (?,?)").run(version,applied);
      return db;
    } catch (error) { db.close(); throw error; }
  }

  recordExperience(input: { ticketId?: string; kind: ExperienceKind; summary: string; evidenceRef: string; outcome?: unknown; now?: Date }) {
    const db = this.open(), experienceId = `CNXE-${randomUUID()}`, createdAt = (input.now ?? new Date()).toISOString();
    try {
      db.prepare("INSERT INTO experiences(experience_id,ticket_id,kind,summary,evidence_ref,outcome_json,created_at) VALUES (?,?,?,?,?,?,?)")
        .run(experienceId,input.ticketId ?? null,input.kind,boundedText(input.summary,"summary"),boundedText(input.evidenceRef,"evidenceRef",1000),input.outcome === undefined ? null : JSON.stringify(input.outcome),createdAt);
      return {experienceId,createdAt};
    } finally { db.close(); }
  }

  createCandidate(input: { summary: string; guidance: string; evidenceRef: string; confidence?: number; now?: Date }): LessonRecord {
    const db = this.open(), lessonId = `CNXL-${randomUUID()}`, now = (input.now ?? new Date()).toISOString();
    const summary = boundedText(input.summary,"summary"), guidance = boundedText(input.guidance,"guidance"), score = confidence(input.confidence ?? 0.5), evidenceRef = boundedText(input.evidenceRef,"evidenceRef",1000);
    try {
      db.exec("BEGIN IMMEDIATE");
      db.prepare("INSERT INTO lessons(lesson_id,status,summary,guidance,confidence,created_at,updated_at) VALUES (?,'hypothesis',?,?,?,?,?)").run(lessonId,summary,guidance,score,now,now);
      db.prepare("INSERT INTO lesson_evidence(lesson_id,evidence_ref,relation,created_at) VALUES (?,?,'supports',?)").run(lessonId,evidenceRef,now);
      db.prepare("INSERT INTO lessons_fts(lesson_id,summary,guidance) VALUES (?,?,?)").run(lessonId,summary,guidance);
      db.exec("COMMIT");
      return this.row(db,lessonId)!;
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  transition(input: { lessonId: string; action: "verify" | "contradict" | "retire"; evidenceRef: string; confidence?: number; now?: Date }): LessonRecord {
    const db = this.open(), now = (input.now ?? new Date()).toISOString();
    const target:LessonStatus = input.action === "verify" ? "verified" : input.action === "contradict" ? "contradicted" : "retired";
    const relation = input.action === "verify" ? "supports" : input.action === "contradict" ? "contradicts" : "retires";
    try {
      db.exec("BEGIN IMMEDIATE");
      const current = db.prepare("SELECT status,confidence FROM lessons WHERE lesson_id=?").get(input.lessonId) as any;
      if (!current) throw new Error("lesson not found");
      if (current.status === "retired") throw new Error("retired lesson is terminal");
      const evidenceRef = boundedText(input.evidenceRef,"evidenceRef",1000);
      const repeated = db.prepare("SELECT 1 present FROM lesson_evidence WHERE lesson_id=? AND evidence_ref=?").get(input.lessonId,evidenceRef) as any;
      if (repeated) throw new Error("lesson transition requires new independent evidence");
      const score = confidence(input.confidence ?? (target === "verified" ? Math.max(Number(current.confidence),0.75) : target === "contradicted" ? Math.min(Number(current.confidence),0.25) : 0));
      db.prepare("UPDATE lessons SET status=?,confidence=?,updated_at=? WHERE lesson_id=?").run(target,score,now,input.lessonId);
      db.prepare("INSERT INTO lesson_evidence(lesson_id,evidence_ref,relation,created_at) VALUES (?,?,?,?)").run(input.lessonId,evidenceRef,relation,now);
      db.exec("COMMIT");
      return this.row(db,input.lessonId)!;
    } catch(error) { try { db.exec("ROLLBACK"); } catch {} throw error; } finally { db.close(); }
  }

  search(query: string, input: { limit?: number; includeUnverified?: boolean } = {}): LessonRecord[] {
    const db = this.open(), match = ftsQuery(boundedText(query,"query",500)), limit = Math.max(1,Math.min(Math.trunc(input.limit ?? 10),50));
    try {
      if (!match) return [];
      const status = input.includeUnverified ? "" : "AND l.status='verified'";
      const rows = db.prepare(`SELECT l.lesson_id FROM lessons_fts f JOIN lessons l ON l.lesson_id=f.lesson_id WHERE lessons_fts MATCH ? ${status} ORDER BY bm25(lessons_fts),l.confidence DESC LIMIT ?`).all(match,limit) as any[];
      return rows.map((item) => this.row(db,item.lesson_id)!).filter(Boolean);
    } finally { db.close(); }
  }

  recordApplication(input: { lessonId: string; ticketId?: string; outcome: ApplicationOutcome; evidenceRef: string; now?: Date }) {
    const db = this.open(), applicationId = `CNXA-${randomUUID()}`, createdAt = (input.now ?? new Date()).toISOString();
    try {
      const lesson = db.prepare("SELECT status FROM lessons WHERE lesson_id=?").get(input.lessonId) as any;
      if (!lesson || lesson.status !== "verified") throw new Error("only verified lessons may be applied");
      db.prepare("INSERT INTO lesson_applications(application_id,lesson_id,ticket_id,outcome,evidence_ref,created_at) VALUES (?,?,?,?,?,?)")
        .run(applicationId,input.lessonId,input.ticketId ?? null,input.outcome,boundedText(input.evidenceRef,"evidenceRef",1000),createdAt);
      return {applicationId,createdAt};
    } finally { db.close(); }
  }

  snapshot() {
    const db = this.open();
    try {
      const lessons = db.prepare("SELECT status,count(*) count FROM lessons GROUP BY status").all() as any[];
      const experiences = db.prepare("SELECT kind,count(*) count FROM experiences GROUP BY kind").all() as any[];
      const applications = db.prepare("SELECT outcome,count(*) count FROM lesson_applications GROUP BY outcome").all() as any[];
      return {lessons:Object.fromEntries(lessons.map(x=>[x.status,Number(x.count)])),experiences:Object.fromEntries(experiences.map(x=>[x.kind,Number(x.count)])),applications:Object.fromEntries(applications.map(x=>[x.outcome,Number(x.count)]))};
    } finally { db.close(); }
  }

  private row(db: DatabaseSync, lessonId: string): LessonRecord | undefined {
    const item = db.prepare("SELECT lesson_id,status,summary,guidance,confidence,created_at,updated_at FROM lessons WHERE lesson_id=?").get(lessonId) as any;
    if (!item) return undefined;
    const evidence = db.prepare("SELECT evidence_ref,relation FROM lesson_evidence WHERE lesson_id=? ORDER BY created_at,evidence_ref").all(lessonId) as any[];
    return {lessonId:item.lesson_id,status:item.status,summary:item.summary,guidance:item.guidance,confidence:Number(item.confidence),provenance:evidence.map(x=>({evidenceRef:x.evidence_ref,relation:x.relation})),createdAt:item.created_at,updatedAt:item.updated_at};
  }
}
