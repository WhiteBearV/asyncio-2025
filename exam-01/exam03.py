# Hint:
# ให้แก้ไขให้พิมพ์ Result: 5 ได้ถูกต้อง
# Result:
# Result: 5

import asyncio

async def compute(x, y):
    await asyncio.sleep(1)
    return x + y

async def main():
    result = [asyncio.create_task(compute(2,3))]
    print(f"Result:", result)


asyncio.run(main())

