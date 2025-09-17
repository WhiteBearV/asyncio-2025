from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# สร้าง FastAPI app สำหรับเป็น Service Registry
app = FastAPI(title="Service Registry")

# เก็บข้อมูล service ที่มาลงทะเบียนไว้ใน dictionary (in-memory)
# โครงสร้าง: { "ชื่อบริการ": {"name":..., "url":..., "city":...} }
registry: Dict[str, Dict] = {}

# กำหนด schema ของข้อมูล service ที่จะส่งเข้ามาลงทะเบียน
class ServiceInfo(BaseModel):
    name: str   # ชื่อของ service (เช่น ชื่อนักเรียน/รหัส)
    url: str    # URL endpoint ของ service (เช่น http://localhost:9001/weather)
    city: str   # เมืองหรือข้อมูลที่เกี่ยวข้องกับ service

# ------------------------------
# API: GET /services
# ใช้ดึงรายชื่อ service ทั้งหมดที่ถูกเก็บใน registry
# ------------------------------
@app.get("/services")
def get_services():
    return {"services": list(registry.values())}

# ------------------------------
# API: POST /register
# ใช้ลงทะเบียน service ใหม่เข้ามาใน registry
# ------------------------------
@app.post("/register")
def register_service(service: ServiceInfo):
    if service.name in registry:
        # ถ้ามีชื่อซ้ำแล้ว → ไม่ให้ลงทะเบียนใหม่
        raise HTTPException(status_code=400, detail="Service already registered")
    # ถ้าไม่ซ้ำ → เก็บข้อมูล service ลงใน registry
    registry[service.name] = service.model_dump()
    return {"message": f"Service {service.name} registered successfully."}

# ------------------------------
# API: PUT /update
# ใช้อัปเดตข้อมูลของ service ที่เคยลงทะเบียนไว้แล้ว
# ------------------------------
@app.put("/update")
def update_service(service: ServiceInfo):
    if service.name not in registry:
        # ถ้าไม่มีชื่อนี้ใน registry → แจ้งว่าไม่พบ
        raise HTTPException(status_code=404, detail="Service not found")
    # ถ้ามี → อัปเดตข้อมูลใหม่แทนที่
    registry[service.name] = service.model_dump()
    return {"message": f"Service {service.name} updated successfully."}

# ------------------------------
# API: DELETE /unregister/{name}
# ใช้ลบ service ออกจาก registry
# ------------------------------
@app.delete("/unregister/{name}")
def unregister_service(name: str):
    if name not in registry:
        # ถ้าไม่มีชื่อนี้ใน registry → แจ้งว่าไม่พบ
        raise HTTPException(status_code=404, detail="Service not found")
    # ลบข้อมูลออกจาก registry
    del registry[name]
    return {"message": f"Service {name} unregistered successfully."}
