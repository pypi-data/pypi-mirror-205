import os

import pandas as pd
import pytest

from ghs import GHS


@pytest.fixture
async def ghs() -> GHS:
    async with GHS(os.environ["GITHUB_TOKEN"], os.environ["GITHUB_REPOSITORY"]) as ghs:
        yield ghs


@pytest.fixture
def df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
        }
    )


async def test_create(ghs: GHS, df: pd.DataFrame) -> None:
    await ghs.create("a.csv", df)


async def test_get(ghs: GHS, df: pd.DataFrame) -> None:
    rv = await ghs.get("a.csv")
    assert rv.equals(df)


async def test_update(ghs: GHS, df: pd.DataFrame) -> None:
    await ghs.update("a.csv", df)


async def test_delete(ghs: GHS) -> None:
    await ghs.delete("a.csv")


async def test_objects(ghs: GHS) -> None:
    rv = await ghs.objects()
    assert rv
