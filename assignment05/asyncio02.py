# example of waiting for the first task to complete
from random import random
import asyncio

async def task_coro(arg):
    value = random()
    await asyncio.sleep(value)
    print (f'>task {arg} done with {value}')

async def main ():
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    done,pending = await asyncio.wait(tasks , return_when= asyncio.FIRST_COMPLETED)
    print('Done')
    first = done.pop()
    print(first)

asyncio.run(main())