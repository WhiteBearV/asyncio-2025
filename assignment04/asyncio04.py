# example of starting many tasks and getting access to all tasks
import time
import asyncio

# coroutine for a task
async def download_image(name, delay):
    print(f"{time.ctime()} {name} Loading...")
    await asyncio.sleep(delay)
    print(f"{time.ctime()} {name} Loading completed!")

# define a main coroutine

async def main():
# report a message
    print(f'{time.ctime()} main coroutine started')

# start many tasks
    started_tasks = [asyncio.create_task (download_image(i, 1)) for i in range(5,-1,-1)]

# allow some of the tasks time to start

    await asyncio.sleep(0.1)
    for task in started_tasks:
        await task

# start the asyncio program

asyncio.run(main())