import colander
from colander_tools import mapping, serializable, strict
from collections import OrderedDict

def test_open_mapping():
    @serializable.serializable
    class Definition(object):
        class Schema(colander.MappingSchema):
            schema_type = strict.Mapping

            foo = colander.SchemaNode(
                mapping.OpenMapping(),
                colander.SchemaNode(colander.String(), name="key"),
                colander.SchemaNode(strict.Integer(), name="value"),
            )

        def __init__(self, foo):
            self.foo = foo

    assert Definition.Schema().deserialize({"foo": {"a": 42}}).foo == {"a": 42}
    assert Definition.Schema().serialize(Definition(foo={"mykey": 1234})) == {"foo": {"mykey": 1234}}



def test_sorted_open_mapping():
    @serializable.serializable
    class Definition(object):
        class Schema(colander.MappingSchema):
            schema_type = strict.Mapping

            foo = colander.SchemaNode(
                mapping.SortedOpenMapping(),
                colander.SchemaNode(colander.String(), name="key"),
                colander.SchemaNode(strict.Integer(), name="value"),
            )

        def __init__(self, foo):
            self.foo = foo

    deserialized = Definition.Schema().deserialize({"foo": {"a": 42}}).foo
    assert deserialized == {"a": 42}
    assert isinstance(deserialized, OrderedDict)
    assert Definition.Schema().serialize(Definition(foo={"mykey": 1234})) == {"foo": {"mykey": 1234}}
