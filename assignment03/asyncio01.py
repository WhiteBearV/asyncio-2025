# check the type of a coroutine
import asyncio
#define a corouine
async def custom_coro():
    #await another coroutine
    await asyncio.sleep(1)

coro = custom_coro()
print(type(coro))