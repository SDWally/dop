import time
import asyncio


async def worker():
    print("enter worker")
    # await
    # return
    await asyncio.sleep(5)
    print("finish worker")


async def main():
    worker_list = [worker() for i in range(5)]
    await asyncio.gather(*worker_list)


asyncio.run(main())