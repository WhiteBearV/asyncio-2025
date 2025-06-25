# Create 2 Tasks with High-Level API

import asyncio

async def download_image(name, delay):

    print(f"{name} loading...")

    await asyncio.sleep(delay)

    print(f"{name} Loaded successfully!")

async def main():

# Create 2 tasks at once

    task1 = asyncio.create_task(download_image("Image 1", 2))

    task2 = asyncio.create_task(download_image("Image 2", 3))

# Wait for both tasks to finish.

    await task1

    await task2

asyncio.run(main())