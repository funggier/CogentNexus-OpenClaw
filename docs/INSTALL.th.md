# ติดตั้ง CogentNexus-OpenClaw v0.9.3 บน Windows

CogentNexus-OpenClaw v0.9.3 ใช้ compatibility baseline ที่ยืนยันแล้วคือ OpenClaw `2026.7.1-2 (0790d9f)` และ managed provider ของ runtime/operator boundary ปัจจุบันคือ **Ollama only**

exact product candidate `f6392da3e4112ce441526d5ef19925c90a872b0b` ผ่าน bounded real-Windows lifecycle acceptance และ final Dashboard semantic/durable-delivery acceptance แล้ว แต่ Task 187 พบว่า current guidance บางไฟล์อยู่ภายใน installed/payload-sensitive product surface และยังมีข้อความก่อน acceptance อยู่ การแก้ไฟล์เหล่านั้นจะเปลี่ยน candidate/artifact identity จึงต้องทำ candidate ใหม่และ requalification ตาม changed surface ก่อน publish

ดังนั้นตอนนี้ยัง **ไม่มี** public GitHub Release/tag `v0.9.3` ห้ามสมมติว่า release asset มีอยู่แล้ว และห้ามถือ moving development branch ว่าเป็น accepted candidate เดิม

## สิ่งที่ต้องมี

- Windows 10/11 หรือ Windows Server พร้อม PowerShell 5.1 ขึ้นไป
- OpenClaw ที่ใช้งานได้
- OpenClaw `2026.7.1-2` สำหรับ validated compatibility baseline
- Python 3.11+ และ PyYAML
- Node.js + npm

รายการนี้เป็น prerequisite ของ installer ส่วน managed-provider readiness ตรวจหลังติดตั้งผ่าน runtime checks ไม่ใช่ความรับผิดชอบของ installer prerequisite contract

## ติดตั้งจาก development candidate

ตั้งใจ **ไม่มี** คำสั่ง `cnxclaw.cmd install` การติดตั้งทำผ่าน repository installer จาก exact source/archive ที่ตรวจสอบแล้ว

บน Windows:

```powershell
python -m pip install "PyYAML>=6.0,<7"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

บน POSIX:

```sh
python -m pip install 'PyYAML>=6.0,<7'
./scripts/install.sh --workspace "$HOME/.openclaw/workspace"
```

## สิ่งที่ installer ทำ

Installer เป็น provider-neutral: ทำหน้าที่ stage/validate skill, สร้าง owned Host/runtime state อย่างปลอดภัย, install/validate OpenClaw Bridge, สร้าง launcher และเปิด runtime หลัง verification ที่ installer เป็นเจ้าของผ่านแล้วเท่านั้น ส่วน provider/runtime readiness เป็น post-install concern แยกต่างหาก

LM Studio เป็นส่วนของ frozen historical v0.9.2 และไม่ใช่ managed provider ของ v0.9.3 ส่วน runtime/operator target ของ v0.9.3 คือ Ollama แต่ responsibility เรื่อง selection/readiness นี้อยู่นอก installer prerequisite boundary

## Accepted-candidate identity

Windows acceptance ที่ผ่านแล้วใช้ตัวตนนี้เท่านั้น:

```text
source candidate: f6392da3e4112ce441526d5ef19925c90a872b0b
active facade SHA-256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
OpenClaw: 2026.7.1-2 (0790d9f)
managed provider: ollama
```

Task 187 พิสูจน์ว่าการแก้ stale current guidance ภายใน installed skill และ npm plugin package จะเปลี่ยน product/payload identity จึงห้ามอ้างว่า corrected candidate ใหม่ยังเป็น artifact เดิมเพียงเพราะ executable source ไม่ได้เปลี่ยน

## ตรวจ runtime/provider หลังติดตั้ง

runtime/provider target ของ v0.9.3 คือ Ollama เท่านั้น ส่วน executable availability, endpoint/model readiness และ provider-specific health checks เป็นความรับผิดชอบของ runtime และตรวจหลังติดตั้ง

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
```

managed readiness ควรมีอย่างน้อย:

- controller mode = `managed`
- managed provider = Ollama
- Ollama ติดตั้งและ reachable
- Gateway healthy
- CogentNexus-OpenClaw plugin enabled/loaded
- Ticket database อ่านได้และ integrity ผ่าน
- ไม่มี recovery/outbox backlog ที่ไม่คาดคิดในระบบ idle

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

`reset` เป็น destructive operation และต้องพิมพ์ `y` ยืนยันอย่างชัดเจน ระบบจะล้างเฉพาะ CogentNexus-OpenClaw-owned Ticket/recovery/delivery/runtime/session/workflow/diagnostic/config state แล้วสร้าง fresh state จาก candidate ที่ติดตั้งอยู่ โดยต้องไม่ลบ OpenClaw ภายนอก, Ollama models/data หรือ unrelated workspace data

Task 183 ยืนยัน boundary นี้บน frozen candidate แล้ว

## ถอน CogentNexus-OpenClaw ออกทั้งหมด

```powershell
.\cnxclaw.cmd uninstall
```

`uninstall` เป็น destructive operation และต้องพิมพ์ `y` ยืนยัน ระบบต้องคืน native/PASSTHROUGH อย่างปลอดภัยแล้วลบเฉพาะ CogentNexus-OpenClaw-owned surfaces โดยรักษา OpenClaw, Ollama, user data และ namespace อื่นไว้

Task 184 ยืนยัน external-preservation boundary แล้ว และ Task 185 ยืนยัน fresh reinstall + post-install health ต่อจาก uninstall แล้ว

## Final semantic acceptance ที่ผ่านแล้วสำหรับ frozen candidate

Task 186 ยืนยันหนึ่ง bounded Dashboard turn หลัง lifecycle sequence:

```text
1 human Send
-> 1 Ticket
-> 1 session/run
-> 1 Ollama model call
-> 1 durable assistant delivery
-> 1 logical Dashboard assistant result
```

ไม่มี retry, duplicate semantic work, direct recovery หรือ outbox residue

## การติดตั้งจาก Release ในอนาคต

หลัง corrected documentation-bearing candidate ผ่าน requalification และ `v0.9.3` ถูก publish จริง ให้ใช้ assets ที่ `.github/workflows/release.yml` สร้าง:

- `cogentnexus-openclaw-v0.9.3.tar.gz`
- `cogentnexus-openclaw-v0.9.3.zip`
- `SHA256SUMS.txt`

ให้ตรวจ checksum ของ archive จาก `SHA256SUMS.txt`, extract archive แล้วรัน installer จาก exact extracted release tree นั้น จนกว่า GitHub Release จะมีอยู่จริง ห้ามเดาหรือสร้าง release download URL ขึ้นเอง

ดูเพิ่มเติมที่ [CURRENT_STATE.md](CURRENT_STATE.md), [PROVIDERS.md](PROVIDERS.md), [CHECK_SYSTEM.md](CHECK_SYSTEM.md) และ [CLEAN_REINSTALL.md](CLEAN_REINSTALL.md)
