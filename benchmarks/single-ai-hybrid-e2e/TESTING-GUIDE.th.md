# คู่มือการทดสอบ Single-AI Hybrid E2E

ชุดทดสอบนี้ใช้วัดว่าโมเดลหนึ่งตัวสามารถสร้าง รัน ตรวจ ซ่อม และยืนยัน workflow
หลายขั้นให้เสร็จจริงได้หรือไม่ โดยไม่ถือคำประกาศของโมเดลว่าเป็นหลักฐานการผ่าน

## 1. สิ่งที่ต้องบันทึกก่อนเริ่ม

บันทึกข้อมูลต่อไปนี้กับผลทดสอบทุกครั้ง:

- ชื่อและรุ่นโมเดลแบบเต็ม
- provider และ agent harness ที่ใช้
- context window และ token limit
- timeout รวม
- จำนวน turn หรือจำนวนครั้งที่อนุญาตให้กลับมาทำงานต่อ
- tools และสิทธิ์เขียนไฟล์/รันคำสั่งที่เปิดให้ใช้
- ใช้ CogentNexus หรือกลไก orchestration อื่นหรือไม่
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

ความหมายของผล:

- `ROOT GATE: PASS` และ exit code `0`: artifact ขั้นต่ำและหลักฐานที่ validator
  ตรวจได้ครบ
- `ROOT GATE: FAIL` และ exit code `1`: ไม่ผ่าน อ่านรายการที่ขาดหรือขัดแย้งใต้
  บรรทัดผลลัพธ์

validator เป็น acceptance gate ขั้นต่ำ ไม่ได้พิสูจน์ว่า transcript ทุกข้อความจริง
จึงควรตรวจ `events.jsonl`, repair evidence และ transcript เพิ่มเมื่อใช้ผลเพื่อการ
ประเมินที่สำคัญ

## 6. เกณฑ์รายงานผลที่แนะนำ

รายงานอย่างน้อย:

```text
Model:
Harness:
CogentNexus: yes/no
Context / token limit:
Timeout / turns:
Platform:
Validator exit code:
Root gate: PASS/FAIL
Elapsed time:
Missing or invalid artifacts:
Human assistance:
Notes:
```

แยกผลลัพธ์เป็นสามระดับ:

1. `PASS`: validator ผ่านโดยไม่มีคนแก้ artifact
2. `ASSISTED PASS`: ผ่านหลังคนให้ข้อมูลหรือแก้ไขระหว่างทาง
3. `FAIL/INCOMPLETE`: validator ไม่ผ่านหรือหมดเวลาก่อนสร้างหลักฐานครบ

## 7. การเปรียบเทียบแบบมีและไม่มี CogentNexus

ใช้ prompt, model, context limit, timeout, tools และเครื่องเดียวกัน เปลี่ยนเฉพาะ
การเปิดใช้ CogentNexus จากนั้นเริ่มด้วย submission ว่างคนละโฟลเดอร์ ควรรันอย่าง
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

