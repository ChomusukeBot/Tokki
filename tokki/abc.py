import abc
import aiohttp
import asyncio


class Build(metaclass=abc.ABCMeta):
    """
    Base class for every CI build.
    """
    def __init__(self, data, client):
        self.data = data
        self.client = client

    @property
    @abc.abstractmethod
    def id(self):
        """
        :class:`int`: The internal identifier of the build.
        """

    @property
    @abc.abstractmethod
    def version(self):
        """
        :class:`str`: The number or version of the build.
        """

    @property
    @abc.abstractmethod
    def status(self):
        """
        :class:`tokki.enums.Status`: The number or version of the build.
        """


class Repo(metaclass=abc.ABCMeta):
    """
    Base repository for all Git/Mercurial services.

    Parameters
    -----------
    data: :class:`dict`
        Raw JSON response sent by the service.
    client: :class:`Client`
        The client that generated this request.
    """
    def __init__(self, data, client):
        self.data = data
        self.client = client

    @property
    @abc.abstractmethod
    def name(self):
        """
        :class:`str`: The name of the repository.
        """

    @property
    @abc.abstractmethod
    def site_slug(self):
        """
        :class:`str`: The slug assigned by the CI service.
        """

    @property
    @abc.abstractmethod
    def repo_slug(self):
        """
        :class:`str`: The slug assigned by Git or Mercurial.
        """

    @property
    @abc.abstractmethod
    def owner(self):
        """
        :class:`str`: The user or organization that owns the repo.
        """

    @property
    @abc.abstractmethod
    def default_branch(self):
        """
        :class:`str`: The default branch of the project.
        """


class Project(Repo, metaclass=abc.ABCMeta):
    """
    Base for all Continous Integration projects.

    A Project is a Repo inside a CI service.

    It takes the same parameters as :class:`Repo`.
    """
    @abc.abstractmethod
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


class Client(metaclass=abc.ABCMeta):
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
