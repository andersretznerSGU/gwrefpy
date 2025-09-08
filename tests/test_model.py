from gwrefpy import Model, Well


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
    obs = strandangers_model.get_wells("obs")
    ref = strandangers_model.get_wells("ref")

    assert isinstance(obs, Well)
    assert isinstance(ref, Well)
    assert obs.name == "obs"
    assert ref.name == "ref"
