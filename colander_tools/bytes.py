
from __future__ import absolute_import

import base64

from colander import SchemaType, null, Invalid, _
import six

from . import compat


class AbstractEncodedBytes(SchemaType):
    encoder = None
    decoder = None

    def serialize(self, node, appstruct):
        if appstruct is null:
            return null

        if not isinstance(appstruct, six.binary_type):
            raise Invalid(node, _("{} must be a byte string ".format(type(appstruct),appstruct)))

        return self.encoder(appstruct)

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null

        if not isinstance(cstruct, compat.chars_type):
            raise Invalid(node, _("{} must be a string".format(type(cstruct))))

        return self.decoder(cstruct)


class Base16Bytes(AbstractEncodedBytes):
    encoder = staticmethod(base64.b16encode)
    decoder = staticmethod(base64.b16decode)


class Base32Bytes(AbstractEncodedBytes):
    encoder = staticmethod(base64.b32encode)
    decoder = staticmethod(base64.b32decode)


class Base64Bytes(AbstractEncodedBytes):
    encoder = staticmethod(lambda p: base64.standard_b64encode(p).decode("ascii"))
    decoder = staticmethod(base64.standard_b64decode)


class URLSafeBase64Bytes(AbstractEncodedBytes):
    encoder = staticmethod(lambda p: base64.urlsafe_b64encode(p).decode("ascii"))
    decoder = staticmethod(base64.urlsafe_b64decode)
