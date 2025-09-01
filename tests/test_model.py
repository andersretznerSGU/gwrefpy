from src.gwrefpy.model import Model
from src.gwrefpy.well import Well


def test_add_well_to_model() -> None:
    model = Model("Test Model")
    well1 = Well("Well 1", is_reference=True)
    well2 = Well("Well 2", is_reference=True)
    model.add_well([well1, well2])

    assert len(model.wells) == 2
    assert model.wells[0].name == "Well 1"
    assert model.wells[1].name == "Well 2"

    try:
        model.add_well("Not a well")  # type: ignore
    except TypeError as e:
        assert str(e) == "Only Well instances can be added to the model."

    try:
        model.add_well(well1)
    except ValueError as e:
        assert str(e) == "Well 'Well 1' is already in the model."


def test_strandangers_model(strandangers_model) -> None:
    assert strandangers_model.name == "Strandangers"
    assert len(strandangers_model.wells) == 2
    assert strandangers_model.wells[0].name == "obs"
    assert strandangers_model.wells[1].name == "ref"

    [obs, ref] = strandangers_model.wells

    strandangers_model.fit(ref, obs, "3.5D")
    [fit] = strandangers_model.fits
    assert fit.n == 3
    assert fit.offset == "3.5D"
