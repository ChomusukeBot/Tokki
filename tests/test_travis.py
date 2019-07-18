import aiohttp
import os
import pytest
from tokki.travis import TravisClient
from tokki.enums import Status

TOKEN = os.environ["TRAVISCI_TOKEN"]
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


@pytest.mark.asyncio
async def test_get_builds():
    client = TravisClient(TOKEN, AGENT)
    repo = await client.get_repo("ChomusukeBot/TestRepo")
    builds = await repo.get_builds(quantity=5)
    assert len(builds) == 5
    for build in builds:
        assert type(build.id) is int
        assert type(build.version) is str
        assert type(build.status) is Status
        assert type(build.branch) is str
