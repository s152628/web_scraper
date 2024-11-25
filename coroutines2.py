import asyncio


async def counter():
    counter = 0
    while True:
        counter += 1
        print(counter)
        await asyncio.sleep(2)


async def task2_def():
    while True:
        print("Ik ben taak 2")
        await asyncio.sleep(3)


async def task3_def():
    while True:
        print("Ik ben taak 3")
        await asyncio.sleep(5)


async def main():
    task1 = asyncio.create_task(counter())
    task2 = asyncio.create_task(task2_def())
    task3 = asyncio.create_task(task3_def())
    await task1
    await task2
    await task3


asyncio.run(main())
