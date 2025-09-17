# Hint:
# แก้โค้ดให้สามารถรัน หลาย task พร้อมกัน ได้ถูกต้อง
# Result:
# Processing data
# Processing data
# Processing data
# Processing data
# Processing data

import asyncio

async def fetch_data():
    await asyncio.sleep(2)
    return "data"

async def process():
    data = await fetch_data()
    print("Processing", data)


async def main():

    started_tasks = [asyncio.create_task (process()) for i in range(5)]
    await asyncio.sleep(0.1)
    for task in started_tasks:
        await task

# start the asyncio program

asyncio.run(main())

