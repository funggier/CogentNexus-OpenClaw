# คู่มือทดสอบ Continuity ของ CogentNexus v0.8 — แบบจับมือทำ

เอกสารนี้ใช้ **หลังติดตั้ง CogentNexus Core v0.8.0 สำเร็จแล้ว** เพื่อพิสูจน์บนเครื่องจริงว่า CogentNexus ไม่เพียง “ทำงานต่อหลัง process ดับ” แต่ยังครอบคลุม failure mode ที่เกิดตรงรอยต่อระหว่าง inference, การแสดงคำตอบ และ history compaction ด้วย

ทดสอบตามลำดับจากเบาไปหนัก อย่าข้ามไปดึงปลั๊กไฟก่อน test ระดับ process/Gateway ผ่านครบ

---

## 1. เตรียม PowerShell สำหรับสังเกตสถานะ

เปิด PowerShell หนึ่งหน้าต่างแล้วเข้า workspace:

```powershell
Set-Location "$HOME\.openclaw\workspace"
```

ตรวจ Host:

```powershell
.\cnx.cmd status
```

ควรเห็น:

```text
mode = managed
desiredGateway = running
```

ตรวจ Gateway:

```powershell
openclaw gateway status
```

จากนั้นเปิดหน้าต่าง PowerShell อีกหนึ่งหน้าต่างไว้สำหรับดู Ticket:

```powershell
Set-Location "$HOME\.openclaw\workspace"
.\cnx.cmd ticket list
```

---

# Test A — Greeting ปกติ

ส่ง:

```text
สวัสดีครับ
```

สิ่งที่ต้องการ:

1. มี Ticket ถูก accept ก่อน inference
2. request อยู่ DIRECT
3. ได้คำตอบธรรมดา
4. หลังการส่ง final reply สำเร็จ Ticket จึงเป็น completed

ตรวจ:

```powershell
.\cnx.cmd ticket list
```

จุดสำคัญคือ DIRECT ยังเบา ไม่ถูกบังคับเข้า STAGED workflow

---

# Test B — คำตอบยาวต้องไม่ completed ก่อนส่งครบ

นี่คือ test สำหรับกรณี **OpenClaw เริ่มแสดงข้อความแล้ว แต่ interrupted ก่อนแสดงครบ**

## B1. ส่งคำขอที่ต้องตอบยาว

ตัวอย่าง:

```text
ช่วยอธิบายสถาปัตยกรรมระบบปฏิบัติการอย่างละเอียดประมาณ 30 ย่อหน้า โดยแบ่งหัวข้อชัดเจน
```

ระหว่างกำลังตอบ ให้สังเกต Ticket:

```powershell
.\cnx.cmd ticket list
```

ในช่วงที่ model ทำเสร็จแล้วแต่ final delivery ยังไม่ยืนยัน ระบบอาจอยู่ในสถานะ non-terminal โดยมี durable `response_ready_at`

**กติกา:**

```text
agent/model เสร็จ
    !=
ผู้ใช้ได้รับคำตอบครบ
```

CogentNexus ต้องไม่ถือว่า completed เพียงเพราะ `agent_end` สำเร็จ

---

# Test C — จำลอง partial reply interruption

ใช้เฉพาะหลัง Test A/B ผ่านแล้ว

## C1. เริ่มคำตอบยาว

ส่งข้อความแบบ Test B แล้วรอจนเห็นคำตอบเริ่มปรากฏ

## C2. ขัดจังหวะ Gateway ระหว่างคำตอบกำลังแสดง

ใน PowerShell:

```powershell
.\cnx.cmd gateway stop
```

อย่าเพิ่งส่งคำขอเดิมซ้ำ

ตรวจ Ticket:

```powershell
.\cnx.cmd ticket list
```

สิ่งที่ **ไม่ควร** เกิด:

```text
คำตอบแสดงไม่ครบ
แต่ Ticket ถูกนับ completed และหายไปจาก recovery
```

สิ่งที่ต้องการคือ delivery ที่ fail หรือไม่ได้รับ receipt ภายใน deadline จะทำให้งานกลับไปอยู่ใน durable recovery path

## C3. เปิด Gateway กลับ

```powershell
.\cnx.cmd gateway start
```

ตรวจ:

```powershell
.\cnx.cmd status
.\cnx.cmd ticket list
```

ระบบควรทำต่อจาก durable state โดยไม่ต้องให้คุณพิมพ์ request เดิมซ้ำ

สำหรับ DIRECT ที่ยังไม่มี durable terminal result ระบบอาจต้องทำ computation ใหม่อย่างปลอดภัย แต่ต้องไม่ทำให้ผู้ใช้ต้องส่งคำขอเดิมซ้ำ ส่วน ACTION/STAGED ที่มี committed result หรือ side effect แล้วต้องใช้ durable evidence เพื่อหลีกเลี่ยงการทำ side effect ซ้ำ

---

# Test D — Terminal outbox ต้องไม่ถือว่า delivered แค่เพราะ schedule สำเร็จ

สำหรับงาน STAGED ให้สร้างงานที่มีผลลัพธ์ terminal เช่น artifact ที่ตรวจสอบเสร็จแล้ว

สิ่งที่ต้องการภายในคือ:

```text
workflow completed
 -> completion outbox = pending
 -> schedule owner continuation
 -> marked delivery turn ทำงาน
 -> final delivery settle
 -> outbox = delivered
```

ไม่ใช่:

```text
schedule สำเร็จ
 -> delivered ทันที   # ผิด
```

ถ้า Gateway ดับหลัง schedule แต่ก่อน owner ได้รับคำตอบ outbox ต้องยัง retry ได้

---

# Test E — Successful history compaction ต้องไม่ทำให้งาน DIRECT เงียบ

นี่คือ test สำหรับกรณี **compacted history เสร็จแล้ว แต่ OpenClaw ไม่ทำงาน DIRECT ที่ค้างต่อ**

## E1. ใช้งาน session ที่ context มีข้อมูลพอสมควร

เลือกงานต่อเนื่องที่ใช้ context มาก แต่ยังเป็นงานที่สามารถทำเป็น DIRECT conversational execution ได้ เช่นการอธิบาย/วิเคราะห์ยาว ๆ โดยยังไม่ต้องสร้าง workflow แบบ STAGED

ตัวอย่าง:

```text
ช่วยวิเคราะห์สถาปัตยกรรมนี้ต่อเนื่องหลายส่วน เชื่อมเหตุผลแต่ละส่วน และทำต่อจนจบโดยไม่ให้ผมต้องสั่งต่อทีละช่วง
```

เป้าหมายคือให้เกิด compaction ตามธรรมชาติของ OpenClaw

## E2. เมื่อเห็นว่า history compaction สำเร็จ

**อย่าส่งข้อความ “ทำต่อ” เองทันที**

CogentNexus จะตรวจ durable Ticket ของ session หลัง `after_compaction`

Guard จะถูกสร้างเฉพาะเมื่อยังมี DIRECT Ticket ที่มีลักษณะ:

```text
status = accepted
workflow_eligible = 0
response_ready_at = null
```

หมายความว่า execution เดิมยังไม่ถึงจุดที่คำตอบพร้อมส่งจริง

ถ้า Ticket อยู่ `RESPONSE_READY` แล้ว จะไม่ใช้ compaction guard เพราะกรณีนั้นเป็นหน้าที่ของ Delivery Commit Gate

ถ้าเป็น workflow STAGED ที่กำลังทำ หรือ terminal outbox ที่กำลังรอส่ง ก็ไม่จำเป็นต้องสร้าง compaction guard ใหม่ เพราะมี deterministic service ของตัวเองอยู่แล้ว

เมื่อเข้าเงื่อนไข ระบบจะ schedule guard แบบ idempotent:

```text
[CogentNexus Continuation: post-compaction]
```

## E3. พฤติกรรมที่ถูกต้อง

มีสองกรณี:

### กรณี 1 — OpenClaw เดิมทำต่อเองตามปกติ

CogentNexus ต้อง cancel delayed guard ก่อนมันยิง เพื่อไม่ให้เกิดงานซ้ำ

### กรณี 2 — หลัง compaction OpenClaw เงียบจริง

เมื่อ delayed guard ยิง ระบบจะ **promote Ticket เดิมแบบ deterministic ก่อน inference**:

```text
accepted / workflow_eligible=0
        ->
waiting / workflow_eligible=1
```

พร้อมบันทึก interruption evidence แล้วให้ durable dispatcher ทำงานต่อจาก **original committed request**

ระบบไม่ควรฝากให้โมเดลเดาว่า compacted history เดิมหมายถึงอะไร และผู้ใช้ไม่ควรต้องพิมพ์:

```text
ทำต่อครับ
```

เพื่อปลุกงานที่ระบบยอมรับไปแล้ว

---

# Test F — Guard ต้องไม่สร้างงานซ้ำหลัง state เปลี่ยนแล้ว

กรณีนี้ทดสอบ idempotency ของ delayed guard

สิ่งที่ต้องการ:

```text
original run เดินต่อเอง
 -> agent_end ยกเลิก guard
```

หรือ:

```text
guard มาถึงช้า
 -> ไม่พบ DIRECT Ticket ที่ยัง eligible
 -> ไม่ promote ซ้ำ
 -> ไม่สร้าง workflow ใหม่ซ้ำ
 -> ไม่ทำ external side effect ซ้ำ
```

Ticket ที่ `RESPONSE_READY` แล้วต้องอยู่ฝั่ง delivery recovery ไม่ถูก compaction guard promote ไปคำนวณใหม่เพียงเพราะ history ถูก compact

---

# Test G — Restart ระหว่าง RESPONSE_READY

กรณีนี้ทดสอบรอยต่อที่สำคัญมาก:

1. ให้ model สร้างคำตอบยาว
2. คำตอบพร้อมแล้วแต่ยังส่งไม่ครบ
3. restart Gateway

```powershell
.\cnx.cmd gateway restart
```

หลังกลับมา:

```powershell
.\cnx.cmd ticket list
```

Ticket ที่ยังไม่มี `delivery_confirmed_at` ต้องไม่ถูกนับ completed แบบเงียบ ๆ

ถ้าพ้น delivery receipt deadline จะถูกนำกลับเข้า durable recovery path

---

# Test H — Windows reboot

เมื่อ Test A-G ผ่านแล้ว:

1. ให้มีงาน non-terminal ที่ recover ได้
2. restart Windows แบบปกติ
3. login กลับมา
4. เปิด PowerShell

```powershell
Set-Location "$HOME\.openclaw\workspace"
.\cnx.cmd status
.\cnx.cmd ticket list
```

Host ต้องอ่าน desired state และ durable Ticket/workflow/outbox state เดิมกลับมา

งานที่ยังไม่ terminal ต้องมีเส้นทาง resume หรือ delivery retry ที่ชัดเจน

---

# Test I — PASSTHROUGH ต้องไม่ถูก continuity guard แทรกแซง

```powershell
.\cnx.cmd disable
```

ตรวจ:

```powershell
.\cnx.cmd status
```

ควรเป็น:

```text
mode = passthrough
```

ตอนนี้ CogentNexus plugin/background ownership ถูกปิด ดังนั้น Delivery Commit Gate และ Post-Compaction Continuation Guard ของ CogentNexus จะไม่ intercept turn ใหม่

OpenClaw ต้องใช้งานแบบ native ได้

เปิดกลับ:

```powershell
.\cnx.cmd enable
```

---

# สิ่งที่ควรบันทึกเมื่อพบปัญหา

ถ้า test ใดไม่ผ่าน ก่อนส่ง request ซ้ำ ให้บันทึกอย่างน้อย:

```powershell
.\cnx.cmd status
.\cnx.cmd ticket list
openclaw gateway status
```

และจดเวลาประมาณที่ failure เกิด เพื่อเทียบกับ Gateway/OpenClaw log

ข้อมูลสำคัญสำหรับวิเคราะห์คือ:

- Ticket ID
- session key
- Ticket status
- workflow ID ถ้ามี
- `workflow_eligible`
- failure class/message
- `response_ready_at` มีหรือไม่
- `delivery_confirmed_at` มีหรือไม่
- Gateway healthy หรือไม่
- failure เกิดก่อน/ระหว่าง/หลัง compaction

**อย่าส่ง request เดิมซ้ำทันที** ถ้า Ticket เดิมยัง non-terminal เพราะอาจสร้าง duplicate work ที่ไม่จำเป็น

---

# Checklist Continuity v0.8

```text
[ ] Greeting DIRECT ตอบปกติ
[ ] Visible reply ไม่ completed ที่ agent_end เพียงอย่างเดียว
[ ] Full delivery receipt แล้วจึง completed
[ ] Delivery receipt มาก่อน/หลัง RESPONSE_READY ก็ให้ผลเดียวกัน
[ ] Partial reply interruption ไม่ถูกนับว่าจบ
[ ] Missing receipt ถูกนำกลับเข้า durable recovery
[ ] Terminal outbox schedule ยังเป็น pending
[ ] Delivery continuation สำเร็จแล้วจึง delivered
[ ] Failed delivery กลับมา retry ได้
[ ] Successful compaction + unfinished DIRECT มี continuation guard
[ ] RESPONSE_READY ไม่ถูก compaction guard promote
[ ] Original run เดินต่อเองแล้ว guard ถูกยกเลิก
[ ] Guard ยิงแล้ว promote Ticket เดิมก่อน inference
[ ] Late guard ไม่สร้าง duplicate workflow/side effect
[ ] Gateway restart ระหว่าง delivery recover ได้
[ ] Windows reboot recover durable state ได้
[ ] PASSTHROUGH ไม่ถูก CogentNexus continuity guard แทรกแซง
```

เมื่อ checklist นี้ผ่าน จึงค่อยถือว่าการติดตั้งผ่านทั้ง **execution continuity**, **delivery continuity**, และ **context/compaction continuity** บนเครื่องจริง
