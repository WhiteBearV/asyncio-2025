# โจทย์ Asynchronous Task Simulation
# โจทย์
# เขียนโปรแกรมจำลอง Worker Tasks แบบอะซิงโครนัส
# 1. มี worker 3 ตัว (Worker-1, Worker-2, Worker-3)
# 2. แต่ละ worker จะทำงานวนลูป 5 รอบ
# 3. แต่ละรอบรอ 1 วินาที (await asyncio.sleep(1)) และพิมพ์ "Worker-{id} is working round {i}"
# 4. หลังทำครบ 5 รอบ → พิมพ์ "Worker-{id} finished"
# 5. โปรแกรมต้องรัน ทุก worker พร้อมกัน โดยไม่ block
# 6. นักศึกษาต้องเติม ส่วนการสร้าง task และรอให้ทุก worker เสร็จ

# Result:
# Worker-1 is working round 1
# Worker-2 is working round 1
# Worker-3 is working round 1
# Worker-1 is working round 2
# Worker-2 is working round 2
# Worker-3 is working round 2
# Worker-1 is working round 3
# Worker-2 is working round 3
# Worker-3 is working round 3
# Worker-1 is working round 4
# Worker-2 is working round 4
# Worker-3 is working round 4
# Worker-1 is working round 5
# Worker-2 is working round 5
# Worker-3 is working round 5
# Worker-1 finished
# Worker-2 finished
# Worker-3 finished

import asyncio

async def worker(id: int, queue: asyncio.Queue):
    for i in range(1, 6):
        print(f"Worker-{id} is working round {i}")
        await asyncio.sleep(1)
    print(f"Worker-{id} finished")

async def main():
    queue = asyncio.Queue()  # สร้างคิวแบบ asyncio สำหรับส่งงานระหว่างโปรดิวเซอร์และคอนซูเมอร์

    tasks = [        
        asyncio.create_task(worker({i+1},queue))  # สร้าง task สำหรับแคชเชียร์แต่ละคน
        for i in range(3)  # ทำซ้ำสำหรับ 2 แคชเชียร์ (i=0..1)]
    ]





    await asyncio.gather(*tasks)  # รอให้ลูกค้าทั้งหมดใส่งานเข้าคิวเสร็จ
    await queue.join()  # รอจนกว่างานในคิวทั้งหมดจะถูกทำเครื่องหมายว่าเสร็จ (task_done เรียกครบ)
    # TODO: สร้าง asyncio task สำหรับ worker 3 ตัว
    # hint: ใช้ asyncio.create_task(worker(id))
    
    # TODO: รอให้ทุก task เสร็จ
    # hint: ใช้ await หรือ asyncio.gather
    pass

asyncio.run(main())
