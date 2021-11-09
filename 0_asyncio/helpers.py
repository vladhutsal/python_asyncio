import aiohttp

# This helper coroutine after completion returns the string,
# like response.text value in regular requests module
async def async_request(url: str):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        return await resp.text()
