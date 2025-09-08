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
