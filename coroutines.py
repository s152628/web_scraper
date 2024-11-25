import asyncio


async def async_hello():
    await asyncio.sleep(3)
    print("Hello, world!")


if __name__ == "__main__":
    asyncio.run(async_hello())
