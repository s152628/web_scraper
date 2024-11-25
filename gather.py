import asyncio
import random


async def wait_max_n_seconds_for_max_number(n):

    random_time = random.randint(0, n)
    await asyncio.sleep(random_time)
    random_number = random.randint(0, n)
    return random_number


async def main():
    tasks = []
    for _ in range(20):
        task = asyncio.create_task(wait_max_n_seconds_for_max_number(5))
        tasks.append(task)
    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results):
        print(f"Willekeurig getal {i} is {result}")


asyncio.run(main())
