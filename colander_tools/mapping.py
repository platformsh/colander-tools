
import collections

import colander
import six

class OrderedMapping(colander.Mapping):
    """A mapping that serializes to an ordered dict."""

    def __init__(self, unknown='raise'):
        super(OrderedMapping, self).__init__()
        self.unknown = unknown

    def __impl(self, node, value, callback, serializing, unknown):  # noqa
        error = None
        result = collections.OrderedDict()

        value = value.copy()
        for num, subnode in enumerate(node.children):
            name = subnode.name
            subval = value.pop(name, colander.null)

            # Skip the `drop` values early, as we are not allowed to pass them to
            # the schema node.
            if subval is colander.drop:
                continue
            if subval is colander.null:
                if serializing and subnode.default is colander.drop:
                    continue
                if not serializing and subnode.missing is colander.drop:
                    continue
            try:
                sub_result = callback(subnode, subval)
            except colander.Invalid as e:
                if error is None:
                    error = colander.Invalid(node)
                error.add(e, num)
            else:
                if sub_result is colander.drop:
                    continue
                result[name] = sub_result

        if unknown == "raise":
            if value:
                raise colander.UnsupportedFields(
                    node, value,
                    msg=colander._('Unrecognized keys in mapping: "${val}"',
                          mapping={'val': value}))

        elif unknown == "preserve":
            result.update(value)

        if error is not None:
            raise error  # pylint: disable=raising-bad-type

        return result

    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            appstruct = collections.OrderedDict()

        def callback(subnode, subappstruct):
            return subnode.serialize(subappstruct)

        unknown = self.unknown
        if unknown == "raise":
            unknown = "ignore"

        return self.__impl(node, appstruct, callback, serializing=True, unknown=unknown)

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null

        def callback(subnode, subcstruct):
            return subnode.deserialize(subcstruct)

        return self.__impl(node, cstruct, callback, serializing=False, unknown=self.unknown)


unset = object()


class OpenMapping(colander.Mapping):
    """
    A mapping where the keys are free-form and the values a specific type.
    """

    def _impl(self, node, value, callback, default_or_missing=unset):
        # default_or_missing is used to specify whether this call is happening
        # during serialization or deserialization, so that the validation can
        # correctly choose between the default or missing attributes. Before
        # colander 2.0, the default attribute was incorrectly used for both
        # directions. Because OpenMapping doesn't validate the presence of
        # specific keys, default and missing are both ignored, and the
        # default_or_missing argument doesn't need to be used.
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
            except colander.Invalid as e:
                if error is None:
                    error = colander.Invalid(node)
                error.add(e, index)

        if error is not None:
            raise error  # noqa

        return result


class SortedOpenMapping(OpenMapping):
    def _impl(self, node, value, callback, default_or_missing=unset):
        result = OpenMapping._impl(
            self, node, value, callback, default_or_missing
        )
        return collections.OrderedDict(sorted(result.items()))
