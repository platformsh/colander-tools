


def _patch_serializable_class_schema(schema_cls, appstruct_cls):
    def serialize(self, appstruct):
        if not isinstance(appstruct, self.AppStructClass):
            raise TypeError("%s is not the expected type %s" % (appstruct, self.AppStructClass))

        return super(schema_cls, self).serialize(self, appstruct.__dict__)

    def deserialize(self, cstruct):
        return self.AppStructClass(**super(schema_cls, self).deserialize(self, cstruct))

    schema_cls.AppStructClass = appstruct_cls
    schema_cls.serialize = serialize
    schema_cls.deserialize = deserialize


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


def serializable(cls):
    """
    Class decorator: bind a colander schema and a python class.
    """
    _patch_serializable_class_schema(cls.Schema, cls)
    _patch_serializable_class(cls)
    return cls
