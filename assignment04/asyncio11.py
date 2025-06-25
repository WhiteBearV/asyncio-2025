# task name

import asyncio

async def simple_task():

    await asyncio.sleep(1)

async def main():

    task = asyncio.create_task(simple_task(), name="Load data")

    print("Task name:", task.get_name())

    await task

asyncio.run(main())