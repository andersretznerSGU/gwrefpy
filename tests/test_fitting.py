import pytest

from gwrefpy import Well
from gwrefpy.fitresults import FitResultData


def test_strandangers_model_basic_fit(strandangers_model) -> None:
    assert strandangers_model.name == "Strandangers"
    assert len(strandangers_model.wells) == 2
    assert strandangers_model.wells[0].name == "obs"
    assert strandangers_model.wells[1].name == "ref"

    [obs, ref] = strandangers_model.wells

    strandangers_model.fit(obs, ref, "3.5D")
    [fit] = strandangers_model.fits
    assert fit.n == 3
    assert fit.offset == "3.5D"


def test_strandangers_model_best_fit_by_names(strandangers_model) -> None:
    # introduce a second reference well
    ref = strandangers_model.get_wells("ref")  # type: Well
    ts2 = ref.timeseries + 0.5
    ref2 = Well("ref2", is_reference=True, timeseries=ts2)
    strandangers_model.add_well(ref2)

    best_fit = strandangers_model.best_fit("obs", ["ref", "ref2"], offset="3.5D")
    assert isinstance(best_fit, FitResultData)

    model_fits = strandangers_model.get_fits("obs")
    assert len(model_fits) == 2

    assert best_fit == min(model_fits, key=lambda x: x.rmse)


def test_strandangers_model_best_fit_by_objects(strandangers_model) -> None:
    # introduce a second reference well
    [obs, ref] = strandangers_model.get_wells(["obs", "ref"])
    ts2 = ref.timeseries + 0.5
    ref2 = Well("ref2", is_reference=True, timeseries=ts2)
    strandangers_model.add_well(ref2)

    best_fit = strandangers_model.best_fit(obs, [ref, ref2], offset="3.5D")
    assert isinstance(best_fit, FitResultData)

    model_fits = strandangers_model.get_fits(obs)
    assert len(model_fits) == 2


def test_strandangers_model_fit_multiple_wells(strandangers_model) -> None:
    # Create additional wells for testing list functionality
    [obs, ref] = strandangers_model.get_wells(["obs", "ref"])

    # Create second observation well
    ts_obs2 = obs.timeseries + 1.0
    obs2 = Well("obs2", is_reference=False, timeseries=ts_obs2)
    strandangers_model.add_well(obs2)

    # Create second reference well
    ts_ref2 = ref.timeseries + 0.5
    ref2 = Well("ref2", is_reference=True, timeseries=ts_ref2)
    strandangers_model.add_well(ref2)

    # Test fitting with lists of wells
    results = strandangers_model.fit([obs, obs2], [ref, ref2], offset="3.5D")


    # Verify we get a list of results
    assert isinstance(results, list)
    assert len(results) == 2

    # Verify each result is a FitResultData instance
    for result in results:
        assert isinstance(result, FitResultData)
        assert result.offset == "3.5D"

    # Verify the correct pairings
    assert results[0].obs_well == obs
    assert results[0].ref_well == ref
    assert results[1].obs_well == obs2
    assert results[1].ref_well == ref2

    # Verify results were added to model fits
    assert len(strandangers_model.fits) >= 2


def test_strandangers_model_fit_mismatched_lists(strandangers_model) -> None:
    # Test error handling for mismatched list lengths
    [obs, ref] = strandangers_model.get_wells(["obs", "ref"])

    # Create second observation well
    ts_obs2 = obs.timeseries + 1.0
    obs2 = Well("obs2", is_reference=False, timeseries=ts_obs2)
    strandangers_model.add_well(obs2)

    # Try to fit with mismatched list lengths (should raise ValueError)
    with pytest.raises(ValueError):
        strandangers_model.fit([obs, obs2], [ref], offset="3.5D")


def test_strandangers_model_fit_string_names(strandangers_model) -> None:
    # Test fitting using string well names instead of Well objects
    [obs, ref] = strandangers_model.get_wells(["obs", "ref"])

    # Create additional wells
    ts_obs2 = obs.timeseries + 1.0
    obs2 = Well("obs2", is_reference=False, timeseries=ts_obs2)
    strandangers_model.add_well(obs2)

    ts_ref2 = ref.timeseries + 0.5
    ref2 = Well("ref2", is_reference=True, timeseries=ts_ref2)
    strandangers_model.add_well(ref2)

    # Test single string names
    result_single = strandangers_model.fit("obs", "ref", offset="3.5D")
    assert isinstance(result_single, FitResultData)
    assert result_single.obs_well.name == "obs"
    assert result_single.ref_well.name == "ref"

    # Test list of string names
    results_list = strandangers_model.fit(
        ["obs", "obs2"], ["ref", "ref2"], offset="3.5D"
    )
    assert isinstance(results_list, list)
    assert len(results_list) == 2
    assert results_list[0].obs_well.name == "obs"
    assert results_list[0].ref_well.name == "ref"
    assert results_list[1].obs_well.name == "obs2"
    assert results_list[1].ref_well.name == "ref2"

    # Test mixed Well objects and strings
    result_mixed = strandangers_model.fit([obs, "obs2"], ["ref", ref2], offset="3.5D")
    assert isinstance(result_mixed, list)
    assert len(result_mixed) == 2
    assert result_mixed[0].obs_well == obs
    assert result_mixed[0].ref_well.name == "ref"
    assert result_mixed[1].obs_well.name == "obs2"
    assert result_mixed[1].ref_well == ref2


def test_strandangers_model_fit_invalid_well_name(strandangers_model) -> None:
    # Test error handling for non-existent well names
    with pytest.raises(ValueError, match="not found in the model"):
        strandangers_model.fit("nonexistent", "ref", offset="3.5D")

    with pytest.raises(ValueError, match="not found in the model"):
        strandangers_model.fit("obs", "nonexistent", offset="3.5D")
