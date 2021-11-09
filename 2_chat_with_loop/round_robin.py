from collections import deque

def counter(n):
    while n:
        yield n
        n -= 1

q = deque([counter(6), counter(5), counter(7)])

def rr(q: deque):
    while q:
        try:
            task = q.popleft()
            res = next(task)
            print(res)
            q.append(task)
        except StopIteration:
            print('Task ended')

rr(q)
