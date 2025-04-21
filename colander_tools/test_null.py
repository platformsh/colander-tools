import colander
from colander_tools import null, serializable, strict


def test_nullable_schema():
    class MaybeNullSchema(colander.MappingSchema):
        schema_type = strict.Mapping

        foo = colander.SchemaNode(colander.String())

    @serializable.serializable
    class Definition(object):
        class Schema(colander.MappingSchema):
            schema_type = strict.Mapping

            foo = null.NullableSchema(MaybeNullSchema)(
                default=None,
                missing=None,
            )

        def __init__(self, foo=None):
            self.foo = foo

    assert Definition.Schema().deserialize({"foo": {"foo": "bar"}}).foo["foo"] == "bar"
    assert Definition.Schema().deserialize({}).foo is None
    assert (
        Definition.Schema().serialize(Definition(foo={"foo": "bar"}))["foo"]["foo"]
        == "bar"
    )
    assert Definition.Schema().serialize(Definition())["foo"] is None
