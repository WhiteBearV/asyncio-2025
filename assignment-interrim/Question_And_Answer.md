# Question
1. ถ้าสร้าง asyncio.create_task(*tasks) ที่ไม่มี await ที่ main() เกิดอะไรบ้าง
   1. งานจะถูกสร้างและนำไปเข้าคิวใน event loop เพื่อรันเมื่อถึงคิว (ลักษณะคล้าย fire-and-forget) แต่ถ้าใช้ asyncio.run(main()) เมื่อ main() จบ event loop จะปิดและยกเลิก (cancel) งานที่ยังไม่เสร็จทันที ส่งผลให้ผลลัพธ์สูญหายและงานไม่เสร็จสมบูรณ์
   2. หากงานใดเกิด ข้อยกเว้น (exception) และไม่มีการ await เพื่อดึงผลลัพธ์ จะมีการแสดงคำเตือน Task exception was never retrieved เพราะ exception นั้นไม่ถูกอ่านหรือจัดการ
   3. ถ้าใช้ asyncio.create_task(*tasks) โดยไม่ await งานจะถูก schedule ให้รัน แต่ถ้า main() จบใน asyncio.run งานที่เหลือจะถูกยกเลิก และถ้ามีข้อยกเว้นจะขึ้นเตือน “Task exception was never retrieved” ควรเก็บ reference แล้ว await หรือใช้ asyncio.gather เพื่อรอและจัดการข้อยกเว้นอย่างเหมาะสม

2. ความแตกต่างระหว่าง asyncio.gather(*tasks) กับ asyncio.wait(tasks) คืออะไร
   1. gather จะรันงานทั้งหมดพร้อมกัน และเมื่อ await จะคืนค่าผลลัพธ์เป็นลิสต์ตามลำดับที่ส่ง args เข้าไป โดยจะคืนค่าหลังจากที่ทุกงานเสร็จสิ้นทั้งหมด
   2. ใน gather (ค่าเริ่มต้น) ถ้างานใดเกิดข้อยกเว้น งานที่เหลือจะถูกยกเลิกและ raise ทันที แต่สามารถกำหนด return_exceptions=True เพื่อรวบรวมข้อยกเว้นไว้ในลิสต์ผลลัพธ์แทนการยกเลิก
   3. หากต้องการให้ “แสดงผลทันทีที่งานใดงานหนึ่งเสร็จ” ควรใช้ wait(..., return_when=FIRST_COMPLETED) ซึ่งจะคืนผลของงานที่เสร็จก่อน ทำให้สามารถประมวลผลแบบ real-time ได้ (เช่นตัวอย่าง iot-wait.py)

3. สร้าง create_task() และ coroutine ของ http ให้อะไรต่างกัน
   1. การรันงาน: coroutine ของ HTTP (เช่นฟังก์ชัน async ที่ await client.get(...)) ถ้าถูก await ทีละตัวจะทำงานแบบลำดับ; ส่วน create_task(coro) จะห่อ coroutine ให้เป็น Task แล้วส่งให้ event loop จัดคิวรันทันที ทำให้ หลายคำขอ HTTP รันพร้อมกัน ได้จริง
   2. การควบคุมงาน: Task มีวงจรชีวิตและเมธอดควบคุม เช่น result(), exception(), cancel(), add_done_callback(...) จึงเหมาะเมื่ออยากตรวจสถานะ/ยกเลิก/ดึงผลของคำขอแต่ละรายการเป็นรายตัว
   3. การรอผลลัพธ์: สร้างหลายคำขอด้วย create_task() แล้ว
   -ใช้ await asyncio.gather(*tasks) เมื่อ “ต้องรอให้ครบทุก API ก่อนสรุป” (จะได้ลิสต์ผลตามลำดับที่ส่งเข้า)
   -ใช้ done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED) เมื่อ “ต้องอัปเดตทันทีที่คำขอใดเสร็จ” แล้ววนเก็บผลแบบ real-time  (ระวัง: ถ้าไม่ await สุดท้าย อาจเจอ cancel เมื่อ loop ปิด และเตือน “Task exception was never retrieved”)