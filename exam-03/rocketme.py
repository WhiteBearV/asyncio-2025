import time
import asyncio
from fastapi import FastAPI
import httpx

student_id = "6610301006"
app = FastAPI(title=f"Rocket Launcher {student_id}")

@app.get("/fire_rocket")
async def fire_rocket(name: str, t0: float):
    async with httpx.AsyncClient() as client:
        url = f"http://172.16.2.117:8088/fire/{student_id}"
        r = await client.get(url)
        data = r.json()

        time_to_target = data.get("time_to_target", 0.0)
        start_time = time.perf_counter() - t0
        end_time = start_time + time_to_target

        return {
            "name": name,
            "start_time": start_time,
            "time_to_target": time_to_target,
            "end_time": end_time
        }

async def main():
    t0 = time.perf_counter()
    print("Rocket prepare to launch ...")

    # ยิง rocket 3 ลูกพร้อมกัน
    tasks = [
        asyncio.create_task(fire_rocket("Rocket-1", t0)),
        asyncio.create_task(fire_rocket("Rocket-2", t0)),
        asyncio.create_task(fire_rocket("Rocket-3", t0)),
    ]

    # รอให้ทุก task เสร็จ
    results = await asyncio.gather(*tasks)

    # เรียงตามเวลาที่ถึงเป้าหมาย
    results.sort(key=lambda r: r["end_time"])

    print("Rockets fired:")
    for r in results:
        print(f"{r['name']} | start_time: {r['start_time']:.2f} sec "
              f"| time_to_target: {r['time_to_target']:.2f} sec "
              f"| end_time: {r['end_time']:.2f} sec")

    # เวลารวมทั้งหมด
    t_total = max(r["end_time"] for r in results)
    print(f"\nTotal time for all rockets: {t_total:.2f} sec")

if __name__ == "__main__":
    asyncio.run(main())

