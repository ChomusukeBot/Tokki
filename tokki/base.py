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

    @property
    def default_branch(self):
        """
        The default branch of the repository.
        """
        raise NotImplementedError


class BaseProject(BaseRepo):
    """
    Base project for all API calls.
    A Project is a Repo inside a CI service.
    """
    async def trigger_build(self, *args, **kwargs):
        """
        Triggers a build on the CI service.
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

    def __del__(self):
        # Once a deletion has been requested, close the session on the same loop
        asyncio.ensure_future(self.session.close(), loop=self.loop)

    async def _get_request(self, url):
        """
        Makes a GET request and handles non 100-200-300 codes.
        """
        # Request the specific URL
        async with self.session.get(url, headers=self.headers) as resp:
            # Ensure that we have a code 200
            resp.raise_for_status()
            # Finally return the response
            return await resp.json()
