# Continuity / Recovery Acceptance (ภาษาไทย)

เอกสารนี้อธิบายสถานะ acceptance ปัจจุบัน ไม่ใช่คำสั่งให้ทำ fault injection กับระบบใช้งานจริงซ้ำโดยไม่มีเหตุผล

## Accepted Recovery Boundary

Baseline ที่ยอมรับคือ v0.9.1 Recovery Core commit `eadb89099637d24f96e265a500d66c577aa939a3` บน OpenClaw `2026.7.1-2`

Test A v16 แบบ live ผ่านเงื่อนไขสำคัญดังนี้:

- prompt เดิมมี Ticket เพียงตัวเดียว;
- Direct request ไม่ถูกโปรโมตไป generic workflow (`workflow_eligible=0`);
- Host timeout authority ถูก commit ก่อน recovery;
- recovery ใช้ provider/model เดิม `ollama/qwen3.5:9b`;
- Direct Recovery มีเพียง attempt 1 และไม่มี retry event;
- transient SQLite BUSY ไม่หลุดออกมาเป็น inference failure;
- ไม่มี recursive recovery Ticket และไม่มี same-session extra Ticket;
- OpenClaw native restart continuation ถูก suppress เฉพาะกรณีที่ CNXCLAW มี durable ownership;
- `response_ready` มีครั้งเดียวและ immutable;
- `direct_result` มีหนึ่ง durable result;
- delivery marker/history ยืนยันหนึ่ง delivery;
- post-recovery session/temp cleanup ผ่าน

## ทำไม Test A v15 ถึงสำคัญ

v15 เปิดเผย race ที่ authority watcher อ่าน SQLite แล้วเจอ `SQLITE_BUSY_RECOVERY` จากนั้น Promise ของ watcher reject และ outer catch ไป schedule retry ทั้งที่ embedded inference เดิมยังวิ่งอยู่

R2 แก้โดยให้ read-only authority connection มี busy timeout และทำให้ transient BUSY เป็นเพียงการอ่านที่ยังสรุป authority ไม่ได้ ไม่ใช่ durable revocation

v16 ยืนยันว่า failure mode ที่เคย escaped ไม่เกิดซ้ำและ recovery จบด้วย inference attempt เดียว

## Native restart ownership

OpenClaw 2026.7.1-2 สามารถสร้าง native restart continuation ได้หลัง Gateway restart จึงมี v099 fence ที่ทำงานก่อน Ticket-first intake และ consume เฉพาะ exact continuation envelope ที่พิสูจน์ได้ว่าเป็นงานเดิมซึ่ง CNXCLAW เป็นเจ้าของ

ordinary user prompt ต้องผ่านตามปกติ และ unreadable DB ต้อง fail open กลับไป native behavior แทนการ suppress แบบเดาสุ่ม

## สิ่งที่ยังไม่ถือว่าผ่าน acceptance

- ไฟดับจริง / cold boot;
- OpenClaw รุ่นใหม่กว่า 2026.7.1-2;
- disk full / database corruption;
- load/concurrency/soak ขนาดสูง;
- exactly-once สำหรับ side effect ภายนอกที่ไม่มี idempotency/receipt

หัวข้อเหล่านี้ถูกเลื่อนการทดสอบ ไม่ได้หมายความว่า recovery core ที่ accepted อยู่ล้มเหลว

## Safe operational checks

ตรวจสถานะทั่วไปได้โดยไม่ fault-inject:

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd ticket list --limit 10
openclaw gateway status
ollama ps
```

อย่ารัน Test A fault injection ซ้ำกับระบบใช้งานจริงเพียงเพื่อเช็กสุขภาพประจำวัน ให้ใช้ deterministic status/health checks แทน
