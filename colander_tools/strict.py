
"""
A collection of strict types for Colander.
"""

from colander import _, SchemaType, Invalid, null, Mapping as BaseMapping
from . import compat


class Number(SchemaType):
    """ Abstract base class for float, int, decimal """

    num = None

    def serialize(self, node, appstruct):
        if appstruct is null:
            return null

        try:
            return self.num(appstruct)  # noqa
        except Exception:
            raise Invalid(node, _('"${val}" is not a number', mapping={'val': appstruct}))

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null

        try:
            if isinstance(cstruct, self.num):
                return self.num(cstruct)  # noqa
        except Exception:
            pass

        raise Invalid(node, _('"${val}" is not a number', mapping={'val': cstruct}))


class Integer(Number):
    """ A type representing an integer.

    On serialize, always returns an integer, except if passed :attr:`colander.null`
    which is returned as-is.

    On deserialize, accepts an integer or an integer represented as a string.
    """
    num = int


class Float(Number):
    """ A type representing a float.

    On serialize, always returns an float, except if passed :attr:`colander.null`
    which is returned as-is.

    On deserialize, accepts a float or a float represented as a string.
    """
    num = float


class Boolean(SchemaType):
    """ A type representing a boolean.

    On serialize, always returns a boolean, except if passed :attr:`colander.null`
    which is returned as-is.

    On deserialize, accepts a boolean or a boolean represented as a string.
    """

    def serialize(self, node, appstruct):  # noqa
        if appstruct is null:
            return null

        return bool(appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null

        if isinstance(cstruct, bool):
            return cstruct

        try:
            result = str(cstruct)
        except Exception:
            raise Invalid(node, _('${val} is not a boolean', mapping={'val': cstruct}))
        result = result.lower()

        if result in ('false', '0'):
            return False

        return True


class String(SchemaType):
    """ A type representing a string.

    On serialize, always returns a unicode string, except if passed :attr:`colander.null`
    which is returned as-is.

    On deserialize, accepts a string or an unicode instance.
    """

    def serialize(self, node, appstruct):  # noqa
        if appstruct is null:
            return null

        return compat.text_type(appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null

        if isinstance(cstruct, compat.string_types):
            return cstruct

        raise Invalid(node, _('${val} is not a string', mapping={'val': cstruct}))


class Mapping(BaseMapping):
    """
    A mapping that doesn't allow unknown keys.

    Note that Mapping by default respects the ``unknown`` parameter for both
    `serialize()` and `deserialize()`. The former doesn't make much sense,
    so we only override the flag when performing the operation.
    """

    def serialize(self, node, appstruct):
        self.unknown = "ignore"
        return BaseMapping.serialize(self, node, appstruct)

    def deserialize(self, node, cstruct):
        self.unknown = "raise"
        return BaseMapping.deserialize(self, node, cstruct)
