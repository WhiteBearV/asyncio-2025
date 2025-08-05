# ตัวอย่างการยกเลิกทุก task ถ้ามี task ใด task หนึ่งล้มเหลว
import asyncio
 
# coroutine ที่ใช้สำหรับ task
async def task_coro(value):
    # แสดงข้อความ
    print(f'>task {value} executing')
    # หน่วงเวลาเล็กน้อย
    await asyncio.sleep(1)
    # ตรวจสอบว่า task นี้ควรล้มเหลวหรือไม่
    if value == 5:
        print(f'>task {value} failing')
        raise Exception('Something bad happened')
    # ถ้าไม่ล้มเหลว ให้หน่วงเวลาอีกครั้ง
    await asyncio.sleep(1)
    print(f'>task {value} done')
 
# coroutine ที่ใช้เป็นจุดเริ่มต้น
async def main():
    # สร้าง coroutine หลายตัว
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    # รัน coroutine ทั้งหมดเป็นกลุ่ม
    group = asyncio.gather(*tasks)
    # จัดการกรณีที่มี task ล้มเหลว
    try:
        # รอให้กลุ่มของ task ทำงานเสร็จ
        await group
    except Exception as e:
        # แสดงข้อความเมื่อเกิดข้อผิดพลาด
        print(f'A task failed with: {e}, canceling all tasks')
        # ยกเลิกทุก task
        for task in tasks:
            task.cancel()
    # รออีกสักพัก
    await asyncio.sleep(2)
 
# เริ่มโปรแกรม asyncio
asyncio.run(main())