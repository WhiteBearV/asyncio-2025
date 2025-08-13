import asyncio, time, random
async def get_temperature():

    await asyncio.sleep (random.uniform(0.5, 2.0))
    return f"{time.ctime()} Temp: 30°C"

async def get_humidity():

    await asyncio.sleep (random.uniform(0.5, 2.0))
    return f"{time.ctime()} Humidity: 60%"

async def get_weather_api():

    await asyncio.sleep(random.uniform(0.5, 2.0))
    return f"{time.ctime()} Weather: Sunny"


async def main():
    start = time.time()
    temp_task = asyncio.create_task(get_temperature())
    humidity_task = asyncio.create_task(get_humidity())
    weather_task = asyncio.create_task(get_weather_api())

    done, pending = await asyncio.wait(
        [temp_task, humidity_task, weather_task],
        return_when=asyncio.ALL_COMPLETED
    )

    for task in done:
        print(task.result())
    end = time.time()
    print(f"Total time taken: {end - start:.2f} seconds")

asyncio.run(main())
