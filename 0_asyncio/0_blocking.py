# TODO:
# Give some examples of blocking functions

import time

def R1():
    print('Running in R1')
    request(1)
    print('Finishing R1')


def R2():
    print('Running in R2')
    request(1)
    print('Finishing R2')


def R3():
    print('Running in R3')
    request(1)
    print('Finishing R3')


def request(n: int):
    time.sleep(n)


start = time.time()
R1()
R2()
R3()
print(f'\n--- {__file__} finished in {time.time()-start:.5f}')
