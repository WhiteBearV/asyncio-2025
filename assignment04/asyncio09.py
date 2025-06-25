# cancel task

import asyncio

async def slow_task():

    await asyncio.sleep(3)

async def main():

    task = asyncio.create_task(slow_task())

    print("Cancel task in 1 sec")

    await asyncio.sleep(1)

    task.cancel()

    try:

        await task

    except asyncio.CancelledError:

        print("Task has been canceled")

asyncio.run(main())