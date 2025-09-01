import pandas as pd

from gwrefpy import test_offsets
from gwrefpy.methods.timeseries import groupby_time_equivalents


def test_strandangers_example(strandangers_example) -> None:
    obs, ref = strandangers_example

    ref_te, obs_te, n = groupby_time_equivalents(ref, obs, "3.5D")
    assert n == 3
    assert ref_te.tolist() == [8.9, 9.2, 9.4]
    assert obs_te.tolist() == [11.4, 11.7, 11.8]


def test_groupby_time_equivalents_no_pairs() -> None:
    obs = pd.Series(
        index=[
            pd.Timestamp("2020-01-07"),
            pd.Timestamp("2020-02-01"),
            pd.Timestamp("2020-02-25"),
        ],
        data=[11.4, 11.7, 11.8],
        name="obs",
    )
    ref = pd.Series(
        index=[
            pd.Timestamp("2024-01-08"),
            pd.Timestamp("2024-02-03"),
            pd.Timestamp("2024-02-08"),
            pd.Timestamp("2024-02-25"),
            pd.Timestamp("2024-02-28"),
        ],
        data=[8.9, 9.2, 9.3, 9.3, 9.5],
        name="ref",
    )
    ref_te, obs_te, n = groupby_time_equivalents(ref, obs, "7D")
    assert n == 0
    assert ref_te.tolist() == []
    assert obs_te.tolist() == []


def test_test_offsets(strandangers_example) -> None:
    obs, ref = strandangers_example
    offsets = ["0D", "1D", "3.5D", "5D", "7D"]
    result = test_offsets(ref, obs, offsets)
    assert len(result) == len(offsets)
    assert result.index.tolist() == offsets
    assert result.name == "n_pairs"

    assert result.loc["0D"] == 1
    assert result.loc["3.5D"] == 3
