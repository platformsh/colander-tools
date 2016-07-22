import colander
from colander_tools import strict
import pytest


def test_integer():
    # Serialization
    integer = strict.Integer().serialize({}, 4)
    assert(integer == 4)

    integer = strict.Integer().serialize({}, True)
    assert(integer == 1)

    with pytest.raises(colander.Invalid):
        integer = strict.Integer().serialize({}, "foo")

    with pytest.raises(colander.Invalid):
        integer = strict.Integer().serialize({}, {})

    # Deserialization
    integer = strict.Integer().deserialize({}, 1)
    assert(integer == 1)

    integer = strict.Integer().deserialize({}, True)
    assert(integer == 1)

    with pytest.raises(colander.Invalid):
        integer = strict.Integer().deserialize({}, "foo")

    with pytest.raises(colander.Invalid):
        integer = strict.Integer().deserialize({}, {})


def test_float():
    # Serialization
    float = strict.Float().serialize({}, 4.5)
    assert(float == 4.5)

    float = strict.Float().serialize({}, True)
    assert(float == 1)

    with pytest.raises(colander.Invalid):
        float = strict.Float().serialize({}, "foo")

    # Deserialization
    float = strict.Float().deserialize({}, 4.5)
    assert(float == 4.5)

    with pytest.raises(colander.Invalid):
        float = strict.Float().deserialize({}, True)

    with pytest.raises(colander.Invalid):
        float = strict.Float().deserialize({}, "foo")


def test_boolean():
    # Serialization
    boolean = strict.Boolean().serialize({}, True)
    assert(boolean is True)

    boolean = strict.Boolean().serialize({}, 1)
    assert(boolean is True)

    boolean = strict.Boolean().serialize({}, "foo")
    assert(boolean is True)

    boolean = strict.Boolean().serialize({}, {})
    assert(boolean is False)

    # Deserialization
    boolean = strict.Boolean().deserialize({}, True)
    assert(boolean is True)

    boolean = strict.Boolean().deserialize({}, 1)
    assert(boolean is True)

    boolean = strict.Boolean().deserialize({}, "foo")
    assert(boolean is True)

    boolean = strict.Boolean().deserialize({}, {})
    assert(boolean is True)


def test_string():
    # Serialization
    string = strict.String().serialize({}, "foo")
    assert(string == "foo")

    string = strict.String().serialize({}, True)
    assert(string == "True")

    string = strict.String().serialize({}, 1)
    assert(string == "1")

    string = strict.String().serialize({}, {})
    assert(string == "{}")

    # Deserialization
    string = strict.String().deserialize({}, "foo")
    assert(string == "foo")

    with pytest.raises(colander.Invalid):
        string = strict.String().deserialize({}, True)

    with pytest.raises(colander.Invalid):
        string = strict.String().deserialize({}, 1)

    with pytest.raises(colander.Invalid):
        string = strict.String().deserialize({}, {})


def test_mapping():
    class Foo(colander.MappingSchema):
        schema_type = strict.Mapping

        foo = colander.SchemaNode(strict.String())
        bar = colander.SchemaNode(strict.String())

    with pytest.raises(colander.Invalid):
        Foo().deserialize({"foo": "bar"})

    with pytest.raises(colander.Invalid):
        Foo().deserialize({"bar": "foo"})

    correct = {"bar": "foo", "foo": "bar"}
    mapping = Foo().deserialize(correct)
    assert(mapping == correct)
