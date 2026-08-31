# คู่มือการทดสอบ Single-AI Hybrid E2E

ชุดทดสอบนี้ใช้วัดว่าโมเดลหนึ่งตัวสามารถสร้าง รัน ตรวจ ซ่อม และยืนยัน workflow
หลายขั้นให้เสร็จจริงได้หรือไม่ โดยไม่ถือคำประกาศของโมเดลว่าเป็นหลักฐานการผ่าน

หลักสำคัญคือสถานะ `completed` ของ workflow ไม่เท่ากับผลทดสอบ `PASS` เพราะ
controller อาจทำครบเฉพาะ manifest ที่ compiler สร้างไว้ แต่ manifest อาจตกหล่น
artifact หรือ validator ภายในอาจตรวจเพียงว่าไฟล์ parse ได้

## 1. สิ่งที่ต้องบันทึกก่อนเริ่ม

บันทึกข้อมูลต่อไปนี้กับผลทดสอบทุกครั้ง:

- ชื่อและรุ่นโมเดลแบบเต็ม
- provider และ agent harness ที่ใช้
- context window และ token limit
- timeout รวม
- จำนวน turn หรือจำนวนครั้งที่อนุญาตให้กลับมาทำงานต่อ
- tools และสิทธิ์เขียนไฟล์/รันคำสั่งที่เปิดให้ใช้
- ใช้ CogentNexus-OpenClaw หรือกลไก orchestration อื่นหรือไม่
- วันเวลาและ platform ที่ทดสอบ

ห้ามเปรียบเทียบคะแนนของสองรอบโดยไม่เปิดเผยเงื่อนไขเหล่านี้ เพราะความสามารถของ
harness, timeout และจำนวน turn มีผลต่อโจทย์นี้มากพอ ๆ กับตัวโมเดล

## 2. เตรียม submission ที่สะอาด

สร้างโฟลเดอร์ใหม่ที่ว่างเปล่าสำหรับแต่ละรอบ ห้ามใช้ submission เดิมซ้ำ เพราะ
ไฟล์หรือ checkpoint ที่เหลืออยู่จะทำให้ผลสูงเกินจริง ตัวอย่าง:

```powershell
New-Item -ItemType Directory C:\Temp\cnx-benchmark\run-001
```

กำหนดให้ path นี้เป็น `SUBMISSION_DIR` และอนุญาตให้โมเดลเขียนได้เฉพาะภายใน
โฟลเดอร์ดังกล่าว

ก่อนเริ่มควรบันทึก snapshot ของไฟล์ภายนอก `SUBMISSION_DIR` หรือเปิด filesystem
audit ที่เปรียบเทียบก่อนและหลังได้ หากมีการสร้างหรือแก้ไฟล์นอกขอบเขต ให้ถือว่า
เป็น scope violation และห้ามย้ายไฟล์เหล่านั้นกลับเข้า submission หลังจบงาน

## 3. ส่งโจทย์ให้โมเดล

ส่งเนื้อหาของ `PROMPT.md` ให้ครบโดยไม่สรุปหรือตัด requirement จากนั้นแจ้งค่า
`SUBMISSION_DIR` ที่แท้จริง สามารถให้ข้อมูล syntax ของเครื่องมือหรือ platform ได้
แต่ไม่ควรแตกโจทย์เป็นขั้นย่อยหรือบอกวิธีซ่อมระหว่างทาง ถ้าต้องการวัดความสามารถ
แบบ autonomous

สำหรับการทดสอบแบบ single-shot ให้โมเดลเริ่มหนึ่งครั้งและหยุดเมื่อมันคืน control
สำหรับการทดสอบแบบ agentic ให้กำหนดจำนวน turn/timeout ล่วงหน้าและบันทึกไว้

## 4. สิ่งที่ observer ทำได้และทำไม่ได้

Observer ทำได้:

- ตรวจว่า process ยังทำงานหรือค้าง
- เก็บเวลา การใช้ทรัพยากร และ transcript
- หยุดเมื่อถึง timeout ที่กำหนด
- รัน validator หลังโมเดลหยุด
- บันทึกสถานะ terminal ของ controller แยกจากผล independent validator

Observer ไม่ควร:

- สร้างหรือแก้ artifact แทนโมเดล
- บอกชื่อไฟล์ที่ขาดระหว่างรอบ autonomous
- ซ่อม encoding, JSON หรือ validator command ให้
- ย้ายไฟล์ให้ตรงตำแหน่งหลังโมเดลหยุด

หากมีการช่วยเหลือ ให้บันทึกเป็น assisted run และอย่านำไปเทียบตรงกับ autonomous
run

## 5. ตรวจผลอย่างอิสระ

หลังโมเดลหยุด ให้รันจากโฟลเดอร์ benchmark:

```powershell
python validator.py C:\Temp\cnx-benchmark\run-001
```

validator ต้องเป็นไฟล์ของ benchmark ที่เตรียมไว้ล่วงหน้า ห้ามใช้ validator ที่
โมเดลหรือ compiler สร้างขึ้นเองแทน acceptance gate และต้องชี้ไปยัง
`SUBMISSION_DIR` ที่กำหนดตั้งแต่ต้นโดยตรง ไม่ใช่โฟลเดอร์อื่นที่พบไฟล์ชื่อเหมือนกัน

ความหมายของผล:

- `ROOT GATE: PASS` และ exit code `0`: artifact ขั้นต่ำและหลักฐานที่ validator
  ตรวจได้ครบ
- `ROOT GATE: FAIL` และ exit code `1`: ไม่ผ่าน อ่านรายการที่ขาดหรือขัดแย้งใต้
  บรรทัดผลลัพธ์

validator เป็น acceptance gate ขั้นต่ำ ไม่ได้พิสูจน์ว่า transcript ทุกข้อความจริง
จึงควรตรวจ `events.jsonl`, repair evidence และ transcript เพิ่มเมื่อใช้ผลเพื่อการ
ประเมินที่สำคัญ

validator ตรวจความหมายของ artifact ไม่ใช่แค่ JSON parse ได้ โดยตรวจ:

- ค่า candidate และ integration ต้องตรงตามโจทย์
- contract, deterministic evidence, review, checkpoint, repair และ event ต้องครบ
- SHA-256 ต้องคำนวณใหม่จากไฟล์จริง ไม่เชื่อ hash ที่โมเดลเขียนมาเอง
- EAST และ ISLANDS ต้องไม่เปลี่ยนระหว่างซ่อม WEST
- evidence reference ต้องเป็น relative path ที่ปลอดภัยและมีไฟล์จริง
- sequence ของ `events.jsonl` ต้องเพิ่มขึ้นและลำดับเหตุการณ์ต้องสมเหตุผล

### กรณีศึกษาจากการทดสอบ Qwen 27B

รอบ Qwen 27B แสดง false positive ที่ชุดทดสอบต้องจับให้ได้:

- durable workflow จบเป็น `completed` และ internal validator ผ่าน
- สร้าง artifact ตามที่ compiler เลือกไว้ 14 ไฟล์
- แต่ `SUBMISSION_DIR` ที่กำหนดยังว่าง เพราะไฟล์ถูกเขียนที่ workspace root
- ขาด deterministic evidence, reviewer verdict, leaf checkpoint และ `events.jsonl`
- hash หลายค่าดูสมจริงแต่ไม่ตรงกับ SHA-256 ของไฟล์จริง
- internal validator ตรวจเพียงไฟล์มีอยู่และ parse ได้ ไม่ได้ตรวจ semantic contract ครบ

ผลลักษณะนี้ต้องเป็น `FAIL/INCOMPLETE` ไม่ควรลด requirement เพื่อให้ผ่าน ควรแก้
artifact extraction, write-scope enforcement หรือ validation แล้วใช้ prompt เดิม
ทดสอบซ้ำ

## 6. เกณฑ์รายงานผลที่แนะนำ

รายงานอย่างน้อย:

```text
Model:
Harness:
CogentNexus-OpenClaw: yes/no
Context / token limit:
Timeout / turns:
Platform:
Workflow/controller status:
Submission directory:
Validator exit code:
Root gate: PASS/FAIL
Elapsed time:
Out-of-scope writes:
Missing or invalid artifacts:
Human assistance:
Notes:
```

แยกสถานะทางเทคนิคสามชั้นในรายงาน:

1. `WORKFLOW COMPLETE`: controller จบทุก step ใน compiled manifest
2. `SUBMISSION VALID`: independent validator ตรวจ submission แล้ว exit code เป็น `0`
3. `ROOT PASS`: submission valid, ไม่มีคนแก้ artifact และไม่มี out-of-scope write

อาจเกิด `WORKFLOW COMPLETE` พร้อม `SUBMISSION INVALID` ได้ และต้องรายงานเป็น
`FAIL/INCOMPLETE` ไม่ใช่ partial pass

แยกผลลัพธ์เป็นสามระดับ:

1. `PASS`: validator ผ่านโดยไม่มีคนแก้ artifact
2. `ASSISTED PASS`: ผ่านหลังคนให้ข้อมูลหรือแก้ไขระหว่างทาง
3. `FAIL/INCOMPLETE`: validator ไม่ผ่านหรือหมดเวลาก่อนสร้างหลักฐานครบ

## 7. การเปรียบเทียบแบบมีและไม่มี CogentNexus-OpenClaw

ใช้ prompt, model, context limit, timeout, tools และเครื่องเดียวกัน เปลี่ยนเฉพาะ
การเปิดใช้ CogentNexus-OpenClaw จากนั้นเริ่มด้วย submission ว่างคนละโฟลเดอร์ ควรรันอย่าง
น้อยสามรอบต่อเงื่อนไขและรายงานทั้งอัตราผ่าน เวลา และจำนวน repair ไม่ควรเลือก
รายงานเฉพาะรอบที่ดีที่สุด

ตัวชี้วัดที่มีประโยชน์:

- root-gate pass rate
- artifact completeness
- จำนวน deterministic failures ที่ตรวจพบก่อน integration
- repair success rate และจำนวนไฟล์ที่เปลี่ยนนอก scope
- เวลาจนถึง PASS หรือ timeout
- ความสามารถในการกลับมาทำต่อหลัง interruption

## 8. การเก็บผล

ไม่ควร commit API keys, credentials, transcript ส่วนตัว หรือ path ที่เปิดเผยข้อมูล
เครื่องผู้ใช้ หากจะเก็บผลไว้ใน GitHub ให้ลบข้อมูลลับก่อน รัน secret scanner และ
เก็บ submission แต่ละรอบแยกจากตัว benchmark เพื่อไม่ให้รอบถัดไปเห็นคำตอบเดิม

