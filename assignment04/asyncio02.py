# Create 1 Task with High-Level API

import asyncio

async def do_something():

    print("Start working...")

    await asyncio.sleep(2)

    print("Work is done!")

async def main():

    task = asyncio.create_task(do_something())

    await task # Waiting for task to complete

asyncio.run(main())