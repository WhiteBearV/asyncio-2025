# ตัวอย่างการใช้ gather ที่มีการยกเลิกหนึ่ง task พร้อมคืนค่า exception
import asyncio
 
# coroutine ที่ใช้สำหรับ task
async def task_coro(value, friend):
    # แสดงข้อความ
    print(f'>task {value} กำลังทำงาน')
    # ยกเลิก task เพื่อน
    if friend:
        friend.cancel()
    # หน่วงเวลาเล็กน้อย
    await asyncio.sleep(1)
 
# coroutine ที่ใช้เป็นจุดเริ่มต้น
async def main():
    # แสดงข้อความ
    print('main กำลังเริ่มต้น')
    # สร้างหลาย task
    task0 = asyncio.create_task(task_coro(0, None))
    task1 = asyncio.create_task(task_coro(1, task0))
    # รัน task ทั้งหมด
    results = await asyncio.gather(task0, task1, return_exceptions=True)
    # แสดงผลลัพธ์
    print(results)
    # แสดงข้อความ
    print('main เสร็จสิ้น')
 
# เริ่มโปรแกรม asyncio
asyncio.run(main())