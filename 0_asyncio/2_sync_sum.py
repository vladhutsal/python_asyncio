# TODO:
# Make this program work asyncrhonously using the async-await syntax
# described on page 12 of presentation

import time

def sleep(how_long: float):
    print(f'Sleeping 1s. Time: {time.time() - start:.5f}\n')
    time.sleep(how_long)


def sum(name: str, numbers: list):
    total = 0
    for number in numbers:
        print(f'Task {name} - working: Computing {total} + {number}')
        sleep(1)
        total += number
    print(f'--- Task {name} - done: Sum = {total}\n')


if __name__ == '__main__':
    start = time.time()
    tasks = [
        sum("A", [1, 2]),
        sum("B", [1, 2, 3]),
    ]

    print(f'\n--- {__file__} finished in {time.time()-start:.5f}')
