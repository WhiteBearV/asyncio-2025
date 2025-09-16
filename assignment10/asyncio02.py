# ตัวอย่างการใช้ asyncio.Queue โดยไม่บล็อก
from random import random
import asyncio
# คอร์รูทีนสำหรับสร้างงาน

async def producer (queue):
    print('Producer: Running')
    # สร้างงาน

    for i in range(10):
        # สร้างค่า
        value = i
        # หน่วงเวลาเพื่อจำลองการทำงาน
        sleeptime = random()
        print(f"> Producer {value} sleep {sleeptime}")
        await asyncio.sleep(sleeptime)
        # เพิ่มลงคิว
        print(f"> Producer put {value}")
        await queue.put(value)
    # ส่งสัญญาณว่าเสร็จทั้งหมด
    await queue.put (None)
    print('Producer: Done')

# คอร์รูทีนสำหรับบริโภคงาน

async def consumer (queue):

    print('Consumer: Running')

    # บริโภคงาน

    while True:
        # ดึงงานหนึ่งหน่วยโดยไม่บล็อก
        try:
            item = queue.get_nowait()
        except asyncio.QueueEmpty:
            print('Consumer: got nothing, waiting a while...')
            await asyncio.sleep(0.5)
            continue
        # ตรวจสอบสัญญาณหยุด
        if item is None:
            break
        # รายงาน
        print(f'\t> Consumer got {item}')
        # เสร็จทั้งหมด
    print('Consumer: Done')
    # คอร์รูทีนจุดเริ่มต้น

async def main():

    # สร้างคิวที่ใช้ร่วมกัน
    queue = asyncio.Queue()

    # รันโปรดิวเซอร์และคอนซูเมอร์
    await asyncio.gather(producer (queue), consumer (queue))

# เริ่มโปรแกรม asyncio
asyncio.run(main())