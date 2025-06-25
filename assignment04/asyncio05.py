# Check if a Task is Done
import asyncio
async def simple_task():
    await asyncio.sleep(1)
    return "completed!"

async def main():
    task = asyncio.create_task(simple_task())
    print("before await:" , task.done())
    await task
    print("after await:" ,task.done())


asyncio.run(main())