from .abc import Build, Client, Project
from .enums import Status


class TravisBuild(Build):
    """
    Build that was created on Travis CI.
    """
    @property
    def id(self):
        return self.data["id"]

    @property
    def version(self):
        return "#" + self.data["number"]

    @property
    def status(self):
        return Status.from_name(self.data["state"])

    @property
    def branch(self):
        return self.data["branch"]["name"]


class TravisProject(Project):
    """
    Project or Repo that resides on Travis CI.

    Create this class by calling :meth:`TravisClient.get_repo`.
    """
    @property
    def name(self):
        return self.data["name"]

    @property
    def site_slug(self):
        return self.data["slug"]

    @property
    def repo_slug(self):
        return self.data["slug"]

    @property
    def owner(self):
        return self.data["owner"]["login"]

    @property
    def default_branch(self):
        return self.data["default_branch"]["name"]

    async def trigger_build(self, *, branch=None, message=None):
        # Format the data to use
        data = {
            "request": {
                "branch": branch if branch else self.default_branch
            }
        }
        # If there is a message
        if message:
            # Set the message
            data["request"]["message"] = message
        # Just make a post request to trigger a build
        await self.client._post_request(f"https://api.travis-ci.com/repo/{self.owner}%2F{self.name}/requests", data)

    async def get_builds(self, *, quantity=10):
        # Request the JSON with the responses
        json = await self.client._get_request(f"https://api.travis-ci.com/repo/{self.owner}%2F{self.name}/builds?limit={quantity}")
        # Then return the JSON parsed as our custom classes
        return [TravisBuild(x, self) for x in json["builds"]]


class TravisClient(Client):
    """
    Represents a client for accessing the Travis CI API.

    Parameters
    -----------
    token: :class:`str`
        The v1 token for accessing the user information.
    useragent: :class:`str`
        The User-Agent header that the REST calls should use.
    """
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers["Authorization"] = f"token {token}"
        self.headers["Travis-API-Version"] = "3"

    async def get_repo(self, slug):
        """
        Gets a project from Travis CI.

        Parameters
        -----------
        slug: :class:`str`
            The `owner/repo` to get the information from.

        Returns
        --------
        :class:`TravisRepo`
            The project of the user if is present on the account.

        Raises
        -------
        :class:`aiohttp.ClientResponseError`
            If the API response returned something other than a 1XX-2XX-3XX code.
        """
        # Change the slash of the repo with one esaped
        slug = slug.replace("/", "%2F")
        # Request the "specific repo" endpoint
        json = await self._get_request(f"https://api.travis-ci.com/repo/{slug}")
        # Return the new object
        return TravisProject(json, self)
