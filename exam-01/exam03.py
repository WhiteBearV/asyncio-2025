# Hint:
# ให้แก้ไขให้พิมพ์ Result: 5 ได้ถูกต้อง
# Result:
# Result: 5

import asyncio

async def compute(x, y):
    await asyncio.sleep(1)
    return x + y

async def main():
    task = asyncio.create_task(compute(2, 3))
    result = await task
    print("Result:", result)

asyncio.run(main())


