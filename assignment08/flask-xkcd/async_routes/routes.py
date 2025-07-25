import asyncio
import random
import time
import httpx
from flask import Blueprint, render_template, current_app

# Create a Blueprint for async routes
async_bp = Blueprint("async", __name__)

# Async helper to fetch one XKCD
async def get_xkcd(client, url):
    response = await client.get(url)
    print(f"{time.ctime()} - get {url}")
    return response.json()

# Async helper to fetch multiple XKCD comics
async def get_xkcds():
    NUMBER_OF_XKCD = current_app.config.get("NUMBER_OF_XKCD", 5)  # fallback default = 5
    rand_list = [random.randint(0, 300) for _ in range(NUMBER_OF_XKCD)]

    xkcd_data = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for number in rand_list:
            url = f'https://xkcd.com/{number}/info.0.json'
            tasks.append(get_xkcd(client, url))
        xkcd_data = await asyncio.gather(*tasks)  # run all concurrently
    return xkcd_data

# Async route
@async_bp.route('/')
async def home():
    start_time = time.perf_counter()
    xkcds = await get_xkcds()
    end_time = time.perf_counter()

    print(f"{time.ctime()} - Get {len(xkcds)} xkcd. Time taken: {end_time-start_time:.2f} seconds")

    return render_template('sync.html',
                           title="XKCD Asynchronous Flask",
                           heading="XKCD Async Version",
                           xkcds=xkcds,
                           end_time=end_time,
                           start_time=start_time)
