# ติดตั้ง CogentNexus v0.9.1 บน Windows

คู่มือนี้อ้างอิง baseline ที่ผ่าน acceptance แล้ว ณ 20 สิงหาคม 2026 โดย compatibility ที่ยืนยันคือ OpenClaw `2026.7.1-2` หากอัปเกรด OpenClaw เป็นรุ่นใหม่กว่านี้ ควรทดสอบ compatibility ก่อนถือว่ารับประกัน recovery boundary เดิม

## สิ่งที่ต้องมี

- Windows + PowerShell 5.1 ขึ้นไป
- OpenClaw ที่ใช้งานได้อยู่แล้ว
- Python 3.11+ และ PyYAML
- Node.js + npm
- provider/model ที่ OpenClaw ใช้งานได้ เช่น Ollama

## แนะนำ: ติดตั้งจาก GitHub Release

1. ดาวน์โหลด `cogentnexus-v0.9.1.zip` และ `SHA256SUMS.txt` จาก GitHub Release v0.9.1
2. ตรวจ SHA256 ให้ตรงก่อนแตกไฟล์
3. แตกไฟล์ไว้ในโฟลเดอร์ source ปกติ ไม่ต้องวางทับ extension ที่กำลังใช้งาน
4. เปิด PowerShell ในโฟลเดอร์ที่แตกไฟล์
5. รัน:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1
```

การตั้ง ExecutionPolicy แบบ `Process` มีผลเฉพาะหน้าต่าง PowerShell ปัจจุบัน ไม่ได้แก้ policy ถาวรของเครื่อง

## สิ่งที่ installer ทำ

Installer จะตรวจ dependency, stage/validate skill, สร้าง Host state เริ่มต้นใน PASSTHROUGH, validate/install plugin, สร้าง `cnx.cmd` และทำ transactional enable ไป MANAGED หลังจากองค์ประกอบที่จำเป็นผ่านการตรวจแล้ว

ตั้งใจ **ไม่มี** คำสั่ง `cnx.cmd install` การติดตั้งใหม่ให้ทำจาก CogentNexus Release ที่แตกไฟล์แล้วตามขั้นตอนด้านบนเสมอ

## ตรวจหลังติดตั้ง

```powershell
cd "$HOME\.openclaw\workspace"
.\cnx.cmd status
openclaw gateway status
openclaw plugins list
```

สำหรับการใช้งานปกติควรเห็น controller เป็น `managed`, Gateway healthy และ plugin CogentNexus พร้อมทำงาน

## คำสั่งใช้งานประจำ

```powershell
.\cnx.cmd status
.\cnx.cmd start
.\cnx.cmd stop
.\cnx.cmd restart
.\cnx.cmd gateway start
.\cnx.cmd gateway stop
.\cnx.cmd gateway restart
.\cnx.cmd ticket list
.\cnx.cmd disable
.\cnx.cmd enable
```

จำความแตกต่างไว้ว่า:

- `disable` = คืน OpenClaw ไปทำงาน native/PASSTHROUGH
- `stop` = ตั้งใจหยุด CNX ใน MAINTENANCE โดยยังเก็บ durable state

## Reset ให้เหมือนเพิ่งติดตั้งใหม่

```powershell
.\cnx.cmd reset
```

`reset` เป็นคำสั่งทำลายข้อมูลและจะทำงานต่อเมื่อผู้ใช้พิมพ์ `y` ยืนยันเท่านั้น หากกด Enter หรือพิมพ์ค่าอื่นจะยกเลิกโดยไม่เปลี่ยนแปลงระบบ

เมื่อยืนยันแล้ว ระบบจะคืน OpenClaw ไป PASSTHROUGH ก่อน จากนั้นล้าง Ticket, recovery/delivery state, runtime/session/workflow state, diagnostics และค่าปรับของ CogentNexus แล้วสร้าง schema/default state ใหม่จาก **release เวอร์ชันที่ติดตั้งอยู่เดิม** ก่อน transactional enable กลับไป MANAGED

ไฟล์โปรแกรมและเวอร์ชัน CogentNexus ที่ติดตั้งอยู่จะไม่ถูกเปลี่ยน และจะไม่ลบข้อมูล OpenClaw หรือ Ollama หากการสร้างใหม่ล้มเหลว CogentNexus ต้องไม่อ้าง MANAGED authority จากสถานะที่สร้างไม่ครบ

## ถอน CogentNexus ออกทั้งหมด

```powershell
.\cnx.cmd uninstall
```

`uninstall` เป็นคำสั่งทำลายข้อมูลและจะทำงานต่อเมื่อผู้ใช้พิมพ์ `y` ยืนยันเท่านั้น

ระบบจะคืน CogentNexus ไป PASSTHROUGH/native OpenClaw ก่อน, ปิด startup/supervisor integration, ถอน OpenClaw plugin, ตรวจว่า native Gateway healthy แล้วจึงลบ `.cogent`, skill ของ CogentNexus, plugin residue และ `cnx.cmd` ออกทั้งหมด

OpenClaw และ Ollama จะไม่ถูกถอน หากต้องการใช้ CogentNexus อีกครั้งหลัง uninstall ให้ดาวน์โหลด Release แล้วติดตั้งใหม่ตามขั้นตอนปกติด้านบน

## ขอบเขตที่ยืนยันแล้ว

Recovery Core ที่ commit `eadb89099637d24f96e265a500d66c577aa939a3` ผ่าน Test A v16 แบบ live แล้ว เหมาะกับการใช้งานทั่วไปบน stack ที่ยืนยัน แต่ยังไม่ได้อ้างว่า production-hardened สำหรับไฟดับจริง, DB corruption/disk full, load สูงมาก หรือ OpenClaw รุ่นใหม่กว่า baseline

ดูสถานะเต็มที่ [CURRENT_STATE.md](CURRENT_STATE.md)
