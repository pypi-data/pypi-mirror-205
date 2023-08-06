import autora.synthetic
from autora.synthetic.inventory import SyntheticExperimentCollection
from autora.variable import VariableCollection


def test_model_registration_retrieval():
    # We can register a model and retrieve it
    autora.synthetic.register("empty", lambda: SyntheticExperimentCollection())
    empty = autora.synthetic.retrieve("empty")
    assert empty.name is None

    # We can register another model and retrieve it as well
    autora.synthetic.register(
        "only_variables",
        lambda: SyntheticExperimentCollection(variables=VariableCollection()),
    )
    only_variables = autora.synthetic.retrieve("only_variables")
    assert only_variables.variables is not None

    # We can still retrieve the first model, and it is equal to the first version
    empty_copy = autora.synthetic.retrieve("empty")
    assert empty_copy == empty
