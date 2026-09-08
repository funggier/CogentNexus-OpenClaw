# คู่มือคำสั่ง CogentNexus-OpenClaw v0.9.4

คู่มือนี้ใช้กับ CogentNexus-OpenClaw v0.9.4 บน Windows โดยรันจาก OpenClaw workspace:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnxclaw.cmd --help
```

> v0.9.4 ยังไม่ถือว่า release จนกว่าจะมี immutable tag และ GitHub Release จริง ให้ตรวจ artifact และ `SHA256SUMS.txt` ก่อนติดตั้งเสมอ

## เลือกโหมดให้ถูก

### Managed Ollama

CogentNexus-OpenClaw เป็นเจ้าของ health check, lifecycle, readiness และ recovery ของ Ollama รวมถึง continuity, Ticket และ durable delivery:

```powershell
.\cnxclaw.cmd enable
.\cnxclaw.cmd start
.\cnxclaw.cmd start --provider ollama
.\cnxclaw.cmd restart
.\cnxclaw.cmd restart --provider ollama
.\cnxclaw.cmd stop
```

- `enable` เปิด managed policy, plugin และ supervisor แล้วทำให้ Ollama/Gateway พร้อมใช้งาน
- `start` ต้องการสถานะ managed และทำให้ managed runtime ทำงาน
- `restart` restart managed runtime ภายใต้ maintenance/recovery fences
- `stop` คือ deliberate MAINTENANCE; เก็บ durable state แต่หยุด managed runtime
- v0.9.4 จัดการ provider ได้เฉพาะ Ollama และไม่จัดการ LM Studio

### OpenClaw-owned Cloud pass-through

ในโหมดนี้ OpenClaw เป็นเจ้าของ authentication/credentials, provider/model selection, routing, provider runtime, lifecycle, probing และ recovery ส่วน CogentNexus-OpenClaw คงเฉพาะ passive continuity, Ticket/session ownership และ durable delivery

ลำดับที่รองรับคือ:

```powershell
.\cnxclaw.cmd cloud
openclaw models set <provider/model>
```

ตัวอย่างรูปแบบ model ID (ให้ใช้ route ที่ OpenClaw ของคุณรองรับจริง):

```powershell
openclaw models set openai/<model-id>
```

ต้องรัน `cnxclaw.cmd cloud` ก่อน เพราะคำสั่งนี้ restore OpenClaw native route, เอา managed policy ออก, ปิด supervisor, ตั้ง Host เป็น PASSTHROUGH, คง plugin enabled ใน passive mode และ restart Gateway หนึ่งครั้ง จากนั้นจึงให้ operator เลือก Cloud route ผ่าน OpenClaw

ข้อห้าม:

- `cnxclaw.cmd cloud` ไม่รับ provider, model หรือ credential argument
- ห้ามส่ง credential ผ่านคำสั่ง CogentNexus-OpenClaw
- ห้ามใช้ `cnxclaw` probe/start/stop/restart/recover Cloud provider
- Cloud error ไม่อนุญาตให้ fallback ไป Ollama หรือเรียก Ollama recovery โดยอัตโนมัติ
- การ delivery retry ต้องส่ง durable result เดิม ห้าม regenerate inference

กลับสู่ Managed Ollama:

```powershell
.\cnxclaw.cmd enable
```

`enable` จะตั้ง plugin `providerMode=managed` และใช้ Ollama ตาม managed provider contract

## ตรวจสถานะ (read-only)

คำสั่งต่อไปนี้เป็น read-only ใน Managed mode:

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider
.\cnxclaw.cmd check provider ollama
.\cnxclaw.cmd check cogentnexus-openclaw
.\cnxclaw.cmd check config
.\cnxclaw.cmd check openclaw
.\cnxclaw.cmd check gateway
.\cnxclaw.cmd check model
.\cnxclaw.cmd check storage
.\cnxclaw.cmd check recovery
.\cnxclaw.cmd check delivery
.\cnxclaw.cmd check resources
.\cnxclaw.cmd provider list
.\cnxclaw.cmd provider status
```

ใน Cloud pass-through ให้ตรวจ route/model/provider ด้วย OpenClaw-owned commands และตรวจ CogentNexus-OpenClaw state จาก passive/durable evidence โดยอย่าเรียก CogentNexus-OpenClaw managed-provider probe

## Gateway

คำสั่งเหล่านี้เป็น lifecycle ของ Gateway ภายใต้ CogentNexus-OpenClaw managed control:

```powershell
.\cnxclaw.cmd gateway start
.\cnxclaw.cmd gateway stop
.\cnxclaw.cmd gateway restart
```

สำหรับ Cloud pass-through ให้ OpenClaw เป็นเจ้าของ Gateway/provider operations ตาม OpenClaw configuration และ operator policy

## Ticket และ session

```powershell
.\cnxclaw.cmd ticket list
.\cnxclaw.cmd ticket cancel <ticket-id>
.\cnxclaw.cmd session cancel <session-key>
```

- ใช้ `ticket cancel` เมื่อมี authority ให้ยกเลิก Ticket ที่ระบุ
- `session cancel` ยกเลิกงานของ session ตาม supported cancellation semantics
- `session cancel` ไม่ใช้แทนการลบ Ticket/session/transcript
- ห้ามแก้ SQLite, Ticket, session หรือ transcript ด้วยมือ
- ห้าม replay/redelivery หรือส่ง semantic request ซ้ำเมื่อไม่มี acceptance authority ชัดเจน

## Disable, reset และ uninstall

```powershell
.\cnxclaw.cmd disable
.\cnxclaw.cmd reset
.\cnxclaw.cmd uninstall
```

- `disable` คืน native/PASSTHROUGH และปิด plugin ทั้งหมด ต่างจาก `cloud` ที่คง passive plugin enabled
- `reset` ล้างเฉพาะ CogentNexus-OpenClaw-owned runtime state แล้วสร้างใหม่ ต้องยืนยัน `y`
- `uninstall` ถอนเฉพาะ CogentNexus-OpenClaw-owned surfaces ต้องยืนยัน `y`
- ก่อนใช้คำสั่ง destructive ให้ backup และตรวจ ownership boundary เสมอ
- ห้ามใช้ `session cancel` เป็น Delete substitute

## ตัวอย่าง workflow

### ตรวจ Managed Ollama

```powershell
.\cnxclaw.cmd status
.\cnxclaw.cmd check system
.\cnxclaw.cmd check provider ollama
```

### เข้า Cloud pass-through

```powershell
.\cnxclaw.cmd cloud
openclaw models set <provider/model>
openclaw config get agents.defaults.model.primary
openclaw gateway status
```

### กลับ Managed Ollama

```powershell
.\cnxclaw.cmd enable
.\cnxclaw.cmd check system
```

## อ่านเพิ่มเติม

- [คู่มือติดตั้งภาษาไทย](INSTALL.th.md)
- [Provider boundaries](PROVIDERS.md)
- [สถานะปัจจุบัน](CURRENT_STATE.md)
- [Clean reinstall ภาษาไทย](CLEAN_REINSTALL.th.md)
