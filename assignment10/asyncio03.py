from random import random
import asyncio
import time

# คอร์รูทีนสำหรับสร้างงาน
async def producer (queue):

    print(F"{time.ctime()} Producer: Running")

    # สร้างงาน
    for i in range(10):

        # สร้างค่าหนึ่งค่า
        value = random()

        # หยุดเพื่อจำลองเวลาทำงาน
        await asyncio.sleep(value)

        # เพิ่มเข้าไปในคิว
        await queue.put(value)

    print(f"{time.ctime()} Producer: Done")

# คอร์รูทีนสำหรับผู้บริโภคเพื่อประมวลงาน
async def consumer (queue):

    print(f"{time.ctime()} Consumer: Running")

    # งานของผู้บริโภค
    while True:

        # ดึงงานหนึ่งหน่วยจากคิว
        item = await queue.get()

        # แสดงผล
        print(f"{time.ctime()} >get {item}")

        # หยุดขณะที่กำลังประมวลผล
        if item:
            await asyncio.sleep(item)

        # ระบุว่างานเสร็จแล้ว
        queue.task_done()

# คอร์รูทีนจุดเข้า (main)
async def main():

    # สร้างคิวที่ใช้ร่วมกัน
    queue = asyncio.Queue()

    # เริ่มผู้บริโภค
    consumer_tasks = asyncio.create_task(consumer (queue))

    # เริ่มผู้ผลิตและรอให้เสร็จ
    await asyncio.create_task(producer (queue))

    # รอให้รายการทั้งหมดถูกประมวลผลเสร็จ
    await queue.join()

# เริ่มโปรแกรม asyncio
asyncio.run(main())
