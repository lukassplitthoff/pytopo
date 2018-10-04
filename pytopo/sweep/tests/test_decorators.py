from qcodes import Parameter
from pytopo.sweep.decorators import (
    getter, setter, parameter_getter, parameter_setter
)


def test_getter():

    gtr = getter(("a", "A"), ("b", "B"))(lambda: (0, 1))
    assert gtr() == {"a": 0, "b": 1}

    table = gtr.parameter_table

    table.resolve_dependencies()
    assert table.nests == [["a"], ["b"]]
    param_a, param_b = table.param_specs

    assert param_a.name == "a"
    assert param_a.unit == "A"

    assert param_b.name == "b"
    assert param_b.unit == "B"


def test_setter():

    strr = setter(("a", "A"), ("b", "B"))(lambda a, b: None)
    assert strr(0, 1) == {"a": 0, "b": 1}

    table = strr.parameter_table
    table.resolve_dependencies()
    assert table.nests == [["a", "b"]]
    param_a, param_b = table.param_specs

    assert param_a.name == "a"
    assert param_a.unit == "A"

    assert param_b.name == "b"
    assert param_b.unit == "B"


def test_param_getter():

    pval = 0

    p = Parameter("p", unit="P", get_cmd=lambda: pval)
    gtr = parameter_getter(p)
    table = gtr.parameter_table

    assert table.nests == [["p"]]
    assert gtr() == {"p": pval}

    param_spec, = table.param_specs
    assert param_spec.name == "p"
    assert param_spec.unit == "P"


def test_param_setter():

    p = Parameter("p", unit="P", get_cmd=None, set_cmd=None)
    strr = parameter_setter(p)
    table = strr.parameter_table

    assert strr(0) == {"p": 0}
    assert p.get() == 0

    table.resolve_dependencies()
    assert table.nests == [["p"]]
    param_spec, = table.param_specs

    assert param_spec.name == "p"
    assert param_spec.unit == "P"
