
from __future__ import absolute_import

from colander import SchemaType, Invalid, null, _
from netaddr import IPAddress, IPNetwork


class IPAddressType(SchemaType):
    def __init__(self, version=None):
        self._version = version

    def serialize(self, node, appstruct):
        if appstruct is null:
            return null

        return str(appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null

        try:
            return IPAddress(cstruct, version=self._version)
        except:
            raise Invalid(node, _("must be a string representation of an IP address"))


class IPNetworkType(SchemaType):
    def __init__(self, version=None):
        self._version = version

    def serialize(self, node, appstruct):
        if appstruct is null:
            return null

        return str(appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null

        if cstruct == "any":
            return "0.0.0.0/0"

        try:
            return IPNetwork(cstruct, version=self._version)
        except:
            raise Invalid(node, _("must be a string representation of an IP address or CIDR"))
