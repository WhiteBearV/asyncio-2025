import time
from fastapi import FastAPI, HTTPException
import httpx


student_id = "6610301006"
app = FastAPI(title=f"Rocket Launcher {student_id}")

@app.get("/fire_rocket")
async def fire_rocket(name: str, t0: float):
    async with httpx.AsyncClient() as client:
        url = f"http://172.16.2.117:8088/fire/{student_id}"
        r = await client.get(url)
        start_time = time.perf_counter() - t0  # เวลาเริ่มสัมพัทธ์
    """
    TODO:
    - ส่ง GET request ไปยัง rocketapp ที่ path /fire/{student_id}
    - อ่านค่า time_to_target จาก response
    - return dict ที่มี:
        {
            "name": name,
            "start_time": start_time,
            "time_to_target": time_to_target,
            "end_time": end_time
        }
    """
    pass

async def main():
    t0 = time.perf_counter()  # เวลาเริ่มของชุด rockets

    print("Rocket prepare to launch ...")  # แสดงตอนเริ่ม main

    # TODO: สร้าง task ยิง rocket 3 ลูกพร้อมกัน
    tasks = []

    # TODO: รอให้ทุก task เสร็จและเก็บผลลัพธ์ตามลำดับ task
    results = []

    # TODO: แสดงผล start_time, time_to_target, end_time ของแต่ละ rocket ตามลำดับ task
    for r in results:
        pass  # แสดงผล rocket

    # TODO: แสดงเวลารวมทั้งหมดตั้งแต่ยิงลูกแรกจนลูกสุดท้ายถึงจุดหมาย
    t_total = 0  # คำนวณ max end_time
    print(f"\nTotal time for all rockets: {t_total:.2f} sec")

