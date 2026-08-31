# ติดตั้ง CogentNexus-OpenClaw v0.9.3 บน Windows

CogentNexus-OpenClaw v0.9.3 ใช้ compatibility baseline ที่ยืนยันแล้วคือ OpenClaw `2026.7.1-2 (0790d9f)` และ managed provider ของ runtime/operator boundary ปัจจุบันคือ **Ollama only**

implementation candidate `f6392da3e4112ce441526d5ef19925c90a872b0b` ผ่าน bounded real-Windows lifecycle acceptance และ final Dashboard semantic/durable-delivery acceptance แล้ว หลังจากนั้น Task 188 แก้ current-facing documentation ภายใน npm package และ installed skill surface โดยไม่เปลี่ยน executable/runtime source โดย corrected package payload-v2 identity คือ `408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b` / `184` files และ installed skill-tree identity คือ `a1e873ba404205507a1623961b49f1b1a0689f9f`

การอ้างว่า artifact ถูก publish หรือติดตั้งต้องผูกกับ exact candidate/release artifact เสมอ GitHub Releases/tags เป็น authority ว่า public `v0.9.3` ถูก publish แล้วหรือยัง ส่วน moving branch ไม่ใช่ release identity

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

## Artifact identity และ acceptance lineage

full Windows acceptance sequence ผ่านครั้งแรกบน implementation baseline นี้:

```text
source candidate: f6392da3e4112ce441526d5ef19925c90a872b0b
active facade SHA-256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
installed plugin inventory fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
OpenClaw: 2026.7.1-2 (0790d9f)
managed provider: ollama
```

Task 188 แก้ documentation-bearing product bytes โดยรักษา executable/runtime source เดิมไว้ corrected artifact identities คือ:

```text
package payload-v2: 408167da1bfba7fa9723d1bd557f29d516ed27c27398b4e48abf9a4f294e6b5b
package file count: 184
installed skill tree: a1e873ba404205507a1623961b49f1b1a0689f9f
executable scripts tree: 3d9d323ba19443d46e970b87cef52ce878da274f (unchanged)
facade Git blob: 879083d6186589d4b2774b8fd87fa93692dd2dfc (unchanged)
```

เพราะ package/skill bytes เปลี่ยน corrected artifact จึงต้องผ่าน proportional changed-surface requalification ก่อน publication การทำเช่นนี้ไม่ได้ลบหลักฐาน lifecycle เดิม แต่เก็บหลักฐานนั้นไว้สำหรับ executable surface ที่พิสูจน์ว่า byte-identical และ requalify เฉพาะ installed documentation/instruction surface ที่เปลี่ยน

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

Task 183 ยืนยัน boundary นี้บน implementation baseline แล้ว Task 188 จะไม่ทำ destructive boundary นี้ซ้ำโดยอัตโนมัติเพราะไฟล์ที่แก้เป็น documentation/instruction bytes และจะทำซ้ำเฉพาะเมื่อ evidence ของ corrected candidate ให้เหตุผลด้าน lifecycle ที่ชัดเจน

## ถอน CogentNexus-OpenClaw ออกทั้งหมด

```powershell
.\cnxclaw.cmd uninstall
```

`uninstall` เป็น destructive operation และต้องพิมพ์ `y` ยืนยัน ระบบต้องคืน native/PASSTHROUGH อย่างปลอดภัยแล้วลบเฉพาะ CogentNexus-OpenClaw-owned surfaces โดยรักษา OpenClaw, Ollama, user data และ namespace อื่นไว้

Task 184 ยืนยัน external-preservation boundary บน implementation baseline แล้ว และ Task 185 ยืนยัน fresh reinstall + post-install health ต่อจาก uninstall แล้ว

## Final semantic acceptance lineage

Task 186 ยืนยันหนึ่ง bounded Dashboard turn หลัง lifecycle sequence:

```text
1 human Send
-> 1 Ticket
-> 1 session/run
-> 1 Ollama model call
-> 1 durable assistant delivery
-> 1 logical Dashboard assistant result
```

ไม่มี retry, duplicate semantic work, direct recovery หรือ outbox residue เนื่องจาก Task 188 เปลี่ยน installed instruction surface การ proportional requalification จึงรวม bounded semantic/durable-delivery turn เพิ่มอีกหนึ่งครั้งก่อน publication

## การติดตั้งจาก Release

เมื่อ GitHub Release `v0.9.3` มีอยู่จริง ให้ใช้ exact assets ที่ `.github/workflows/release.yml` สร้างและ verify:

- `cogentnexus-openclaw-v0.9.3.tar.gz`
- `cogentnexus-openclaw-v0.9.3.zip`
- `SHA256SUMS.txt`

ให้ตรวจ checksum ของ archive จาก `SHA256SUMS.txt`, extract archive แล้วรัน installer จาก exact extracted release tree นั้น หาก GitHub Release/tag ยังไม่มีอยู่ ให้ใช้ exact candidate ที่ได้รับการ review ชัดเจนแทน และห้ามเดาหรือสร้าง release download URL ขึ้นเอง

ดูเพิ่มเติมที่ [CURRENT_STATE.md](CURRENT_STATE.md), [PROVIDERS.md](PROVIDERS.md), [CHECK_SYSTEM.md](CHECK_SYSTEM.md) และ [CLEAN_REINSTALL.md](CLEAN_REINSTALL.md)
