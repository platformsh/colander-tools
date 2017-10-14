from colander import MappingSchema, Invalid, null


class SubSchemaMappingSchema(MappingSchema):
    """
    A schema that delegates to sub-schema depending on a type key.
    """
    type_key = "type"

    def serialize(self, appstruct=null):
        if appstruct is null:
            return null

        schema_type = appstruct[self.type_key]
        subschema = self._build_schema(schema_type)
        return MappingSchema.serialize(subschema, appstruct)

    def deserialize(self, cstruct=null):
        if cstruct is null:
            return null

        schema_type = self._deserialize_type(cstruct)
        subschema = self._build_schema(schema_type)
        return MappingSchema.deserialize(subschema, cstruct)

    def get_schema(self, schema_type):
        raise Invalid(self[self.type_key], "Invalid value for key %s" % self.type_key)

    def _deserialize_type(self, cstruct):
        """
        Get the type of the entity based on `cstruct`.
        """
        # Build a schema containing only the type key.
        type_schema = MappingSchema()
        type_schema[self.type_key] = self[self.type_key]
        # Assign the proper name to the subschema so that
        # Invalid exceptions contains the right hierarchy.
        type_schema.name = self.name

        return type_schema.deserialize(cstruct)[self.type_key]

    def _build_schema(self, schema_type):
        # Start with a clone of the current schema.
        schema = self.clone()

        # Build the subschema and bind it.
        subschema = self.get_schema(schema_type)
        if self.bindings is not None:
            subschema = subschema.bind(**self.bindings)

        if hasattr(subschema, "validator"):
            schema.validator = subschema.validator

        if hasattr(subschema, "preparer"):
            schema.preparer = subschema.preparer

        # Add the nodes of the subschema to the schema.
        for node in subschema.children:
            schema[node.name] = node

        return schema
