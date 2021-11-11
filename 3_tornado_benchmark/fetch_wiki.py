#/Users/vladhutsal/Coxit/playground/workshop/aio_wsh_answers

import asyncio
import threading
from typing import Callable
import aiohttp
import requests
import time
from concurrent import futures
import argparse


RESPONSES = []
LOCK = threading.RLock()

async def async_fetch(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        await response.text()
        RESPONSES.append(f'{response.status}')

async def get_async_session(urls: list):
    async with aiohttp.ClientSession() as session:
        cors = [async_fetch(session, url) for url in urls]
        await asyncio.gather(*cors)

def run_async(urls: list):
    asyncio.run(get_async_session(urls))



def fetch_wiki_with_threads(url: str) -> None:
    response = get_response(url)
    with LOCK:
        RESPONSES.append(response.status_code)

def run_with_threads(urls: list):
    with futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(fetch_wiki_with_threads, urls)



def run_sync(urls: list):
    for url in urls:
        resp = get_response(url)
        RESPONSES.append(resp.status_code)



def get_response(url: str) -> requests.Response:
    return requests.get(url, timeout=5)

def get_flow(mode: str) -> Callable:
    if mode == 'async':
        return run_async
    if mode == 'threads':
        return run_with_threads
    return run_sync

def main(exec_func: Callable, urls: list):
    start = time.time()

    exec_func(urls)

    if len(RESPONSES) >= 50:
        print(len(RESPONSES))
        print('Total time: ', time.time() - start)
    else:
        print('something went wrong, no time')



if __name__ == '__main__':
    URLS = [f'http://localhost:8888/?num={i}' for i in range(1000)]
    
    parser = argparse.ArgumentParser(
        description='Fetch wiki in sync, async and threadpool modes'
    )
    parser.add_argument(
        'mode', default='sync', nargs='?',
        choices=['sync', 'async', 'threads'],
        help='Default mode - "sync". Other: "async", "threads"',
    )

    args = parser.parse_args()
    exec_flow_func = get_flow(args.mode)
    main(exec_flow_func, URLS)
