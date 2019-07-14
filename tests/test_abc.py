import pytest
from tokki.abc import Client, Project, Repo

AGENT = "Tests for Tokki +(https://github.com/ChomusukeBot/Tokki)"


@pytest.mark.asyncio
async def test_no_agent():
    with pytest.raises(TypeError, match=r": 'useragent'"):
        Client()


@pytest.mark.asyncio
async def test_rest():
    client = Client(AGENT)
    await client._get_request("https://httpbin.org/get")
    await client._post_request("https://httpbin.org/post", {})


@pytest.mark.asyncio
async def test_not_implemented():
    client = Client(AGENT)

    with pytest.raises(TypeError):
        Project(None, client)

    with pytest.raises(TypeError):
        Repo(None, client)
