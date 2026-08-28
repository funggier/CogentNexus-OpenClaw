# ติดตั้ง CogentNexus-OpenClaw v0.9.3 บน Windows

CogentNexus-OpenClaw v0.9.3 ตอนนี้ยังเป็น **development candidate** โดย compatibility baseline ที่ยืนยันคือ OpenClaw `2026.7.1-2` และ managed provider ของ v0.9.3 คือ **Ollama only**

ตอนนี้ยังไม่มี GitHub Release v0.9.3 ที่เผยแพร่แล้ว คู่มือนี้จึงใช้สำหรับ source/development candidate ที่ผ่านการตรวจสอบเท่านั้น จนกว่าจะผ่าน repository stabilization, freeze exact candidate, real-Windows acceptance และ human release review

## สิ่งที่ต้องมี

- Windows 10/11 หรือ Windows Server พร้อม PowerShell 5.1 ขึ้นไป
- OpenClaw ที่ใช้งานได้
- OpenClaw `2026.7.1-2` สำหรับ compatibility baseline ที่ยืนยันในปัจจุบัน
- Ollama
- Python 3.11+ และ PyYAML
- Node.js + npm

LM Studio เป็นส่วนของ provider layer ใน historical v0.9.2 และไม่ใช่ managed provider ของ v0.9.3

## ติดตั้งจาก development candidate

สำหรับงาน acceptance ต้องใช้ candidate ที่ระบุตัวตนแน่นอนแล้วเท่านั้น จาก checkout หรือ archive ของ candidate:

```powershell
python -m pip install "PyYAML>=6.0,<7"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

ตั้งใจ **ไม่มี** คำสั่ง `cnxclaw.cmd install` การติดตั้งทำผ่าน installer จาก source/archive

ก่อน final real-machine acceptance ต้องบันทึก exact commit SHA, payload-v2 fingerprint, payload file count, archive SHA256 และ GitHub Actions evidence ให้ครบก่อน ห้ามแก้ worktree หลัง freeze แล้วถือว่าเป็น candidate เดิม

## การติดตั้งจาก Release ในอนาคต

เมื่อ v0.9.3 ถูกเผยแพร่จริงแล้ว คู่มือ release จึงค่อยอ้าง archive และ checksum ของ release ที่มีอยู่จริงได้ ระหว่างนี้อย่าสมมติว่า v0.9.3 release asset มีอยู่แล้ว

## สิ่งที่ installer ทำ

Installer จะ stage/validate skill, สร้าง owned Host/runtime state อย่างปลอดภัย, install/validate OpenClaw Bridge, สร้าง `cnxclaw.cmd`, ตรวจ provider/Gateway preflight และเข้า MANAGED mode เฉพาะเมื่อ verification ที่ต้องการผ่านแล้ว

operator-facing provider target ของ v0.9.3 คือ Ollama

## ตรวจหลังติดตั้งแบบ Pre-flight

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
```

managed state ที่พร้อมควรมีอย่างน้อย:

- controller mode = `managed`
- managed provider = Ollama
- Ollama ติดตั้งและ reachable
- Gateway healthy
- CogentNexus-OpenClaw plugin enabled/loaded
- Ticket database อ่านได้และ integrity ผ่าน
- ไม่มี recovery/outbox backlog ที่ไม่คาดคิดในระบบที่ idle

ทุกคำสั่งใต้ `check` ต้องเป็น **read-only** และห้ามแก้ lifecycle/config/Ticket state

## คำสั่งใช้งานประจำ

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd provider list
.\cnxclaw.cmd check system
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
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

- `disable` = คืน OpenClaw ไป native/PASSTHROUGH
- `stop` = deliberate MAINTENANCE โดยเก็บ durable state

## Reset ให้เหมือน fresh install

```powershell
.\cnxclaw.cmd reset
```

หรือระบุ Ollama อย่างชัดเจนเมื่อ interface รองรับ:

```powershell
.\cnxclaw.cmd reset --provider ollama
```

`reset` เป็น destructive operation และต้องพิมพ์ `y` ยืนยันอย่างชัดเจน ระบบต้องล้างเฉพาะ CogentNexus-OpenClaw-owned Ticket/recovery/delivery/runtime/session/workflow/diagnostic/config state แล้วสร้าง fresh state จาก candidate ที่ติดตั้งอยู่ โดยต้องไม่ลบ OpenClaw ภายนอก, Ollama models/data หรือ unrelated workspace data

## ถอน CogentNexus-OpenClaw ออกทั้งหมด

```powershell
.\cnxclaw.cmd uninstall
```

`uninstall` เป็น destructive operation และต้องพิมพ์ `y` ยืนยัน ระบบต้องคืน native/PASSTHROUGH อย่างปลอดภัยแล้วลบเฉพาะ CogentNexus-OpenClaw-owned surfaces โดยรักษา OpenClaw, Ollama, user data และ namespace อื่นไว้

## ขอบเขต acceptance

ระหว่าง repository stabilization **ห้าม** uninstall/install/reset/restart live target และห้ามส่ง Dashboard semantic acceptance message ใหม่

หลัง repository candidate ถูก freeze แล้วเท่านั้นจึงเปิด bounded real-Windows task สำหรับ:

1. clean uninstall
2. fresh install exact frozen candidate
3. install-over/reset/uninstall/reinstall lifecycle tests
4. runtime readiness + installed fingerprint parity
5. final Dashboard semantic/durable-delivery acceptance หนึ่งครั้ง

Recovery Core checkpoint `eadb89099637d24f96e265a500d66c577aa939a3` เป็น historical technical evidence ที่ผ่าน live Test A v16 บน Windows/OpenClaw/Ollama แล้ว แต่ไม่ใช่ final v0.9.3 release acceptance โดยตัวมันเอง

ดูเพิ่มเติมที่ [CURRENT_STATE.md](CURRENT_STATE.md), [PROVIDERS.md](PROVIDERS.md) และ [CHECK_SYSTEM.md](CHECK_SYSTEM.md)
