import select
from collections import deque
from typing import Generator
from logger import logger

tasks = deque([])  # generator, that executes handler and yields the tuple(reason (e.g. write, read), socket)
clients = set()  # { socket: deque[messages to this client] }

write_queue = {}
read_queue = {}


def start_event_loop():
    logger.info('Event loop: initialized')

    while any([tasks, write_queue, read_queue]):
        while not tasks:
            logger.info('Event loop: going to block')
            read_ready, write_ready, _ = select.select(read_queue, write_queue, [])     # blocks while waiting for socket events

            add_tasks_from_select_queue(write_ready)
            add_tasks_from_select_queue(read_ready)

        execute_task()


def add_tasks_from_select_queue(queue: list):
    for sock in queue:
        generator = write_queue.pop(sock)
        tasks.append(generator)


def add_task(task: Generator):
    tasks.append(tasks)


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
