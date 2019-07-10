from .base import BaseClient


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


class AppVeyorClient(BaseClient):
    """
    AppVeyor API implementation.
    """
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers["Authorization"] = f"Bearer {token}"

    async def get_repo(self, name):
        """
        Gets a repo from the AppVeyor server.
        """
        # Request the specific repo endpoint
        async with self.session.get("") as resp:
            # Ensure that we have a code 200
            resp.raise_for_status()

            # Return the new object
            return AppVeyorRepo(await resp.json())
