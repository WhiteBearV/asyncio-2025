import asyncio  # นำเข้าโมดูล asyncio เพื่อใช้เขียนโปรแกรมแบบ asynchronous
import time     # นำเข้าโมดูล time เพื่อเรียกใช้งานเวลา

def now():  # ฟังก์ชันช่วยเหลือเพื่อคืนค่าสตริงเวลาปัจจุบัน
    return time.ctime()  # คืนค่าสตริงเวลาปัจจุบันจาก time.ctime()

# ---------- Producers (ลูกค้า) ----------
async def customer(name, items, queue: asyncio.Queue):  # coroutine สำหรับลูกค้า รับชื่อ รายการ และคิว
    await queue.put((name, items))  # ใส่ข้อมูลลูกค้า (ชื่อ, รายการ) ลงในคิวแบบไม่บล็อก
    print(f"[{now()}] [{name}] finished shopping: {items}")  # พิมพ์ข้อความว่าเลิกช็อปแล้วพร้อมรายการ

# ---------- Consumers (แคชเชียร์) ----------
async def cashier(worker_name, per_item_sec: float, queue: asyncio.Queue, stats: dict):  # coroutine สำหรับแคชเชียร์
    try:
        while True:  # วนลูปไม่รู้จบเพื่อดึงลูกค้าจากคิวเข้ามาประมวลผล
            cust_name, items = await queue.get()  # รอและดึงงาน (ลูกค้า) ออกจากคิว
            print(f"[{now()}] [{worker_name}] processing {cust_name} with orders {items}")  # แจ้งเริ่มประมวลผลลูกค้า

            process_time = len(items) * per_item_sec  # คำนวณเวลาที่ใช้ตามจำนวนชิ้น * เวลาต่อชิ้น
            await asyncio.sleep(process_time)  # จำลองการทำงานโดยพักแบบ asynchronous เป็นเวลาที่คำนวณได้

            print(f"[{now()}] [{worker_name}] finished {cust_name}")  # แจ้งว่าทำงานเสร็จสำหรับลูกค้านี้
            queue.task_done()  # แจ้งว่าเอางานนี้ออกจากคิวเรียบร้อยแล้ว

            # อัปเดตสถิติ
            stats[worker_name]["count"] += 1  # เพิ่มจำนวนลูกค้าที่แคชเชียร์นี้ให้บริการ
            stats[worker_name]["time"] += process_time  # เพิ่มเวลาที่ใช้ให้กับสถิติของแคชเชียร์
    except asyncio.CancelledError:  # จับการยกเลิกงานแบบ asyncio
        raise  # ส่งต่อ CancelledError เพื่อให้การยกเลิกทำงานอย่างถูกต้อง

# ---------- Main ----------
async def main():  # coroutine หลักของโปรแกรม
    queue = asyncio.Queue()  # สร้างคิวแบบ asyncio สำหรับส่งงานระหว่างโปรดิวเซอร์และคอนซูเมอร์

    # เก็บสถิติของแคชเชียร์ทุกคน
    stats = {f"Cashier-{i+1}": {"count": 0, "time": 0} for i in range(2)}  # สร้าง dict เก็บสถิติเริ่มต้นสำหรับ 2 แคชเชียร์

    # สร้างแคชเชียร์ 20 คน (เพิ่มเวลาทีละ 1 วินาที/ชิ้น)
    cashier_tasks = [
        asyncio.create_task(cashier(f"Cashier-{i+1}", i+1, queue, stats))  # สร้าง task สำหรับแคชเชียร์แต่ละคน
        for i in range(2)  # ทำซ้ำสำหรับ 2 แคชเชียร์ (i=0..1)
    ]

    # สร้างลูกค้า 20 คน (สินค้า 2–5 ชิ้น)
    customer_tasks = [
        asyncio.create_task(
            customer(
                f"Customer-{i+1}",  # ชื่อของลูกค้า
                [f"Item{k+1}" for k in range((i % 4) + 1)],  # สร้างรายการสินค้าแบบไดนามิก จำนวน 1–4 ชิ้นตาม i % 4 + 1
                queue  # ส่งคิวให้ลูกค้าเพื่อใส่งาน
            )
        )
        for i in range(10)  # สร้างลูกค้า 10 คน (i=0..9)
    ]

    await asyncio.gather(*customer_tasks)  # รอให้ลูกค้าทั้งหมดใส่งานเข้าคิวเสร็จ
    await queue.join()  # รอจนกว่างานในคิวทั้งหมดจะถูกทำเครื่องหมายว่าเสร็จ (task_done เรียกครบ)

    # ยกเลิกงานของแคชเชียร์
    for i, t in enumerate(cashier_tasks):  # วนลูปผ่าน task ของแคชเชียร์
        t.cancel()  # ส่งการยกเลิกให้ task
        try:
            await t  # รอให้ task ยกเลิกเสร็จ (จะเกิด CancelledError)
        except asyncio.CancelledError:
            pass  # ปิดการยกเลิกเงียบ ๆ
        print(f"[{now()}] [Cashier-{i+1}] closed")  # แจ้งว่าแคชเชียร์ปิดทำการ

    # สรุปผลการทำงานของแคชเชียร์แต่ละคน
    print("\n===== Summary =====")  # พิมพ์หัวข้อสรุป
    for name, data in stats.items():  # วนลูปพิมพ์สถิติจาก dict
        print(f"{name}: รับลูกค้า {data['count']} คน, ใช้เวลา {data['time']} วินาที")  # พิมพ์สถิติเช่น จำนวนลูกค้าและเวลา

    print(f"[{now()}] [Main] Supermarket closed!")  # แจ้งปิดซูเปอร์มาร์เก็ต

asyncio.run(main())  # เรียกใช้งาน event loop และรัน coroutine หลักจนเสร็จ
