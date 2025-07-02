# example of waiting for all tasks to be completed with a timeout
from random import random
import asyncio

async def task_coro(arg):
    value = random()
    await asyncio.sleep(value)
    print (f'>task {arg} done with {value}')
    return f">task {arg} done with {value}"

async def main ():
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    done,pending = await asyncio.wait(tasks ,timeout=0.5)
    print(f'Done, {len(done)} tasks completed in time')


asyncio.run(main())