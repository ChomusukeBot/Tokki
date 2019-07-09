import aiohttp
import asyncio


class AppVeyorRepo:
    """
    Repository for an AppVeyor user.
    """
    def __init__(self, data, client):
        self.data = data
        self.client = client


class AppVeyor:
    """
    AppVeyor API implementation.
    """
    def __init__(self, token, useragent, loop=None):
        self.token = token
        self.useragent = useragent
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": useragent
        }
        self.repos = []

    def __getitem__(self, key) -> AppVeyorRepo:
        return AppVeyorRepo(key)

    @property
    def repos(self):
        """
        Gets all of the repos for the AppVeyor account.
        """
        return self.repos
