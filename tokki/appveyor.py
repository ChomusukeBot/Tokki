from .base import BaseClient, BaseRepo


class AppVeyorRepo(BaseRepo):
    """
    Repository for an AppVeyor user.
    """
    @property
    def name(self):
        """
        The name of the repository.
        """
        return self.data["project"]["name"]

    @property
    def slug(self):
        """
        The slug of the repository.
        """
        return self.data["project"]["slug"]

    @property
    def owner(self):
        """
        The user or organization that owns the repo.
        """
        return self.data["project"]["accountName"]


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
