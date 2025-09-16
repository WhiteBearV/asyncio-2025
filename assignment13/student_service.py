# student_service.py
import os
import httpx
import folium
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()  # โหลดค่าจาก .env

app = FastAPI(title="Student Weather Service")

# โหลดค่าจาก .env
OWM_API_KEY = os.getenv("OWM_API_KEY")
CITY = os.getenv("CITY")
LAT = float(os.getenv("LAT"))
LON = float(os.getenv("LON"))
SERVICE_REGISTRY_URL = os.getenv("SERVICE_REGISTRY_URL")
STUDENT_NAME = os.getenv("STUDENT_NAME")
SELF_URL = os.getenv("SELF_URL")


# -------------------------
# Models
# -------------------------
class RegisterInfo(BaseModel):
    name: str
    url: str
    city: str


# -------------------------
# 1. ดึงข้อมูลอากาศของเมืองตัวเอง
# -------------------------
@app.get("/weather")
async def get_weather():
    async with httpx.AsyncClient() as client:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OWM_API_KEY}&units=metric&lang=th"
        r = await client.get(url)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail="Failed to fetch weather data")

    data = r.json()
    return {
        "student": STUDENT_NAME,
        "city": CITY,
        "temperature": data["main"]["temp"],
        "weather": data["weather"][0]["description"]
    }


# -------------------------
# 2. สมัครตัวเองเข้ากับ Service Registry
# -------------------------
@app.post("/register")
async def register_self():
    info = {
        "name": STUDENT_NAME,
        "url": SELF_URL,
        "city": CITY
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{SERVICE_REGISTRY_URL}/register", json=info)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# -------------------------
# 3. อัปเดตข้อมูลตัวเอง
# -------------------------
@app.put("/update_self")
async def update_self():
    info = {
        "name": STUDENT_NAME,
        "url": SELF_URL,
        "city": CITY
    }
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{SERVICE_REGISTRY_URL}/update", json=info)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# -------------------------
# 4. ถอนตัวเองออกจาก Registry
# -------------------------
@app.delete("/unregister_self")
async def unregister_self():
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{SERVICE_REGISTRY_URL}/unregister/{STUDENT_NAME}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# -------------------------
# 5. Aggregate เพื่อนทั้งหมด + แสดงบน Folium Map
# -------------------------
@app.get("/aggregate")
async def aggregate_services():
    async with httpx.AsyncClient() as client:
        # ดึงรายชื่อ services จาก Registry
        r = await client.get(f"{SERVICE_REGISTRY_URL}/services")
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail="Failed to fetch registry services")

    services = r.json()["services"]

    # สร้างแผนที่เริ่มต้น (โฟกัสประเทศไทย)
    fmap = folium.Map(location=[15.8700, 100.9925], zoom_start=6)

    results = []
    async with httpx.AsyncClient() as client:
        for svc in services:
            try:
                resp = await client.get(svc["url"])
                if resp.status_code == 200:
                    data = resp.json()
                    results.append(data)

                    # ใส่ marker ลงแผนที่
                    folium.Marker(
                        location=[float(os.getenv("LAT")), float(os.getenv("LON"))],
                        popup=f"{svc['city']} ({data['temperature']}°C, {data['weather']})",
                        tooltip=svc["name"]
                    ).add_to(fmap)
            except Exception as e:
                results.append({"error": str(e)})

    # บันทึกเป็น HTML
    fmap.save("aggregate_map.html")

    return {"services_data": results, "map_file": "aggregate_map.html"}