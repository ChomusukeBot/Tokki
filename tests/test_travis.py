import aiohttp
import os
import pytest
from tokki.travis import TravisClient

TOKEN = os.environ["TRAVIS_TOKEN"]
AGENT = "Tests for Tokki +(https://github.com/ChomusukeBot/Tokki)"


@pytest.mark.asyncio
async def test_no_login():
    with pytest.raises(TypeError, match=r": 'token'"):
        TravisClient()


@pytest.mark.asyncio
async def test_no_agent():
    with pytest.raises(TypeError, match=r": 'useragent'"):
        TravisClient(TOKEN)


@pytest.mark.asyncio
async def test_not_found():
    with pytest.raises(aiohttp.ClientResponseError) as exception:
        client = TravisClient(TOKEN, AGENT)
        await client.get_repo("ChomusukeBot/ThisIsAnInvalidRepo")
    assert exception.value.status == 404


@pytest.mark.asyncio
async def test_repo():
    client = TravisClient(TOKEN, AGENT)
    repo = await client.get_repo("ChomusukeBot/TestRepo")
    assert repo.name == "TestRepo"
    assert repo.site_slug == "ChomusukeBot/TestRepo"
    assert repo.repo_slug == "ChomusukeBot/TestRepo"
    assert repo.owner == "ChomusukeBot"
    assert repo.default_branch == "master"


@pytest.mark.asyncio
async def test_trigger_build():
    client = TravisClient(TOKEN, AGENT)
    repo = await client.get_repo("ChomusukeBot/TestRepo")
    await repo.trigger_build(branch="master", message="Run from Tokki's tests")
