


def _wrap_serializable_class_schema(cls, schema_cls):
    def serialize(self, appstruct):
        if not isinstance(appstruct, self.AppStructClass):
            raise TypeError("%s is not the expected type %s" % (appstruct, self.AppStructClass))

        return schema_cls.serialize(self, appstruct.__dict__)

    def deserialize(self, cstruct):
        return self.AppStructClass(**schema_cls.deserialize(self, cstruct))

    return type(
        "%sSchema" % cls.__name__,
        (cls.Schema, ),
        {
            "AppStructClass": cls,
            "serialize": serialize,
            "deserialize": deserialize,
            },
        )

def _wrap_serializable_class(cls):
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

    return type(
        cls.__name__,
        (cls, ),
        {
            "serialize": serialize,
            "deserialize": classmethod(deserialize),
            },
        )


def serializable(cls):
    """
    Class decorator: bind a colander schema and a python class.
    """
    cls.Schema = _wrap_serializable_class_schema(cls, cls.Schema)
    return _wrap_serializable_class(cls)
