
from colander import SchemaType, drop


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

    def serialize(self, node, appstruct):
        return drop

    def deserialize(self, node, cstruct):
        return drop
