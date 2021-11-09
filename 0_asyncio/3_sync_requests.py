# TODO:
# Make this program work asyncrhonously using the async-await syntax
# described on page 12 of presentation

import asyncio
from helpers import async_request
import requests
import time

URLS = [
    'http://localhost:5588/one',
    'http://localhost:5588/two',
    'http://localhost:5588/three',
]

RESPONSES = []


def show_responses():
    for response in RESPONSES:
        if len(response) > 0:
            print('\n', response)


if __name__ == '__main__':
    start = time.time()
    
    for url in URLS:
        resp = requests.get(url)
        RESPONSES.append(resp.text)
    
    print(f'\n--- {__file__} finished in {time.time()-start:.5f}')
    show_responses()
