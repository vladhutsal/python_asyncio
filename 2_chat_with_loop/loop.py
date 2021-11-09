import select
from collections import deque
from typing import Generator
from logger import logger

# generator, that executes handler and yield -> tuple(reason: str, socket: socket)
# reasons - 'write' or 'read')
tasks = deque([])

write_queue = {}    # { socket: deque[messages to this client] }
read_queue = {}


def start_event_loop():
    logger.info('Event loop: initialized')

    while any([tasks, write_queue, read_queue]):
        while not tasks:
            logger.info('Event loop: going to block')
            read_ready, write_ready, _ = select.select(read_queue, write_queue, [])     # blocks while waiting for socket events

            add_tasks_from_select_queue(write_ready, write_queue)
            add_tasks_from_select_queue(read_ready, read_queue)

        execute_task()


def add_tasks_from_select_queue(ready: list, sockets_q: dict):
    for sock in ready:
        generator = sockets_q.pop(sock)
        tasks.append(generator)


def add_task(task: Generator):
    tasks.append(task)


def execute_task():
    task = tasks.popleft()

    try:
        reason, socket = next(task)
        if reason == 'read':
            read_queue[socket] = task
        elif reason == 'write':
            write_queue[socket] = task
        else:
            raise Exception('wrong reason')

    except StopIteration:
        logger.info('Event loop: some task has ended')
