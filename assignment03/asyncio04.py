# Starting task
# Event Loop

import asyncio

async def greet():
    print("Hello World")
    await asyncio.sleep(1)
    print("7K เร้าจายยยยย")

asyncio.run(greet()) # + Create and run an event loop

#
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(greet())
# loop.close()