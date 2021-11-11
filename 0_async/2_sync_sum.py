# ANSWER

import asyncio
import time

async def sleep(how_long: float):
    print(f'Sleeping 1s. Time: {time.time() - start:.5f}\n')
    await asyncio.sleep(1)


async def sum(name: str, numbers: list):
    total = 0
    for number in numbers:
        print(f'Task {name} - working: Computing {total} + {number}')
        await asyncio.sleep(1)
        total += number
    print(f'--- Task {name} - done: Sum = {total}\n')


async def main(coros: list):
    await asyncio.gather(*coros)


if __name__ == '__main__':
    start = time.time()

    tasks = [sum("A", [1, 2]), sum("B", [1, 2, 3])]
    asyncio.run(main(tasks))

    end = time.time()
    print(f'END! Total execution time: {end-start:.5f} sec')
