# file: rocketapp.py

from fastapi import FastAPI, HTTPException
import asyncio
import random

app = FastAPI(title="Asynchronous Rocket Launcher")

# เก็บ task ของจรวด (optional, เผื่อ debug)
rockets = []

async def launch_rocket(student_id: str, time_to_target: float):
    """จำลองการบินของจรวด"""
    print(f"Rocket {student_id} launched! ETA: {time_to_target:.2f} seconds")
    await asyncio.sleep(time_to_target)
    print(f"Rocket {student_id} reached destination after {time_to_target:.2f} seconds")

@app.get("/fire/{student_id}")
async def fire_rocket(student_id: str):
    # ตรวจสอบ student_id
    if not (student_id.isdigit() and len(student_id) == 10):
        raise HTTPException(status_code=400, detail="student_id must be 10 digits")

    # random เวลาบิน 1–2 วินาที
    time_to_target = round(random.uniform(1, 2), 2)

    # สร้าง background task
    task = asyncio.create_task(launch_rocket(student_id, time_to_target))
    rockets.append(task)

    # ส่ง response ทันที
    return {
        "message": f"Rocket {student_id} fired!",
        "time_to_target": time_to_target
    }
