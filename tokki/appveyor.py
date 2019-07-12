from .base import BaseClient, BaseProject


class AppVeyorRepo(BaseProject):
    """
    Project or Repo managed by an AppVeyor user.

    Create this class by calling :meth:`AppVeyorClient.get_repo`.
    """
    @property
    def name(self):
        """
        :class:`str`: The name of the repository.
        """
        return self.data["project"]["name"]

    @property
    def slug(self):
        """
        :class:`str`: The slug of the repository.
        """
        return self.data["project"]["slug"]

    @property
    def owner(self):
        """
        :class:`str`: The user or organization that owns the repo.
        """
        return self.data["project"]["accountName"]

    @property
    def default_branch(self):
        """
        :class:`str`: The default branch of the project.
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
    Represents a client for accessing the information of a single user with their v1 token.

    Parameters
    -----------
    token: :class:`str`
        The v1 token for accessing the user information.
    args: :class:`list`
        Arguments to pass into the :class:`BaseClient`.
    kwargs: :class:`dict`
        Keyword arguments to pass into the :class:`BaseClient`.
    """
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers["Authorization"] = f"Bearer {token}"

    async def get_repo(self, slug):
        """
        Gets a repository (also called project) from the AppVeyor account.

        Parameters
        -----------
        slug: :class:`str`
            The `username/repo` or `organization/repo` to get the information from.

            If the repo exists on the Git service but is not available on AppVeyor, this raises an exception.

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
