# ตัวอย่างการใช้ gather กับ tasks และ coroutines
import asyncio
 
# coroutine ที่ใช้สำหรับ task
async def task_coro(value):
    # แสดงข้อความ
    print(f'>task {value} กำลังทำงาน')
    # หน่วงเวลาเล็กน้อย
    await asyncio.sleep(1)
 
# coroutine ที่ใช้เป็นจุดเริ่มต้น
async def main():
    # แสดงข้อความ
    print('main กำลังเริ่มต้น')
    # สร้าง awaitables แบบผสม
    awaitables = [task_coro(0),
        asyncio.create_task(task_coro(1)),
        task_coro(2),
        asyncio.create_task(task_coro(3)),
        task_coro(4),]
    # จัดกลุ่มงาน
    _ = asyncio.gather(*awaitables)
    # รอเวลาสักพัก
    await asyncio.sleep(2)
    # แสดงข้อความ
    print('main เสร็จสิ้น')
 
# เริ่มโปรแกรม asyncio
asyncio.run(main())