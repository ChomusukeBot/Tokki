from .base import BaseClient, BaseProject


class AppVeyorRepo(BaseProject):
    """
    Project or Repo managed by an AppVeyor user.

    Create this class by calling :meth:`AppVeyorClient.get_repo`.
    """
    @property
    def name(self):
        return self.data["project"]["slug"]

    @property
    def site_slug(self):
        return self.owner + "/" + self.name

    @property
    def repo_slug(self):
        return self.data["project"]["repositoryName"]

    @property
    def owner(self):
        return self.data["project"]["accountName"]

    @property
    def default_branch(self):
        return self.data["project"]["repositoryBranch"]

    async def trigger_build(self, *, branch=None, message=None):
        # Format the data to use
        data = {
            "accountName": self.owner,
            "projectSlug": self.name,
            "branch": branch if branch else self.default_branch
        }
        # Just make a post request to trigger a build
        await self.client._post_request("https://ci.appveyor.com/api/builds", data)


class AppVeyorClient(BaseClient):
    """
    Represents a client for accessing the information of a single user with their v1 token.

    Parameters
    -----------
    token: :class:`str`
        The v1 token for accessing the user information.
    useragent: :class:`str`
        The User-Agent header that the REST calls should use.
    """
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers["Authorization"] = f"Bearer {token}"

    async def get_repo(self, slug):
        """
        Gets a project from the AppVeyor account.

        Parameters
        -----------
        slug: :class:`str`
            The `owner/repo` to get the information from.

        Returns
        --------
        :class:`AppVeyorRepo`
            The project of the user if is present on the account.

        Raises
        -------
        :class:`aiohttp.ClientResponseError`
            If the API response returned something other than a 1XX-2XX-3XX code.
        """
        # Request the "specific repo" endpoint
        json = await self._get_request(f"https://ci.appveyor.com/api/projects/{slug}")
        # Return the new object
        return AppVeyorRepo(json, self)
