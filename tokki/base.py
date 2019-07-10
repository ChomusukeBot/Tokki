import aiohttp
import asyncio


class BaseClient():
    """
    Base client for all of the API calls.
    """
    def __init__(self, useragent, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.headers = {
            "Accept": "application/json",
            "User-Agent": useragent
        }
