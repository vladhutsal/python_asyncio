import asyncio

import time

async def R1():
    print('Running in R1')
    await request(1)
    print('Finishing R1')


async def R2():
    print('Running in R2')
    await request(0.5)
    print('Finishing R2')


async def R3():
    print('Running in R3')
    await request(0.6)
    print('Finishing R3')


async def request(n: int):
    await asyncio.sleep(n)


if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(R1()),
        loop.create_task(R2()),
        loop.create_task(R3())
    ]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    loop.close()
    
    print(f'\n--- {__file__} finished in {time.time()-start:.5f}')