# ANSWER

import asyncio
import aiohttp
import requests
import time

URLS = [
    'http://localhost:5588/one',
    'http://localhost:5588/two',
    'http://localhost:5588/three',
]

RESPONSES = []

async def async_request(url: str):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        return await resp.text()


async def main(urls):
    cors = [async_request(url) for url in urls]
    responses = await asyncio.gather(*cors)
    RESPONSES.extend(responses)


def show_responses():
    for response in RESPONSES:
        if len(response) > 0:
            print('\n', response)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main(URLS))
    
    # for url in URLS:
    #     resp = requests.get(url)
    #     RESPONSES.append(resp.text)
    
    print(f'Total time: {time.time() - start:.5f}')
    show_responses()











# async def async_fetch(session: aiohttp.ClientSession, url: str):
#     async with session.get(url) as response:
#         response = await response.text()
#         RESPONSES.append(response)

# async def get_async_session(urls: list):
#     async with aiohttp.ClientSession() as session:
#         cors = [async_fetch(session, url) for url in urls]
#         await asyncio.gather(*cors)