# ล้าง CogentNexus และติดตั้งใหม่แบบสะอาดบน Windows

ใช้ `scripts/clean-reinstall.ps1` เมื่ออยากเอา CogentNexus ที่ติดตั้งอยู่ใน workspace ปัจจุบันออกให้สะอาด แล้วติดตั้ง v0.9.1 จาก package/source ที่กำลังเปิดอยู่ใหม่ทั้งหมด

## คำเตือนสำคัญ

การ clean reinstall จะลบ `.cogent` ตัวจริง ซึ่งมี Ticket, recovery state, evidence และ durable runtime state อยู่ด้วย

ค่าเริ่มต้นของสคริปต์จึง **backup ก่อนลบเสมอ** และเก็บ backup ไว้นอก workspace ที่:

```text
%LOCALAPPDATA%\CogentNexus\clean-reinstall-backups\<timestamp>
```

อย่าใช้ `-NoBackup` ถ้ายังต้องการเก็บ Ticket/evidence เก่า

## ลำดับที่สคริปต์ทำ

1. ตรวจ installer และ command ที่ต้องใช้
2. backup `.cogent`, skill, `cnx.cmd`, plugin directory, `AGENTS.md`, OpenClaw config และ plugin index ถ้ามี
3. ถ้ามี CNX ติดตั้งอยู่ ต้องรัน `cnx disable` สำเร็จก่อน เพื่อคืน OpenClaw ไป native/PASSTHROUGH
4. uninstall plugin ผ่าน OpenClaw
5. ลบ extension residue ที่อาจเหลือจาก linked/manual install
6. ลบเฉพาะ path ที่ CogentNexus เป็นเจ้าของ
7. เรียก `scripts/install.ps1` จาก package ปัจจุบัน
8. ตรวจ CNX status, Gateway และ plugin inventory หลังติดตั้ง

ถ้าคืน PASSTHROUGH ไม่สำเร็จ สคริปต์จะหยุดก่อนการลบแบบ destructive

## วิธีใช้

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\clean-reinstall.ps1
```

ถ้าตั้ง workspace เอง:

```powershell
.\scripts\clean-reinstall.ps1 -Workspace "D:\OpenClaw\workspace"
```

ถ้าตั้งใจไม่เก็บ backup จริง ๆ:

```powershell
.\scripts\clean-reinstall.ps1 -NoBackup
```

หลังจบควรตรวจ:

```powershell
cd "$HOME\.openclaw\workspace"
.\cnx.cmd status
openclaw gateway status
openclaw plugins list
```
