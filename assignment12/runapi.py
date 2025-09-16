# runapi_fixed.py
import asyncio
import httpx
import json
from urllib.parse import urljoin

SERVERS = [
    "http://192.168.43.97:8000/",
    "http://172.20.49.54:8000/",
    "http://172.20.50.19:8000/",
]

ENDPOINTS = [
    "/students",
    "/analytics/group",
    "/analytics/year",
]

async def fetch_endpoint(client: httpx.AsyncClient, server: str, endpoint: str):
    url = urljoin(server, endpoint.lstrip("/"))
    try:
        resp = await client.get(url, timeout=5.0)
        resp.raise_for_status()
        data = resp.json()

        # จัดรูปผลลัพธ์ให้ตรง requirement
        if endpoint == "/students":
            result = {
                "server": server.rstrip("/"),
                "student_count": len(data) if isinstance(data, list) else 0,
            }
        elif endpoint == "/analytics/group":
            result = {
                "server": server.rstrip("/"),
                "group_analytics": data,
            }
        elif endpoint == "/analytics/year":
            result = {
                "server": server.rstrip("/"),
                "year_analytics": data,
            }
        else:
            result = {
                "server": server.rstrip("/"),
                "endpoint": endpoint,
                "data": data,
            }

        return {"ok": True, "result": result}

    except Exception as e:
        return {
            "ok": False,
            "result": {
                "server": server.rstrip("/"),
                "endpoint": endpoint,
                "error": str(e),
            }
        }

async def fetch_from_server(client: httpx.AsyncClient, server: str):
    tasks = [fetch_endpoint(client, server, ep) for ep in ENDPOINTS]
    return await asyncio.gather(*tasks)

async def main():
    async with httpx.AsyncClient() as client:
        server_tasks = [fetch_from_server(client, server) for server in SERVERS]
        all_results = await asyncio.gather(*server_tasks)

        # แสดงผลเป็น JSON สวย ๆ
        for server_results in all_results:
            for item in server_results:
                print(json.dumps(item["result"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
