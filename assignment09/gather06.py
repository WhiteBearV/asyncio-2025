# ตัวอย่างการยกเลิกทุก task ถ้ามี task ใด task หนึ่งล้มเหลว
import asyncio
 
# ยกเลิกทุก task ยกเว้น task ปัจจุบัน
def cancel_all_tasks():
    # รับทุก task ที่กำลังทำงานอยู่
    tasks = asyncio.all_tasks()
    # รับ task ปัจจุบัน
    current = asyncio.current_task()
    # ลบ task ปัจจุบันออกจากทุก task
    tasks.remove(current)
    # ยกเลิกทุก task ที่เหลืออยู่
    for task in tasks:
        task.cancel()
 
# coroutine ที่ใช้สำหรับ task
async def task_coro(value):
    # แสดงข้อความ
    print(f'>task {value} executing')
    # หน่วงเวลาเล็กน้อย
    await asyncio.sleep(1)
    # ตรวจสอบว่า task นี้ควรล้มเหลวหรือไม่
    if value == 5:
        print(f'>task {value} failing')
        raise Exception('เกิดข้อผิดพลาดบางอย่าง')
    # ถ้าไม่ล้มเหลว ให้หน่วงเวลาอีกครั้ง
    await asyncio.sleep(1)
    print(f'>task {value} done')
    return value
 
# coroutine ที่ใช้เป็นจุดเริ่มต้น
async def main():
    # สร้าง coroutine หลายตัว
    coros = [task_coro(i) for i in range(10)]
    # รัน coroutine ทั้งหมดเป็นกลุ่ม
    group = asyncio.gather(*coros)
    # จัดการกรณีที่มี task ล้มเหลว
    try:
        # รอให้กลุ่ม task ทำงานเสร็จ
        await group
    except Exception as e:
        # แสดงข้อความเมื่อเกิดข้อผิดพลาด
        print(f'A task failed with: {e}, canceling all tasks')
        # ยกเลิกทุก task
        cancel_all_tasks()
    # หน่วงเวลาอีกเล็กน้อย
    await asyncio.sleep(2)
 
# เริ่มโปรแกรม asyncio
asyncio.run(main())