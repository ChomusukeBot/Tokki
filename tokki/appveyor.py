from .base import BaseClient, BaseProject


class AppVeyorRepo(BaseProject):
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

    @property
    def default_branch(self):
        """
        The default branch of the repository.
        """
        return self.data["project"]["repositoryBranch"]

    async def trigger_build(self, *, branch=None):
        """
        Triggers an AppVeyor build for the specified branch with the specified message.
        If branch is None, the build is triggered on the default branch.
        """
        # Format the data to use
        data = {
            "accountName": self.owner,
            "projectSlug": self.slug,
            "branch": branch if branch else self.default_branch
        }
        # Just make a post request to trigger a build
        await self.client._post_request("https://ci.appveyor.com/api/builds", data)


class AppVeyorClient(BaseClient):
    """
    AppVeyor API implementation.
    """
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers["Authorization"] = f"Bearer {token}"

    async def get_repo(self, slug):
        """
        Gets a repo from the AppVeyor server.
        """
        # Request the "specific repo" endpoint
        json = await self._get_request(f"https://ci.appveyor.com/api/projects/{slug}")
        # Return the new object
        return AppVeyorRepo(json, self)
