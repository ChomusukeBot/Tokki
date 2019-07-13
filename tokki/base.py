import aiohttp
import asyncio


class BaseRepo():
    """
    Base repository for all Git/Mercurial services.

    Parameters
    -----------
    data: :class:`dict`
        Raw JSON response sent by the service.
    client: :class:`BaseClient`
        The client that generated this request.
    """
    def __init__(self, data, client):
        self.data = data
        self.client = client

    @property
    def name(self):
        """
        :class:`str`: The name of the repository.
        """
        raise NotImplementedError

    @property
    def site_slug(self):
        """
        :class:`str`: The slug assigned by the CI service.
        """
        raise NotImplementedError

    @property
    def repo_slug(self):
        """
        :class:`str`: The slug assigned by Git or Mercurial.
        """
        raise NotImplementedError

    @property
    def owner(self):
        """
        :class:`str`: The user or organization that owns the repo.
        """
        raise NotImplementedError

    @property
    def default_branch(self):
        """
        :class:`str`: The default branch of the project.
        """
        raise NotImplementedError


class BaseProject(BaseRepo):
    """
    Base for all Continous Integration projects.

    A Project is a Repo inside a CI service.

    It takes the same parameters as :class:`BaseRepo`.
    """
    async def trigger_build(self, *, branch=None, message=None):
        """
        Triggers a manual build of the project.

        Parameters
        -----------
        branch: :class:`str`
            The branch to trigger the build from.
        message: :class:`str`
            The custom message to show on the build.
            Custom messages are not available on AppVeyor.
        """
        raise NotImplementedError


class BaseClient():
    """
    Base client for all of the APIs.

    Parameters
    -----------
    useragent: :class:`str`
        The User-Agent header that the REST calls should use.
    """
    def __init__(self, useragent, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(loop=self.loop, raise_for_status=True)
        self.headers = {
            "Accept": "application/json",
            "User-Agent": useragent
        }

    def __del__(self):
        # If the loop is closed, get another one
        loop = asyncio.get_event_loop() if self.loop.is_closed() else self.loop
        # Once a deletion has been requested, close the session on the same loop
        asyncio.ensure_future(self.session.close(), loop=loop)

    async def _get_request(self, url):
        """
        Makes a standard GET request.

        Parameters
        -----------
        url: :class:`str`
            The URL to use for the request.

        Returns
        --------
        :class:`dict`
            The JSON response.
        """
        # Request the specific URL
        async with self.session.get(url, headers=self.headers) as resp:
            # Finally return the response
            return await resp.json()

    async def _post_request(self, url, data):
        """
        Makes a standard POST request.

        Parameters
        -----------
        url: :class:`str`
            The URL to use for the request.
        data: :class:`dict`
            The data to send as part of the request.

        Returns
        --------
        :class:`dict`
            The JSON response.
        """
        # Request the specific URL
        async with self.session.post(url, headers=self.headers, data=data) as resp:
            # Finally return the response
            return await resp.json()
