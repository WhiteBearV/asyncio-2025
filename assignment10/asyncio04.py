import asyncio
import time

def now():
    return time.ctime()

# ---------- Producers (Customers) ----------
async def customer(name, items, queue: asyncio.Queue):
    # ลูกค้าหยิบของเสร็จ -> ส่งออเดอร์เข้าคิว
    await queue.put((name, items))
    print(f"[{now()}] [{name}] finished shopping: {items}")

# ---------- Consumers (Cashiers) ----------
async def cashier(worker_name, per_item_sec: float, queue: asyncio.Queue):
    try:
        while True:
            cust_name, items = await queue.get()       # รอคิวลูกค้า
            print(f"[{now()}] [{worker_name}] processing {cust_name} with orders {items}")
            await asyncio.sleep(len(items) * per_item_sec)  # เวลาคิดเงินตามจำนวนสินค้า
            print(f"[{now()}] [{worker_name}] finished {cust_name}")
            queue.task_done()
    except asyncio.CancelledError:
        # ถูกยกเลิกโดย main เพื่อปิดร้าน
        raise

# ---------- Main ----------
async def main():
    queue = asyncio.Queue()

    # สร้างและสตาร์ตแคชเชียร์ 2 คน
    c1 = asyncio.create_task(cashier("Cashier-1", 1.0, queue))  # 1 วินาที/สินค้า
    c2 = asyncio.create_task(cashier("Cashier-2", 2.0, queue))  # 2 วินาที/สินค้า

    # ลูกค้า 3 คน ส่งออเดอร์เข้าคิว (แต่ละคนเป็น 1 task)
    customers = [
        asyncio.create_task(customer("Alice",   ["Apple", "Banana", "Milk"], queue)),
        asyncio.create_task(customer("Bob",     ["Bread", "Cheese"],         queue)),
        asyncio.create_task(customer("Charlie", ["Eggs", "Juice", "Butter"], queue)),
    ]
    await asyncio.gather(*customers)      # ทุกลูกค้าส่งออเดอร์เข้าคิวแล้ว

    # รอให้แคชเชียร์คิดเงินลูกค้าทั้งหมดจนเสร็จ
    await queue.join()

    # ปิดแคชเชียร์อย่างปลอดภัย
    for t, name in [(c1, "Cashier-1"), (c2, "Cashier-2")]:
        t.cancel()
        try:
            await t
        except asyncio.CancelledError:
            pass
        print(f"[{now()}] [{name}] closed")

    print(f"[{now()}] [Main] Supermarket closed!")

asyncio.run(main())