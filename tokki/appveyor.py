import aiohttp
import asyncio


class AppVeyorRepo:
    """
    Repository for an AppVeyor user.
    """
    def __init__(self, name, client):
        self.name = name
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

    def __getitem__(self, key) -> AppVeyorRepo:
        return AppVeyorRepo(key)
