# ติดตั้ง CogentNexus-OpenClaw v0.9.6 บน Windows

คู่มือนี้เป็น **current-facing installation guide** สำหรับสาย v0.9.6 ครับ ควรติดตั้งจาก GitHub Release ที่ระบุเวอร์ชันชัดเจนและตรวจ `SHA256SUMS.txt` ก่อนใช้งานเสมอ

## ข้อมูล compatibility ที่ต้องแยกให้ออก

- OpenClaw ที่ pin ไว้สำหรับ regression/dev dependency: `2026.7.1-2`
- OpenClaw ที่ผ่าน physical runtime acceptance ล่าสุดจริง: `2026.9.5 (ec9c1a1)`

สองค่านี้มีความหมายต่างกัน ไม่ควรใช้ peer/dependency range เป็นหลักฐานว่า runtime ทุกเวอร์ชันผ่าน acceptance แล้ว

## สิ่งที่ต้องมี

- Windows 10/11 หรือ Windows Server
- PowerShell 5.1 ขึ้นไป
- OpenClaw ที่ใช้งานได้
- Python 3.11+ และ PyYAML
- Node.js + npm เมื่อติดตั้งจาก source/release tree

## ติดตั้งจาก development candidate

ไม่มีคำสั่ง `cnxclaw.cmd install` โดยตั้งใจ การติดตั้งทำผ่าน repository installer จาก exact release tree หรือ source checkout ที่ตรวจแล้ว

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

Installer เป็น provider-neutral: ติดตั้งและตรวจเฉพาะ CogentNexus-OpenClaw-owned surfaces ที่จำเป็น โดยไม่รับ provider/model credential เป็น installation authority

หลังติดตั้ง:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
```

## Provider boundary ปัจจุบัน

- Managed local provider lifecycle: **Ollama**
- Cloud/provider/model/auth routing: **OpenClaw เป็นเจ้าของ**
- CogentNexus-OpenClaw ดูแล Ticket/session/generation continuity และ durable delivery
- ไม่เก็บ/refresh Cloud credentials
- ไม่ fallback provider แบบเงียบ

## พฤติกรรม Stop/Queue ที่ v0.9.6 รับรอง

ข้อความที่สองใน owner session เดียวกันจะถูก persist แล้ว hold ที่ `before_dispatch` หาก Ticket ก่อนหน้ายังไม่ terminal จึงยังไม่เข้า Host queue

เมื่อผู้ใช้กด Stop:

- generation เพิ่มหนึ่งครั้ง
- active + held Ticket ถูก cancel
- held Ticket ที่ยังไม่เคย bind run จะถูก consume ก่อน Host queue
- ต้องไม่มี inference ของ held Ticket
- ต้องไม่มี successor Host run จากข้อความที่ถูกยกเลิก

CNX-442 ผ่าน physical Discord acceptance บน OpenClaw 2026.9.5 แล้ว

## คำสั่งประจำ

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd start
.\cnxclaw.cmd stop
.\cnxclaw.cmd restart
.\cnxclaw.cmd gateway start
.\cnxclaw.cmd gateway stop
.\cnxclaw.cmd gateway restart
.\cnxclaw.cmd ticket list
.\cnxclaw.cmd ticket cancel <ticket-id>
.\cnxclaw.cmd session cancel <session-key>
.\cnxclaw.cmd disable
.\cnxclaw.cmd enable
```

ดูรายละเอียดเพิ่มที่ [COMMANDS.th.md](COMMANDS.th.md)

## Reset / Uninstall

```powershell
.\cnxclaw.cmd reset
.\cnxclaw.cmd uninstall
```

ทั้งสองคำสั่งเป็น destructive operation และต้องยืนยันอย่างชัดเจน ระบบต้องลบเฉพาะ CogentNexus-OpenClaw-owned state และรักษา OpenClaw/Ollama/user data ที่อยู่นอก ownership boundary

## Clean reinstall

ใช้ [CLEAN_REINSTALL.th.md](CLEAN_REINSTALL.th.md) เมื่อต้องการล้าง CNX-owned durable state และติดตั้งใหม่ โดยค่าเริ่มต้นควร backup ออกนอก active tree ก่อน

## ติดตั้งจาก GitHub Release v0.9.6

ไฟล์ที่คาดหวัง:

- `cogentnexus-openclaw-v0.9.6.tar.gz`
- `cogentnexus-openclaw-v0.9.6.zip`
- `SHA256SUMS.txt`
- release notes

ให้ตรวจ checksum ก่อน extract/install

## อ่านเพิ่มเติม

- [CURRENT_STATE.md](CURRENT_STATE.md)
- [PROVIDERS.md](PROVIDERS.md)
- [CHECK_SYSTEM.md](CHECK_SYSTEM.md)
- [COMMANDS.th.md](COMMANDS.th.md)
- [CLEAN_REINSTALL.th.md](CLEAN_REINSTALL.th.md)
