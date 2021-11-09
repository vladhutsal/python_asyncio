import asyncio

import time

async def R1():
    print('Running in R1')
    await request(1)
    print('Finishing R1')


async def R2():
    print('Running in R2')
    await request(1)
    print('Finishing R2')


async def R3():
    print('Running in R3')
    await request(1)
    print('Finishing R3')


async def request(n: int):
    await asyncio.sleep(n)


async def main():
    coroutines = [R1(), R2(), R3()]
    await asyncio.gather(*coroutines)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())

    print(f'\n--- {__file__} finished in {time.time()-start:.5f}')