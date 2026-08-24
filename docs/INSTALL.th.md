# ติดตั้ง CogentNexus-OpenClaw v0.9.3 บน Windows

คู่มือนี้อ้างอิง Recovery Core ที่ผ่าน acceptance แล้ว โดย compatibility ที่ยืนยันคือ OpenClaw `2026.7.1-2` หากอัปเกรด OpenClaw เป็นรุ่นใหม่กว่านี้ ควรทดสอบ compatibility ก่อนถือว่ารับประกัน recovery boundary เดิม

v0.9.2 เก็บ Recovery Core ของ v0.9.1 ไว้ และเพิ่ม provider-neutral lifecycle สำหรับ Ollama/LM Studio พร้อม `cnxclaw check ...` แบบ read-only

## สิ่งที่ต้องมี

- Windows + PowerShell 5.1 ขึ้นไป
- OpenClaw ที่ใช้งานได้อยู่แล้ว
- Python 3.11+ และ PyYAML
- Node.js + npm
- local provider อย่างน้อยหนึ่งตัวถ้าต้องการให้ CNXCLAW ควบคุม local inference:
  - Ollama หรือ
  - LM Studio ที่มี `lms` CLI

Ollama และ LM Studio สามารถติดตั้งอยู่เครื่องเดียวกันได้ตามปกติ เพราะใช้ loopback port คนละตัว (`11434` และ `1234`)

## แนะนำ: ติดตั้งจาก GitHub Release

1. ดาวน์โหลด `cogentnexus-openclaw-v0.9.3.zip` และ `SHA256SUMS.txt` จาก GitHub Release v0.9.3
2. ตรวจ SHA256 ให้ตรงก่อนแตกไฟล์
3. แตกไฟล์ไว้ในโฟลเดอร์ source ปกติ ไม่ต้องวางทับ extension ที่กำลังใช้งาน
4. เปิด PowerShell ในโฟลเดอร์ที่แตกไฟล์
5. เลือก provider ที่ต้องการให้ CNXCLAW supervise:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1 -Provider ollama
```

หรือ:

```powershell
.\scripts\install.ps1 -Provider lmstudio
```

ถ้าในเครื่องมี supported provider เพียงตัวเดียว สามารถไม่ระบุ `-Provider` ได้ แต่ถ้ามีทั้ง Ollama และ LM Studio ใน fresh CNXCLAW state จะต้องเลือกให้ชัดเจน

การตั้ง ExecutionPolicy แบบ `Process` มีผลเฉพาะหน้าต่าง PowerShell ปัจจุบัน ไม่ได้แก้ policy ถาวรของเครื่อง

## สิ่งที่ installer ทำ

Installer จะตรวจ dependency, stage/validate skill, สร้าง Host state เริ่มต้นใน PASSTHROUGH, validate/install Bridge plugin, สร้าง `cnxclaw.cmd`, ทำ provider preflight และ transactional enable ไป MANAGED หลัง provider + Gateway ผ่านการตรวจแล้ว

ตั้งใจ **ไม่มี** คำสั่ง `cnxclaw.cmd install` การติดตั้งใหม่ให้ทำจาก CogentNexus-OpenClaw Release ที่แตกไฟล์แล้ว

## กรณีใช้ LM Studio

LM Studio ต้องมี `lms` CLI เพื่อให้ CogentNexus-OpenClaw สามารถ start/stop server แบบ deterministic ได้ โดย default server ใช้ port `1234`

การเลือก provider ใน CogentNexus-OpenClaw **ไม่แอบเปลี่ยนโมเดลใน OpenClaw** ให้เอง ต้องตั้งค่า model route ของ LM Studio ใน OpenClaw ให้เรียบร้อยก่อน แล้วจึงให้ CNXCLAW supervise backend ด้วย:

```powershell
.\cnxclaw.cmd start --provider lmstudio
```

## ตรวจหลังติดตั้งแบบ Pre-flight

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
```

หากต้องการตรวจสมมุติว่าเปลี่ยนไปใช้ LM Studio โดยยังไม่เปลี่ยน provider ที่จำไว้:

```powershell
.\cnxclaw.cmd check system --provider lmstudio
```

`check system` จะตรวจ CNXCLAW state/config, OpenClaw, provider, model route, Gateway, Ticket DB, recovery/delivery และ resource headroom แล้วสรุปเป็น:

- `READY`
- `READY_WITH_WARNINGS`
- `NOT_READY`
- `INDETERMINATE`

ทุกคำสั่งใต้ `check` เป็น **read-only** และต้องไม่ start/restart process, ไม่แก้ config, ไม่เปลี่ยน selected provider และไม่ repair DB

## คำสั่งใช้งานประจำ

```powershell
.\cnxclaw.cmd provider list
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd start --provider lmstudio
.\cnxclaw.cmd stop
.\cnxclaw.cmd restart
.\cnxclaw.cmd restart --provider ollama
.\cnxclaw.cmd gateway start
.\cnxclaw.cmd gateway stop
.\cnxclaw.cmd gateway restart
.\cnxclaw.cmd ticket list
.\cnxclaw.cmd disable
.\cnxclaw.cmd enable
```

เมื่อ `start --provider ...` สำเร็จ CNXCLAW จะจำ provider ตัวนั้นแบบ durable ครั้งถัดไปใช้ `start` หรือ `restart` เปล่า ๆ จะใช้ provider ล่าสุดที่ยืนยันสำเร็จ

จำความแตกต่างไว้ว่า:

- `disable` = คืน OpenClaw ไป native/PASSTHROUGH
- `stop` = ตั้งใจหยุด CNXCLAW ใน MAINTENANCE โดยยังเก็บ durable state

ทั้งสองกรณีไม่ลืม selected provider

## Reset ให้เหมือนเพิ่งติดตั้งใหม่

ถ้ามี supported provider เพียงตัวเดียว:

```powershell
.\cnxclaw.cmd reset
```

ถ้ามีทั้ง Ollama และ LM Studio จะต้องเลือก provider ใหม่สำหรับ fresh state:

```powershell
.\cnxclaw.cmd reset --provider ollama
# หรือ
.\cnxclaw.cmd reset --provider lmstudio
```

`reset` เป็นคำสั่งทำลายข้อมูลและจะทำงานต่อเมื่อผู้ใช้พิมพ์ `y` ยืนยันเท่านั้น หากกด Enter หรือพิมพ์ค่าอื่นจะยกเลิกโดยไม่เปลี่ยนแปลงระบบ

เมื่อยืนยันแล้ว ระบบจะคืน OpenClaw ไป PASSTHROUGH ก่อน จากนั้นล้าง Ticket, recovery/delivery state, runtime/session/workflow state, diagnostics และค่าปรับของ CogentNexus-OpenClaw แล้วสร้าง fresh state จาก **release เวอร์ชันที่ติดตั้งอยู่เดิม** ก่อน transactional enable กลับไป MANAGED

ไฟล์โปรแกรมและเวอร์ชัน CogentNexus-OpenClaw ที่ติดตั้งอยู่จะไม่ถูกเปลี่ยน และจะไม่ลบข้อมูล OpenClaw, Ollama หรือ LM Studio หากการสร้างใหม่ล้มเหลว CogentNexus-OpenClaw ต้องไม่อ้าง MANAGED authority จากสถานะที่สร้างไม่ครบ

## ถอน CogentNexus-OpenClaw ออกทั้งหมด

```powershell
.\cnxclaw.cmd uninstall
```

`uninstall` เป็นคำสั่งทำลายข้อมูลและจะทำงานต่อเมื่อผู้ใช้พิมพ์ `y` ยืนยันเท่านั้น

ระบบจะคืน CogentNexus-OpenClaw ไป PASSTHROUGH/native OpenClaw ก่อน, ปิด startup/supervisor integration, ถอน OpenClaw Bridge, ตรวจว่า native Gateway healthy แล้วจึงลบ `.cogentnexus-openclaw`, skill ของ CogentNexus-OpenClaw, plugin residue และ `cnxclaw.cmd`

OpenClaw, Ollama และ LM Studio จะไม่ถูกถอน

## ขอบเขตที่ยืนยันแล้ว

Recovery Core ที่ commit `eadb89099637d24f96e265a500d66c577aa939a3` ผ่าน Test A v16 แบบ live บน Windows/OpenClaw/Ollama แล้ว

LM Studio lifecycle support อยู่ใน v0.9.2 และผ่าน repository validation/unit tests แต่ยังควรทำ live acceptance บนเครื่องจริงก่อนอ้าง operational confidence ระดับเดียวกับ Ollama baseline

ดูเพิ่มเติมที่ [CURRENT_STATE.md](CURRENT_STATE.md), [PROVIDERS.md](PROVIDERS.md) และ [CHECK_SYSTEM.md](CHECK_SYSTEM.md)
