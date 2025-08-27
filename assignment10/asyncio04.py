import asyncio
import time

def now():
    return time.ctime()

# ---------- Producers (ลูกค้า) ----------
async def customer(name, items, queue: asyncio.Queue):
    await queue.put((name, items))
    print(f"[{now()}] [{name}] finished shopping: {items}")

# ---------- Consumers (แคชเชียร์) ----------
async def cashier(worker_name, per_item_sec: float, queue: asyncio.Queue, stats: dict):
    try:
        while True:
            cust_name, items = await queue.get()
            print(f"[{now()}] [{worker_name}] processing {cust_name} with orders {items}")

            process_time = len(items) * per_item_sec
            await asyncio.sleep(process_time)

            print(f"[{now()}] [{worker_name}] finished {cust_name}")
            queue.task_done()

            # อัปเดตสถิติ
            stats[worker_name]["count"] += 1
            stats[worker_name]["time"] += process_time
    except asyncio.CancelledError:
        raise

# ---------- Main ----------
async def main():
    queue = asyncio.Queue()

    # เก็บสถิติของแคชเชียร์ทุกคน
    stats = {f"Cashier-{i+1}": {"count": 0, "time": 0} for i in range(2)}

    # สร้างแคชเชียร์ 20 คน (เพิ่มเวลาทีละ 1 วินาที/ชิ้น)
    cashier_tasks = [
        asyncio.create_task(cashier(f"Cashier-{i+1}", i+1, queue, stats))
        for i in range(2)
    ]

    # สร้างลูกค้า 20 คน (สินค้า 2–5 ชิ้น)
    customer_tasks = [
        asyncio.create_task(
            customer(
                f"Customer-{i+1}",
                [f"Item{k+1}" for k in range((i % 4) + 1)],
                queue
            )
        )
        for i in range(10)
    ]

    await asyncio.gather(*customer_tasks)
    await queue.join()

    # ยกเลิกงานของแคชเชียร์
    for i, t in enumerate(cashier_tasks):
        t.cancel()
        try:
            await t
        except asyncio.CancelledError:
            pass
        print(f"[{now()}] [Cashier-{i+1}] closed")

    # สรุปผลการทำงานของแคชเชียร์แต่ละคน
    print("\n===== Summary =====")
    for name, data in stats.items():
        print(f"{name}: รับลูกค้า {data['count']} คน, ใช้เวลา {data['time']} วินาที")

    print(f"[{now()}] [Main] Supermarket closed!")

asyncio.run(main())
