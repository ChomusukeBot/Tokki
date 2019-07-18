import pytest
from tokki.enums import Status


@pytest.mark.asyncio
async def test_all_values():
    assert Status.from_name("created") == Status.InProgress
    assert Status.from_name("received") == Status.InProgress
    assert Status.from_name("started") == Status.InProgress
    assert Status.from_name("passed") == Status.Success
    assert Status.from_name("failed") == Status.Failed
    assert Status.from_name("errored") == Status.Failed
    assert Status.from_name("canceled") == Status.Canceled


@pytest.mark.asyncio
async def test_invalid_values():
    with pytest.raises(ValueError):
        Status.from_name("invalid_value")
    with pytest.raises(ValueError):
        Status.from_name("not_a_real_status")
