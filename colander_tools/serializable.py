
def serializable(cls):
    """
    Class decorator: bind a colander schema and a python class.

    When used in a class like this::

        @serializable
        class Country(object):
            class Schema(MappingSchema):
                code = SchemaNode(
                    String(),
                )

            def __init__(self, code):
                self.code = code

    It patches ``Country.Schema`` to serialize to and deserialize from instances of ``Country``,
    and in addition gives you:

    * A ``Country.deserialize(value, bind_kwargs=None)`` class method;
    * A ``country.serialize(bind_kwargs=None)`` instance method.

    You can reuse ``Country.Schema`` in other schemas, like this::

        @serializable
        class City(object):
            class Schema(MappingSchema):
                name = SchemaNode(
                    String(),
                )

                country = Country.Schema()

            def __init__(self, name, country):
                self.name = name
                self.country = country

    """
    cls.Schema = _patch_serializable_class_schema(cls.Schema, cls)
    _patch_serializable_class(cls)
    return cls


def _patch_serializable_class_schema(schema_cls, appstruct_cls):
    def serialize(self, appstruct):
        if not isinstance(appstruct, self.AppStructClass):
            raise TypeError("%s is not the expected type %s" % (appstruct, self.AppStructClass))

        return schema_cls.serialize(self, appstruct.__dict__)

    def deserialize(self, cstruct):
        return self.AppStructClass(**schema_cls.deserialize(self, cstruct))

    return type(
        schema_cls.__name__,
        (schema_cls,),
        {
            "AppStructClass": appstruct_cls,
            "serialize": serialize,
            "deserialize": deserialize,
        }
    )


def _patch_serializable_class(cls):
    def serialize(self, bind_kwargs=None):
        schema = self.Schema()
        if bind_kwargs is not None:
            schema = schema.bind(**bind_kwargs)
        return schema.serialize(self)

    def deserialize(cls, values, bind_kwargs=None):
        schema = cls.Schema()
        if bind_kwargs is not None:
            schema = schema.bind(**bind_kwargs)
        return schema.deserialize(values)

    cls.serialize = serialize
    cls.deserialize = classmethod(deserialize)
