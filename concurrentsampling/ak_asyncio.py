import asyncio
import time
import datetime


async def display_date():
    loop = asyncio.get_running_loop()
    print(f"loop time is: {loop.time()}")
    end_time = loop.time() + 5.0
    while True:
        print(f"loop time is: {loop.time()}")
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(display_date())


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())


async def main2():
    print(f"started at {time.strftime('%X')}")
    task1 = asyncio.create_task(say_after(1, 'hello2'))
    task2 = asyncio.create_task(say_after(0, 'world2'))
    await task1
    await task2

asyncio.run(main2())
print('salamsalam')


async def nested():
    asyncio.sleep(1)
    return 42


async def main3():
    # nested()
    print(await nested())
    print('salam')

asyncio.run(main3())
