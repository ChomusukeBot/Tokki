import aiohttp
import os
import pytest
from tokki.appveyor import AppVeyorClient

TOKEN = os.environ["APPVEYOR_TOKEN"]
AGENT = "Tests for Tokki +(https://github.com/ChomusukeBot/Tokki)"


@pytest.mark.asyncio
async def test_no_login():
    with pytest.raises(TypeError, match=r": 'token'"):
        AppVeyorClient()


@pytest.mark.asyncio
async def test_no_agent():
    with pytest.raises(TypeError, match=r": 'useragent'"):
        AppVeyorClient(TOKEN)


@pytest.mark.asyncio
async def test_not_found():
    with pytest.raises(aiohttp.ClientResponseError) as exception:
        client = AppVeyorClient(TOKEN, AGENT)
        await client.get_repo("ChomusukeBot/ThisIsAnInvalidRepo")
    assert exception.value.status == 404


@pytest.mark.asyncio
async def test_repo():
    client = AppVeyorClient(TOKEN, AGENT)
    repo = await client.get_repo("justalemon/testrepo")
    assert repo.name == "testrepo"
    assert repo.site_slug == "justalemon/testrepo"
    assert repo.repo_slug == "ChomusukeBot/TestRepo"
    assert repo.owner == "justalemon"
    assert repo.default_branch == "master"


@pytest.mark.asyncio
async def test_trigger_build():
    client = AppVeyorClient(TOKEN, AGENT)
    repo = await client.get_repo("justalemon/testrepo")
    await repo.trigger_build(branch="master", message="Run from Tokki's tests")
