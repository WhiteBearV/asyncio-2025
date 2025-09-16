from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Service Registry")
registry: Dict[str, Dict] = {}

class ServiceInfo(BaseModel):
    name: str
    url: str
    city: str


@app.get("/services")
def get_services():
    return {"services": list(registry.values())}


@app.post("/register")
def register_service(service: ServiceInfo):
    if service.name in registry:
        raise HTTPException(status_code=400, detail="Service already registered")
    registry[service.name] = service.model_dump()

    return {"message": f"Service {service.name} registered successfully."}


@app.put("/update")
def update_service(service: ServiceInfo):
    if service.name not in registry:
        raise HTTPException(status_code=404, detail="Service not found")
    registry[service.name] = service.model_dump()

    return {"message": f"Service {service.name} updated successfully."}

@app.delete("/unregister/{name}")
def unregister_service(name: str):
    if name not in registry:
        raise HTTPException(status_code=404, detail="Service not found")
    del registry[name]
    return {"message": f"Service {name} unregistered successfully."}