import aiohttp
import asyncio


class AppVeyorRepo:
    """
    Repository for an AppVeyor user.
    """
    def __init__(self, data, client):
        self.data = data
        self.client = client

    @property
    def name(self):
        """
        The name of the repository.
        """
        return self.data.get("name", None)

    @property
    def slug(self):
        """
        The slug of the repository.
        """
        return self.data.get("slug", None)

    @property
    def owner(self):
        """
        The user or organization that owns the repo.
        """
        return self.data.get("accountName", None)


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
        found = [x for x in self.repos if x.name == key]
        return found[0] if found else None

    @property
    def repos(self):
        """
        Gets all of the repos for the AppVeyor account.
        """
        return self.repos
