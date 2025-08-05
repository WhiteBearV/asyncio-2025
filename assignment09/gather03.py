# ตัวอย่างการใช้ gather ที่คืนค่า exception
import asyncio
 
# coroutine ที่ใช้สำหรับ task
async def task_coro(value):
    # แสดงข้อความ
    print(f'>task {value} กำลังทำงาน')
    # หน่วงเวลาเล็กน้อย
    await asyncio.sleep(1)
    # ตรวจสอบข้อผิดพลาด
    if value == 0:
        raise Exception('เกิดข้อผิดพลาดบางอย่าง')
    return value
 
# coroutine ที่ใช้เป็นจุดเริ่มต้น
async def main():
    # แสดงข้อความ
    print('main กำลังเริ่มต้น')
    # สร้าง coroutine หลายตัว
    coros = [task_coro(i) for i in range(10)]
    # รัน task ทั้งหมด
    results = await asyncio.gather(*coros, return_exceptions=True)
    # แสดงผลลัพธ์
    print(results)
    # แสดงข้อความ
    print('main เสร็จสิ้น')
 
# เริ่มโปรแกรม asyncio
asyncio.run(main())