# ตัวอย่างการใช้ asyncio.Queue
from random import random
import asyncio

# คอรูทีนสำหรับสร้างงาน

async def producer (queue):
    print('Producer: Running')
# สร้างงาน
    for i in range(10):

# สร้างค่าหนึ่งค่า

        value = i
        # หยุดชั่วคราวเพื่อจำลองการทำงาน
        await asyncio.sleep(random())
        # เพิ่มเข้าไปในคิว
        print(f"> Producer put {value}")
        await queue.put(value)

    # ส่งสัญญาณว่าทำงานเสร็จทั้งหมด
    await queue.put(None)
    print('Producer: Done')

# คอรูทีนสำหรับรับงาน

async def consumer (queue):

    print('Consumer: Running')

    # รับงานจากคิว

    while True:
        # ดึงงานหนึ่งชิ้น
        item = await queue.get()
        # ตรวจสอบสัญญาณหยุด
        if item is None:
            break
        # แสดงผล
        print(f'\t> Consumer got {item}')
        # ทำงานเสร็จ
        print('Consumer: Done')
        # จุดเริ่มต้นของคอรูทีน

async def main():
    # สร้างคิวที่ใช้ร่วมกัน
    queue = asyncio.Queue()
    # รันโปรดิวเซอร์และคอนซูเมอร์
    await asyncio.gather (producer (queue), consumer (queue))
    # เริ่มโปรแกรม asyncio

asyncio.run(main())