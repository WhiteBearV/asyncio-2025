# student_service.py
import os
import httpx
import folium
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# โหลดค่าตัวแปรจากไฟล์ .env มาเก็บไว้ใน Environment Variables
load_dotenv()

# สร้าง FastAPI แอป สำหรับบริการ Student Weather
app = FastAPI(title="Student Weather Service")

# โหลดค่าจาก .env เพื่อใช้เป็น config ของ service
OWM_API_KEY = os.getenv("OWM_API_KEY")          # API key ของ OpenWeatherMap
CITY = os.getenv("CITY")                        # ชื่อเมือง
LAT = float(os.getenv("LAT"))                   # latitude ของเมือง
LON = float(os.getenv("LON"))                   # longitude ของเมือง
SERVICE_REGISTRY_URL = os.getenv("SERVICE_REGISTRY_URL")  # URL ของ Service Registry
STUDENT_NAME = os.getenv("STUDENT_NAME")        # ชื่อ/รหัสนักเรียน
SELF_URL = os.getenv("SELF_URL")                # URL endpoint ของ service ตัวเอง

# -------------------------
# Model ข้อมูลสำหรับลงทะเบียนกับ Registry
# -------------------------
class RegisterInfo(BaseModel):
    name: str
    url: str
    city: str

# -------------------------
# 1. Endpoint: /weather
# ดึงข้อมูลอากาศของเมืองตัวเองจาก OpenWeatherMap API
# -------------------------
@app.get("/weather")
async def get_weather():
    async with httpx.AsyncClient() as client:
        # สร้าง URL ไปยัง OWM API (ใช้ metric = องศาเซลเซียส, lang=th)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OWM_API_KEY}&units=metric&lang=th"
        r = await client.get(url)

    # ถ้าดึงไม่สำเร็จ → คืน error
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail="Failed to fetch weather data")

    # แปลงผลลัพธ์เป็น JSON และเลือก field ที่ต้องการ
    data = r.json()
    return {
        "student": STUDENT_NAME,
        "city": CITY,
        "temperature": data["main"]["temp"],
        "weather": data["weather"][0]["description"]
    }

# -------------------------
# 2. Endpoint: /register
# สมัครตัวเองเข้ากับ Service Registry
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
# 3. Endpoint: /update_self
# อัปเดตข้อมูลตัวเองใน Registry (ใช้กรณีเปลี่ยนค่า เช่น เมืองหรือ URL)
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
# 4. Endpoint: /unregister_self
# ถอนตัวเองออกจาก Registry
# -------------------------
@app.delete("/unregister_self")
async def unregister_self():
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{SERVICE_REGISTRY_URL}/unregister/{STUDENT_NAME}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()

# -------------------------
# 5. Endpoint: /aggregate
# ดึงข้อมูลจาก service เพื่อน ๆ ทั้งหมดใน Registry
# แล้วรวมผลลัพธ์ + สร้างแผนที่ Folium พร้อม marker
# -------------------------
@app.get("/aggregate")
async def aggregate_services():
    async with httpx.AsyncClient() as client:
        # ดึงรายชื่อ services ที่ลงทะเบียนจาก Registry
        r = await client.get(f"{SERVICE_REGISTRY_URL}/services")
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail="Failed to fetch registry services")

    services = r.json()["services"]

    # สร้างแผนที่ Folium เริ่มต้น (โฟกัสประเทศไทย)
    fmap = folium.Map(location=[15.8700, 100.9925], zoom_start=6)

    results = []
    async with httpx.AsyncClient() as client:
        for svc in services:
            try:
                # เรียก /weather ของ service แต่ละตัว
                resp = await client.get(svc["url"])
                if resp.status_code == 200:
                    data = resp.json()
                    results.append(data)

                    # ใส่ marker ลงบนแผนที่
                    # (ตอนนี้ยังใช้ lat/lon จาก .env ตัวเอง → marker ทุกคนซ้อนกัน)
                    folium.Marker(
                        location=[LAT, LON],
                        popup=f"{svc['city']} ({data['temperature']}°C, {data['weather']})",
                        tooltip=svc["name"]
                    ).add_to(fmap)
            except Exception as e:
                results.append({"error": str(e)})

    # เซฟแผนที่เป็นไฟล์ HTML
    fmap.save("aggregate_map.html")

    return {"services_data": results, "map_file": "aggregate_map.html"}
