# ตัวอย่างการใช้ gather สำหรับ coroutine หลายตัวที่คืนค่า
import asyncio
 
# coroutine ที่ใช้สำหรับ task
async def task_coro(value):
    # แสดงข้อความ
    print(f'>task {value} กำลังทำงาน')
    # หน่วงเวลาเล็กน้อย
    await asyncio.sleep(1)
    # คืนค่า
    return value * 10
 
# coroutine ที่ใช้เป็นจุดเริ่มต้น
async def main():
    # แสดงข้อความ
    print('main เริ่มต้น')
    # สร้าง task หลายตัว
    tasks = [task_coro(i) for i in range(10)]
    # รัน task ทั้งหมด
    values = await asyncio.gather(*tasks)
    # แสดงค่าที่ได้
    print(values)
    # แสดงข้อความ
    print('main เสร็จสิ้น')
 
# เริ่มโปรแกรม asyncio
asyncio.run(main())