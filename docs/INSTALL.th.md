# คู่มือติดตั้ง CogentNexus แบบจับมือทำ — Windows + OpenClaw + Ollama

คู่มือนี้ออกแบบสำหรับผู้ใช้ Windows ที่ต้องการติดตั้ง CogentNexus แบบ **ติดตั้งแล้วใช้งานได้ทันที** โดยให้ CogentNexus ทำหน้าที่เป็น Host Controller ภายนอก OpenClaw และยังสามารถสั่ง `disable` เพื่อคืน OpenClaw ให้ทำงานแบบปกติได้ทุกเมื่อ

> Baseline ของคู่มือนี้: CogentNexus v0.8.0, OpenClaw 2026.7.1-2 หรือใหม่กว่า, Python 3.10+, Node.js 22+

---

## สิ่งที่จะได้หลังติดตั้ง

เมื่อทำครบแล้ว ระบบจะมีเส้นทางประมาณนี้:

```text
ข้อความของคุณ
   -> Ticket ถูกบันทึกก่อน inference
   -> OpenClaw / LLM ทำงาน
   -> ถ้าค้าง/ดับ CogentNexus Host ตรวจและกู้ได้
   -> ได้ผลลัพธ์หรือจบด้วยสถานะที่ชัดเจน
```

และจะมีคำสั่งหลักใน OpenClaw workspace:

```powershell
.\cnx.cmd status
.\cnx.cmd start
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd disable
.\cnx.cmd enable
```

ความหมายสำคัญ:

- `start` = ให้ CogentNexus กลับมาควบคุมและให้ runtime ทำงาน
- `stop` = หยุดแบบตั้งใจ (MAINTENANCE) ระบบจะไม่พยายามเปิดเอง
- `restart` = restart แล้วกลับมาทำงานต่อ
- `disable` = ปิด CogentNexus และคืน OpenClaw เป็นโหมดปกติ
- `enable` = เปิด CogentNexus MANAGED mode กลับมา

---

# ส่วนที่ 1 — ตรวจเครื่องก่อนติดตั้ง

เปิด **PowerShell** ปกติหนึ่งหน้าต่าง

> ไม่จำเป็นต้อง Run as Administrator สำหรับการติดตั้งแบบ user-level ปกติ

## 1.1 ตรวจ Python

พิมพ์:

```powershell
python --version
```

ควรเห็นประมาณ:

```text
Python 3.11.x
```

หรือ Python 3.10 ขึ้นไป

ถ้าขึ้นว่า `python is not recognized` ให้ติดตั้ง Python ก่อน และเลือก **Add Python to PATH** ตอนติดตั้ง

ตรวจ path เพิ่มเติมได้ด้วย:

```powershell
where.exe python
```

---

## 1.2 ตรวจ Node.js

```powershell
node --version
npm --version
```

ควรใช้ Node.js 22 หรือใหม่กว่า

ตัวอย่าง:

```text
v24.x.x
10.x.x
```

ถ้าไม่มี `node` หรือ `npm` ให้ติดตั้ง Node.js ก่อน

---

## 1.3 ตรวจ OpenClaw

```powershell
openclaw --version
```

สำหรับ baseline นี้ควรเป็น:

```text
2026.7.1-2
```

หรือใหม่กว่า

จากนั้น:

```powershell
openclaw gateway status
```

ถ้า Gateway ทำงานอยู่ ควรเห็นว่า service/task ถูกติดตั้งและ Gateway reachable

ถ้า Gateway ยังไม่ทำงาน **ไม่เป็นปัญหา** เพราะ CogentNexus สามารถ start ให้ตอนติดตั้งได้

---

## 1.4 ตรวจ Ollama

ถ้าคุณใช้ local model ผ่าน Ollama:

```powershell
ollama --version
ollama list
```

ควรเห็น Ollama และรายชื่อ model ที่มีอยู่

ตัวอย่าง:

```text
gpt-oss:20b
```

ถ้าใช้ cloud provider แทน Ollama สามารถข้ามส่วน Ollama ได้ แต่ต้องตั้ง OpenClaw provider ให้ใช้งานได้ก่อน

---

## 1.5 ตรวจว่า OpenClaw ใช้ model ได้จริง

ก่อนเพิ่ม CogentNexus แนะนำให้ตรวจว่า OpenClaw/Ollama เดิมใช้งานได้ก่อน

ถ้า Gateway เปิดอยู่:

```powershell
openclaw gateway status
```

ถ้ามีคำสั่ง inference diagnostic ใน OpenClaw เวอร์ชันของคุณ สามารถทดสอบ direct model path เพิ่มเติมได้

จุดสำคัญคือ **อย่าเริ่มแก้ CogentNexus หาก Ollama/OpenClaw เดิมยังใช้ model ไม่ได้** เพราะจะทำให้แยกสาเหตุยาก

---

# ส่วนที่ 2 — เตรียม Python dependency

CogentNexus ใช้ PyYAML สำหรับ validation

ติดตั้งด้วย:

```powershell
python -m pip install "PyYAML>=6.0,<7"
```

ทดสอบ:

```powershell
python -c "import yaml; print(yaml.__version__)"
```

ถ้าแสดงเลข version แปลว่าพร้อม

---

# ส่วนที่ 3 — ดาวน์โหลด CogentNexus Release

แนะนำให้ใช้ Release แทนการ clone `main` เพื่อให้ไฟล์ทุกอย่างเป็นชุดเดียวกัน

ตัวอย่างด้านล่างใช้ v0.8.0

## 3.1 สร้างโฟลเดอร์ดาวน์โหลด

```powershell
New-Item -ItemType Directory -Force "$HOME\Downloads\CogentNexus" | Out-Null
Set-Location "$HOME\Downloads\CogentNexus"
```

## 3.2 ดาวน์โหลด ZIP และ checksum

```powershell
$version = "v0.8.0"
$base = "https://github.com/funggier/cogentnexus/releases/download/$version"
Invoke-WebRequest "$base/cogentnexus-$version.zip" -OutFile "cogentnexus-$version.zip"
Invoke-WebRequest "$base/SHA256SUMS.txt" -OutFile "SHA256SUMS.txt"
```

ตรวจว่ามีไฟล์:

```powershell
Get-ChildItem
```

ควรเห็นอย่างน้อย:

```text
cogentnexus-v0.8.0.zip
SHA256SUMS.txt
```

---

# ส่วนที่ 4 — ตรวจ SHA256 ก่อนติดตั้ง

คำนวณ hash ของ ZIP:

```powershell
$actual = (Get-FileHash ".\cogentnexus-v0.8.0.zip" -Algorithm SHA256).Hash.ToLower()
$expected = ((Get-Content ".\SHA256SUMS.txt" | Select-String "cogentnexus-v0.8.0.zip") -split "\s+")[0].ToLower()
$actual
$expected
```

สองค่าต้องเหมือนกัน

ให้ตรวจอัตโนมัติ:

```powershell
if ($actual -ne $expected) {
    throw "SHA256 mismatch - ห้ามติดตั้งไฟล์นี้"
}
Write-Host "SHA256 OK"
```

ต้องเห็น:

```text
SHA256 OK
```

ถ้าไม่ตรง **หยุดทันที** และดาวน์โหลดใหม่

---

# ส่วนที่ 5 — แตก ZIP

```powershell
Expand-Archive ".\cogentnexus-v0.8.0.zip" -DestinationPath ".\cogentnexus-v0.8.0" -Force
Set-Location ".\cogentnexus-v0.8.0\cogentnexus-v0.8.0"
```

ตรวจ:

```powershell
Get-ChildItem
```

ควรเห็นประมาณ:

```text
skills
plugins
scripts
docs
README.md
```

ถ้า ZIP ถูกแตกออกมาโดยไม่มีโฟลเดอร์ซ้อน ให้ `Set-Location` เข้าโฟลเดอร์ที่มี `scripts\install.ps1` จริง

ตรวจได้ด้วย:

```powershell
Test-Path ".\scripts\install.ps1"
```

ต้องได้:

```text
True
```

---

# ส่วนที่ 6 — ติดตั้ง CogentNexus

## 6.1 ถ้า PowerShell บล็อก script

ใช้เฉพาะ process นี้:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

ไม่จำเป็นต้องเปลี่ยน execution policy ทั้งเครื่อง

## 6.2 รัน installer

```powershell
.\scripts\install.ps1
```

Installer จะทำตามลำดับนี้:

1. ตรวจ `python`, `openclaw`, `npm`
2. ตรวจ PyYAML
3. backup CogentNexus เดิมถ้ามี
4. copy skill เข้า OpenClaw workspace
5. validate skill
6. update เฉพาะ CogentNexus managed block ใน `AGENTS.md`
7. `npm ci`
8. build/validate OpenClaw plugin
9. ติดตั้ง plugin
10. สร้าง `cnx.cmd`
11. initialize Host Controller state
12. enable MANAGED mode
13. เปิด Ticket-first settings
14. เปิด hidden Host supervisor
15. start/reconcile Gateway/provider
16. ตรวจ Gateway และ supervisor health

ระหว่างติดตั้งอาจใช้เวลาตรง `npm ci` และ plugin validation

เมื่อสำเร็จควรเห็นท้าย ๆ ประมาณ:

```text
CogentNexus installation completed successfully.
```

ถ้า installer จบด้วย error อย่ารันซ้ำแบบสุ่ม ให้ดูหัวข้อ Troubleshooting ด้านล่าง

---

# ส่วนที่ 7 — เข้า OpenClaw workspace

ค่า default คือ:

```powershell
Set-Location "$HOME\.openclaw\workspace"
```

ตรวจ launcher:

```powershell
Test-Path ".\cnx.cmd"
```

ต้องได้:

```text
True
```

---

# ส่วนที่ 8 — ตรวจสถานะ CogentNexus หลังติดตั้ง

```powershell
.\cnx.cmd status
```

ผลลัพธ์เป็น JSON

สิ่งที่ควรตรวจ:

```text
mode = managed
desiredGateway = running
```

และ Gateway ควร healthy

ถ้า Ticket database ยังว่างถือว่าปกติ เพราะยังไม่ได้ส่งข้อความ

ตรวจ OpenClaw อีกครั้ง:

```powershell
openclaw gateway status
```

---

# ส่วนที่ 9 — ทดสอบข้อความแรก

เปิดช่องทางที่คุณใช้คุยกับ OpenClaw แล้วส่ง:

```text
สวัสดีครับ
```

สิ่งที่ต้องการคือ:

```text
message
 -> Ticket commit
 -> DIRECT
 -> LLM ตอบธรรมดา
 -> delivered/completed
```

หลังจากส่งแล้ว กลับมาที่ PowerShell:

```powershell
.\cnx.cmd ticket list
```

คุณควรเห็น Ticket ล่าสุดและสถานะของมัน

เป้าหมายของการทดสอบนี้คือพิสูจน์ว่า **แม้ข้อความง่ายก็ถูก durable ก่อน แต่ไม่ได้ถูกบังคับเข้า STAGED workflow**

---

# ส่วนที่ 10 — ทดสอบ stop / start

## 10.1 หยุดแบบตั้งใจ

```powershell
.\cnx.cmd stop
```

จากนั้น:

```powershell
.\cnx.cmd status
```

ควรเห็น:

```text
mode = maintenance
desiredGateway = stopped
```

CogentNexus supervisor จะไม่พยายามเปิด Gateway กลับเอง เพราะรู้ว่าคุณเป็นคนสั่งหยุด

## 10.2 เปิดกลับ

```powershell
.\cnx.cmd start
```

แล้ว:

```powershell
.\cnx.cmd status
```

ควรกลับเป็น:

```text
mode = managed
desiredGateway = running
```

หากมีงานที่ถูก commit ไว้และยัง eligible ระบบสามารถทำต่อจาก durable state ได้

---

# ส่วนที่ 11 — ทดสอบ restart

```powershell
.\cnx.cmd restart
```

จากนั้น:

```powershell
.\cnx.cmd status
```

เป้าหมายคือ Gateway restart แต่ MANAGED intent ยังคงอยู่ และ supervisor สามารถ resume งานที่ยังไม่จบได้

---

# ส่วนที่ 12 — ทดสอบเฉพาะ Gateway

หยุดเฉพาะ Gateway โดยยังใช้ CogentNexus Host semantics:

```powershell
.\cnx.cmd gateway stop
```

เปิดกลับ:

```powershell
.\cnx.cmd gateway start
```

restart:

```powershell
.\cnx.cmd gateway restart
```

ใน MANAGED mode คำสั่งพวกนี้ผ่าน Host Controller

---

# ส่วนที่ 13 — ทดสอบ PASSTHROUGH: ปิด CogentNexus แต่ใช้ OpenClaw ต่อ

นี่คือ test สำคัญมาก

```powershell
.\cnx.cmd disable
```

จากนั้น:

```powershell
.\cnx.cmd status
```

ควรเห็น:

```text
mode = passthrough
```

CogentNexus จะ:

- ปิด background ownership ของตัวเอง
- เอา CogentNexus managed block ออกจาก `AGENTS.md`
- disable CogentNexus plugin
- restart/start OpenClaw แบบ native
- **ไม่ลบ durable state เดิม**

ตอนนี้ลองคุย OpenClaw อีกครั้ง

ควรทำงานเหมือน OpenClaw ปกติที่ไม่มี CogentNexus คั่น

เปิด CogentNexus กลับ:

```powershell
.\cnx.cmd enable
```

แล้วตรวจ:

```powershell
.\cnx.cmd status
```

ควรกลับเป็น MANAGED

---

# ส่วนที่ 14 — ทดสอบการ cancel Ticket

ดูรายการ:

```powershell
.\cnx.cmd ticket list
```

ถ้ามี Ticket ที่ไม่ต้องการแล้ว:

```powershell
.\cnx.cmd ticket cancel <ticket-id> --reason "ยกเลิกโดยผู้ใช้"
```

เช่น:

```powershell
.\cnx.cmd ticket cancel CNX-123 --reason "ไม่ต้องทำงานนี้ต่อ"
```

Ticket ที่ cancelled เป็น terminal และไม่ควรถูก supervisor ปลุกกลับมาทำอีก

---

# ส่วนที่ 15 — ยกเลิกงานทั้ง session

```powershell
.\cnx.cmd session cancel "<session-key>" --reason "session นี้ถูกยกเลิก"
```

คำสั่งนี้จะ cancel Ticket ที่ยังไม่ terminal ใน session นั้น

เหมาะสำหรับกรณีที่คุณลบ/เลิกใช้ session แล้วไม่ต้องการให้ detached work กลับมาทำต่อ

---

# ส่วนที่ 16 — ทดสอบ recovery จาก Gateway interruption

ทำเฉพาะเมื่อการใช้งานปกติผ่านแล้ว

แนวทางทดสอบ:

1. ส่งงานที่ใช้เวลานานกว่า greeting
2. ตรวจว่ามี Ticket ถูกสร้าง
3. ระหว่างงานกำลังทำ ให้หยุด Gateway
4. ตรวจ Ticket ยังไม่หาย
5. start Gateway ผ่าน `cnx`
6. ตรวจว่า Host reconcile และงาน eligible ถูก resume
7. ตรวจว่าไม่มี duplicate side effect

คำสั่งหลัก:

```powershell
.\cnx.cmd ticket list
.\cnx.cmd gateway stop
.\cnx.cmd status
.\cnx.cmd gateway start
.\cnx.cmd ticket list
```

---

# ส่วนที่ 17 — ทดสอบ reboot

หลังจาก stop/start/restart ผ่านแล้ว ค่อยทดสอบ reboot

1. ให้ CogentNexus อยู่ MANAGED
2. มีงานที่สามารถ resume ได้
3. restart Windows
4. login กลับมา
5. เปิด PowerShell
6. เข้า workspace

```powershell
Set-Location "$HOME\.openclaw\workspace"
.\cnx.cmd status
```

ตรวจว่า Host supervisor ถูก reconcile และ desired state ยังอยู่

จากนั้น:

```powershell
.\cnx.cmd ticket list
```

งาน non-terminal ที่ปลอดภัยต่อ recovery ควรสามารถทำต่อได้

---

# ส่วนที่ 18 — เรื่องไฟดับจริง

CogentNexus ออกแบบให้ state ที่ commit ลง disk แล้วสามารถใช้ recovery หลัง boot ได้ แต่การดึงปลั๊กไฟจริงมีความเสี่ยงต่อ filesystem/hardware

แนะนำให้ทดสอบตามลำดับ:

1. kill/restart Gateway
2. restart OpenClaw process
3. restart Windows ปกติ
4. ค่อยทดสอบ unexpected shutdown ในเครื่องที่ยอมรับความเสี่ยงได้

สิ่งที่ CogentNexus รับประกันในเชิง architecture คือ **งานที่ commit แล้วต้องมี state สำหรับ recovery** ไม่ใช่การรับประกันว่าดิสก์ที่เสียหายทางกายภาพจะกู้ได้

---

# ส่วนที่ 19 — อัปเดต CogentNexus

สำหรับ stable release:

1. ดาวน์โหลด release ใหม่
2. ตรวจ SHA256
3. แตกไฟล์ใหม่
4. รัน installer ใหม่

```powershell
.\scripts\install.ps1
```

Installer จะ backup skill/policy เดิมและ preserve durable `.cogent` state

อย่าลบ `$HOME\.openclaw\workspace\.cogent` ถ้าต้องการเก็บ Ticket/workflow/history

---

# ส่วนที่ 20 — Troubleshooting

## `python` not found

```powershell
where.exe python
```

ถ้าไม่พบ ให้ติดตั้ง Python และเพิ่ม PATH

## `yaml` import ไม่ได้

```powershell
python -m pip install "PyYAML>=6.0,<7"
```

## `npm` not found

```powershell
node --version
npm --version
```

ติดตั้ง Node.js ใหม่ถ้าจำเป็น

## `openclaw` not found

```powershell
where.exe openclaw
openclaw --version
```

ตรวจการติดตั้ง global npm / PATH

## Gateway ไม่ healthy

```powershell
openclaw gateway status
openclaw status
```

จากนั้นลอง:

```powershell
.\cnx.cmd restart
```

ถ้า CogentNexus ยังติดตั้งไม่สำเร็จ ใช้ native command:

```powershell
openclaw gateway restart
```

## ต้องการกลับไปใช้ OpenClaw ปกติทันที

```powershell
.\cnx.cmd disable
```

นี่คือ recovery path ที่ตั้งใจออกแบบไว้ ไม่ต้อง uninstall

## CogentNexus หยุดแล้วแต่ supervisor เปิดกลับ

อย่าฆ่า process อย่างเดียว ให้ใช้:

```powershell
.\cnx.cmd stop
```

เพื่อ persist MAINTENANCE intent

## งานค้าง ไม่แน่ใจว่าควรส่งใหม่หรือไม่

**อย่าส่งซ้ำก่อน**

ตรวจ:

```powershell
.\cnx.cmd status
.\cnx.cmd ticket list
```

ถ้า Ticket เดิมยังอยู่ ระบบอาจกำลังกู้มันอยู่

---

# Checklist หลังติดตั้ง

ให้ทำเครื่องหมายทีละข้อ:

```text
[ ] python --version ผ่าน
[ ] node/npm ผ่าน
[ ] openclaw --version ผ่าน
[ ] ollama/model พร้อม (ถ้าใช้ Ollama)
[ ] SHA256 release ตรง
[ ] install.ps1 สำเร็จ
[ ] cnx.cmd มีอยู่
[ ] cnx status = managed
[ ] gateway healthy
[ ] ส่ง "สวัสดีครับ" แล้วตอบได้
[ ] ticket list เห็น Ticket
[ ] cnx stop แล้วไม่ auto-start
[ ] cnx start แล้วกลับมาทำงาน
[ ] cnx restart ผ่าน
[ ] cnx disable แล้ว OpenClaw ใช้ได้ปกติ
[ ] cnx enable แล้วกลับ MANAGED
[ ] ทดสอบ Gateway interruption recovery
[ ] ทดสอบ Windows reboot recovery
```

เมื่อ checklist นี้ผ่านทั้งหมด จึงค่อยถือว่า CogentNexus ถูกติดตั้งและตรวจ end-to-end บนเครื่องจริงแล้ว
