import pytest
from tokki.base import BaseClient, BaseProject, BaseRepo

AGENT = "Tests for Tokki +(https://github.com/ChomusukeBot/Tokki)"


@pytest.mark.asyncio
async def test_no_agent():
    with pytest.raises(TypeError, match=r": 'useragent'"):
        BaseClient()


@pytest.mark.asyncio
async def test_rest():
    client = BaseClient(AGENT)
    await client._get_request("https://httpbin.org/get")
    await client._post_request("https://httpbin.org/post", {})


@pytest.mark.asyncio
async def test_not_implemented():
    client = BaseClient(AGENT)

    project = BaseProject(None, client)
    with pytest.raises(NotImplementedError):
        await project.trigger_build()

    repo = BaseRepo(None, client)
    with pytest.raises(NotImplementedError):
        repo.name
    with pytest.raises(NotImplementedError):
        repo.site_slug
    with pytest.raises(NotImplementedError):
        repo.repo_slug
    with pytest.raises(NotImplementedError):
        repo.owner
    with pytest.raises(NotImplementedError):
        repo.default_branch
