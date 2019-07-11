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
        return None

    @property
    def slug(self):
        """
        The slug of the repository.
        """
        return None

    @property
    def owner(self):
        """
        The user or organization that owns the repo.
        """
        return None


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
