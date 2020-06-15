
from colander import SchemaType, drop, null


class NullType(SchemaType):
    """
    Type wrapper that accepts `None` as a valid value.
    """

    def __init__(self, typ):
        self.typ = typ

    def serialize(self, node, appstruct):
        if appstruct is None:
            return None

        return self.typ.serialize(node, appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is None:
            return None

        return self.typ.deserialize(node, cstruct)


class IgnoreType(SchemaType):
    """
    Type that is silently ignored from mappings.
    """

    def serialize(self, node, appstruct):  # noqa
        return drop

    def deserialize(self, node, cstruct):  # noqa
        return drop


def NullableSchema(schema_cls):
    def _serialize(self, appstruct=null):
        # Replicate colander behavior w.r.t. default.
        if appstruct is null:
            appstruct = self.default

        if appstruct is None:
            return None

        return schema_cls.serialize(self, appstruct)

    def _deserialize(self, cstruct=null):
        # Replicate colander behavior w.r.t. missing.
        if cstruct is null:
            cstruct = self.missing

        if cstruct is None:
            return None

        return schema_cls.deserialize(self, cstruct)

    return type(
        "Nullable%s" % schema_cls.__name__,
        (schema_cls, ),
        {
            "serialize": _serialize,
            "deserialize": _deserialize,
        }
    )
