from collections import OrderedDict

import six
from colander import Mapping, Invalid, SchemaNode


class OpenMapping(Mapping):
    """
    A mapping where the keys are free-form and the values a specific type.
    """

    def _impl(self, node, value, callback):
        value = self._validate(node, value)

        error = None
        result = {}

        for index, (k, v) in enumerate(six.iteritems(value)):
            key_node = node["key"]
            value_node = node["value"].clone()
            value_node.name = k

            try:
                name = callback(key_node, k)
                result[name] = callback(value_node, v)
            except Invalid as e:
                if error is None:
                    error = Invalid(node)
                error.add(e, index)

        if error is not None:
            raise error

        return result


class OpenMappingSchema(SchemaNode):
    schema_type = OpenMapping


class SortedOpenMapping(OpenMapping):
    def _impl(self, node, value, callback):
        result = OpenMapping._impl(self, node, value, callback)
        return OrderedDict(sorted(result.items()))


class SortedOpenMappingSchema(SchemaNode):
    schema_type = SortedOpenMapping
