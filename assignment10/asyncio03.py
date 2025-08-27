from random import random
import asyncio
import time

# coroutine to generate work

async def producer (queue):

    print(F"{time.ctime()} Producer: Running")

    # gnerate work

    for i in range(10):

    # generate a value

        value = random()

        # block to simulate work

        await asyncio.sleep(value)

        # add to the queue

        await queue.put(value)

    print(f"{time.ctime()} Producer: Done")

# corotine to consume work

async def consumer (queue):

    print(f"{time.ctime()} Consumer: Running")

    # cosumer work

    while True:

        # get a unit of work

        item = await queue.get()

        # report

        print(f"{time.ctime()} >get {item}")

        # block while processing

        if item:

            await asyncio.sleep(item)

        # mark the task as done

        queue.task_done()

# entry point coroutine

async def main():

    # create the shared queue

    queue = asyncio.Queue()

    # start the consumer

    consumer_tasks = asyncio.create_task(consumer (queue))

    # start producer and wait fot it to finish

    await asyncio.create_task(producer (queue))

    # wait for all items to be processes

    await queue.join()

# start the asyncio program

asyncio.run(main())