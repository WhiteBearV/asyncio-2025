import asyncio
import random
import time
import httpx
from flask import Blueprint, render_template, current_app

# สร้าง Blueprint สำหรับ route แบบ async
async_bp = Blueprint("async", __name__)

# ฟังก์ชัน async สำหรับดึงข้อมูลโปเกมอนตัวเดียว
async def get_pokemon(client, url):
    response = await client.get(url)
    print(f"{time.ctime()} - GET {url}")
    return response.json()

# ฟังก์ชัน async สำหรับดึงข้อมูลโปเกมอนหลายตัวพร้อมกัน
async def get_pokemons():
    NUMBER_OF_POKEMON = current_app.config.get("NUMBER_OF_POKEMON", 5)  # จำนวนโปเกมอนที่ต้องการสุ่ม
    rand_list = [random.randint(1, 151) for _ in range(NUMBER_OF_POKEMON)]  # สุ่มหมายเลขโปเกมอนจาก Gen 1

    async with httpx.AsyncClient() as client:
        tasks = []
        for number in rand_list:
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'  # สร้าง URL สำหรับแต่ละโปเกมอน
            tasks.append(get_pokemon(client, url))  # เพิ่ม task สำหรับดึงข้อมูลแต่ละตัว
        pokemons = await asyncio.gather(*tasks)  # รันทุก task พร้อมกันแบบ async
    return pokemons

# route แบบ async สำหรับหน้าแรก
@async_bp.route('/')
async def home():
    start_time = time.perf_counter()  # เวลาที่เริ่มต้น
    pokemons = await get_pokemons()   # ดึงข้อมูลโปเกมอนแบบ async
    end_time = time.perf_counter()    # เวลาที่สิ้นสุด

    print(f"{time.ctime()} - Got {len(pokemons)} Pokémon. Time taken: {end_time - start_time:.2f} seconds")

    # ส่งข้อมูลไปยัง template เพื่อแสดงผล
    return render_template('sync.html',
                           title="Pokémon Async Flask",
                           heading="Random Pokémon (Async)",
                           pokemons=pokemons,
                           end_time=end_time,
                           start_time=start_time)
