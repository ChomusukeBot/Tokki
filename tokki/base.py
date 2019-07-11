import aiohttp
import asyncio


class BaseRepo():
    """
    Base repository for all API calls.
    """
    def __init__(self, data, client):
        self.data = data
        self.client = client

    @property
    def name(self):
        """
        The name of the repository.
        """
        raise NotImplementedError

    @property
    def slug(self):
        """
        The slug of the repository.
        """
        raise NotImplementedError

    @property
    def owner(self):
        """
        The user or organization that owns the repo.
        """
        raise NotImplementedError


class BaseClient():
    """
    Base client for all of the API calls.
    """
    def __init__(self, useragent, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(loop=self.loop)
        self.headers = {
            "Accept": "application/json",
            "User-Agent": useragent
        }

    async def _get_request(self, url):
        """
        Makes a GET request and handles non 100-200-300 codes.
        """
        # Request the specific URL
        async with self.session.get(url, headers=self.headers) as resp:
            # Ensure that we have a code 200
            resp.raise_for_status()
            # Finally return the response
            return resp, await resp.json()
