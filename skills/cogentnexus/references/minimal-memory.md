# Minimal Memory

Use when information must survive session boundaries.

Store only:

- durable user preferences
- architecture and project decisions
- verified environment facts
- reusable lessons
- resumable task state

Do not store secrets unless explicitly requested. Do not copy full conversations or private reasoning.

Route information:

- raw same-day events and full structured lesson records -> `memory/YYYY-MM-DD.md`
- distilled long-term knowledge and durable lesson rules -> `MEMORY.md`
- active resumable work -> `memory/interrupted-tasks.json`
- machine-specific notes -> `TOOLS.md` or `ENVIRONMENT.md`

For reusable experience, follow [lesson-learning.md](lesson-learning.md). Daily memory holds the evidence-backed record; long-term memory holds the shortest rule that will change future behavior.

Before writing, read and merge. Deduplicate equivalent lessons, remove obsolete facts during curation, and verify the saved content.
